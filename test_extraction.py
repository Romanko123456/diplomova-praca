import pdfplumber
import sys

def test_extraction(pdf_path, page_num, x_tolerance_values):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1] # 0-indexed
        
        print(f"--- Testing Extraction on Page {page_num} ---")
        
        for x_tol in x_tolerance_values:
            print(f"\n[x_tolerance = {x_tol}]")
            text = page.extract_text(x_tolerance=x_tol)
            # Print first 500 chars to see effect
            print(text[:500])
            print("-" * 20)

if __name__ == "__main__":
    pdf_file = "original_75pages.pdf"
    # Page 2 usually has the start of introduction/text
    # Testing tolerance values: default is 3. 
    # If words are merged, we might need smaller tolerance (to force split) 
    # OR the logical grouping is wrong.
    test_extraction(pdf_file, 15, [1, 2, 3, 4]) # Page 15 is where Chapter 1 starts roughly
