import fitz, json

doc = fitz.open('test_p2_p3.pdf')
print(f"Total pages: {len(doc)}")

p2 = doc[1]
print("=== TEST PAGE 2 DRAWINGS ===")
for d in p2.get_drawings():
    print(d['items'], d['rect'], d.get('width'))
print("=== TEST PAGE 2 TEXT ===")
for b in json.loads(p2.get_text('json'))['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            for s in l['spans']:
                if s['text'].strip():
                    print(s['bbox'], s['font'], s['size'], repr(s['text']))

p3 = doc[2]
print("\n=== TEST PAGE 3 LINES ===")
for b in json.loads(p3.get_text('json'))['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            line_str = "".join([s['text'] for s in l['spans']])
            if line_str.strip():
                print(f"y={round(l['bbox'][1], 1)} - {round(l['bbox'][3], 1)}: {line_str.strip()}")
