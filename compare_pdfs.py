import fitz
import sys

def analyze():
    doc_orig = fitz.open('Final Report AI final+++.pdf')
    doc_gen = fitz.open('Brozer_Final_Report.pdf')

    print(f"Original PDF total pages: {len(doc_orig)}")
    print(f"Generated PDF total pages: {len(doc_gen)}")

    mismatches = []
    
    for i in range(max(len(doc_orig), len(doc_gen))):
        p_num = i + 1
        if i >= len(doc_orig):
            print(f"Page {p_num}: Extra page in Generated PDF!")
            continue
        if i >= len(doc_gen):
            print(f"Page {p_num}: Missing page in Generated PDF!")
            continue

        p_orig = doc_orig[i]
        p_gen = doc_gen[i]

        orig_blocks = p_orig.get_text("blocks")
        gen_blocks = p_gen.get_text("blocks")

        orig_lines = [l.strip() for l in p_orig.get_text().splitlines() if l.strip()]
        gen_lines = [l.strip() for l in p_gen.get_text().splitlines() if l.strip()]

        orig_top = orig_lines[0] if orig_lines else "[EMPTY]"
        gen_top = gen_lines[0] if gen_lines else "[EMPTY]"
        orig_bot = orig_lines[-1] if orig_lines else "[EMPTY]"
        gen_bot = gen_lines[-1] if gen_lines else "[EMPTY]"

        # Calculate bounding boxes
        orig_rects = [b[:4] for b in orig_blocks if b[4].strip()]
        gen_rects = [b[:4] for b in gen_blocks if b[4].strip()]

        orig_min_y = min([r[1] for r in orig_rects]) if orig_rects else 0
        orig_max_y = max([r[3] for r in orig_rects]) if orig_rects else 0
        gen_min_y = min([r[1] for r in gen_rects]) if gen_rects else 0
        gen_max_y = max([r[3] for r in gen_rects]) if gen_rects else 0

        # Check alignment / content
        print(f"Page {p_num:2d} | Orig Y: ({orig_min_y:5.1f} - {orig_max_y:5.1f}) | Gen Y: ({gen_min_y:5.1f} - {gen_max_y:5.1f})")
        print(f"         Orig Top: {orig_top[:50]}")
        print(f"         Gen  Top: {gen_top[:50]}")
        print(f"         Orig Bot: {orig_bot[:50]}")
        print(f"         Gen  Bot: {gen_bot[:50]}")
        print("-" * 70)

if __name__ == '__main__':
    analyze()
