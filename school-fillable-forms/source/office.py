"""Exercise Writer content controls through UNO; never fill by changing XML."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
import uno
from com.sun.star.beans import PropertyValue


def prop(name, value):
    p = PropertyValue(); p.Name = name; p.Value = value; return p


def located_controls(text, label=''):
    result = []
    enum = text.createEnumeration()
    while enum.hasMoreElements():
        item = enum.nextElement()
        if item.supportsService('com.sun.star.text.TextTable'):
            for name in item.getCellNames(): result.extend(located_controls(item.getCellByName(name), label))
        elif item.supportsService('com.sun.star.text.Paragraph'):
            portions = item.createEnumeration(); found = []
            while portions.hasMoreElements():
                part = portions.nextElement()
                if part.TextPortionType == 'ContentControl': found.append((part.ContentControl, label))
            if found: result.extend(found)
            elif item.getString().strip(): label = item.getString().strip()
    return result


def controls(text):
    return [control for control, label in located_controls(text)]


def read_controls(doc, fields):
    items = located_controls(doc.Text)
    if len(items) != len(fields): raise ValueError('LibreOffice control count differs from source')
    rows = []
    for field, (control, actual_label) in zip(fields, items):
        expected_label = field['label'] + (' *' if field['required'] else '')
        if actual_label != expected_label: raise ValueError('LibreOffice adjacent label differs: ' + field['id'])
        is_checkbox = bool(control.getPropertyValue('Checkbox'))
        if is_checkbox != (field['type'] == 'checkbox'): raise ValueError('LibreOffice control type differs from source')
        rows.append({'field_id': field['id'], 'adjacent_label_read': actual_label, 'type': field['type'], 'value': bool(control.Checked) if is_checkbox else control.getAnchor().getString()})
    return rows


def main():
    job = json.loads(Path(sys.argv[1]).read_text())
    profile = os.environ['LO_PROFILE_URI']
    process = subprocess.Popen(['libreoffice', '-env:UserInstallation=' + profile, '--headless', '--norestore', '--nodefault', '--nofirststartwizard', '--accept=pipe,name=schoolforms;urp;StarOffice.ComponentContext'], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    desktop = None
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', local)
        deadline = time.monotonic() + 30
        while True:
            try:
                context = resolver.resolve('uno:pipe,name=schoolforms;urp;StarOffice.ComponentContext'); break
            except Exception:
                if time.monotonic() > deadline: raise RuntimeError('LibreOffice UNO startup exceeded 30 seconds')
                time.sleep(0.2)
        desktop = context.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', context)
        def open_document(path):
            doc = desktop.loadComponentFromURL(Path(path).resolve().as_uri(), '_blank', 0, (prop('Hidden', True), prop('UpdateDocMode', 0), prop('MacroExecutionMode', 0)))
            if doc is None: raise ValueError('LibreOffice could not open ' + Path(path).name)
            return doc
        if job['action'] == 'fill':
            doc = open_document(job['blank'])
            try:
                before = read_controls(doc, job['fields'])
                doc.storeAsURL(Path(job['blank']).resolve().as_uri(), (prop('FilterName', 'Office Open XML Text'), prop('Overwrite', True)))
                for field, control in zip(job['fields'], controls(doc.Text)):
                    value = job['values'].get(field['id'], '' if field['type'] == 'text' else False)
                    if field['type'] == 'checkbox':
                        control.setPropertyValue('Checked', value)
                        entered_text = '☒' if value else '☐'
                    else:
                        control.setPropertyValue('ShowingPlaceHolder', False)
                        entered_text = value
                    # Writer 7.4 exposes control boundaries through XTextRange.
                    # Move past the opening marker, retaining the control itself.
                    anchor = control.getAnchor()
                    cursor = anchor.getText().createTextCursorByRange(anchor.getStart())
                    cursor.goRight(1, False)
                    cursor.gotoRange(anchor.getEnd(), True)
                    cursor.setString(entered_text)
                entered = read_controls(doc, job['fields'])
                for row in entered:
                    if row['value'] != job['values'].get(row['field_id'], '' if row['type'] == 'text' else False):
                        raise ValueError('UNO did not retain entered value: ' + repr(row))
                doc.storeAsURL(Path(job['filled']).resolve().as_uri(), (prop('FilterName', 'Office Open XML Text'), prop('Overwrite', True)))
            finally: doc.close(True)
            result = {'method': 'LibreOffice UNO cursor inside ContentControl / Checked; storeAsURL; close', 'before': before, 'entered': entered}
        else:
            result = {}
            for name in ('blank', 'filled'):
                doc = open_document(job[name])
                try:
                    result[name] = read_controls(doc, job['fields'])
                    if name == 'filled':
                        for row in result[name]:
                            expected = job['values'].get(row['field_id'], '' if row['type'] == 'text' else False)
                            if row['value'] != expected: raise ValueError('Reopened value differs: ' + row['field_id'])
                    doc.storeToURL(Path(job[name + '_pdf']).resolve().as_uri(), (prop('FilterName', 'writer_pdf_Export'), prop('Overwrite', True)))
                finally: doc.close(True)
            result['method'] = 'Reopen sanitized DOCX in LibreOffice UNO; inspect controls; export PDF'
        Path(job['record']).write_text(json.dumps(result, indent=2) + '\n')
    finally:
        if desktop is not None: desktop.terminate()
        try: process.wait(timeout=10)
        except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=5)


if __name__ == '__main__': main()
