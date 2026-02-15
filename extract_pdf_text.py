#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract text from PDF pages 2-62 using pdfplumber
"""

import pdfplumber
import sys
import os

def extract_text_from_pdf(pdf_path, start_page=2, end_page=62):
    """Extract text from PDF pages"""
    all_text = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages in PDF: {total_pages}", file=sys.stderr)
        
        # Adjust page numbers (0-indexed)
        for page_num in range(start_page-1, min(end_page, total_pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if text:
                all_text.append(f"\n{'='*60}\n")
                all_text.append(f"PAGE {page_num + 1}\n")
                all_text.append(f"{'='*60}\n")
                all_text.append(text)
                all_text.append("\n")
        
    return "".join(all_text)

if __name__ == "__main__":
    pdf_file = "original_75pages.pdf"
    output_file = "kapitoly/extracted_pdf_text.txt"
    
    print(f"Extracting text from {pdf_file}...", file=sys.stderr)
    
    # Configuration
    start_page = 2
    end_page = 1000
    
    # Create images directory
    if not os.path.exists("obrazky"):
        os.makedirs("obrazky")

    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        
        # Process all pages (or subset if configured)
        # Using end_page=1000 ensures we go to the end if total_pages < 1000
        target_end_page = min(total_pages, end_page)
        
        for i in range(start_page - 1, target_end_page):
            page = pdf.pages[i]
            page_num = i + 1
            
            # Extract text
            text = page.extract_text(x_tolerance=2) or ""
            
            if text:
                extracted_text += f"=== PAGE {page_num} ===\n"
                extracted_text += text + "\n"
                
            # TEXT-HEAVY PAGE WITH CHARTS (Chapter 3/4)
            if len(text) > 200: 
                # Detect vector graphics
                vectors = page.rects + page.curves
                if len(vectors) > 2:
                    # Find bounding box of all vectors
                    # vectors are dicts with x0, top, x1, bottom
                    v_x0 = [v['x0'] for v in vectors]
                    v_top = [v['top'] for v in vectors]
                    v_x1 = [v['x1'] for v in vectors]
                    v_bottom = [v['bottom'] for v in vectors]
                    
                    if v_x0:
                        # Add margin
                        bbox = (
                            max(0, min(v_x0) - 10),
                            max(0, min(v_top) - 10),
                            min(page.width, max(v_x1) + 10),
                            min(page.height, max(v_bottom) + 10)
                        )
                        
                        # Only save if dimensions are reasonable (not tiny, not full page header)
                        if (bbox[2] - bbox[0]) > 100 and (bbox[3] - bbox[1]) > 100:
                            try:
                                image_path = f"obrazky/page_{page_num}_chart.png"
                                page.crop(bbox).to_image(resolution=300).save(image_path)
                                extracted_text += f"\n[[CHART: {image_path}]]\n"
                                print(f"Extracted chart (cropped): {image_path}", file=sys.stderr)
                            except Exception as e:
                                print(f"Failed to crop chart on page {page_num}: {e}", file=sys.stderr)

            # TEXT-LIGHT PAGE (Likely Scanned Appendix or Full Image)
            elif len(text) < 200:
                 try:
                     image_path = f"obrazky/page_{page_num}_scan.png"
                     # Crop top 50px and bottom 50px to remove potential page numbers/headers if they exist
                     # Assuming A4 size approx 595x842 pts
                     crop_box = (0, 50, page.width, page.height - 50)
                     page.crop(crop_box).to_image(resolution=300).save(image_path)
                     extracted_text += f"\n[[FULL_PAGE: {image_path}]]\n"
                     print(f"Extracted full page (scan): {image_path}", file=sys.stderr)
                 except Exception as e:
                     print(f"Failed to extract scan page {page_num}: {e}", file=sys.stderr)
            
            # Extract standard raster images (photos) independently
            if page.images and len(text) > 200:
                for j, img in enumerate(page.images):
                    if img['width'] < 100 or img['height'] < 100: continue # Skip small icons
                    try:
                        bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                        image_path = f"obrazky/page_{page_num}_img_{j+1}.png"
                        page.crop(bbox).to_image(resolution=300).save(image_path)
                        extracted_text += f"\n[[IMAGE: {image_path}]]\n"
                    except: pass

            extracted_text += "\n"
            
            if page_num % 10 == 0:
                print(f"Processed page {page_num}/{target_end_page}...", file=sys.stderr)

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    
    print(f"✓ Text extracted to {output_file}", file=sys.stderr)
    print(f"Total characters: {len(extracted_text)}", file=sys.stderr)
