@echo off
echo ====================================
echo AUTOMATICKA OPRAVA LATEX DOKUMENTU
echo ====================================
echo.

cd /d "c:\Users\Legion\Desktop\skola\DPText"

echo Mazem pokazene pomocne subory...
del /F /Q main.aux main.out main.log main.toc main.lof main.lot main.bcf main.bbl main.blg main.run.xml 2>nul

echo.
echo Kompilujem dokument (1. prechod)...
pdflatex -interaction=nonstopmode main.tex

echo.
echo Kompilujem dokument (2. prechod)...
pdflatex -interaction=nonstopmode main.tex

echo.
echo ====================================
echo HOTOVO!
echo ====================================
echo.
echo PDF subor: main.pdf
echo.
pause
