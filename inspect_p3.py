import fitz, json

doc = fitz.open('Final Report AI final+++.pdf')
p = doc[2]
data = json.loads(p.get_text('json'))
print("=== ORIGINAL PAGE 3 ===")
for b in data['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            line_str = "".join([s['text'] for s in l['spans']])
            if line_str.strip():
                print(f"y={round(l['bbox'][1], 1)} - {round(l['bbox'][3], 1)}: {line_str.strip()}")

doc_gen = fitz.open('Brozer_Final_Report.pdf')
p_gen = doc_gen[2]
data_gen = json.loads(p_gen.get_text('json'))
print("\n=== GENERATED PAGE 3 ===")
for b in data_gen['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            line_str = "".join([s['text'] for s in l['spans']])
            if line_str.strip():
                print(f"y={round(l['bbox'][1], 1)} - {round(l['bbox'][3], 1)}: {line_str.strip()}")
