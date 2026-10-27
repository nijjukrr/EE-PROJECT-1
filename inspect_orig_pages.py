import fitz

doc_orig = fitz.open('Final Report AI final+++.pdf')
doc_gen = fitz.open('Brozer_Final_Report.pdf')

print("--- ORIGINAL PDF PAGES ---")
for i in range(len(doc_orig)):
    p = doc_orig[i]
    lines = [l.strip() for l in p.get_text().splitlines() if l.strip()]
    top = lines[0] if lines else ''
    bot = lines[-1] if lines else ''
    print(f"P{i+1:02d}: top='{top[:40]}' | bot='{bot[:40]}'")

print("\n--- GENERATED PDF PAGES ---")
for i in range(len(doc_gen)):
    p = doc_gen[i]
    lines = [l.strip() for l in p.get_text().splitlines() if l.strip()]
    top = lines[0] if lines else ''
    bot = lines[-1] if lines else ''
    print(f"P{i+1:02d}: top='{top[:40]}' | bot='{bot[:40]}'")
