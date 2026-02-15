
# Dictionary mapping Page Numbers to a list of Graph LaTeX strings
# The script will pop them one by one as it encounters [[CHART]] markers on that page.

PAGE_CHARTS = {
    48: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 3: Porovnanie intenzity bolesti (VAS) pred a po terapii},
            ylabel={Intenzita bolesti (VAS 0-10)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=10,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 7.24) (Po terapii, 4.92)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 7.00) (Po terapii, 5.40)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:3}
\end{figure}
"""
    ],
    49: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 4: Charakter bolesti u jednotlivých skupín},
            ylabel={Zastúpenie (\%)},
            symbolic x coords={ITF+Kinezio, Kinezioterapia},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.20)}, anchor=north, legend columns=2},
            ymin=0, ymax=35,
            bar width=10pt,
            width=0.9\textwidth,
            height=7cm
        ]
        % Data approx from text/chart
        \addplot[fill=blue!50] coordinates {(ITF+Kinezio, 26) (Kinezioterapia, 28)}; \addlegendentry{Tupá}
        \addplot[fill=red!50] coordinates {(ITF+Kinezio, 6) (Kinezioterapia, 6)}; \addlegendentry{Pálivá}
        \addplot[fill=gray!50] coordinates {(ITF+Kinezio, 22) (Kinezioterapia, 20)}; \addlegendentry{Bodavá}
        \addplot[fill=purple!50] coordinates {(ITF+Kinezio, 26) (Kinezioterapia, 24)}; \addlegendentry{Pulzujúca}
        \addplot[fill=orange!50] coordinates {(ITF+Kinezio, 20) (Kinezioterapia, 22)}; \addlegendentry{Tlaková}
        \end{axis}
    \end{tikzpicture}
    \label{graf:4}
\end{figure}
""",
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 5: Časový výskyt bolesti počas dňa},
            ylabel={Počet pacientov},
            symbolic x coords={Ráno, Popoludní},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=50,
            bar width=30pt,
            width=0.8\textwidth,
            height=7cm
        ]
        \addplot[fill=blue!60] coordinates {(Ráno, 36) (Popoludní, 14)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Ráno, 34) (Popoludní, 16)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:5}
\end{figure}
"""
    ],
    50: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 6: Porovnanie intenzity rannej stuhnutosti (VAS)},
            ylabel={Intenzita stuhnutosti (VAS 0-10)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=10,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 6.02) (Po terapii, 3.02)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 5.32) (Po terapii, 4.42)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:6}
\end{figure}
"""
    ],
    51: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 7: Výskyt rannej stuhnutosti u oboch skupín},
            ylabel={Zastúpenie (\%)},
            symbolic x coords={Áno, Nie},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=100,
            bar width=30pt,
            width=0.8\textwidth,
            height=7cm
        ]
        % Based on text: Exp (72% Yes, 28% No), Control (76% Yes, 24% No)
        \addplot[fill=blue!60] coordinates {(Áno, 72) (Nie, 28)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Áno, 76) (Nie, 24)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:7}
\end{figure}
"""
    ],
    52: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 8: Goniometria zápästia – Flexia},
            ylabel={Rozsah pohybu (stupne)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=80,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 60.14) (Po terapii, 65.50)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 59.54) (Po terapii, 61.49)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:8}
\end{figure}
""",
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 9: Goniometria zápästia – Extenzia},
            ylabel={Rozsah pohybu (stupne)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=70,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 50.68) (Po terapii, 55.79)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 52.18) (Po terapii, 54.11)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:9}
\end{figure}
"""
    ],
    53: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 10: Goniometria MCP – Flexia},
            ylabel={Rozsah pohybu (stupne)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=90,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 67.30) (Po terapii, 72.60)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 67.90) (Po terapii, 69.78)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:10}
\end{figure}
"""
    ],
    54: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 11: Goniometria MCP – Extenzia},
            ylabel={Rozsah pohybu (stupne)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=50,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 34.92) (Po terapii, 39.21)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 34.23) (Po terapii, 35.46)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:11}
\end{figure}
""",
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 12: Goniometria PIP – Flexia},
            ylabel={Rozsah pohybu (stupne)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=90,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 75.31) (Po terapii, 78.42)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 76.51) (Po terapii, 79.28)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:12}
\end{figure}
"""
    ],
    56: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 13: Goniometria MTP – Flexia},
            ylabel={Rozsah pohybu (stupne)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=60,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 31.42) (Po terapii, 39.82)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 31.09) (Po terapii, 32.19)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:13}
\end{figure}
""",
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 14: Goniometria MTP – Extenzia},
            ylabel={Rozsah pohybu (stupne)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=80,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 55.70) (Po terapii, 66.14)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 58.41) (Po terapii, 60.41)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:14}
\end{figure}
"""
    ],
    57: [
        r"""
\begin{figure}[ht]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            ybar,
            title={Graf 15: Celkové skóre dotazníka vlastnej konštrukcie},
            ylabel={Skóre (body)},
            symbolic x coords={Pred terapiou, Po terapii},
            xtick=data,
            nodes near coords,
            legend style={at={(0.5,-0.15)}, anchor=north, legend columns=-1},
            ymin=0, ymax=80,
            bar width=30pt,
            width=0.95\textwidth,
            height=11cm
        ]
        \addplot[fill=blue!60] coordinates {(Pred terapiou, 59.20) (Po terapii, 49.22)}; \addlegendentry{ITF + Kinezioterapia}
        \addplot[fill=green!60] coordinates {(Pred terapiou, 50.30) (Po terapii, 46.06)}; \addlegendentry{Kinezioterapia}
        \end{axis}
    \end{tikzpicture}
    \label{graf:15}
\end{figure}
"""
    ]
}

TABLES = {
    # Page 51
    "Tabul’ka 4": r"""
\begin{table}[ht]
\centering
\caption{Porovnanie rannej stuhnutosti a ADL (body 0-10)}
\begin{tabular}{|l|c|c|c|c|c|c|}
\hline
\textbf{Parameter / Skupina} & \textbf{$\bar{x}$ Pred} & \textbf{sd Pred} & \textbf{min-max} & \textbf{$\bar{x}$ Po} & \textbf{sd Po} & \textbf{min-max} \\ \hline
\multicolumn{7}{|l|}{\textbf{Ranná stuhnutosť}} \\ \hline
Exp. (ITF + K) & 6,02 & 2,24 & 2-10 & 3,02 & 1,95 & 1-7 \\ \hline
Kontr. (K) & 5,32 & 2,15 & 2-10 & 4,42 & 2,00 & 2-9 \\ \hline
\multicolumn{7}{|l|}{\textbf{ADL}} \\ \hline
Exp. (ITF + K) & 5,34 & 1,85 & 2-9 & 3,48 & 1,62 & 1-6 \\ \hline
Kontr. (K) & 5,12 & 1,28 & 3-8 & 4,54 & 1,66 & 2-8 \\ \hline
\end{tabular}
\label{tab:4}
\end{table}
""",
    # Page 53
    "Tabul’ka 5": r"""
\begin{table}[ht]
\centering
\caption{Goniometria zápästného kĺbu – flexia a extenzia (stupne)}
\begin{tabular}{|l|c|c|c|c|c|c|}
\hline
\textbf{Parameter / Strana} & \textbf{$\bar{x}$ Pred} & \textbf{sd Pred} & \textbf{min-max} & \textbf{$\bar{x}$ Po} & \textbf{sd Po} & \textbf{min-max} \\ \hline
\multicolumn{7}{|l|}{\textbf{Zápästie - Flexia (Experimentálna skupina ITF)}} \\ \hline
Dx (vpravo) & 60,08 & 7,29 & 47-73 & 65,34 & 7,45 & 53-78 \\ \hline
Sin (vľavo) & 60,20 & 6,58 & 46-72 & 65,66 & 6,46 & 52-77 \\ \hline
\multicolumn{7}{|l|}{\textbf{Zápästie - Flexia (Kontrolná skupina K)}} \\ \hline
Dx (vpravo) & 59,26 & 7,16 & 47-72 & 61,25 & 7,39 & 48-74 \\ \hline
Sin (vľavo) & 59,82 & 6,94 & 50-73 & 61,73 & 6,89 & 50-73 \\ \hline
\multicolumn{7}{|l|}{\textbf{Zápästie - Extenzia (Experimentálna skupina ITF)}} \\ \hline
Dx (vpravo) & 50,64 & 7,73 & 39-67 & 55,76 & 7,70 & 43-70 \\ \hline
Sin (vľavo) & 50,72 & 7,18 & 38-67 & 55,82 & 7,23 & 42-69 \\ \hline
\multicolumn{7}{|l|}{\textbf{Zápästie - Extenzia (Kontrolná skupina K)}} \\ \hline
Dx (vpravo) & 51,96 & 7,48 & 39-68 & 53,87 & 7,83 & 39-67 \\ \hline
Sin (vľavo) & 52,40 & 6,77 & 38-68 & 54,35 & 6,48 & 40-67 \\ \hline
\end{tabular}
\label{tab:5}
\end{table}
""",
    # Page 55
    "Tabul’ka 6": r"""
\begin{table}[ht]
\centering
\caption{Goniometria kĺbov ruky – MCP a PIP (stupne)}
\resizebox{\textwidth}{!}{%
\begin{tabular}{|l|c|c|c|c|c|c|}
\hline
\textbf{Parameter / Strana} & \textbf{$\bar{x}$ Pred} & \textbf{sd Pred} & \textbf{min-max} & \textbf{$\bar{x}$ Po} & \textbf{sd Po} & \textbf{min-max} \\ \hline
\multicolumn{7}{|l|}{\textbf{MCP - Flexia (Experimentálna skupina ITF)}} \\ \hline
Dx (vpravo) & 67,82 & 7,24 & 55-82 & 73,06 & 7,32 & 61-90 \\ \hline
Sin (vľavo) & 66,78 & 6,84 & 52-80 & 72,14 & 7,28 & 58-88 \\ \hline
\multicolumn{7}{|l|}{\textbf{MCP - Flexia (Kontrolná skupina K)}} \\ \hline
Dx (vpravo) & 68,62 & 8,31 & 56-84 & 70,42 & 7,81 & 58-83 \\ \hline
Sin (vľavo) & 67,18 & 8,83 & 53-86 & 69,13 & 8,58 & 55-86 \\ \hline
\multicolumn{7}{|l|}{\textbf{MCP - Extenzia (Experimentálna skupina ITF)}} \\ \hline
Dx (vpravo) & 35,08 & 6,28 & 22-54 & 39,26 & 6,15 & 25-58 \\ \hline
Sin (vľavo) & 34,76 & 6,82 & 20-52 & 39,16 & 6,47 & 23-56 \\ \hline
\multicolumn{7}{|l|}{\textbf{MCP - Extenzia (Kontrolná skupina K)}} \\ \hline
Dx (vpravo) & 34,32 & 6,83 & 23-55 & 35,52 & 6,78 & 25-54 \\ \hline
Sin (vľavo) & 34,14 & 6,82 & 23-54 & 35,40 & 7,08 & 22-54 \\ \hline
\multicolumn{7}{|l|}{\textbf{PIP - Flexia (Experimentálna skupina ITF)}} \\ \hline
Dx (vpravo) & 74,50 & 8,12 & 62-95 & 77,98 & 8,45 & 65-102 \\ \hline
Sin (vľavo) & 76,12 & 8,28 & 64-98 & 78,86 & 8,25 & 68-105 \\ \hline
\multicolumn{7}{|l|}{\textbf{PIP - Flexia (Kontrolná skupina K)}} \\ \hline
Dx (vpravo) & 76,90 & 8,72 & 64-92 & 79,66 & 8,56 & 67-95 \\ \hline
Sin (vľavo) & 76,12 & 8,66 & 64-92 & 78,89 & 8,29 & 68-95 \\ \hline
\end{tabular}%
}
\label{tab:6}
\end{table}
""",
    # Page 57
    "Tabul’ka 7": r"""
\begin{table}[ht]
\centering
\caption{Goniometria kĺbov nohy – MTP (stupne)}
\resizebox{\textwidth}{!}{%
\begin{tabular}{|l|c|c|c|c|c|c|}
\hline
\textbf{Parameter / Strana} & \textbf{$\bar{x}$ Pred} & \textbf{sd Pred} & \textbf{min-max} & \textbf{$\bar{x}$ Po} & \textbf{sd Po} & \textbf{min-max} \\ \hline
\multicolumn{7}{|l|}{\textbf{MTP - Flexia (Experimentálna skupina ITF)}} \\ \hline
Dx (vpravo) & 31,48 & 4,32 & 22-38 & 39,85 & 4,20 & 30-48 \\ \hline
Sin (vľavo) & 31,36 & 4,18 & 22-40 & 39,79 & 4,10 & 31-48 \\ \hline
\multicolumn{7}{|l|}{\textbf{MTP - Flexia (Kontrolná skupina K)}} \\ \hline
Dx (vpravo) & 31,40 & 6,84 & 22-42 & 32,46 & 6,10 & 25-42 \\ \hline
Sin (vľavo) & 30,78 & 6,00 & 22-42 & 31,92 & 6,01 & 22-43 \\ \hline
\multicolumn{7}{|l|}{\textbf{MTP - Extenzia (Experimentálna skupina ITF)}} \\ \hline
Dx (vpravo) & 55,75 & 6,38 & 45-66 & 66,18 & 6,15 & 55-78 \\ \hline
Sin (vľavo) & 55,65 & 6,22 & 44-68 & 66,10 & 6,05 & 54-78 \\ \hline
\multicolumn{7}{|l|}{\textbf{MTP - Extenzia (Kontrolná skupina K)}} \\ \hline
Dx (vpravo) & 58,26 & 6,36 & 45-65 & 60,18 & 6,28 & 45-68 \\ \hline
Sin (vľavo) & 58,56 & 5,37 & 48-65 & 60,64 & 5,45 & 50-68 \\ \hline
\end{tabular}%
}
\label{tab:7}
\end{table}
"""
}
