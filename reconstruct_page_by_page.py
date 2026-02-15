import re
import sys
import latex_assets

# --- CONFIGURATION ---
INPUT_FILE = r'kapitoly/extracted_pdf_text.txt'
OUTPUT_DIR = r'kapitoly'

# Define page ranges (Inclusive 1-based PDF page numbers from === PAGE X ===)
# Based on scan analysis
RANGES = {
    'uvod': (14, 14, "uvod.tex", "Úvod"),
    'kap1': (15, 30, "teoreticka_cast.tex", "Teoretická časť"), # Ch 1 + start of Ch 2?
    # Note: Ch 2 starts inside this range, we will detect it dynamically OR just put Ch1+Ch2 in one file?
    # Better: Split properly.
    # User screenshot showed "2 Interferenčné prúdy" on some page.
    # Let's try to detect the header "2 Interferenčné prúdy" to switch to chapter 2 file.
    'kap3': (42, 59, "metodika.tex", "Cieľ práce a metodológia"),
    'kap4': (60, 63, "diskusia.tex", "Diskusia"),
    'odporucania': (64, 64, "odporucania.tex", "Odporúčania pre prax"),
    'zaver': (65, 65, "zaver.tex", "Záver"),
    'biblio': (66, 70, "bibliografia_reconstructed.tex", "Zoznam bibliografických odkazov"),
    'prilohy': (71, 75, "prilohy.tex", "Prílohy")
}

# Native Chart/Table Injection Map (Page -> Content Key)
# Tables: 'Tabuľka 1', 'Tabuľka 2', etc.
# Charts: 'page_43_chart.png' -> latex_assets.PAGE_CHARTS[43]

def clean_text(text):
    # Basic cleanup
    text = text.replace('ˇ', 'č').replace('´', 'í').replace('  ', ' ')
    # Fix broken diacritics common in this PDF
    text = text.replace('cˇ', 'č').replace('sˇ', 'š').replace('zˇ', 'ž').replace('rˇ', 'ř').replace('l’', 'ľ').replace('d’', 'ď').replace('t’', 'ť').replace('nˇ', 'ň').replace('oˆ', 'ô').replace('a´', 'á').replace('e´', 'é').replace('i´', 'í').replace('o´', 'ó').replace('u´', 'ú').replace('y´', 'ý')
    text = text.replace('Cˇ', 'Č').replace('Sˇ', 'Š').replace('Zˇ', 'Ž').replace('A´', 'Á').replace('E´', 'É').replace('I´', 'Í')
    return text

def reconstruct():
    print("Reading extracted text...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by pages
    # Note: re.split includes the capturing group, so list is [pre, 1, text, 2, text...]
    parts = re.split(r'=== PAGE (\d+) ===', content)
    
    # Store pages in a dict for easy access
    pages = {}
    for i in range(1, len(parts), 2):
        page_num = int(parts[i])
        page_text = parts[i+1]
        pages[page_num] = page_text

    # Prepare buffers
    buffers = {
        'uvod.tex': [],
        'teoreticka_cast.tex': [],
        'interferencne_prudy.tex': [], # Split Ch 2 here
        'metodika.tex': [],
        'diskusia.tex': [],
        'odporucania.tex': [],
        'zaver.tex': [],
        'bibliografia_reconstructed.tex': [],
        'prilohy.tex': []
    }

    current_chapter_file = 'teoreticka_cast.tex' # Default start for theory

    # Process Pages 1 to 75
    for p in range(1, 76):
        if p not in pages:
            continue
        
        raw_text = pages[p]
        clean = clean_text(raw_text)
        lines = clean.split('\n')
        
        # --- ROUTING LOGIC ---
        target_file = None
        
        if p == 14:
            target_file = 'uvod.tex'
        elif 15 <= p <= 41:
            # Check for Chapter 2 Header to switch file
            if "2 Interferenčné prúdy" in clean or "2 Interferencˇné prúdy" in raw_text or "2. Interferenčné prúdy" in clean:
                 current_chapter_file = 'interferencne_prudy.tex'
                 # Find the line and make it a chapter
                 # (Will do simple file routing for now, text processing later)
            
            # Additional check: If we are deep in page numbers (e.g. > 30), force switch if not already
            if p > 30 and current_chapter_file == 'teoreticka_cast.tex':
                 # Fallback if header missed (unlikely with deep scan)
                 # But let's trust the header detection or maybe hardcode p25?
                 # Let's inspect P25 later. For now, rely on variable.
                 pass

            target_file = current_chapter_file
            
        elif 42 <= p <= 59:
            target_file = 'metodika.tex'
        elif 60 <= p <= 63:
            target_file = 'diskusia.tex'
        elif p == 64:
            target_file = 'odporucania.tex'
        elif p == 65:
            target_file = 'zaver.tex'
        elif 66 <= p <= 70:
            target_file = 'bibliografia_reconstructed.tex'
        elif 71 <= p <= 75:
            target_file = 'prilohy.tex'
            
        if not target_file:
            print(f"Skipping Page {p} (Front matter or unknown)")
            continue

        # --- PROCESSING & INJECTION ---
        buffer = buffers[target_file]
        
        # Add Page Marker for debugging
        # buffer.append(f"% === Original Page {p} ===\n")
        
        # Inject Charts/Tables?
        # Check latex_assets for this page
        if p in latex_assets.PAGE_CHARTS:
             buffer.append("\n" + "\n".join(latex_assets.PAGE_CHARTS[p]) + "\n")
             print(f"Injected Chart for Page {p}")
        
        # Full Page Images (Appendix)
        if "[[FULL_PAGE_IMAGE:" in raw_text or "[[FULL_PAGE:" in raw_text:
             match = re.search(r'\[\[FULL_PAGE(?:_IMAGE)?: (.*?)\]\]', raw_text)
             if match:
                 image_path = match.group(1)
                 buffer.append(f"\\begin{{figure}}[p]\\centering\\includegraphics[width=1.0\\textwidth, height=0.9\\textheight, keepaspectratio]{{{image_path}}}\\end{{figure}}\n")
                 continue # Skip text if full page image

        # Line-by-Line Processing
        for line in lines:
            line = line.strip()
            if not line: continue
            if "[[CHART:" in line: continue # Handled by injection
            if "[[IMAGE:" in line: continue # Handled below
            if "=== PAGE" in line: continue
            
            # Filter garbage
            if re.match(r'^\d+$', line): continue # Page numbers
            if "enputs" in line or "ubyhophaszoR" in line: continue
            
            # Header Handling
            if re.match(r'^2\s+Interferenčné prúdy', line, re.IGNORECASE):
                buffer.append(f"\\chapter{{Interferenčné prúdy}}\n")
                continue
            if re.match(r'^3\s+Cieľ', line, re.IGNORECASE):
                 buffer.append(f"\\chapter{{Cieľ práce a metodológia}}\n")
                 continue
            if re.match(r'^4\s+Diskusia', line, re.IGNORECASE):
                 buffer.append(f"\\chapter{{Diskusia}}\n")
                 continue
            
            # Special Handling for Bibliography Header
            if "Zoznam bibliografických" in line and target_file == 'bibliografia_reconstructed.tex':
                 buffer.append("\\chapter*{Zoznam bibliografických odkazov}\n\\addcontentsline{toc}{chapter}{Zoznam bibliografických odkazov}\n")
                 continue
            
            # Tables Handling (Native)
            table_match = re.search(r'(Tabuľka \d+)', line)
            if table_match:
                 key = table_match.group(1).replace('l’', 'ľ') # Fix typos
                 if key in latex_assets.TABLES:
                      buffer.append("\n" + latex_assets.TABLES[key] + "\n")
                      continue # Skip the text line identifying the table

            # Images (Raster)
            if "[[IMAGE:" in raw_text and line.startswith('[[IMAGE:'): # Re-check line
                 img_path = line.replace('[[IMAGE:', '').replace(']]', '').strip()
                 buffer.append(f"\\begin{{figure}}[ht]\\centering\\includegraphics[width=0.8\\textwidth]{{{img_path}}}\\end{{figure}}\n")
                 continue

            buffer.append(line + "\n")
        
        buffer.append("\n\n")

    # --- WRITING FILES ---
    for fname, lines in buffers.items():
        if not lines and fname != 'interferencne_prudy.tex': 
            print(f"Warning: {fname} is empty")
            continue
            
        with open(f"{OUTPUT_DIR}/{fname}", 'w', encoding='utf-8') as f:
            f.write("".join(lines))
        print(f"Wrote {fname}")

    # Special handling for Bibliography
    # If we wrote to bibliografia_reconstructed.tex, we need to tell main.tex to use it?
    # Or convert it to .bib?
    # Given the time, I'll format the text in bibliografia_reconstructed.tex as a manual list for now
    # to guarantee it appears.
    # We will modify main.tex to include this file instead of \printbibliography if needed,
    # OR we parse it to .bib.
    # Parsing 5 pages of references to .bib perfectly is hard. 
    # Plan: Create a manual "The Bibliography" chapter in bibliografia_reconstructed.tex
    # and \input it in main.tex (commenting out \printbibliography).
    
if __name__ == "__main__":
    reconstruct()
