"""Render AGREEMENT_SHORT_HE.html to AGREEMENT_SHORT_HE.pdf via headless Chromium.

Run after build_html.py. Adds a page-number footer ("עמוד X מתוך Y") on
every page via Chromium's native header/footer template mechanism, so the
signed, printed document can be checked for missing/out-of-order pages.
"""
from playwright.sync_api import sync_playwright
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(_HERE, "AGREEMENT_SHORT_HE.html")
PDF_PATH = os.path.join(_HERE, "AGREEMENT_SHORT_HE.pdf")
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

FOOTER_TEMPLATE = """
<div style="width:100%;font-family:Heebo,Helvetica,Arial,sans-serif;font-size:7.5pt;
 color:#7D6F5C;text-align:center;direction:rtl;letter-spacing:.04em;
 -webkit-print-color-adjust:exact;print-color-adjust:exact;">
  עמוד <span class="pageNumber"></span> מתוך <span class="totalPages"></span>
</div>
"""

# Repeating per-page brand/confidentiality header — matches the Guide's
# in-flow .pagehead breadcrumb (which the Agreement can't replicate exactly,
# since its content flows across native page breaks rather than pre-cut
# .page divs); this is the equivalent signal via Chromium's own header slot,
# present on every physical page instead of only page 1's masthead.
HEADER_TEMPLATE = """
<div style="width:100%;font-family:Heebo,Helvetica,Arial,sans-serif;font-size:6.8pt;
 color:#7D6F5C;text-align:center;direction:rtl;letter-spacing:.09em;
 -webkit-print-color-adjust:exact;print-color-adjust:exact;">
  LOS GARDIOS &nbsp;·&nbsp; סודי · CONFIDENTIAL &nbsp;·&nbsp; הסכם התקשרות עם לקוח
</div>
"""

# margins must match the CSS @page rule in build_html_short.py's CSS block —
# Chromium's print pipeline uses this `margin` option (not the CSS @page
# margin) to size the header/footer box once display_header_footer is on.
# Top is taller than bottom to make room for the repeating header line above.
MARGIN = {"top": "22mm", "bottom": "17mm", "left": "15mm", "right": "15mm"}


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page()
        page.goto(f"file://{HTML_PATH}")
        page.pdf(
            path=PDF_PATH, format="A4", print_background=True, prefer_css_page_size=True,
            display_header_footer=True, header_template=HEADER_TEMPLATE,
            footer_template=FOOTER_TEMPLATE, margin=MARGIN,
        )
        browser.close()
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
