"""Bloques MyST: pasos en pestañas, tablas y matrices."""

NEW = "#a94700"


def c(s):
    """Texto LaTeX resaltado como 'lo nuevo' del paso."""
    return rf"\textcolor{{{NEW}}}{{{s}}}"


def steps(title, contents, dropdown=True, label="Paso"):
    out = [f":::::{{admonition}} {title}"]
    if dropdown:
        out.append(":class: dropdown")
    out.append("::::{tab-set}")
    for i, body in enumerate(contents, 1):
        out.append(f":::{{tab-item}} {label} {i}")
        out.append(body.strip("\n"))
        out.append("")
        out.append(":::")
    out.append("::::")
    out.append(":::::")
    return "\n".join(out)


def img(path, alt):
    return f"![{alt}]({path})"


def md_table(header, rows):
    """rows: lista de listas de celdas ya formateadas."""
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def hl(s):
    """Celda resaltada dentro de una tabla markdown.

    KaTeX no reconoce algunos símbolos Unicode en modo texto (−, ↑, →); en esas
    celdas el resaltado es solo negrita.
    """
    if s == "":
        return ""
    if any(ch in str(s) for ch in "−↑→←∞"):
        return f"**{s}**"
    return f"$\\textcolor{{{NEW}}}{{\\textbf{{{s}}}}}$"


def latex_matrix(name, rows, cols, M, changed=(), fmt=str, sub=None):
    """Matriz con encabezados de fila/columna; celdas cambiadas en color."""
    head = " & " + " & ".join(rf"\mathbf{{{x}}}" for x in cols)
    body = []
    for i, r_ in enumerate(rows):
        cells = []
        for j, _ in enumerate(cols):
            v = fmt(M[i][j])
            cells.append(c(rf"\mathbf{{{v}}}") if (i, j) in changed else v)
        body.append(rf"\mathbf{{{r_}}} & " + " & ".join(cells))
    s = sub if sub is not None else ""
    return (rf"{name}{s} = \begin{{array}}{{c|{'c' * len(cols)}}}" + head + r" \\ \hline "
            + r" \\ ".join(body) + r"\end{array}")
