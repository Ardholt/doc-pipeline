"""Inspect PDF bytes, text geometry, resources, navigation, and source mapping."""
import hashlib, json, re, subprocess, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from layout import load_input, make_html, norm


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract(pdf):
    with tempfile.TemporaryDirectory() as tmp:
        dest=Path(tmp)/'text.html'
        subprocess.run(['pdftotext','-bbox-layout','-enc','UTF-8',str(pdf),str(dest)],check=True,timeout=60)
        root=ET.parse(dest).getroot()
    pages=[]
    for pg in root.findall('.//{*}page'):
        lines=[]
        for line in pg.findall('.//{*}line'):
            words=line.findall('{*}word')
            lines.append({'text':' '.join(w.text or '' for w in words),
                          'box':[float(line.get(k)) for k in ('xMin','yMin','xMax','yMax')]})
        lines.sort(key=lambda line:(round(line['box'][1],1),line['box'][0]))
        pages.append(lines)
    return pages


def inspect(root, out):
    cfg,ast=load_input(root)
    _,renderer=make_html(cfg,ast,root)
    pdf=Path(out)/'interior.pdf'
    reader=PdfReader(pdf)
    pages=extract(pdf)
    checks=[]
    def add(name, passed, observation):
        checks.append({'name':name,'passed':bool(passed),'observation':observation})
    scale=72/25.4
    w,h,b,m=[cfg[k]*scale for k in ('trim_width_mm','trim_height_mm','bleed_mm','margin_mm')]
    expected_media=[0,0,w+2*b,h+2*b]
    expected_trim=[b,b,w+b,h+b]
    paragraph_text=norm(''.join(rec['text'] for rec in renderer.records if rec['kind']=='paragraph'))
    boxes=[]; fonts={}; rasters=[]; annotations=[]; violations=[]; body_sizes=[]; size_chars={}; bad_links=[]; uri_links=[]
    for number,page in enumerate(reader.pages,1):
        box={'page':number,'media':[float(v) for v in page.mediabox],'trim':[float(v) for v in page.trimbox], 'crop':[float(v) for v in page.cropbox]}
        boxes.append(box)
        for key,expected in [('media',expected_media),('crop',expected_media),('trim',expected_trim)]:
            if any(abs(a-e)>0.03 for a,e in zip(box[key],expected)):
                violations.append(f'page {number}: wrong {key} box')
        font_table=page['/Resources'].get('/Font',{})
        if hasattr(font_table,'get_object'): font_table=font_table.get_object()
        for key,fontref in font_table.items():
            font=fontref.get_object(); name=str(font.get('/BaseFont'))
            descendants=font.get('/DescendantFonts',[font])
            descriptors=[f.get_object().get('/FontDescriptor') for f in descendants]
            embedded=all(d and any(k in d.get_object() for k in ('/FontFile','/FontFile2','/FontFile3')) for d in descriptors)
            fonts[name]={'name':name,'embedded':bool(embedded),'type':str(font.get('/Subtype'))}
        image_table=page['/Resources'].get('/XObject',{})
        if hasattr(image_table,'get_object'): image_table=image_table.get_object()
        for key,xref in image_table.items():
            obj=xref.get_object()
            if obj.get('/Subtype')=='/Image': rasters.append({'page':number,'width_px':obj['/Width'],'height_px':obj['/Height']})
        for ref in page.get('/Annots',[]):
            a=ref.get_object()
            dest=a.get('/Dest')
            action=a.get('/A',{})
            if isinstance(dest,str) and dest not in reader.named_destinations: bad_links.append({'page':number,'destination':dest})
            elif dest is not None and not isinstance(dest,str):
                if len(dest)<2: bad_links.append({'page':number,'destination':'invalid destination array'})
            elif dest is None and action.get('/S')=='/URI': uri_links.append(str(action.get('/URI')))
            elif dest is None: bad_links.append({'page':number,'destination':'missing or unsupported link action'})
            annotations.append({'page':number,'type':str(a.get('/Subtype')),'destination':str(a.get('/Dest',a.get('/A','')))})
        page_height=float(page.mediabox.height)
        def visitor(text,cm,tm,font,size):
            if text.strip():
                body_sizes.append(round(float(size),3))
                top=page_height-(tm[4]*cm[1]+tm[5]*cm[3]+cm[5])  # distance from the top edge, points
                piece=norm(text)
                # Count only text that belongs to a manuscript paragraph and sits between running head and folio.
                if len(piece)>=6 and piece in paragraph_text and b+m+8*scale < top < h+b-m-8*scale:
                    size_chars[round(float(size),3)]=size_chars.get(round(float(size),3),0)+len(piece)
        page.extract_text(visitor_text=visitor)
        for line in pages[number-1]:
            x0,y0,x1,y1=line['box']
            if x0 < b+m-0.8 or x1 > b+w-m+0.8 or y0 < b+m-0.8 or y1 > b+h-m+0.8:
                violations.append(f'page {number}: text outside safe margins: {line["text"][:55]}')
    add('even_page_count',len(pages)%2==0,{'pages':len(pages),'blank_pages':[n+1 for n,lines in enumerate(pages) if not lines]})
    add('page_boxes', not any('box' in x for x in violations), {'expected_media_pt':expected_media,'expected_trim_pt':expected_trim,'pages':len(boxes)})
    add('safe_margins',not any('margins' in x for x in violations),{'margin_mm':cfg['margin_mm'],'tolerance_pt':0.8,'violations':violations})
    add('embedded_fonts',bool(fonts) and all(f['embedded'] for f in fonts.values()),list(fonts.values()))
    add('metadata_removed', reader.metadata is None and '/Metadata' not in reader.trailer['/Root'], 'PDF Info and XMP absent')
    add('no_attachments_or_active_content',not reader.attachments and '/OpenAction' not in reader.trailer['/Root'] and all(a['type']=='/Link' for a in annotations), 'Only link annotations permitted; no attachments or open action')
    # Running heads and folios are outside the body area. Content mapping includes note text separately.
    text_pages=[]
    for lines in pages:
        text_pages.append(norm(' '.join(l['text'] for l in lines if b+m+8*scale < l['box'][1] < h+b-m-8*scale)))
    stream=''.join(text_pages)
    offsets=[]; cursor=0
    for p in text_pages:
        offsets.append((cursor,cursor+len(p))); cursor+=len(p)
    note_map=[]
    main=stream
    for note in renderer.notes:
        target=norm(note['text']); at=stream.find(target)
        note_map.append({**note,'found':at>=0,'page':next((i+1 for i,(lo,hi) in enumerate(offsets) if lo<=at<hi),None)})
        main=main.replace(str(note['number'])+'.'+target,'')
    missing=[]; mapping=[]; start=0
    for rec in renderer.records:
        target=norm(rec['text'])
        pattern=''.join(re.escape(norm(part['text'])) if 'text' in part else str(part['note']) for part in rec['parts'])
        match=re.search(pattern,main[start:])
        if match: found=start+match.start(); end=start+match.end()
        else: found=-1; end=-1
        if found<0: missing.append(rec['id'])
        else: start=end
        # Locate individual record by its opening, with note-independent physical page offsets.
        at=stream.find(target[:min(65,len(target))])
        mapping.append({**rec,'found_in_order':found>=0,'start_page':next((i+1 for i,(lo,hi) in enumerate(offsets) if lo<=at<hi),None)})
    add('source_text_and_order',not missing,{'mapped_blocks':len(mapping),'missing_or_out_of_order':missing,'normalization':'Single-column geometric line order; NFKC; whitespace and soft hyphens removed; note-call digits matched only at source note positions'})
    add('footnotes_retained',all(x['found'] for x in note_map),note_map)
    chapters=[x for x in mapping if x['kind']=='heading' and any(y['level']==1 and y['text']==x['text'] for y in renderer.headings)]
    # The contents repeats chapter names: locate chapter headings from full-size PDF lines after front matter.
    for ch in chapters:
        matches=[n+1 for n,lines in enumerate(pages) if n>=2 and any(norm(l['text'])==norm(ch['text']) and l['box'][3]-l['box'][1]>18 for l in lines)]
        heading=next(y for y in renderer.headings if y['level']==1 and y['text']==ch['text'])
        dest=reader.named_destinations.get(heading['id'])
        ch['start_page']=reader.get_destination_page_number(dest)+1 if dest else (matches[0] if matches else ch['start_page'])
    add('recto_chapter_openings',all(c['start_page'] and c['start_page']%2==1 for c in chapters),[{'title':c['text'],'page':c['start_page']} for c in chapters])
    note_calls=[]
    for number,note in enumerate(note_map,1):
        found_pages=[p+1 for p,lines in enumerate(pages) if any(re.search(r'\b'+str(number)+r'\.',l['text']) and l['box'][1]>h*0.55 for l in lines)]
        note_calls.append({'number':number,'note_page':note['page'],'bottom_marker_found':note['page'] in found_pages})
    add('footnotes_at_page_bottom',all(n['bottom_marker_found'] for n in note_calls),note_calls)
    add('contents_links',sum(a['type']=='/Link' for a in annotations)>=len(chapters)+len(renderer.links),{'link_annotations':len(annotations),'chapters':len(chapters),'manuscript_links':len(renderer.links)})
    expected_fragments=[x[1:] for x in renderer.links if x.startswith('#')]+[x['id'] for x in renderer.headings if x['level']==1]
    missing_targets=[x for x in expected_fragments if x not in reader.named_destinations]
    missing_uris=[x for x in renderer.links if not x.startswith('#') and x not in uri_links]
    add('navigation_targets',not bad_links and not missing_targets and not missing_uris,{'invalid_links':bad_links,'missing_targets':missing_targets,'missing_uris':missing_uris})
    folios=[]
    for n,lines in enumerate(pages,1):
        if n>2 and lines:
            footer=[l['text'] for l in lines if l['box'][1]>h+b-m-8*scale]
            folios.append({'page':n,'found':str(n) in footer})
    add('page_numbers',all(x['found'] for x in folios),folios)
    add('vector_illustrations',len(rasters)==0,{'svg_sources':renderer.assets,'raster_images':rasters,'resolution':'SVG illustrations remain vector; no raster DPI applies'})
    # Word bounding boxes detect text collision across distinct baselines, excluding intentional superscripts.
    collisions=[]
    for n,lines in enumerate(pages,1):
        for i,a in enumerate(lines):
            for z in lines[i+1:]:
                x0,y0,x1,y1=a['box']; u0,v0,u1,v1=z['box']
                if min(x1,u1)-max(x0,u0)>3 and min(y1,v1)-max(y0,v0)>2 and abs(y0-v0)>2:
                    collisions.append({'page':n,'text_a':a['text'][:40],'text_b':z['text'][:40]})
    add('text_line_collisions',not collisions,collisions)
    used_sizes=sorted(set(body_sizes))
    # WeasyPrint uses a 0.75 content transform; font operators are CSS px.
    physical_sizes=sorted(set(round(x*.75,3) for x in used_sizes))
    # Body type is the size that carries most of the manuscript's paragraph text in the body area, not merely a size that occurs somewhere.
    dominant=max(size_chars,key=size_chars.get) if size_chars else 0
    dominant_pt=round(dominant*.75,3); dominant_share=round(size_chars.get(dominant,0)/max(1,sum(size_chars.values())),3)
    add('body_type_size',abs(dominant_pt-cfg['body_pt'])<0.1,{'requested_pt':cfg['body_pt'],'size_with_most_paragraph_text_pt':dominant_pt,'share_of_paragraph_text':dominant_share,'observed_sizes_pt':physical_sizes})
    add('footnote_call_type_size',not renderer.notes or any(abs(x-cfg['body_pt']*.7)<0.1 for x in physical_sizes),{'requested_call_pt':cfg['body_pt']*.7,'observed_sizes_pt':physical_sizes})
    qpdf=subprocess.run(['qpdf','--check',str(pdf)],capture_output=True,text=True,timeout=60)
    add('qpdf_structure',qpdf.returncode==0,'qpdf --check exit '+str(qpdf.returncode))
    return {'last_text_page':max(n+1 for n,lines in enumerate(pages) if lines),'checks':checks,'counts':{'pages':len(pages),'chapters':len(chapters),'source_blocks':len(mapping),'missing_blocks':len(missing),'footnotes':len(note_map),'svg_illustrations':len(renderer.assets),'embedded_fonts':len(fonts),'link_annotations':len(annotations)},'boxes':boxes,'fonts':list(fonts.values()),'source_map':mapping,'footnote_map':note_map,'chapters':chapters,'image_resolution':{'kind':'vector','raster_images':rasters}}
