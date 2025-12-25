# Diplomová práca - Roman Ballek

## Využitie fyzioterapie u pacientov s reumatickým ochorením

Trenčianska univerzita Alexandra Dubčeka v Trenčíne  
Fakulta zdravotníctva  
Rok: 2026

---

### Štruktúra projektu

```
diplomova-praca/
├── main.tex                 # Hlavný súbor
├── bibliografia.bib         # Bibliografické záznamy
├── kapitoly/
│   ├── titulna_strana.tex   # Titulná strana
│   ├── cestne_vyhlasenie.tex
│   ├── podakovanie.tex
│   ├── abstrakt.tex
│   ├── zoznam_skratiek.tex
│   ├── uvod.tex
│   ├── teoreticka_cast.tex
│   ├── ciele_hypotezy.tex
│   ├── metodika.tex
│   ├── vysledky.tex
│   ├── diskusia.tex
│   ├── zaver.tex
│   └── prilohy.tex
├── obrazky/                 # Priečinok pre obrázky
└── tabulky/                 # Priečinok pre tabuľky
```

### Kompilácia

Pre správne zostavenie práce použite:

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Alebo použite editor ako **TeXstudio**, **Overleaf** alebo **VS Code s LaTeX Workshop**.

### Požiadavky

- TeX distribúcia (MiKTeX, TeX Live)
- Balíčky: babel (slovak), biblatex, biber

### Autor

Roman Ballek  
roman.ballek@student.tnuni.sk