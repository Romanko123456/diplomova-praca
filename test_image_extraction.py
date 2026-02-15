import pdfplumber
import sys
import os

def test_image_extraction(pdf_path):
    print(f"Opening {pdf_path}...")
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            # Check for images
            if page.images:
                print(f"Page {i+1} has {len(page.images)} images.")
                # Try to extract the first image
                img_def = page.images[0]
                bbox = (img_def['x0'], img_def['top'], img_def['x1'], img_def['bottom'])
                print(f"Attempting to extract image at {bbox}...")
                
                try:
                    # Crop and extract
                    # We need a higher resolution for quality
                    # 300 dpi is standard
                    # pdfplumber to_image() returns a PageImage object wrapped around a PIL Image
                    p_img = page.crop(bbox).to_image(resolution=300)
                    output_path = f"obrazky/test_page_{i+1}.png"
                    p_img.save(output_path)
                    print(f"Success! Saved to {output_path}")
                    return # Stop after one success
                except Exception as e:
                    print(f"Failed to extract image: {e}")
            else:
                 # print(f"Page {i+1} has no images.")
                 pass

if __name__ == "__main__":
    if not os.path.exists("obrazky"):
        os.makedirs("obrazky")
    test_image_extraction("original_75pages.pdf")
