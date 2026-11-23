"""
Build the submission technical report PDF from its Markdown source.

Source of truth : reports/SUBMISSION_TECHNICAL_REPORT.md
Outputs         : submission/pdf/technical_report.html
                  submission/pdf/OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf

Usage:  python testing/scripts/build_technical_report_pdf.py [WORKSPACE_ROOT]
Requires: the `markdown` package and Google Chrome / Chromium (headless print).
Images referenced in the Markdown are resolved relative to WORKSPACE_ROOT and embedded.
"""
import base64
import os
import re
import shutil
import subprocess
import sys

import markdown

WORKSPACE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                            os.environ.get("OSDAG_WORKSPACE", r"F:\FOSSEE internship"))
MD_SRC = os.path.join(WORKSPACE, "reports", "SUBMISSION_TECHNICAL_REPORT.md")
PDF_DIR = os.path.join(WORKSPACE, "submission", "pdf")
HTML_OUT = os.path.join(PDF_DIR, "technical_report.html")
PDF_OUT = os.path.join(PDF_DIR, "OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf")

CSS = """
@page { size: A4; margin: 15mm 15mm 16mm 15mm;
        @bottom-center { content: counter(page); font-family: 'Segoe UI', Inter, Arial, sans-serif;
                        font-size: 8pt; color: #7a8599; } }
body { font-family: 'Segoe UI', Inter, Arial, sans-serif; font-size: 9.4pt; line-height: 1.42;
       color: #1d2330; margin: 0; }
h1 { font-size: 17pt; color: #0b3a6e; margin: 0 0 2px 0; line-height: 1.2; }
h1 + p { margin-top: 0; color: #46546a; font-size: 10pt; }
h2 { font-size: 12pt; color: #0b3a6e; border-bottom: 1.5px solid #0b3a6e; padding-bottom: 2px;
     margin: 14px 0 6px 0; page-break-after: avoid; }
p, li { margin: 4px 0; }
ul, ol { margin: 4px 0 4px 0; padding-left: 20px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 8px 0; font-size: 8.5pt;
        page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #0b3a6e; color: #fff; text-align: left; padding: 3px 5px; font-weight: 600; }
td { border-bottom: 1px solid #d5dbe5; padding: 3px 5px; vertical-align: top; }
tr:nth-child(even) td { background: #f5f7fb; }
code { font-family: Consolas, 'DejaVu Sans Mono', monospace; font-size: 8.3pt;
       background: #eef1f6; padding: 0 3px; border-radius: 2px; }
pre { background: #f3f5f9; border: 1px solid #d5dbe5; border-left: 3px solid #0b3a6e;
      padding: 6px 8px; font-size: 8.2pt; line-height: 1.35; white-space: pre-wrap;
      page-break-inside: avoid; }
pre code { background: none; padding: 0; }
img { display: block; max-width: 88%; max-height: 95mm; margin: 6px auto 2px auto;
      border: 1px solid #c8d0dc; }
img + em, p > em:only-child { display: block; text-align: center; font-size: 8.2pt; color: #46546a; }
strong { color: #111; }
"""


def embed_images(html: str) -> str:
    def repl(m):
        src = m.group(1)
        path = os.path.join(WORKSPACE, *src.split("/"))
        if not os.path.exists(path):
            raise FileNotFoundError(f"Report image not found: {path}")
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        ext = os.path.splitext(path)[1].lstrip(".").lower().replace("jpg", "jpeg")
        return f'src="data:image/{ext};base64,{data}"'
    return re.sub(r'src="([^"]+)"', repl, html)


def find_chrome():
    for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              shutil.which("google-chrome"), shutil.which("chromium"),
              shutil.which("chromium-browser")):
        if c and os.path.exists(c):
            return c
    raise FileNotFoundError("Chrome/Chromium not found")


def main():
    with open(MD_SRC, encoding="utf-8") as f:
        md_text = f.read()
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    body = embed_images(body)
    title = "OsdagBridge Technical Report - Subodh Bansode"
    html = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")
    os.makedirs(PDF_DIR, exist_ok=True)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)
    cmd = [find_chrome(), "--headless=new", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", f"--print-to-pdf={PDF_OUT}",
           "file:///" + HTML_OUT.replace("\\", "/").lstrip("/")]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not os.path.exists(PDF_OUT):
        sys.exit(f"PDF build failed:\n{res.stderr}")
    print("Wrote", PDF_OUT)


if __name__ == "__main__":
    main()
