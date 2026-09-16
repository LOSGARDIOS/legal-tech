"""Render CLIENT_GUIDE_HE.html to CLIENT_GUIDE_HE.pdf via headless Chromium."""
from playwright.sync_api import sync_playwright
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(_HERE, "CLIENT_GUIDE_HE.html")
PDF_PATH = os.path.join(_HERE, "CLIENT_GUIDE_HE.pdf")
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

FOOTER_TEMPLATE = """
<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7.5pt;
 color:#8a8072;text-align:center;direction:rtl;letter-spacing:.04em;
 -webkit-print-color-adjust:exact;print-color-adjust:exact;">
  עמוד <span class="pageNumber"></span> מתוך <span class="totalPages"></span>
</div>
"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page()
        page.goto(f"file://{HTML_PATH}")
        page.pdf(
            path=PDF_PATH, format="A4", print_background=True, prefer_css_page_size=True,
            display_header_footer=True, header_template="<span></span>",
            footer_template=FOOTER_TEMPLATE, margin={"top": "0mm", "bottom": "12mm", "left": "0mm", "right": "0mm"},
        )
        browser.close()
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
