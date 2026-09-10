"""Render AGREEMENT_v2_HE.html to AGREEMENT_v2_HE.pdf via headless Chromium.

Run after build_html.py. Adds a page-number footer ("עמוד X מתוך Y") on
every page via Chromium's native header/footer template mechanism, so the
signed, printed document can be checked for missing/out-of-order pages.
"""
from playwright.sync_api import sync_playwright
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(_HERE, "AGREEMENT_v2_HE.html")
PDF_PATH = os.path.join(_HERE, "AGREEMENT_v2_HE.pdf")
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

FOOTER_TEMPLATE = """
<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7.5pt;
 color:#5b6472;text-align:center;direction:rtl;letter-spacing:.04em;
 -webkit-print-color-adjust:exact;print-color-adjust:exact;">
  עמוד <span class="pageNumber"></span> מתוך <span class="totalPages"></span>
</div>
"""

# margins must match the CSS @page rule in build_html.py's CSS block —
# Chromium's print pipeline uses this `margin` option (not the CSS @page
# margin) to size the header/footer box once display_header_footer is on.
MARGIN = {"top": "17mm", "bottom": "17mm", "left": "15mm", "right": "15mm"}


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page()
        page.goto(f"file://{HTML_PATH}")
        page.pdf(
            path=PDF_PATH, format="A4", print_background=True, prefer_css_page_size=True,
            display_header_footer=True, header_template="<span></span>",
            footer_template=FOOTER_TEMPLATE, margin=MARGIN,
        )
        browser.close()
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
