import json

root="D:/project/blog/fribge/serve/src"

def FileGetter(path):
    with open(root+f'/data/{path}.json','r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def LabelGetter(path):
    with open(root+f'/data/label/{path}.json','r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def PokeGetter(path):
    with open(root+f'/data/pokemon/{path}.json','r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def SrcPath():
    return root