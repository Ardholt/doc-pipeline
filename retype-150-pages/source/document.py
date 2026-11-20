"""Build editable paragraphs and tables with source-page bookmarks."""
from docx import Document
from docx.shared import Pt,Mm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from common import strip_docx


def build(pages,path):
    doc=Document(); sec=doc.sections[0]
    sec.page_width=Mm(210); sec.page_height=Mm(297)
    sec.top_margin=sec.bottom_margin=Mm(18); sec.left_margin=sec.right_margin=Mm(20)
    normal=doc.styles['Normal']; normal.font.name='DejaVu Sans'; normal.font.size=Pt(10)
    normal.paragraph_format.space_after=Pt(7); normal.paragraph_format.line_spacing=1.12
    for name,size in [('Heading 1',15),('Heading 2',11)]:
        s=doc.styles[name]; s.font.name='DejaVu Sans'; s.font.size=Pt(size); s.font.color.rgb=RGBColor.from_string('183C42')
        s.paragraph_format.space_before=Pt(4); s.paragraph_format.space_after=Pt(8)
    for i,page in enumerate(pages):
        anchor=None
        for j,block in enumerate(page['blocks']):
            if block['kind']=='table':
                if anchor is None:anchor=doc.add_paragraph()
                rows=block['rows']; table=doc.add_table(rows=0,cols=len(rows[0])); table.style='Table Grid'
                for ri,row in enumerate(rows):
                    cells=table.add_row().cells
                    for cell,value in zip(cells,row):
                        cell.text=value
                        for p in cell.paragraphs:
                            p.paragraph_format.space_after=Pt(4); p.paragraph_format.space_before=Pt(4)
                            for run in p.runs:
                                run.font.size=Pt(10); run.bold=(ri==0)
                doc.add_paragraph().paragraph_format.space_after=Pt(0)
            else:
                p=doc.add_paragraph(block['text'],style=('Heading 1' if j==0 else 'Heading 2') if block['kind']=='heading' else 'Normal')
                if anchor is None:anchor=p
        if anchor is None:raise ValueError('Empty source page')
        anchor.paragraph_format.page_break_before=bool(i)
        mark=OxmlElement('w:bookmarkStart'); mark.set(qn('w:id'),str(i+1)); mark.set(qn('w:name'),f"source_page_{page['page']:03d}")
        end=OxmlElement('w:bookmarkEnd'); end.set(qn('w:id'),str(i+1))
        anchor._p.insert(1,mark); anchor._p.append(end)
    doc.save(path); strip_docx(path)
