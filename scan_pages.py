import re

def scan_pages():
    with open('kapitoly/extracted_pdf_text.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by pages
    pages = re.split(r'=== PAGE (\d+) ===', content)
    
    # pages[0] is preamble before first page marker
    # pages[1] is page num 1, pages[2] is content of page 1
    # pages[3] is page num 2, pages[4] is content of page 2
    
    print("--- PAGE MAP ---")
    for i in range(1, len(pages), 2):
        page_num = pages[i]
        text = pages[i+1].strip()
        
        # Look for headers in the first 200 chars of the page
        header_text = text[:200].replace('\n', ' ')
        
        qt = ""
        if "Úvod" in header_text or "ÚVOD" in header_text:
            qt = "ÚVOD"
        elif "Kapitola 1" in header_text or "TEORETICKÁ ČASŤ" in header_text.upper():
            qt = "KAPITOLA 1"
        elif "Kapitola 2" in header_text:
            qt = "KAPITOLA 2"
        elif "Kapitola 3" in header_text or "Cieľ práce" in header_text:
            qt = "KAPITOLA 3"
        elif "Kapitola 4" in header_text or "Diskusia" in header_text:
            qt = "KAPITOLA 4"
        elif "Záver" in header_text or "ZÁVER" in header_text:
            qt = "ZÁVER"
        elif "Zoznam bibliografických" in header_text or "BIBLIOGRAFIA" in header_text.upper():
            qt = "BIBLIOGRAFIA"
        elif "Zoznam príloh" in header_text:
            qt = "ZOZNAM PRÍLOH"
        
        if qt:
            print(f"Page {page_num}: {qt}")

if __name__ == "__main__":
    scan_pages()
