# PowerShell skript na konverziu PDF textu do LaTeX formátu
$inputFile = "kapitoly\teoreticka_cast_PDF_BACKUP.txt"
$outputFile = "kapitoly\teoreticka_cast_CONVERTED.tex"

# Načítaj text
$content = Get-Content $inputFile -Raw -Encoding UTF8

# Fix1: Odstráň čísla strán (samotné číslo na riadku)
$content = $content -replace '(?m)^\s*\d+\s*$\r?\n', ''

# Fix 2: Spoj rozdelené riadky (slová ukončené pomlčkou na konci riadka)
$content = $content -replace '(\w+)-\s*\r?\n\s*(\w+)', '$1$2'

# Fix 3: Spoj rozdelené vety (riadky nekončiace bodkou/dvojbodkou/čiarkou)
$content = $content -replace '(?<!\.)\s*\r?\n(?!\r?\n|^\d|\s*•)', ' '

# Fix 4: Nahraď hlavné sekcie LaTeX značkami
$content = $content -replace '(?m)^1 Reumatoidn', '% ============================================================================
% TEORETICKÁ ČASŤ
% Podľa metodických pokynov FZ TnUAD - cca 30% práce
% Písané v 1. osobe množného čísla, minulý čas (autorský plurál)
% ============================================================================

\chapter{Súčasný stav riešenej problematiky}

\section{Reumatoidn'

# Fix 5: Konvertuj sekcie 1.1, 1.2, ... na \subsection{}
$content = $content -replace '(?m)^1\.(\d+)\s+([^\r\n]+)', '\subsection{$2}'

# Fix 6: Konvertuj podsekcie 1.1.1, 1.1.2, ... na \subsubsection{}
$content = $content -replace '(?m)^1\.\d+\.(\d+)\s+([^\r\n]+)', '\subsubsection{$2}'

# Fix 7: Oprav apostrof a úvodzovky
$content = $content -replace "'", "'"
$content = $content -replace '"', '``'
$content = $content -replace '"', "''"

# Fix 8: Nahraď odrážky itemize environmentom
$content = $content -replace '(?m)^[ \t]*•\s*', '    \item '

# Ulož
$content | Out-File $outputFile -Encoding UTF8 -NoNewline

Write-Host "Konverzia dokončená: $outputFile"
