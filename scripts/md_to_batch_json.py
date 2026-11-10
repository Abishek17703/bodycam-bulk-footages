import os
import re
import json

out_dir = r'C:\Users\abish\.gemini\antigravity\brain\882b3be2-cdc7-4132-8a3e-0334cc030687\scratch\snap_yt_analysis'

def parse_inline_runs(text):
    # Split by **bold** or *italic*
    runs = []
    pos = 0
    for m in re.finditer(r'(\*\*([^*]+)\*\*|\*([^*]+)\*)', text):
        if m.start() > pos:
            runs.append({'text': text[pos:m.start()], 'bold': False, 'italic': False})
        if m.group(2) is not None:
            runs.append({'text': m.group(2), 'bold': True, 'italic': False})
        else:
            runs.append({'text': m.group(3), 'bold': False, 'italic': True})
        pos = m.end()
    if pos < len(text):
        runs.append({'text': text[pos:], 'bold': False, 'italic': False})
    return runs if runs else [{'text': text, 'bold': False, 'italic': False}]

def md_to_ops(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\r\n') for l in f]

    ops = [
        {
            'op': 'set-default-style',
            'font_family': 'Arial',
            'font_size': 11,
            'text_color': '#000000',
            'space_above': 12,
            'space_below': 12
        }
    ]

    i = 0
    is_first_h3 = True
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == '---':
            ops.append({'op': 'horizontal-rule'})
            i += 1
            continue
        if line.startswith('# '):
            clean = line[2:].replace('**', '').strip()
            ops.append({
                'op': 'heading',
                'text': clean,
                'level': '1',
                'bold': True,
                'font_family': 'Arial',
                'font_size': 23,
                'text_color': '#000000',
                'space_above': 0,
                'space_below': 0
            })
            i += 1
            continue
        if line.startswith('## '):
            clean = line[3:].replace('**', '').strip()
            ops.append({
                'op': 'heading',
                'text': clean,
                'level': '2',
                'bold': True,
                'font_family': 'Arial',
                'font_size': 17,
                'text_color': '#000000',
                'space_above': 18,
                'space_below': 4
            })
            i += 1
            continue
        if line.startswith('### '):
            raw = line[4:].strip()
            if is_first_h3 and raw.startswith('*') and not raw.startswith('**'):
                clean = raw.strip('*').strip()
                ops.append({
                    'op': 'heading',
                    'text': clean,
                    'level': '3',
                    'bold': False,
                    'italic': True,
                    'font_family': 'Arial',
                    'font_size': 13,
                    'text_color': '#000000',
                    'space_above': 0,
                    'space_below': 12
                })
                is_first_h3 = False
            else:
                clean = raw.replace('**', '').strip()
                ops.append({
                    'op': 'heading',
                    'text': clean,
                    'level': '3',
                    'bold': True,
                    'italic': False,
                    'font_family': 'Arial',
                    'font_size': 13,
                    'text_color': '#000000',
                    'space_above': 14,
                    'space_below': 4
                })
                is_first_h3 = False
            i += 1
            continue
        if line.startswith('|'):
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                tline = lines[i].strip()
                cells = [c.strip() for c in tline.strip('|').split('|')]
                if not all(re.match(r'^:?-+:?$', c) for c in cells if c):
                    clean_cells = [c.replace('**', '').strip() for c in cells]
                    table_rows.append(clean_cells)
                i += 1
            if table_rows:
                nrows = len(table_rows)
                ncols = max(len(r) for r in table_rows)
                alignments = [['CENTER' if r == 0 else 'START' for _ in range(ncols)] for r in range(nrows)]
                ops.append({
                    'op': 'insert-table',
                    'table_data': table_rows,
                    'table_header_bold': True,
                    'table_header_bg_color': '#ffffff',
                    'table_header_text_color': '#000000',
                    'table_font_family': 'Arial',
                    'table_font_size': 11,
                    'table_border_color': '#000000',
                    'table_border_width': 0.5,
                    'table_cell_alignments': alignments
                })
            continue
        if line.startswith('- '):
            btext = line[2:].strip()
            runs = parse_inline_runs(btext)
            if len(runs) == 1 and not runs[0]['bold'] and not runs[0]['italic']:
                ops.append({
                    'op': 'bullet-list',
                    'text': runs[0]['text'],
                    'font_size': 11,
                    'text_color': '#000000',
                    'space_above': 0,
                    'space_below': 0
                })
            else:
                ops.append({
                    'op': 'rich-text',
                    'bullet_preset': 'BULLET_DISC_CIRCLE_SQUARE',
                    'font_family': 'Arial',
                    'font_size': 11,
                    'text_color': '#000000',
                    'runs': runs
                })
            i += 1
            continue

        # Normal paragraph
        runs = parse_inline_runs(line)
        if len(runs) == 1:
            ops.append({
                'op': 'append',
                'text': runs[0]['text'],
                'bold': runs[0]['bold'],
                'italic': runs[0]['italic'],
                'font_family': 'Arial',
                'font_size': 11,
                'text_color': '#000000'
            })
        else:
            ops.append({
                'op': 'rich-text',
                'font_family': 'Arial',
                'font_size': 11,
                'text_color': '#000000',
                'runs': runs
            })
        i += 1

    return ops

for name in ['updated_bodycam_doc', 'snapchat_workflow_doc']:
    ops = md_to_ops(os.path.join(out_dir, f'{name}.md'))
    out_json = os.path.join(out_dir, f'{name}_ops.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(ops, f, indent=2)
    print(f'Generated {len(ops)} batch ops -> {out_json}')
