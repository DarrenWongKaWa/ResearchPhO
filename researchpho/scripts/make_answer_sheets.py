"""Generate a ResearchPhO Answer Sheet booklet from a question paper (one framed box per subquestion/sub-part).

Usage:  python3 make_answer_sheets.py questions.tex answersheets.tex
Reads \\problem{n}{title}{points} and \\question{label}{points}{text}; sub-parts are detected from \\textbf{(a)}.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BASE_CM, PER_POINT_CM, MIN_CM, MAX_CM = 2.0, 2.4, 2.6, 16.0

PREAMBLE = r"""\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[scaled=0.96]{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{amsmath,amssymb}
\usepackage{newtxmath}
\usepackage[margin=20mm,top=35mm,bottom=20mm,headheight=57pt,headsep=10mm]{geometry}
\usepackage{needspace,xcolor,fancyhdr}
\usepackage[most]{tcolorbox}
\definecolor{ink}{HTML}{172A3A}
\definecolor{rulegray}{HTML}{5E6670}
\setlength{\parindent}{0pt}
\newcommand{\pagecode}{A}
\renewcommand{\thepage}{\pagecode-\arabic{page}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\begin{minipage}[b]{0.6\textwidth}\textbf{\large Theory --- Answer Sheet}\\[-1pt]{\small ResearchPhO \enspace|\enspace Answer Sheets}\\[-1pt]{\footnotesize English}\end{minipage}}
\fancyhead[R]{\fontsize{29}{31}\selectfont\bfseries \thepage}
\renewcommand{\headrulewidth}{0.9pt}
\fancyfoot[L]{\footnotesize Student code: \rule{35mm}{0.4pt}\qquad Write final answers only inside the boxes.}
\newcommand{\sheetproblem}[2]{\clearpage\renewcommand{\pagecode}{A#1}\setcounter{page}{1}{\Large\bfseries\color{ink}Problem #1: #2}\par\medskip}
\newcommand{\answerbox}[3]{\Needspace{6\baselineskip}\begin{tcolorbox}[enhanced,breakable=false,colback=white,colframe=rulegray,boxrule=0.5pt,arc=0pt,height=#3cm,valign=top,left=6pt,right=6pt,top=4pt,before skip=5pt,after skip=5pt]{\bfseries #1}\hfill{\small\bfseries #2}\end{tcolorbox}}
\begin{document}
"""


def braces(text: str, start: int) -> int:
    depth = 0
    for k in range(start, len(text)):
        if text[k] == "{" and text[k - 1] != "\\":
            depth += 1
        elif text[k] == "}" and text[k - 1] != "\\":
            depth -= 1
            if depth == 0:
                return k + 1
    raise ValueError("unbalanced braces")


def main() -> None:
    source, target = Path(sys.argv[1]), Path(sys.argv[2])
    tex = source.read_text().split("\\begin{document}", 1)[1]
    out = [PREAMBLE]
    for m in re.finditer(r"\\(problem|question)\{([^}]*)\}\{([^}]*)\}\{", tex):
        if m.group(1) == "problem":
            out.append(f"\\sheetproblem{{{m.group(2)}}}{{{m.group(3)}}}\n")
            continue
        label, points = m.group(2), float(m.group(3))
        body = tex[m.end():braces(tex, m.end() - 1) - 1]
        parts = re.findall(r"\\textbf\{\((\w)\)\}", body)
        if not parts:
            height = min(MAX_CM, max(MIN_CM, BASE_CM + PER_POINT_CM * points))
            out.append(f"\\answerbox{{{label}}}{{{points:.1f} pt}}{{{height:.1f}}}\n")
            continue
        each = min(MAX_CM, max(MIN_CM, (BASE_CM + PER_POINT_CM * points) / len(parts) + 0.8))
        for index, part in enumerate(parts):
            tag = f"{points:.1f} pt" if index == 0 else ""
            out.append(f"\\answerbox{{{label}({part})}}{{{tag}}}{{{each:.1f}}}\n")
    out.append("\\end{document}\n")
    target.write_text("".join(out))
    print(target)


if __name__ == "__main__":
    main()
