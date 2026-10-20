"""Dibujo en SVG de los grafos y árboles de CyED1.

Las figuras llevan fondo blanco para verse igual en el libro y en un visor de
imágenes.
"""
import html
import math
import os

PAL = {
    "ink": "#023047",
    "muted": "#49636f",
    "new": "#a94700",      # color de lo nuevo en cada paso, el mismo de CyED2
    "teal": "#219ebc",
    "sky": "#8ecae6",
    "border": "#b9d8e5",
    "soft": "#f2f9fc",
    "yellow": "#ffb703",
    "orange": "#fb8500",
    "gray": "#b8c4ca",
    "dim": "#c9d3d8",
    "white": "#ffffff",
    "goal": "#2a9d4b",
    "bad": "#c0392b",
}

FONT = "Plus Jakarta Sans, Arial, sans-serif"

# Estilos de vértice: (relleno, borde, color del texto, grosor del borde)
NODE_STYLES = {
    "plain": (PAL["white"], PAL["ink"], PAL["ink"], 1.6),
    "white": (PAL["white"], PAL["ink"], PAL["ink"], 1.6),
    "gray": (PAL["gray"], PAL["ink"], PAL["ink"], 1.6),
    "black": (PAL["ink"], PAL["ink"], PAL["white"], 1.6),
    "new": (PAL["white"], PAL["new"], PAL["new"], 3.0),
    "newgray": (PAL["gray"], PAL["new"], PAL["ink"], 3.0),
    "newblack": (PAL["ink"], PAL["new"], PAL["white"], 3.0),
    "hl": ("#ffe8c2", PAL["new"], PAL["ink"], 3.0),
    "tree": ("#e5f5f9", PAL["teal"], PAL["ink"], 2.4),
    "dim": (PAL["white"], PAL["dim"], "#9aabb3", 1.4),
    "goal": ("#dff3e4", PAL["goal"], PAL["ink"], 2.6),
    "bad": ("#fbe3e0", PAL["bad"], PAL["ink"], 2.6),
    "ghost": (PAL["white"], PAL["dim"], "#9aabb3", 1.2),
}

# Estilos de arista: (color, grosor, guiones)
EDGE_STYLES = {
    "plain": (PAL["muted"], 1.5, None),
    "tree": (PAL["teal"], 3.2, None),
    "new": (PAL["new"], 3.6, None),
    "dim": (PAL["dim"], 1.3, None),
    "cand": (PAL["orange"], 1.8, "6,4"),
    "reject": (PAL["bad"], 2.2, "3,4"),
    "back": (PAL["muted"], 1.8, "6,4"),
    "ghost": (PAL["dim"], 1.2, "4,4"),
}


def esc(s):
    return html.escape(str(s), quote=True)


class SVG:
    def __init__(self):
        self.items = []
        self.minx = self.miny = float("inf")
        self.maxx = self.maxy = float("-inf")

    def _box(self, x0, y0, x1, y1):
        self.minx = min(self.minx, x0)
        self.miny = min(self.miny, y0)
        self.maxx = max(self.maxx, x1)
        self.maxy = max(self.maxy, y1)

    def line(self, x1, y1, x2, y2, color, width=1.5, dash=None, marker=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        self.items.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}"{d}{m}/>')
        self._box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    def path(self, d, color, width=1.5, dash=None, marker=None, fill="none"):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        self.items.append(
            f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}"{ds}{m}/>')

    def circle(self, x, y, r, fill, stroke, width):
        self.items.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"/>')
        self._box(x - r - 2, y - r - 2, x + r + 2, y + r + 2)

    def rect(self, x, y, w, h, fill, stroke, width=1.2, rx=4):
        self.items.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
        self._box(x - 1, y - 1, x + w + 1, y + h + 1)

    def text(self, x, y, s, size=15, color=PAL["ink"], anchor="middle", bold=False,
             italic=False, bg=False):
        s = str(s)
        w = text_width(s, size)
        if bg:
            x0 = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
            self.items.append(
                f'<rect x="{x0 - 3:.1f}" y="{y - size * 0.82:.1f}" width="{w + 6:.1f}" '
                f'height="{size * 1.1:.1f}" fill="#ffffff" fill-opacity="0.92"/>')
        fw = ' font-weight="bold"' if bold else ""
        fs = ' font-style="italic"' if italic else ""
        self.items.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}"{fw}{fs}>{esc(s)}</text>')
        x0 = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
        self._box(x0, y - size, x0 + w, y + size * 0.3)

    def render(self, margin=14, min_width=0):
        minx, miny = self.minx - margin, self.miny - margin
        w = self.maxx - self.minx + 2 * margin
        h = self.maxy - self.miny + 2 * margin
        if w < min_width:
            minx -= (min_width - w) / 2
            w = min_width
        defs = "".join(
            f'<marker id="arr-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="11" '
            f'markerHeight="11" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
            f'fill="{c}"/></marker>'
            for k, c in (("plain", PAL["muted"]), ("tree", PAL["teal"]), ("new", PAL["new"]),
                         ("dim", PAL["dim"]), ("cand", PAL["orange"]), ("reject", PAL["bad"]),
                         ("back", PAL["muted"]), ("ghost", PAL["dim"])))
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
                f'viewBox="{minx:.1f} {miny:.1f} {w:.1f} {h:.1f}" font-family="{FONT}">\n'
                f'<defs>{defs}</defs>\n'
                f'<rect x="{minx:.1f}" y="{miny:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#ffffff"/>\n')
        return head + "\n".join(self.items) + "\n</svg>\n"

    def save(self, path, **kw):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render(**kw))


def text_width(s, size):
    # Aproximación suficiente para Plus Jakarta Sans / Arial.
    w = 0
    for ch in str(s):
        if ch in "il.,:;|!'·":
            w += 0.3
        elif ch in "mwMW":
            w += 0.85
        elif ch.isupper() or ch in "∞→⟨⟩":
            w += 0.68
        elif ch == " ":
            w += 0.3
        else:
            w += 0.56
    return w * size


R = 18  # radio de vértice


def _shorten(x1, y1, x2, y2, r1, r2):
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    return (x1 + dx * r1 / d, y1 + dy * r1 / d, x2 - dx * r2 / d, y2 - dy * r2 / d)


def draw_graph(svg, pos, edges, directed=False, node_style=None, edge_style=None,
               node_text=None, labels=None, label_style=None, label_pos=None,
               weights=None, weight_style=None, r=R, curved=None, font=15,
               label_font=13):
    """Dibuja un grafo.

    pos: {v: (x, y)}; edges: lista de (u, v) o (u, v, w).
    node_style / edge_style: estilos por vértice / por arista (clave (u, v)).
    labels: anotación junto al vértice (p. ej. "d=1" o "[2,a]").
    """
    node_style = node_style or {}
    edge_style = edge_style or {}
    node_text = node_text or {}
    labels = labels or {}
    label_style = label_style or {}
    label_pos = label_pos or {}
    weight_style = weight_style or {}
    eset = {(e[0], e[1]) for e in edges}
    curved = curved or {}

    def est(u, v):
        s = edge_style.get((u, v))
        if s is None and not directed:
            s = edge_style.get((v, u))
        return s or "plain"

    # Aristas primero (debajo de los vértices).
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) > 2 else None
        ebend = e[3] if len(e) > 3 else None   # aristas paralelas: curvatura propia
        st = est(u, v)
        color, width, dash = EDGE_STYLES[st]
        marker = f"arr-{st}" if directed else None
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        if u == v:  # bucle, orientado hacia afuera del dibujo
            cx0 = sum(x for x, _ in pos.values()) / len(pos)
            cy0 = sum(y for _, y in pos.values()) / len(pos)
            ang = math.atan2(y1 - cy0, x1 - cx0) if (x1, y1) != (cx0, cy0) else -math.pi / 2
            ang = round(ang / (math.pi / 2)) * (math.pi / 2)
            ux, uy = math.cos(ang), math.sin(ang)
            px, py = -uy, ux

            def P(a, b):
                return x1 + ux * a + px * b, y1 + uy * a + py * b
            s0, c1, c2, s1 = P(r - 2, -8), P(r + 38, -30), P(r + 38, 30), P(r - 2, 8)
            svg.path(f"M{s0[0]:.1f},{s0[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} "
                     f"{c2[0]:.1f},{c2[1]:.1f} {s1[0]:.1f},{s1[1]:.1f}",
                     color, width, dash, marker)
            tip = P(r + 30, 0)
            svg._box(min(c1[0], c2[0], x1) - 4, min(c1[1], c2[1], y1) - 4,
                     max(c1[0], c2[0], x1) + 4, max(c1[1], c2[1], y1) + 4)
            if w is not None:
                svg.text(tip[0] + ux * 10, tip[1] + uy * 10 + 5, w, 13, PAL["ink"], bg=True)
            continue
        bend = ebend if ebend is not None else curved.get((u, v))
        if bend is None and directed and (v, u) in eset:
            bend = 18
        if bend:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            d = math.hypot(dx, dy)
            nx, ny = -dy / d, dx / d
            cx, cy = mx + nx * bend * 2, my + ny * bend * 2
            # recortar en los círculos
            sx1, sy1, _, _ = _shorten(x1, y1, cx, cy, r, 0)
            _, _, sx2, sy2 = _shorten(cx, cy, x2, y2, 0, r + (2 if directed else 0))
            svg.path(f"M{sx1:.1f},{sy1:.1f} Q{cx:.1f},{cy:.1f} {sx2:.1f},{sy2:.1f}",
                     color, width, dash, marker)
            lx, ly = mx + nx * bend, my + ny * bend
            svg._box(min(x1, x2, cx), min(y1, y2, cy), max(x1, x2, cx), max(y1, y2, cy))
        else:
            sx1, sy1, sx2, sy2 = _shorten(x1, y1, x2, y2, r, r + (2 if directed else 0))
            svg.line(sx1, sy1, sx2, sy2, color, width, dash, marker)
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
        if w is not None:
            wst = weight_style.get((u, v)) or (None if directed else weight_style.get((v, u)))
            wc = {None: PAL["teal"], "new": PAL["new"], "dim": "#9aabb3",
                  "tree": PAL["teal"]}.get(wst, PAL["teal"])
            svg.text(lx, ly + 5, w, 14, wc, bold=(wst == "new"), bg=True)

    for v, (x, y) in pos.items():
        st = node_style.get(v, "plain")
        fill, stroke, tc, width = NODE_STYLES[st]
        svg.circle(x, y, r, fill, stroke, width)
        t = node_text.get(v, v)
        size = font if len(str(t)) <= 2 else max(10, font - 2 * (len(str(t)) - 2))
        svg.text(x, y + size * 0.35, t, size, tc, bold=st.startswith("new") or st == "hl")
        if v in labels and labels[v] != "":
            where = label_pos.get(v, "above")
            ls = label_style.get(v)
            lc = PAL["new"] if ls == "new" else ("#9aabb3" if ls == "dim" else PAL["ink"])
            off = r + 7
            if where == "above":
                svg.text(x, y - off, labels[v], label_font, lc, bold=(ls == "new"))
            elif where == "below":
                svg.text(x, y + off + label_font * 0.75, labels[v], label_font, lc,
                         bold=(ls == "new"))
            elif where == "left":
                svg.text(x - off, y + 4, labels[v], label_font, lc, anchor="end",
                         bold=(ls == "new"))
            else:
                svg.text(x + off, y + 4, labels[v], label_font, lc, anchor="start",
                         bold=(ls == "new"))


def draw_panel(svg, x, y, title, items, new=(), dim=(), cell=34, mark=None, wrap=None):
    """Fila de casillas (cola, pila, lista de visitados...). Devuelve la y inferior."""
    svg.text(x, y + 22, title, 13, PAL["muted"], anchor="start", bold=True)
    tx0 = x + text_width(title, 13) + 10
    tx = tx0
    if not items:
        svg.rect(tx, y, cell, 32, PAL["soft"], PAL["border"])
        svg.text(tx + cell / 2, y + 21, "∅", 14, PAL["muted"])
        return y + 32
    for i, it in enumerate(items):
        if wrap and i and i % wrap == 0:
            tx = tx0
            y += 38
        w = max(cell, text_width(it, 14) + 14)
        isnew = i in new
        isdim = i in dim
        fill = "#ffe8c2" if isnew else (PAL["white"] if isdim else PAL["soft"])
        stroke = PAL["new"] if isnew else (PAL["dim"] if isdim else PAL["border"])
        svg.rect(tx, y, w, 32, fill, stroke, 2.2 if isnew else 1.2)
        col = PAL["new"] if isnew else ("#9aabb3" if isdim else PAL["ink"])
        svg.text(tx + w / 2, y + 21, it, 14, col, bold=isnew)
        tx += w + 4
    if mark:
        svg.text(tx + 6, y + 21, mark, 12, PAL["muted"], anchor="start", italic=True)
    return y + 32


def caption(svg, x, y, s, color=PAL["ink"], size=14, anchor="start"):
    svg.text(x, y, s, size, color, anchor=anchor)


# Árboles

def bin_layout(t, dx=46, dy=62):
    """t = (clave, izq, der) o None. Devuelve pos, aristas y padres por id."""
    pos, edges, keys = {}, [], {}
    counter = [0]
    ids = [0]

    def rec(node, depth):
        if node is None:
            return None
        k, l, r_ = node
        lid = rec(l, depth + 1)
        my = f"n{ids[0]}"
        ids[0] += 1
        pos[my] = (counter[0] * dx, depth * dy)
        keys[my] = k
        counter[0] += 1
        rid = rec(r_, depth + 1)
        if lid:
            edges.append((my, lid))
        if rid:
            edges.append((my, rid))
        return my

    root = rec(t, 0)
    return pos, edges, keys, root


def nary_layout(t, dx=50, dy=64):
    """t = (etiqueta, [hijos]). Hojas consecutivas, padres centrados."""
    pos, edges, keys = {}, [], {}
    counter = [0]
    ids = [0]

    def rec(node, depth):
        lab, ch = node
        my = f"n{ids[0]}"
        ids[0] += 1
        keys[my] = lab
        kids = [rec(c, depth + 1) for c in ch]
        if kids:
            xs = [pos[k][0] for k in kids]
            pos[my] = ((min(xs) + max(xs)) / 2, depth * dy)
            for k in kids:
                edges.append((my, k))
        else:
            pos[my] = (counter[0] * dx, depth * dy)
            counter[0] += 1
        return my

    root = rec(t, 0)
    return pos, edges, keys, root
