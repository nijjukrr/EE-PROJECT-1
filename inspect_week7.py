import fitz

doc = fitz.open("WEEK 7 NEW ABSTRACT- final.pdf")
print("Page count:", len(doc))
for pno in range(len(doc)):
    page = doc[pno]
    print(f"\n================ PAGE {pno+1} ================")
    data = page.get_text("dict")
    for block in data["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                line_str = " ".join([s["text"] for s in line["spans"] if s["text"].strip()])
                if not line_str.strip():
                    continue
                first_span = line["spans"][0]
                print(f"[{first_span['font']}, {first_span['size']:.1f}pt, flags={first_span['flags']}] ({line['bbox'][0]:.1f}, {line['bbox'][1]:.1f}): {line_str}")
