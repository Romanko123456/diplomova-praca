#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert extracted PDF text to LaTeX format for thesis
Handles Slovak special characters, section markers, citations, etc.
"""

import re
import sys
import latex_assets

def clean_ocr_text(text):
    """Clean up OCR artifacts and normalize text"""
    # Order matters! Replace multi-char sequences first.
    replacements = {
        # Fix split diacritics first
        'cˇ': 'č',
        'Cˇ': 'Č',
        'rˇ': 'ř',
        'sˇ': 'š',
        'Sˇ': 'Š',
        'zˇ': 'ž',
        'Zˇ': 'Ž',
        'l’': 'ľ',
        'L’': 'Ľ',
        'd’': 'ď',
        'D’': 'Ď',
        't’': 'ť',
        'T’': 'Ť',
        'nˇ': 'ň',
        'Nˇ': 'Ň',
        
        # Then remove artifacts
        'ˇ': '',  # Remove remaining hat artifacts
        '´': '',  # Remove remaining acute artifacts  
        '`': '',  # Remove grave artifacts
        
        # Standardize characters
        'ä': 'ä',
        'ö': 'ö',
        ''': "'",
        ''': "'",
        '"': '"',
        '"': '"',
        '–': '--',
        '—': '---',
        '...': '\\ldots{}',
        ' %': '\\%',
        
        # Math and Greek symbols
        'α': '$\\alpha$',
        'β': '$\\beta$',
        'γ': '$\\gamma$',
        'δ': '$\\delta$',
        'µ': '$\\mu$',
        '−': '$-$',  # Minus sign U+2212
        '≈': '$\\approx$',
        '≤': '$\\le$',
        '≥': '$\\ge$',
        '±': '$\\pm$',
        '×': '$\\times$',
        '°': '$^\\circ$',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def extract_chapter_content(text, chapter_num, start_pattern, end_pattern):
    """Extract content for a specific chapter"""
    # Find start page
    start_match = re.search(start_pattern, text, re.IGNORECASE | re.MULTILINE)
    if not start_match:
        # Try fuzzy match if exact failed (some OCR issues)
        if "Cieľ práce" in start_pattern:
             start_match = re.search(r'3\s*Cieľ\s*práce', text, re.IGNORECASE)
        
        if not start_match:
            print(f"Warning: Start pattern '{start_pattern}' not found.", file=sys.stderr)
            return ""
    
    start_pos = start_match.start()
    
    # Find end page or next chapter
    if end_pattern:
        end_match = re.search(end_pattern, text[start_pos+100:], re.IGNORECASE | re.MULTILINE) # Offset to avoid self-match
        if end_match:
            end_pos = start_pos + 100 + end_match.start()
        else:
            end_pos = len(text)
    else:
        end_pos = len(text)
    
    return text[start_pos:end_pos]

def dehyphenate_text(text):
    """Fix hyphenated words across lines (e.g., 're-\numatickým' -> 'reumatickým')"""
    # Pattern: Word ending with -, newline, word starting next line
    # Note: We need to be careful not to remove hyphens from actual hyphenated words like "Socio-ekonomická"
    # But usually those don't span lines unless split.
    # If it's "slo- \n vo", we want "slovo".
    
    # Simple approach: remove -\n and join. 
    # Valid for Slovak where hyphen at end of line usuall means word split.
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    return text

def convert_to_latex(text, chapter_name):
    """Convert raw text to LaTeX format"""
    # De-hyphenate first
    text = dehyphenate_text(text)
    
    lines = text.split('\n')
    latex_lines = []
    
    # Add chapter header
    latex_lines.append(f"\\chapter{{{chapter_name}}}\n")
    
    in_paragraph = False
    paragraph_text = []
    current_page_num = 0
    
    for line in lines:
        line = line.strip()
        
        # Parse Page Number
        if line.startswith('=== PAGE'):
            try:
                current_page_num = int(line.replace('=== PAGE', '').replace('===', '').strip())
            except:
                pass
            continue
            
        # Skip empty lines
        if not line:
            continue
        
        # Handle Image Markers (Raster)
        if line.startswith('[[IMAGE:') and line.endswith(']]'):
            if paragraph_text:
                latex_lines.append(' '.join(paragraph_text))
                latex_lines.append('\n\n')
                paragraph_text = []
            
            image_path = line.replace('[[IMAGE:', '').replace(']]', '').strip()
            image_path = image_path.replace('\\', '/')
            
            latex_lines.append(f"\\begin{{figure}}[ht]\n")
            latex_lines.append(f"    \\centering\n")
            latex_lines.append(f"    \\includegraphics[width=0.6\\textwidth]{{{image_path}}}\n") # Smaller for icons/photos
            latex_lines.append(f"    \\caption{{Obrázok}}\n")
            latex_lines.append(f"\\end{{figure}}\n")
            continue


        # Handle Chart Markers (Vector Graphics) -> Replace with Native PGFPlots
        if line.startswith('[[CHART:') and line.endswith(']]'):
            # Flush paragraph
            if paragraph_text:
                latex_lines.append(' '.join(paragraph_text))
                latex_lines.append('\n\n')
                paragraph_text = []
            
            # Check if we have a native chart for this page
            if current_page_num in latex_assets.PAGE_CHARTS:
                # Pop the first chart key for this page
                if latex_assets.PAGE_CHARTS[current_page_num]:
                    chart_code = latex_assets.PAGE_CHARTS[current_page_num].pop(0)
                    latex_lines.append(chart_code)
                    latex_lines.append('\n')
            else:
                # Fallback to image if no native chart defined (should not happen for key pages)
                image_path = line.replace('[[CHART:', '').replace(']]', '').strip()
                image_path = image_path.replace('\\', '/')
                latex_lines.append(f"\\begin{{figure}}[ht]\n")
                latex_lines.append(f"    \\centering\n")
                latex_lines.append(f"    \\includegraphics[width=0.95\\textwidth, height=0.5\\textheight, keepaspectratio]{{{image_path}}}\n")
                latex_lines.append(f"    \\caption{{Graf}}\n")
                latex_lines.append(f"\\end{{figure}}\n")
            continue

        # Handle Tables -> Replace with Native Tabular
        # Regex to detect "Tabuľka X Description"
        table_match = re.match(r'^(Tabul’ka \d+)(.*)', line)
        if table_match:
            table_key = table_match.group(1) # e.g. "Tabul’ka 4"
            
            # If we have a native definition for this table
            if table_key in latex_assets.TABLES:
                 if paragraph_text:
                    latex_lines.append(' '.join(paragraph_text))
                    latex_lines.append('\n\n')
                    paragraph_text = []
                 
                 latex_lines.append(latex_assets.TABLES[table_key])
                 latex_lines.append('\n')
                 # Skip this line as it's part of the header we just replaced
                 continue

        # Filter out reversed text artifacts from charts
        if 'enputs(ubyhophaszoR' in line or 'einepútsaZ' in line or 'eróksSAV' in line or 'aitunhutsatiznetnI' in line or 'votneicaptečoP' in line or 'vodobtečúS' in line:
            continue

        # Filter out raw data lines often found near charts (e.g. "60", "50", "28 26")
        # Heuristic: Line contains only digits, spaces, or single chars, or specific keywords like "MTP - Flexia"
        if re.match(r'^[\d\s,\.\-±]+$', line) and len(line) < 50:
            continue
        if line.strip() in ['Pred terapiou', 'Po terapii', 'ITF + kinezioterapia Kinezioterapia', 'Kinezioterapia', 'ITF + kinezioterapia']:
            continue
        if "MTP - Flexia" in line or "MTP - Extenzia" in line or "Zápästie - Flexia" in line:
            # These are headers of the raw tables we replaced
            continue

        # Handle Tables -> Replace with Native Tabular
        # Regex to detect "Tabuľka X Description"
        table_match = re.match(r'^(Tabul’ka \d+)(.*)', line)
        if table_match:
            table_key = table_match.group(1) # e.g. "Tabul’ka 4"
            
            # If we have a native definition for this table
            if table_key in latex_assets.TABLES:
                 if paragraph_text:
                    latex_lines.append(' '.join(paragraph_text))
                    latex_lines.append('\n\n')
                    paragraph_text = []
                 
                 latex_lines.append(latex_assets.TABLES[table_key])
                 latex_lines.append('\n')
                 # Skip this line as it's part of the header we just replaced
                 continue

        # Filter out reversed text artifacts from charts
        if 'enputs(ubyhophaszoR' in line or 'einepútsaZ' in line or 'eróksSAV' in line or 'aitunhutsatiznetnI' in line or 'votneicaptečoP' in line or 'vodobtečúS' in line:
            continue

        # Filter out raw data lines often found near charts (e.g. "60", "50", "28 26")
        # Heuristic: Line contains only digits, spaces, or single chars, or specific keywords like "MTP - Flexia"
        if re.match(r'^[\d\s,\.\-±]+$', line) and len(line) < 50:
            continue
        if line.strip() in ['Pred terapiou', 'Po terapii', 'ITF + kinezioterapia Kinezioterapia', 'Kinezioterapia', 'ITF + kinezioterapia']:
            continue
        if "MTP - Flexia" in line or "MTP - Extenzia" in line or "Zápästie - Flexia" in line:
            # These are headers of the raw tables we replaced
            continue


        # Handle Full Page Scans (Appendices)
        if line.startswith('[[FULL_PAGE:') and line.endswith(']]'):
            if paragraph_text:
                latex_lines.append(' '.join(paragraph_text))
                latex_lines.append('\n\n')
                paragraph_text = []
            
            image_path = line.replace('[[FULL_PAGE:', '').replace(']]', '').strip()
            image_path = image_path.replace('\\', '/')
            
            latex_lines.append(f"\\begin{{figure}}[p]\n")
            latex_lines.append(f"    \\centering\n")
            # Maximize size for full page scan
            latex_lines.append(f"    \\includegraphics[width=1.0\\textwidth, height=0.95\\textheight, keepaspectratio]{{{image_path}}}\n")
            latex_lines.append(f"\\end{{figure}}\n")
            # Add clearpage to force float placement
            latex_lines.append(f"\\clearpage\n")
            continue

        # Detect section headers (e.g., "1.1 Funkčná anatómia")
        section_match = re.match(r'^(\d+\.\d+)\s+(.+)$', line)
        if section_match:
            # Flush paragraph if exists
            if paragraph_text:
                latex_lines.append(' '.join(paragraph_text))
                latex_lines.append('\n')
                paragraph_text = []
            
            section_num, section_title = section_match.groups()
            latex_lines.append(f"\\section{{{section_title}}}\n")
            continue
        
        # Detect subsection headers (e.g., "1.1.1 Stavba synoviálneho kĺbu")
        subsection_match = re.match(r'^(\d+\.\d+\.\d+)\s+(.+)$', line)
        if subsection_match:
            if paragraph_text:
                latex_lines.append(' '.join(paragraph_text))
                latex_lines.append('\n')
                paragraph_text = []
            
            _, subsection_title = subsection_match.groups()
            latex_lines.append(f"\\subsection{{{subsection_title}}}\n")
            continue
        
        # Add to current paragraph
        paragraph_text.append(line)
    
    # Flush remaining paragraph
    if paragraph_text:
        latex_lines.append(' '.join(paragraph_text))
        latex_lines.append('\n')
    
    return '\n'.join(latex_lines)

def get_text_after_page(full_text, page_num):
    """Return text starting from === PAGE {page_num} === to end"""
    marker = f"=== PAGE {page_num} ==="
    pos = full_text.find(marker)
    if pos != -1:
        return full_text[pos:]
    return full_text # Fallback

def main():
    input_file = "kapitoly/extracted_pdf_text.txt"
    
    # Read extracted text
    with open(input_file, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # Clean OCR artifacts
    full_text = clean_ocr_text(full_text)
    
    # Extract Chapter 1 (pages 15-20 roughly - Reumatoidná artritída)
    chapter1 = extract_chapter_content(
        full_text,
        1,
        r'^1\s+Reumatoidná artritída\s*$',
        r'^2\s+Interferenčné prúdy\s*$'
    )
    
    if chapter1:
        latex_ch1 = convert_to_latex(chapter1, "Reumatoidná artritída")
        with open("kapitoly/teoreticka_cast.tex", 'w', encoding='utf-8') as f:
            f.write(latex_ch1)
        print(f"[OK] Chapter 1 converted: {len(latex_ch1)} characters")
    
    # Extract Chapter 2
    chapter2 = extract_chapter_content(
        full_text,
        2,
        r'^2\s+Interferenčné prúdy\s*$',
        r'^3\s+Cieľ práce'
    )
    
    if chapter2:
        latex_ch2 = convert_to_latex(chapter2, "Interferenčné prúdy")
        with open("kapitoly/interferencne_prudy.tex", 'w', encoding='utf-8') as f:
            f.write(latex_ch2)
        print(f"[OK] Chapter 2 converted: {len(latex_ch2)} characters")

    # Extract Chapter 3 - Cieľ práce a metodológia (covers 3.1 to 3.7)
    chapter3 = extract_chapter_content(
        full_text,
        3,
        r'^3\s+Cieľ práce a metodológia\s*$',
        r'^4\s+Diskusia\s*$'
    )
    
    if chapter3:
        latex_ch3 = convert_to_latex(chapter3, "Cieľ práce a metodológia")
        with open("kapitoly/metodika.tex", 'w', encoding='utf-8') as f:
            f.write(latex_ch3)
        print(f"[OK] Chapter 3 converted: {len(latex_ch3)} characters")

    # Extract Chapter 4 - Diskusia
    chapter4 = extract_chapter_content(
        full_text,
        4,
        r'^4\s+Diskusia\s*$',
        r'(Odporú.ania\s+pre\s+prax|^\s*Záver\s*$)' # Robust matching for Odporúčania (wildcard char) and STRICT match for Záver
    )
    
    if chapter4:
        latex_ch4 = convert_to_latex(chapter4, "Diskusia")
        with open("kapitoly/diskusia.tex", 'w', encoding='utf-8') as f:
            f.write(latex_ch4)
        print(f"[OK] Chapter 4 converted: {len(latex_ch4)} characters")

    # Extract Recommendations
    # Search in text AFTER page 60 to avoid TOC matches or early mentions
    text_after_p60 = get_text_after_page(full_text, 60)
    
    recommendations = extract_chapter_content(
        text_after_p60,
        5,
        r'Odporú.ania\s+pre\s+prax', # Wildcard for c/č/C
        r'^\s*Záver\s*$'
    )
    
    if recommendations:
        # Custom cleaning for recommendations as it's not a numbered chapter
        latex_rec = convert_to_latex(recommendations, "Odporúčania pre prax")
        # Change \chapter to \chapter* or \section* for recommendations if needed, usually just \chapter*
        # Use simple string for replacement to interpret \n correctly as newline
        latex_rec = latex_rec.replace(r'\chapter{Odporúčania pre prax}', "\\chapter*{Odporúčania pre prax}\n\\addcontentsline{toc}{chapter}{Odporúčania pre prax}")
        with open("kapitoly/odporucania.tex", 'w', encoding='utf-8') as f:
            f.write(latex_rec)
        print(f"[OK] Recommendations converted: {len(latex_rec)} characters")

    # Extract Conclusion
    # Use text after p60
    conclusion = extract_chapter_content(
        text_after_p60,
        6,
        r'^\s*Záver\s*$',  # Strict matching for "Záver" header
        r'(Zoznam bibliografických odkazov|Bibliografia|Prílohy|Zoznam príloh)'
    )
    # If regex failed, try looser match BUT check context
    if not conclusion:
         # Try finding "ZÁVER" with loose spacing
         conclusion = extract_chapter_content(
            text_after_p60,
            6,
            r'ZÁVER',
            r'(Zoznam bibliografických odkazov|Bibliografia|Prílohy|Zoznam príloh)'
        )

    if conclusion:
        latex_con = convert_to_latex(conclusion, "Záver")
        latex_con = latex_con.replace(r'\chapter{Záver}', "\\chapter*{Záver}\n\\addcontentsline{toc}{chapter}{Záver}")
        with open("kapitoly/zaver.tex", 'w', encoding='utf-8') as f:
            f.write(latex_con)
        print(f"[OK] Conclusion converted: {len(latex_con)} characters")

    # Extract Bibliography Text (Text dump for verification)
    bibliography = extract_chapter_content(
        text_after_p60,
        7,
        r'(Zoznam bibliografických odkazov|Bibliografia)',
        r'(Zoznam príloh|Príloha 1)'
    )
    
    if bibliography:
        with open("kapitoly/bibliografia_RAW_TEXT.txt", 'w', encoding='utf-8') as f:
             f.write(bibliography)
        print(f"[OK] Bibliography text extracted: {len(bibliography)} characters")

    # Extract Appendices
    # Search in text AFTER page 65 (Bibliography is around 66-70)
    text_after_p70 = get_text_after_page(full_text, 70)
    if not text_after_p70: # Fallback if p70 not found
        text_after_p70 = text_after_p60

    appendices = extract_chapter_content(
        text_after_p70,
        8,
        r'(Zoznam príloh|Príloha 1)',
        None # End of file
    )

    if appendices:
        # Basic conversion
        latex_app = convert_to_latex(appendices, "Prílohy")
        # Fix chapter command for appendices
        latex_app = latex_app.replace(r'\chapter{Prílohy}', "\\chapter*{Prílohy}\n\\addcontentsline{toc}{chapter}{Prílohy}")
        with open("kapitoly/prilohy.tex", 'w', encoding='utf-8') as f:
            f.write(latex_app)
        print(f"[OK] Appendices converted: {len(latex_app)} characters")

    print("\n[OK] Conversion complete!")
    print("Next steps:")
    print("1. Update main.tex to include 'kapitoly/odporucania.tex'")
    print("2. Check 'kapitoly/metodika.tex' (it now implies Results too)")
    print("3. Verify Bibliography")

if __name__ == "__main__":
    main()
