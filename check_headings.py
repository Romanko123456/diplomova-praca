
import zipfile
import re
import xml.dom.minidom

def get_docx_headings(path):
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml').decode('utf-8')
            document = xml.dom.minidom.parseString(xml_content)
            body = document.getElementsByTagName('w:body')[0]
            
            paragraphs = body.getElementsByTagName('w:p')
            headings = []
            
            for p in paragraphs:
                style_node = p.getElementsByTagName('w:pStyle')
                if style_node:
                    style_val = style_node[0].getAttribute('w:val')
                    # Hľadanie nadpisov (Heading 1, Heading 2...)
                    if 'Heading' in style_val or 'Nadpis' in style_val:
                        text = ""
                        for t in p.getElementsByTagName('w:t'):
                            text += t.firstChild.nodeValue
                        if text.strip():
                            headings.append((style_val, text.strip()))
                            
            return headings
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    path = r"c:\Users\Legion\Desktop\Ked mi padol.docx"
    headings = get_docx_headings(path)
    print("--- DOCX STRUCTURE ---")
    for h in headings:
        print(f"{h[0]}: {h[1]}")
