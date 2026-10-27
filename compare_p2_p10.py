import fitz

doc_orig = fitz.open('Final Report AI final+++.pdf')
doc_gen = fitz.open('Brozer_Final_Report.pdf')

for pno in range(1, 10):
    po = doc_orig[pno]
    pg = doc_gen[pno]
    print(f"\n==================== PAGE {pno+1} ====================")
    bo = [b for b in po.get_text('blocks') if b[4].strip()]
    bg = [b for b in pg.get_text('blocks') if b[4].strip()]
    
    print(f"ORIG (count={len(bo)}):")
    for b in bo[:3]:
        print(f"  y: {b[1]:.1f}-{b[3]:.1f}, x: {b[0]:.1f}-{b[2]:.1f} | {b[4][:50].strip()}")
    if len(bo) > 3:
        print(f"  ... ({len(bo)-4} intermediate blocks) ...")
        b = bo[-1]
        print(f"  LAST y: {b[1]:.1f}-{b[3]:.1f}, x: {b[0]:.1f}-{b[2]:.1f} | {b[4][:50].strip()}")

    print(f"GEN  (count={len(bg)}):")
    for b in bg[:3]:
        print(f"  y: {b[1]:.1f}-{b[3]:.1f}, x: {b[0]:.1f}-{b[2]:.1f} | {b[4][:50].strip()}")
    if len(bg) > 3:
        print(f"  ... ({len(bg)-4} intermediate blocks) ...")
        b = bg[-1]
        print(f"  LAST y: {b[1]:.1f}-{b[3]:.1f}, x: {b[0]:.1f}-{b[2]:.1f} | {b[4][:50].strip()}")
