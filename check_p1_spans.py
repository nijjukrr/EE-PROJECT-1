import fitz

doc = fitz.open('Final Report AI final+++.pdf')
p1 = doc[0]
for block in p1.get_text('dict')['blocks']:
    if 'lines' in block:
        for line in block['lines']:
            for span in line['spans']:
                txt = span['text'].strip()
                if txt:
                    print(f"{txt:40s} | font={span['font']}, size={span['size']:.1f}, origin=({span['origin'][0]:.1f}, {span['origin'][1]:.1f})")
