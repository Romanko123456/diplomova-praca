import pdfplumber

def analyze_density(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        print("Page | Chars | Rects | Curves | Images")
        print("-----|-------|-------|--------|-------")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            chars = len(text)
            rects = len(page.rects)
            curves = len(page.curves)
            images = len(page.images)
            print(f"{i+1:4d} | {chars:5d} | {rects:5d} | {curves:6d} | {images:5d}")

if __name__ == "__main__":
    analyze_density("original_75pages.pdf")
