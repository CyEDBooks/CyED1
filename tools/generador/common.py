import os
import re

from figlib import (SVG, draw_graph, draw_panel, PAL, nary_layout, compact_nary_layout,
                    bin_layout, tile)
from mdlib import steps, md_table, hl, c, latex_matrix

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
TPL = os.path.join(HERE, "..", "plantillas")

INF = float("inf")


def fmt(x):
    return "∞" if x == INF else str(x)


def lfmt(x):
    return r"\infty" if x == INF else str(x)


class Page:
    def __init__(self, rel):
        self.rel = rel                      # p. ej. Unidad5-Grafos/BFS
        self.dir = os.path.join(REPO, rel)
        self.frags = {}

    def img(self, name, svg, **kw):
        path = os.path.join(self.dir, "images", name + ".svg")
        svg.save(path, **kw)
        return f"images/{name}.svg"

    def put(self, key, text):
        self.frags[key] = text.strip("\n")

    def assemble(self, tpl_name="index.md"):
        src = os.path.join(TPL, self.rel, tpl_name)
        with open(src, encoding="utf-8") as f:
            text = f.read()

        def rep(m):
            key = m.group(1)
            if key not in self.frags:
                raise KeyError(f"{self.rel}/{tpl_name}: falta el fragmento {key}")
            return self.frags[key]

        text = re.sub(r"\{\{GEN:([\w\-]+)\}\}", rep, text)
        out = os.path.join(self.dir, tpl_name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        return out

    def assemble_all(self):
        d = os.path.join(TPL, self.rel)
        for name in sorted(os.listdir(d)):
            if name.endswith(".md"):
                self.assemble(name)


def scale(pos, sx=1.0, sy=None):
    sy = sx if sy is None else sy
    return {k: (x * sx, y * sy) for k, (x, y) in pos.items()}


def tree_pos(t, dx=50, dy=64, compact=False):
    """Árbol n-ario con etiquetas únicas -> pos y aristas por etiqueta."""
    pos, edges, keys, _ = (compact_nary_layout if compact else nary_layout)(t, dx, dy)
    p = {keys[k]: v for k, v in pos.items()}
    e = [(keys[a], keys[b]) for a, b in edges]
    return p, e


def circle_pos(names, R=70, start=-90, cx=0, cy=0):
    import math
    n = len(names)
    return {v: (cx + R * math.cos(math.radians(start + 360 * i / n)),
                cy + R * math.sin(math.radians(start + 360 * i / n))) for i, v in enumerate(names)}


def gfig(page, name, pos, edges, directed=False, **kw):
    svg = SVG()
    draw_graph(svg, pos, edges, directed, **kw)
    return f"![{name}]({page.img(name, svg)})"


def gfig_caption(page, name, pos, edges, cap, directed=False, **kw):
    svg = SVG()
    draw_graph(svg, pos, edges, directed, **kw)
    ys = max(y for _, y in pos.values()) + kw.get("r", 18) + 24
    xs = [x for x, _ in pos.values()]
    svg.text((min(xs) + max(xs)) / 2, ys, cap, 14, PAL["ink"], bold=True)
    return f"![{cap}]({page.img(name, svg)})"



def graph_row(page, name, items, gap=80, alt=None, directed=False):
    """Varios grafos lado a lado (en varias filas si no caben).
    items: lista de (pos, aristas, rótulo, opciones de draw_graph)."""
    parts = []
    for it in items:
        pos, E = it[0], it[1]
        kw = it[3] if len(it) > 3 else {}
        d = kw.pop("directed", directed)
        svg = SVG()
        draw_graph(svg, pos, E, d, **kw)
        parts.append(svg)
    caps = [it[2] for it in items]
    return f"![{alt or name}]({page.img(name, tile(parts, gap, caps=caps))})"
