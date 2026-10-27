import fitz

doc = fitz.open('Final Report AI final+++.pdf')
for pno in [7, 8, 9]:
    print(f"\n=== PAGE {pno+1} SPANS ===")
    p = doc[pno]
    for block in p.get_text('dict')['blocks']:
        if 'lines' in block:
            for line in block['lines']:
                for span in line['spans']:
                    t = span['text'].strip()
                    if t:
                        print(f"  y={span['origin'][1]:5.1f}, x={span['origin'][0]:5.1f} | font={span['font']:25s} sz={span['size']:4.1f} | {t[:45]}")
