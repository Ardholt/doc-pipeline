"""Prove invalid mapping and damaged delivered content are rejected."""
import copy,json,shutil,tempfile,zipfile
from model import load,validate
from check import inspect

def run(src,out):
    pages,tr=load(src); total=0
    mutations=[lambda p,t:t['pages'].append(copy.deepcopy(t['pages'][0])),
               lambda p,t:t['pages'].clear(),
               lambda p,t:t['pages'][0]['blocks'].append(copy.deepcopy(t['pages'][0]['blocks'][0])),
               lambda p,t:t['pages'][0]['blocks'][0].update(text=t['pages'][0]['blocks'][0]['text']+' [unclear]'),
               lambda p,t:p['pages'][0].update(file='../escape.png'),
               lambda p,t:t['pages'][0]['blocks'][0].update(kind='table')]
    for mutate in mutations:
        p,t=copy.deepcopy(pages),copy.deepcopy(tr);mutate(p,t)
        try: validate(src,p,t)
        except ValueError: total+=1
        else: raise AssertionError('Invalid input accepted')
    with tempfile.TemporaryDirectory() as tmp:
        dst=__import__('pathlib').Path(tmp);shutil.copytree(out,dst,dirs_exist_ok=True)
        target=dst/'notes.docx'
        with zipfile.ZipFile(target) as z: files={n:z.read(n) for n in z.namelist()}
        from xml.etree import ElementTree as ET
        tree=ET.fromstring(files['word/document.xml']); first=next(tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'));first.text='DAMAGED VALUE'
        files['word/document.xml']=ET.tostring(tree)
        with zipfile.ZipFile(target,'w') as z:
            for n,b in files.items():z.writestr(n,b)
        try:inspect(src,dst,hashes=False)
        except AssertionError:total+=1
        else:raise AssertionError('Damaged DOCX accepted')
    print(f'PASS: {total} rejection checks including a damaged DOCX value')
    return total
