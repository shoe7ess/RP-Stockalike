import re
class Node:
    def __init__(s,name): s.name=name; s.items=[]
    def values(s,k): return [i[2] for i in s.items if i[0]=='v' and i[1]==k]
    def get(s,k,d=None):
        for i in s.items:
            if i[0]=='v' and i[1]==k: return i[2]
        return d
    def set(s,k,v):
        for n,i in enumerate(s.items):
            if i[0]=='v' and i[1]==k: s.items[n]=('v',k,v); return
        s.items.append(('v',k,v))
    def nodes(s,name=None): return [i[1] for i in s.items if i[0]=='n' and (name is None or i[1].name==name)]
    def delkey(s,k): s.items=[i for i in s.items if not (i[0]=='v' and i[1]==k)]
def strip_comment(line):
    i=line.find('//')
    while i!=-1:
        if not re.search(r'https?:$',line[:i]): return line[:i]
        i=line.find('//',i+2)
    return line
def parse(text):
    root=Node('root'); stack=[root]; pending=None
    for raw in text.splitlines():
        line=strip_comment(raw).strip()
        while line:
            if line[0]=='{':
                n=Node(pending or ''); stack[-1].items.append(('n',n)); stack.append(n); pending=None; line=line[1:].strip(); continue
            if line[0]=='}':
                if len(stack)>1: stack.pop()
                line=line[1:].strip(); continue
            m=re.match(r'([^{}=]*?)\s*=\s*([^{}]*)',line)
            if m:
                if pending: stack[-1].items.append(('n',Node(pending))); pending=None
                stack[-1].items.append(('v',m.group(1).strip(),m.group(2).strip())); line=line[m.end():].strip(); continue
            m=re.match(r'([^{}]+)',line); pending=m.group(1).strip(); line=line[m.end():].strip()
    return root
def dump(node,ind=0):
    out=[]; t='\t'*ind
    for i in node.items:
        if i[0]=='v': out.append(f"{t}{i[1]} = {i[2]}")
        else: out+= [f"{t}{i[1].name}", t+'{']+dump(i[1],ind+1)+[t+'}']
    return out
def walk(node):
    yield node
    for c in node.nodes(): yield from walk(c)
