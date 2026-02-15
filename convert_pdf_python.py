import sys
import re

# Načítaj text z PDF backup súboru
with open('kapitoly/teoreticka_cast_PDF_BACKUP.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# LaTeX hlavička
latex_content = """% ============================================================================
% TEORETICKÁ ČASŤ
% Podľa metodických pokynov FZ TnUAD - cca 30% práce
% Písané v 1. osobe množného čísla, minulý čas (autorský plurál)
% ============================================================================

\\chapter{Súčasný stav riešenej problematiky}

"""

# Rozdeľ text na riadky
lines = content.split('\n')

current_text = []
in_section = False

for line in lines:
    line = line.strip()
    
    # Preskač prázdne riadky a čísla strán
    if not line or line.isdigit():
        continue
    
    # Deteguj hlavný nadpis kapitoly
    if re.match(r'^1\s+Reumatoidná artritída', line):
        current_text.append('\n\\section{Reumatoidná artritída}\n')
        in_section = True
        continue
    
    # Deteguj podsekcie 1.1, 1.2, ...
    match = re.match(r'^1\.(\d+)\s+(.+)$', line)
    if match:
        section_num, section_title = match.groups()
        current_text.append(f'\n\\subsection{{{section_title}}}\n')
        continue
    
    # Deteguj pod-podsekcie 1.1.1, 1.2.1, ...
    match = re.match(r'^1\.\d+\.(\d+)\s+(.+)$', line)
    if match:
        subsection_num, subsection_title = match.groups()
        current_text.append(f'\n\\subsubsection{{{subsection_title}}}\n')
        continue
    
    # Pridaj bežný text
    if in_section:
        current_text.append(line + ' ')

# Spoj text
latex_content += ''.join(current_text)

# Ulož
with open('kapitoly/teoreticka_cast_PYTHON.tex', 'w', encoding='utf-8') as f:
    f.write(latex_content)

print("Conversion completed!")
print(f"Output: kapitoly/teoreticka_cast_PYTHON.tex")
