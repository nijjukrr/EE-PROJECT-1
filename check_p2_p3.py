import fitz, json

doc = fitz.open('Final Report AI final+++.pdf')
p = doc[2]
data = json.loads(p.get_text('json'))
print("=== PAGE 3 ORIGINAL SPANS ===")
for b in data['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            for s in l['spans']:
                bbox = [round(x, 1) for x in s['bbox']]
                print(f"{bbox} font={s['font']} size={round(s['size'],1)} flags={s['flags']} text={s['text']!r}")

doc_gen = fitz.open('Brozer_Final_Report.pdf')
p_gen = doc_gen[2]
data_gen = json.loads(p_gen.get_text('json'))
print("\n=== PAGE 3 GENERATED SPANS ===")
for b in data_gen['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            for s in l['spans']:
                bbox = [round(x, 1) for x in s['bbox']]
                print(f"{bbox} font={s['font']} size={round(s['size'],1)} flags={s['flags']} text={s['text']!r}")
