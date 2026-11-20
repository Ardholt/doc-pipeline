"""Count wrong record and item codes in the delivered DOCX against the reference.

    python3 tests/code_errors.py [--write proof/code-errors.json]

A code is a record code (D01-01), a first-column item code (K001) or a second-column item code (R001).
For every source page, a reference code is wrong when the retyped page does not contain it as a whole
word (for example DQ1-02 or ROO2). Reads source/reference.json, output/retyped.docx, output/pages.json
and, for the search figure, the text of output/preview.pdf (pypdf); nothing is converted.
"""
import collections, json, re, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from common import block_text, docx_pages

case=Path(__file__).resolve().parents[1]
CODE=re.compile(r'(?<![A-Za-z0-9])(?:D\d\d-\d\d|K\d{3}|R\d{3})(?![A-Za-z0-9])')
KINDS={'D':'record codes (D##-##)','K':'first item codes (K###)','R':'second item codes (R###)'}


def count(reference, texts):
    total=collections.Counter(); wrong=collections.Counter(); pages=set()
    for page,ref in reference.items():
        want=collections.Counter(CODE.findall(ref)); got=collections.Counter(CODE.findall(texts[page]))
        for code,n in want.items(): total[code[0]]+=n
        for code,n in (want-got).items():
            wrong[code[0]]+=n; pages.add(page)
    return {'codes':sum(total.values()),'wrong':sum(wrong.values()),'pages_with_a_wrong_code':len(pages),
            'by_kind':{KINDS[k]:{'codes':total[k],'wrong':wrong[k]} for k in sorted(KINDS)}}


def pdf_search(reference):
    """Distinct reference codes that an exact search of the searchable PDF text does not find."""
    from pypdf import PdfReader
    text='\n'.join(page.extract_text() or '' for page in PdfReader(case/'output/preview.pdf').pages)
    found=set(CODE.findall(text)); distinct=sorted({c for ref in reference.values() for c in CODE.findall(ref)})
    missing=[c for c in distinct if c not in found]
    return {'distinct_codes':len(distinct),'not_found_by_exact_search':len(missing),
            'by_kind':{KINDS[k]:{'distinct_codes':sum(c[0]==k for c in distinct),'not_found':sum(c[0]==k for c in missing)} for k in sorted(KINDS)}}


def main(argv):
    reference={p['page']:block_text(p['blocks']) for p in json.loads((case/'source/reference.json').read_text())['pages']}
    delivered={p['page']:block_text(p['blocks']) for p in docx_pages(case/'output/retyped.docx')}
    raw={p['page']:p['raw_text'] for p in json.loads((case/'output/pages.json').read_text())['pages']}
    result={'schema_version':1,
            'definition':'A reference code is wrong when its source page, as extracted, does not contain it as a whole word.',
            'reference':'source/reference.json','delivered':'output/retyped.docx','raw_extraction':'output/pages.json raw_text',
            'delivered_docx':count(reference,delivered),'raw_extraction_counts':count(reference,raw),
            'searchable_pdf':{'text':'output/preview.pdf','definition':'A distinct code is not found when its exact text, as a whole word, appears nowhere in the PDF text.',**pdf_search(reference)}}
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if len(argv)==3 and argv[1]=='--write': (case/argv[2]).write_text(text)
    print(text,end='')
    return 0


if __name__=='__main__':
    sys.exit(main(sys.argv))
