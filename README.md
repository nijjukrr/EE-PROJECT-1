# Brozer: A Privacy Boundary for Browser Agents

**Department of Computer Science and Engineering**  
*Final Year Project Report Engineering & Automation Suite*

---

## 📌 Overview

**Brozer** is an autonomous browser-agent architecture with a testable, client-side privacy boundary. Unlike conventional browser agents that offload complete visual viewports and raw DOM trees to third-party reasoning engines, Brozer introduces an on-device perception and sanitization pipeline that enforces least-privilege context transmission:

$$\text{PERCEIVE} \longrightarrow \text{DETECT} \longrightarrow \text{SANITIZE} \longrightarrow \text{REASON} \longrightarrow \text{POLICY CHECK} \longrightarrow \text{ACT}$$

1. **Local Perception**: Extracts interactive DOM elements and runs lightweight visual detection locally via WebAssembly / ONNX Runtime Web.
2. **Multi-Signal Detection**: Flags passwords, tokens, payment data, and PII across regex, accessibility labels, and visual regions.
3. **Context Sanitization**: Replaces confidential values with semantic tokens (`[EMAIL]`, `[PASSWORD]`) and blurs private screen regions prior to network transmission.
4. **Structured Reasoning**: Remote or local Vision-Language Models (VLM) reason only on sanitized context, returning structured actions.
5. **Policy Gate**: Client-side execution firewall evaluates actions against deterministic security rules (`ALLOW`, `REDACT`, `BLOCK`, `ASK USER`).
6. **Local Execution**: Native DOM dispatch with client-vault credential autofill.

---

## 📂 Repository Structure

```
.
├── Brozer_Final_Report.docx        # Compiled final institutional report (60 pages)
├── Brozer_Final_Report.pdf         # Exported PDF with strict page & line budgets
├── Brozer_Project_Report.docx      # Secondary standalone report document
├── DATA.md                         # Complete project specifications & knowledge base
├── README.md                       # Project overview and documentation
│
├── generate_exact_report.py        # Master script: 60-page pixel-perfect docx generator
├── build_report.py                 # Core document generation pipeline
├── generate_figures.py             # Programmatic architecture & telemetry figure generator
├── convert_to_pdf.ps1              # Headless Word COM automation for docx -> pdf conversion
│
├── compare_pdfs.py                 # Multi-page layout, margin, and typography comparator
├── check_all_pages_alignment.py    # Cross-document page-by-page alignment validation
├── inspect_orig_pages.py           # Text span and header/footer boundary inspector
│
├── generated_assets/               # Production screenshots & diagrams used in the report
│   ├── fig_4_1_system_architecture.jpg
│   ├── fig_4_2_flowchart.jpg
│   ├── fig_4_3_dashboard.jpg       # Brozer Extension UI / ACT mode prompt
│   ├── fig_4_4_live_feed.jpg       # Live page perception & action feed on Amazon.in
│   ├── fig_4_5_violation.png       # User's View vs AI's View redaction comparison
│   ├── fig_4_6_plate_records.jpg   # Policy Gate confirmation on form submission
│   ├── fig_4_7_analytics.png       # System latency & redaction analytics
│   └── fig_4_8_settings.jpg        # Privacy policy & threshold configuration
│
└── extracted_assets/               # Extracted institutional emblems and reference graphics
```

---

## 🛠️ Usage & Compilation

### 1. Requirements
- Python 3.10+
- `python-docx`
- `PyMuPDF` (`fitz`)
- `Pillow`
- Microsoft Word (for headless PDF export via PowerShell)

### 2. Generate Final Report (.docx)
```bash
python generate_exact_report.py
```

### 3. Convert to PDF
```powershell
powershell -ExecutionPolicy Bypass -File .\convert_to_pdf.ps1 -inputFile .\Brozer_Final_Report.docx -outputFile .\Brozer_Final_Report.pdf
```

### 4. Validate Page Budget and Alignment
```bash
python compare_pdfs.py
```

---

## 📜 License & Acknowledgments
Built for the academic project submission in Computer Science & Engineering. Based on the open-source WebBrain architecture with privacy boundary enhancements.
