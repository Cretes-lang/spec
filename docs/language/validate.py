#!/usr/bin/env python3
"""Experimental Phase 3 grammar recognizer; NOT a production Cretes frontend.
Python standard library only. No evaluation, AST, type checking or code generation.
Run: python3 validate.py (from any directory).
"""
from pathlib import Path
import ast
import json
import re
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
KEYWORDS = set('as break const continue else enum false fn for from if import in let loop match module mut new pub return struct true type var while'.split())
CATEGORIES = {'IDENT', 'INT', 'FLOAT', 'STRING', 'CHAR', 'BYTES'}
OPERATORS = sorted(':: -> => == != <= >= << >> && || + - * / % & | ^ ~ ! = < > ? . ( ) [ ] { } , ; :'.split(), key=len, reverse=True)
NUMBER = re.compile(r'(?:0b[01](?:_?[01])*|0o[0-7](?:_?[0-7])*|0x[0-9a-fA-F](?:_?[0-9a-fA-F])*|[0-9](?:_?[0-9])*(?:\.[0-9](?:_?[0-9])*)?(?:[eE][+-]?[0-9](?:_?[0-9])*)?)')
IDENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')

class Invalid(ValueError):
    pass

def lex(data):
    try:
        s = data.decode('utf-8') if isinstance(data, bytes) else data
    except UnicodeDecodeError as e:
        raise Invalid(f'L001 invalid UTF-8 at byte {e.start}') from e
    offsets = [0]
    for c in s:
        offsets.append(offsets[-1] + len(c.encode('utf-8')))
    for i,c in enumerate(s):
        n = ord(c)
        if (n < 32 and c not in '\t\r\n') or 127 <= n <= 159 or n in {0x61c,0x200e,0x200f,0x2060,0xfeff,0x2028,0x2029} or 0x200b <= n <= 0x200d or 0x202a <= n <= 0x202e or 0x2066 <= n <= 0x2069:
            raise Invalid(f'L001 prohibited raw scalar at byte {offsets[i]}')
        if c == '\r' and (i+1 == len(s) or s[i+1] != '\n'):
            raise Invalid('L001 bare CR')
    out=[]; i=0
    def emit(k,a,b): out.append((k, s[a:b], offsets[a], offsets[b]))
    while i < len(s):
        if s[i] in ' \t\r\n': i+=1; continue
        if s.startswith('//',i):
            while i < len(s) and s[i] not in '\r\n': i+=1
            continue
        if s.startswith('/*',i):
            i+=2; depth=1
            while i < len(s) and depth:
                if s.startswith('/*',i): depth+=1; i+=2
                elif s.startswith('*/',i): depth-=1; i+=2
                else: i+=1
            if depth: raise Invalid('L005 unterminated comment')
            continue
        start=i
        byte = s.startswith('b"',i)
        if byte or s[i] in '\"\'':
            if byte: i+=1
            quote=s[i]; i+=1; scalars=0
            while i < len(s) and s[i] != quote:
                c=s[i]
                if c in '\r\n\t': raise Invalid('L004 raw whitespace in literal')
                if c == '\\':
                    i+=1
                    if i>=len(s): raise Invalid('L004 unfinished escape')
                    c=s[i]
                    if c in 'nrt0\\"\'': i+=1
                    elif c=='x' and byte:
                        if not re.fullmatch('[0-9a-fA-F]{2}',s[i+1:i+3]): raise Invalid('L004 invalid byte escape')
                        i+=3
                    elif c=='u' and not byte:
                        m=re.match(r'u\{([0-9a-fA-F]{1,6})\}',s[i:])
                        if not m: raise Invalid('L004 invalid Unicode escape')
                        cp=int(m[1],16)
                        if cp>0x10ffff or 0xd800<=cp<=0xdfff: raise Invalid('L004 non-scalar escape')
                        i+=len(m[0])
                    else: raise Invalid('L004 unknown escape')
                else:
                    if byte and not 32<=ord(c)<=126: raise Invalid('L004 non-ASCII byte literal')
                    i+=1
                scalars+=1
            if i>=len(s): raise Invalid('L004 unterminated literal')
            i+=1
            if quote=="'" and scalars!=1: raise Invalid('L004 character needs one scalar')
            emit('BYTES' if byte else 'CHAR' if quote=="'" else 'STRING',start,i); continue
        if s[i].isdigit() and s[i].isascii():
            m=NUMBER.match(s,i)
            i=m.end()
            if i<len(s) and (s[i].isalnum() or s[i]=='_'): raise Invalid('L003 invalid numeric suffix/digit')
            word=m[0]; emit('FLOAT' if not word.startswith(('0b','0o','0x')) and any(c in word for c in '.eE') else 'INT', start,i); continue
        m=IDENT.match(s,i)
        if m:
            i=m.end(); word=m[0]
            if word.startswith('__'): raise Invalid('L002 reserved internal identifier')
            emit(word if word in KEYWORDS or word=='_' else 'IDENT',start,i); continue
        op=next((op for op in OPERATORS if s.startswith(op,i)),None)
        if op: i+=len(op); emit(op,start,i); continue
        raise Invalid(f'L002 invalid character at byte {offsets[i]}')
    return out

# Read only the documented token-level EBNF notation and expand optional/repeat
# forms to ordinary BNF. This engine is grammar-generic, not a production parser.
def grammar():
    text=(ROOT/'cretes.ebnf').read_text()
    ts=re.findall(r'"(?:[^"\\]|\\.)*"|[A-Za-z_][A-Za-z0-9_]*|[=;|()\[\]{}]',text)
    if re.sub(r'\s+','',text) != ''.join(ts): raise Invalid('unsupported EBNF text')
    rules=defaultdict(list); p=0; generated=0
    def symbol():
        nonlocal p,generated
        t=ts[p]; p+=1
        if t[0]=='"': return ('t',ast.literal_eval(t))
        if t in ('(', '[', '{'):
            end={'(':')','[':']','{':'}'}[t]
            alts=alternatives(end)
            if ts[p]!=end: raise Invalid('grammar delimiter')
            p+=1; generated+=1; name=f'_g{generated}'
            rules[name].extend(alts)
            if t=='[': rules[name].append(())
            if t=='{': rules[name]=[a+(('n',name),) for a in alts]+[()]
            return ('n',name)
        return ('t',t) if t in CATEGORIES else ('n',t)
    def alternatives(end):
        nonlocal p
        alts=[]; seq=[]
        while p<len(ts) and ts[p]!=end:
            if ts[p]=='|': alts.append(tuple(seq)); seq=[]; p+=1
            else: seq.append(symbol())
        alts.append(tuple(seq)); return alts
    while p<len(ts):
        name=ts[p]; p+=1
        if name in rules or ts[p]!='=': raise Invalid('duplicate/invalid production')
        p+=1; rules[name]=alternatives(';'); p+=1
    refs={v for alts in rules.values() for a in alts for k,v in a if k=='n'}
    if refs-set(rules): raise Invalid(f'undefined rules {refs-set(rules)}')
    reachable={'program'}
    while True:
        new=reachable|{v for n in reachable for a in rules[n] for k,v in a if k=='n'}
        if new==reachable: break
        reachable=new
    if set(rules)-reachable: raise Invalid(f'unreachable {set(rules)-reachable}')
    terminals={v for alts in rules.values() for a in alts for k,v in a if k=='t'}
    words={x for x in terminals if x.isalpha() and x not in CATEGORIES}
    if words!=KEYWORDS: raise Invalid(f'keyword drift {words^KEYWORDS}')
    return rules

RULES=grammar()

def accepts(source):
    tokens=lex(source)
    # Earley recognizer. State = (rule, alternative, dot, origin).
    rules=dict(RULES); rules['$']=[(('n','program'),)]
    chart=[set() for _ in range(len(tokens)+1)]; chart[0].add(('$',0,0,0))
    for pos in range(len(chart)):
        changed=True
        while changed:
            before=len(chart[pos])
            for name,ai,dot,origin in tuple(chart[pos]):
                rhs=rules[name][ai]
                if dot==len(rhs):
                    for pn,pa,pd,po in tuple(chart[origin]):
                        pr=rules[pn][pa]
                        if pd<len(pr) and pr[pd]==('n',name): chart[pos].add((pn,pa,pd+1,po))
                elif rhs[dot][0]=='n':
                    for idx in range(len(rules[rhs[dot][1]])): chart[pos].add((rhs[dot][1],idx,0,pos))
                elif pos<len(tokens) and rhs[dot][1]==tokens[pos][0]:
                    chart[pos+1].add((name,ai,dot+1,origin))
            changed=len(chart[pos])!=before
    return ('$',0,1,0) in chart[-1]

def main():
    fixtures=json.loads((ROOT/'fixtures.json').read_text())
    failures=[]; counts=defaultdict(int)
    for f in fixtures:
        try: actual=accepts(f['source'])
        except Invalid: actual=False
        counts[f['kind']]+=1
        if actual!=f['parse']: failures.append(f['id'])
    examples=sorted(ROOT.glob('*.cretes'))
    for f in examples:
        try: ok=accepts(f.read_bytes())
        except Invalid: ok=False
        if not ok: failures.append(f.name)
    try: lex(b'\xff')
    except Invalid: pass
    else: failures.append('invalid-utf8')
    spans=lex('"é"\r\nlet x = 1;')
    if spans[0][2:]!=(0,4) or spans[1][2:]!=(6,9): failures.append('utf8-crlf-spans')
    # Proposed-source docs link check uses the supplied repository snapshot when
    # available, otherwise checks links local to this candidate directory.
    for f in ROOT.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
            if '://' in target or target.startswith('#'): continue
            path=target.split('#')[0]
            if not path or path.startswith('../'): continue
            if not (ROOT/path).exists(): failures.append(f'{f.name}: {target}')
    print(json.dumps({'examples':len(examples),'fixtures':dict(counts),'rules':len([r for r in RULES if not r.startswith('_')]),'keyword_count':len(KEYWORDS),'failures':failures},indent=2))
    raise SystemExit(bool(failures))

if __name__=='__main__': main()
