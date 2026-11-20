def claims(report):
    c=report['counts']
    return {'schema_version':1,'claims':[
        {'claim':f"{c['reduction_percent']:.2f}% smaller; {c['input_bytes']/1e6:.2f} MB to {c['output_bytes']/1e6:.3f} MB",
         'evidence':[{'file':'output/report.json','pointer':'/counts/input_bytes'},{'file':'output/report.json','pointer':'/counts/output_bytes'},{'file':'input/input.pdf','field':'file length in bytes'},{'file':'output/fixed.pdf','field':'file length in bytes'}],
         'calculation':'MB = bytes / 1000000; percent = round((1 - output_bytes / input_bytes) * 100, 2); Python 3.11.2'},
        {'claim':f"All {c['pages']} pages, {c['words']} words and all images retained; text stays searchable",
         'evidence':[{'file':'output/report.json','pointer':'/checks'},{'file':'output/report.json','pointer':'/counts/source_output_map'}],
         'calculation':'pypdf 5.1.0 extracts each actual page; exact word sequence after whitespace normalization; image count compared per page'},
        {'claim':'Crop hid the start of lines; repaired lines are complete at the same reading scale',
         'evidence':[{'file':'output/previews/frames.json','pointer':'/hero'},{'file':'media/hero.png','frame':'full image'},{'file':'output/previews/comparison-1.png','frame':'full image'}]},
        {'claim':'Sideways page is upright; mixed page boxes become portrait A4 with safe margins',
         'evidence':[{'file':'output/report.json','pointer':'/pages_before'},{'file':'output/report.json','pointer':'/pages_after'},{'file':'output/report.json','pointer':'/transformations'},{'file':'output/previews/all-pages.png','frame':'all three rows'}]},
        {'claim':'Small print, vector diagrams and colour images remain readable; images are recompressed, with small measured pixel differences',
         'evidence':[{'file':'output/report.json','pointer':'/checks'},{'file':'output/previews/detail-1.png','frame':'caption, vector lines, note and footer'},{'file':'output/previews/image-detail-3.png','frame':'colour field'},{'file':'proof/visual-review.json','field':'reviewed_files'}]},
        {'claim':'Original text and graphics; real full-resolution uncompressed RGB input, without padding',
         'evidence':[{'file':'source/content.json','pointer':'/pages'},{'file':'source/make_input.py','field':'RGB contour generation, image streams, crop and rotation assignments'},{'file':'source/README.md','field':'generation recipe'}]},
        {'claim':'Tool versions quoted on the page were run',
         'evidence':[{'file':'output/report.json','pointer':'/tools'},{'file':'output/packages.tsv','field':'complete package version inventory'}]},
        {'claim':'Broken pages, text, crops and images are detected; invalid input is rejected',
         'evidence':[{'file':'output/adversarial.json','pointer':'/checks'},{'file':'tests/adversarial.py','field':'mutation tests'}]},
        {'claim':'No Acrobat, Microsoft Office, email-delivery, PDF/A or accessibility certification claim; annotations need separate review',
         'evidence':[{'file':'output/report.json','pointer':'/uncertainties'},{'file':'source/common.py','field':'load_input rejection checks'}]}
    ]}
