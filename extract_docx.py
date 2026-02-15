
import zipfile
import re
import sys
import os

def extract_docx_text(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml').decode('utf-8')
            
            # Simple XML tag removal
            text_content = re.sub('<[^>]+>', '', xml_content)
            
            # Print content to stdout
            print(text_content)
    except Exception as e:
        print(f"Error reading docx: {e}")

if __name__ == "__main__":
    docx_path = r"c:\Users\Legion\Desktop\Ked mi padol.docx"
    extract_docx_text(docx_path)
