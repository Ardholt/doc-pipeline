"""Validate public inputs and retain exact money as decimal values."""
import csv, json, re
from decimal import Decimal
from pathlib import Path

def read_inputs(folder):
    folder = Path(folder)
    for name in ('data.csv', 'deck.json'):
        if not (folder / name).is_file():
            raise ValueError(f'missing required input: {name}')
    cfg = json.loads((folder / 'deck.json').read_text(encoding='utf-8'))
    if not isinstance(cfg, dict):
        raise ValueError('deck.json: expected a JSON object')
    if type(cfg.get('schema_version')) is not int or cfg.get('schema_version') != 1:
        raise ValueError('deck.json: schema_version must be 1')
    title = cfg.get('title')
    if not isinstance(title, str) or not title.strip() or len(title) > 70 or '\n' in title:
        raise ValueError('deck.json: title must be a single line of 1–70 characters')
    if not re.fullmatch(r'[A-Z]{3}', str(cfg.get('currency', ''))):
        raise ValueError('deck.json: currency must be a three-letter uppercase code')
    rows, seen = [], set()
    with (folder / 'data.csv').open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['period', 'department', 'revenue', 'cost']:
            raise ValueError('data.csv: expected period,department,revenue,cost header')
        for line, row in enumerate(reader, 2):
            if None in row:
                raise ValueError(f'data.csv line {line}: unexpected extra column')
            p, d = row['period'], row['department']
            if not p or not re.fullmatch(r'[0-9]{4}-(0[1-9]|1[0-2])', p):
                raise ValueError(f'data.csv line {line}: period must be YYYY-MM')
            if not d or not re.fullmatch(r'[A-Z][A-Z0-9_-]{0,7}', d):
                raise ValueError(f'data.csv line {line}: department must be an anonymous code, 1–8 characters')
            if (p, d) in seen:
                raise ValueError(f'data.csv line {line}: duplicate period/department')
            seen.add((p, d))
            for field in ('revenue', 'cost'):
                if not isinstance(row[field], str) or not re.fullmatch(r'(0|[1-9][0-9]*)(\.[0-9]{1,2})?', row[field]):
                    raise ValueError(f'data.csv line {line}: {field} must be nonnegative decimal money with up to two decimal places')
                row[field] = Decimal(row[field])
                if row[field] > Decimal('999999999.99'):
                    raise ValueError(f'data.csv line {line}: {field} exceeds supported money range')
            row['profit'] = row['revenue'] - row['cost']
            row['line'] = line
            rows.append(row)
    if not rows:
        raise ValueError('data.csv: no data rows')
    order = cfg.get('department_order')
    if not isinstance(order, list) or not all(isinstance(x, str) for x in order) or len(set(order)) != len(order) or set(order) != {r['department'] for r in rows}:
        raise ValueError('deck.json: department_order must cover every department exactly once')
    colours = cfg.get('colours')
    if not isinstance(colours, dict) or any(not re.fullmatch(r'#[0-9A-Fa-f]{6}', str(colours.get(d, ''))) for d in order):
        raise ValueError('deck.json: colours must provide #RRGGBB for every department')
    periods = sorted({r['period'] for r in rows})
    if len(order) > 12 or len(periods) > 24:
        raise ValueError('supported boundary: at most 12 departments and 24 periods')
    if len(rows) != len(order) * len(periods):
        raise ValueError('data.csv: each period must contain every department; missing rows are not treated as zero')
    return cfg, rows, periods

def sums(rows):
    return {key: sum((r[key] for r in rows), Decimal(0)) for key in ('revenue', 'cost', 'profit')}

def money(value):
    return f'{value:,.0f}' if value == value.to_integral() else f'{value:,.2f}'
