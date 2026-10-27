import fitz

doc_orig = fitz.open('Final Report AI final+++.pdf')
doc_gen = fitz.open('Brozer_Final_Report.pdf')

print(f"{'Page':<5} | {'Orig Top':<35} | {'Gen Top':<35} | {'Orig Lines':<10} | {'Gen Lines':<10} | {'Orig Y-range':<15} | {'Gen Y-range':<15}")
print("-" * 135)

for i in range(len(doc_orig)):
    p_num = i + 1
    po = doc_orig[i]
    pg = doc_gen[i]
    
    lo = [l.strip() for l in po.get_text().splitlines() if l.strip()]
    lg = [l.strip() for l in pg.get_text().splitlines() if l.strip()]
    
    top_o = lo[0][:32] if lo else "[EMPTY]"
    top_g = lg[0][:32] if lg else "[EMPTY]"
    
    bo = [b for b in po.get_text('blocks') if b[4].strip()]
    bg = [b for b in pg.get_text('blocks') if b[4].strip()]
    
    yo_min = min([b[1] for b in bo]) if bo else 0
    yo_max = max([b[3] for b in bo]) if bo else 0
    yg_min = min([b[1] for b in bg]) if bg else 0
    yg_max = max([b[3] for b in bg]) if bg else 0
    
    print(f"{p_num:<5d} | {top_o:<35} | {top_g:<35} | {len(lo):<10d} | {len(lg):<10d} | {yo_min:5.1f}-{yo_max:5.1f}   | {yg_min:5.1f}-{yg_max:5.1f}")
