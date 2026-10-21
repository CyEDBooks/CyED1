"""Dibujo en SVG de los grafos y árboles de CyED1.

Las figuras llevan fondo blanco para verse igual en el libro y en un visor de
imágenes.
"""
import html
import math
import os

# Paleta de las diapositivas de Bedoya: trazo negro, pesos en azul y lo nuevo
# de cada paso en rojo.
PAL = {
    "ink": "#111111",
    "muted": "#555555",
    "new": "#d62020",      # lo nuevo de cada paso (rojo, como las etiquetas de Bedoya)
    "teal": "#1f3c88",     # azul de los pesos y del árbol que se va formando
    "sky": "#9db4e8",
    "border": "#9a9a9a",
    "soft": "#f4f4f4",
    "yellow": "#ffe680",
    "orange": "#e08a00",
    "gray": "#bdbdbd",
    "dim": "#cfcfcf",
    "white": "#ffffff",
    "goal": "#2e7d32",
    "bad": "#d62020",
    "green": "#92d050",    # nodos de los árboles de búsqueda de Bedoya
}

# Las figuras de Bedoya usan Comic Sans. Comic Neue es la alternativa libre
# para los equipos que no tienen Comic Sans MS.
FONT = "'Comic Sans MS', 'Comic Neue', 'Comic Relief', 'Chalkboard SE', cursive"

# Tamaño en pantalla respecto a las coordenadas del dibujo. Escala todo por igual
# (letra, trazos, vértices); las figuras más anchas que la columna las ajusta el
# navegador a su ancho.
SCALE = 1.5

# Ancho (en coordenadas del dibujo) a partir del cual una fila de figuras se parte
# en varias: más ancha, el navegador la encoge y la letra vuelve a quedar pequeña.
MAX_W = 680

# Estilos de vértice dibujado como círculo: (relleno, borde, color del texto, grosor del borde)
NODE_STYLES = {
    "plain": (PAL["white"], PAL["ink"], PAL["ink"], 1.3),
    "white": (PAL["white"], PAL["ink"], PAL["ink"], 1.3),
    "out": (PAL["white"], PAL["ink"], PAL["ink"], 1.3),
    "gray": (PAL["gray"], PAL["ink"], PAL["ink"], 1.3),
    "black": (PAL["ink"], PAL["ink"], PAL["white"], 1.3),
    "new": (PAL["white"], PAL["new"], PAL["new"], 2.6),
    "newgray": (PAL["gray"], PAL["new"], PAL["ink"], 2.8),
    "newblack": (PAL["ink"], PAL["new"], PAL["white"], 3.0),
    "hl": ("#fff2b3", PAL["new"], PAL["ink"], 2.4),
    "tree": ("#dfe7fb", PAL["teal"], PAL["ink"], 2.0),
    "dim": (PAL["white"], PAL["dim"], "#9a9a9a", 1.2),
    "goal": ("#c6efce", PAL["goal"], PAL["ink"], 2.4),
    "bad": ("#ffd9d9", PAL["bad"], PAL["ink"], 2.4),
    "ghost": (PAL["white"], PAL["dim"], "#9a9a9a", 1.1),
    "green": (PAL["green"], "#4d7a1f", PAL["ink"], 1.3),
    "v1": ("#e6d5f2", "#7030a0", PAL["ink"], 2.0),
    "v2": ("#ffd9d9", PAL["new"], PAL["ink"], 2.0),
}

# Vértice dibujado como punto (grafos de Bedoya): (relleno, borde, radio, color del nombre)
DOT_STYLES = {
    "plain": (PAL["ink"], PAL["ink"], 4.2, PAL["ink"]),
    "white": (PAL["white"], PAL["ink"], 4.6, PAL["ink"]),
    "out": (PAL["white"], PAL["ink"], 4.6, PAL["ink"]),
    "gray": (PAL["gray"], PAL["ink"], 5.0, PAL["ink"]),
    "black": (PAL["ink"], PAL["ink"], 4.6, PAL["ink"]),
    "new": (PAL["new"], PAL["new"], 5.6, PAL["new"]),
    "newgray": (PAL["new"], PAL["new"], 5.6, PAL["new"]),
    "newblack": (PAL["new"], PAL["new"], 5.6, PAL["new"]),
    "hl": (PAL["new"], PAL["new"], 5.6, PAL["new"]),
    "tree": (PAL["ink"], PAL["ink"], 5.2, PAL["ink"]),
    "dim": (PAL["dim"], PAL["dim"], 4.0, "#9a9a9a"),
    "goal": (PAL["goal"], PAL["goal"], 6.0, PAL["goal"]),
    "bad": (PAL["bad"], PAL["bad"], 5.6, PAL["bad"]),
    "ghost": (PAL["white"], PAL["dim"], 4.0, "#9a9a9a"),
    "green": (PAL["green"], "#4d7a1f", 5.6, PAL["ink"]),
    "v1": ("#7030a0", "#7030a0", 5.2, PAL["ink"]),   # bipartitos: V1 morado, V2 rojo
    "v2": (PAL["new"], PAL["new"], 5.2, PAL["ink"]),
}

# Estilos de arista: (color, grosor, guiones)
EDGE_STYLES = {
    "plain": (PAL["ink"], 1.2, None),
    "tree": (PAL["teal"], 3.0, None),
    "new": (PAL["new"], 3.2, None),
    "dim": (PAL["dim"], 1.1, None),
    "cand": (PAL["orange"], 1.8, "6,4"),
    "reject": (PAL["bad"], 2.0, "3,4"),
    "back": (PAL["muted"], 1.6, "6,4"),
    "ghost": (PAL["dim"], 1.1, "4,4"),
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

    def add(self, sub, dx, dy):
        """Copia otro dibujo desplazado (dx, dy)."""
        for it in sub.items:
            self.items.append(f'<g transform="translate({dx:.1f},{dy:.1f})">{it}</g>')
        self._box(sub.minx + dx, sub.miny + dy, sub.maxx + dx, sub.maxy + dy)

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

    def ellipse(self, x, y, rx, ry, fill, stroke, width=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"{d}/>')
        self._box(x - rx - 1, y - ry - 1, x + rx + 1, y + ry + 1)

    def polygon(self, pts, fill, stroke, width=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(
            f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"{d}/>')
        for x, y in pts:
            self._box(x - 1, y - 1, x + 1, y + 1)

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
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * SCALE:.0f}" height="{h * SCALE:.0f}" '
                f'viewBox="{minx:.1f} {miny:.1f} {w:.1f} {h:.1f}" font-family="{FONT}">\n'
                f'<defs>{defs}</defs>\n'
                f'<rect x="{minx:.1f}" y="{miny:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#ffffff"/>\n')
        return head + "\n".join(self.items) + "\n</svg>\n"

    def save(self, path, **kw):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render(**kw))


def tile(parts, gap=60, vgap=36, max_w=MAX_W, caps=None, cap_dy=26):
    """Pone varios dibujos lado a lado. Si la fila pasa de max_w, los reparte por igual
    en más filas (4 quedan 2 y 2; 3 quedan 2 y 1), cada fila centrada. Los rótulos
    (caps) van debajo de cada dibujo, a la misma altura en toda la fila."""
    n = len(parts)
    caps = caps or [""] * n
    ws = [max(s.maxx - s.minx, text_width(c, 14)) for s, c in zip(parts, caps)]
    for nrows in range(1, n + 1):
        per = -(-n // nrows)
        groups = [range(i, min(i + per, n)) for i in range(0, n, per)]
        widths = [sum(ws[i] for i in g) + gap * (len(g) - 1) for g in groups]
        if max(widths) <= max_w:
            break
    svg = SVG()
    y0 = 0
    for g, w in zip(groups, widths):
        x0 = (max(widths) - w) / 2
        top = min(parts[i].miny for i in g)
        bottom = y0 + max(parts[i].maxy for i in g) - top
        for i in g:
            s = parts[i]
            cx = x0 + ws[i] / 2
            svg.add(s, cx - (s.minx + s.maxx) / 2, y0 - top)
            if caps[i]:
                svg.text(cx, bottom + cap_dy, caps[i], 14, PAL["ink"])
            x0 += ws[i] + gap
        y0 = svg.maxy + vgap
    return svg


def text_width(s, size):
    # Aproximación suficiente para Comic Sans MS / Comic Neue.
    w = 0
    for ch in str(s):
        if ch in "il.,:;|!'·":
            w += 0.3
        elif ch in "mwMW":
            w += 0.9
        elif ch.isupper() or ch in "∞→⟨⟩":
            w += 0.7
        elif ch == " ":
            w += 0.32
        else:
            w += 0.6
    return w * size


R = 18  # radio de vértice


def _shorten(x1, y1, x2, y2, r1, r2):
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    return (x1 + dx * r1 / d, y1 + dy * r1 / d, x2 - dx * r2 / d, y2 - dy * r2 / d)


DIRS = {  # dirección de una etiqueta junto a un punto: ángulo en grados (y hacia abajo)
    "above": -90, "below": 90, "left": 180, "right": 0,
    "above-left": -135, "above-right": -45, "below-left": 135, "below-right": 45,
}
_PREF = ["above", "left", "right", "below", "above-left", "above-right", "below-left",
         "below-right"]


def _angdist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _place(svg, x, y, where, s, size, color, bold=False, off=10):
    """Texto junto al punto (x, y) en la dirección 'where'."""
    ang = math.radians(DIRS[where])
    cx, cy = math.cos(ang), math.sin(ang)
    tx, ty = x + cx * off, y + cy * off
    anchor = "start" if cx > 0.35 else ("end" if cx < -0.35 else "middle")
    if cy > 0.35:
        ty += size * 0.75
    elif cy < -0.35:
        ty -= 1
    else:
        ty += size * 0.35
    svg.text(tx, ty, s, size, color, anchor=anchor, bold=bold)


def label_dirs(pos, edges, v, avoid=()):
    """Direcciones libres alrededor de v, de la más despejada a la menos."""
    x, y = pos[v]
    angs = []
    cx0 = sum(p[0] for p in pos.values()) / len(pos)
    cy0 = sum(p[1] for p in pos.values()) / len(pos)
    for e in edges:
        a, b = e[0], e[1]
        if a == b:
            if a == v:  # el bucle sale hacia afuera del dibujo, como en draw_graph
                ang = math.atan2(y - cy0, x - cx0) if (x, y) != (cx0, cy0) else -math.pi / 2
                ang = round(ang / (math.pi / 2)) * (math.pi / 2)
                angs += [math.degrees(ang) - 30, math.degrees(ang), math.degrees(ang) + 30]
            continue
        if a == v or b == v:
            w = b if a == v else a
            wx, wy = pos[w]
            angs.append(math.degrees(math.atan2(wy - y, wx - x)))
    out_ang = math.degrees(math.atan2(y - cy0, x - cx0)) if (x, y) != (cx0, cy0) else -90

    def score(dname):
        a = DIRS[dname]
        free = min((_angdist(a, b) for b in angs), default=180)
        if any(_angdist(a, DIRS[o]) < 50 for o in avoid):
            free -= 200
        # se prefiere ligeramente hacia afuera del dibujo
        return (round(min(free, 90) / 15), -_angdist(a, out_ang) / 180, -_PREF.index(dname))
    return sorted(DIRS, key=score, reverse=True)


def draw_graph(svg, pos, edges, directed=False, node_style=None, edge_style=None,
               node_text=None, labels=None, label_style=None, label_pos=None,
               weights=None, weight_style=None, r=R, curved=None, font=15,
               label_font=13, dots=True, name_pos=None):
    """Dibuja un grafo.

    pos: {v: (x, y)}; edges: lista de (u, v) o (u, v, w).
    node_style / edge_style: estilos por vértice / por arista (clave (u, v)).
    labels: anotación junto al vértice (p. ej. "d=1" o "[2,a]").
    dots: True dibuja cada vértice como un punto con el nombre al lado (grafos de
    Bedoya); False, como un círculo con el nombre adentro.
    name_pos: {v: dirección} para fijar dónde va el nombre de un vértice punto.
    """
    node_style = node_style or {}
    edge_style = edge_style or {}
    node_text = node_text or {}
    labels = labels or {}
    label_style = label_style or {}
    label_pos = label_pos or {}
    name_pos = name_pos or {}
    weight_style = weight_style or {}
    eset = {(e[0], e[1]) for e in edges}
    curved = curved or {}

    def rad(v):
        if dots:
            return DOT_STYLES[node_style.get(v, "plain")][2] + 1.5
        return r

    def est(u, v):
        s = edge_style.get((u, v))
        if s is None and not directed:
            s = edge_style.get((v, u))
        return s or "plain"

    used_labels = []
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
        ru, rv = rad(u), rad(v)
        if u == v:  # bucle, orientado hacia afuera del dibujo
            cx0 = sum(x for x, _ in pos.values()) / len(pos)
            cy0 = sum(y for _, y in pos.values()) / len(pos)
            ang = math.atan2(y1 - cy0, x1 - cx0) if (x1, y1) != (cx0, cy0) else -math.pi / 2
            ang = round(ang / (math.pi / 2)) * (math.pi / 2)
            ux, uy = math.cos(ang), math.sin(ang)
            px, py = -uy, ux
            k = 0.55 if dots else 1.0

            def P(a, b):
                return x1 + ux * a + px * b, y1 + uy * a + py * b
            s0, c1, c2, s1 = (P(ru - 2, -8 * k), P(ru + 38 * k, -30 * k), P(ru + 38 * k, 30 * k),
                              P(ru - 2, 8 * k))
            svg.path(f"M{s0[0]:.1f},{s0[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} "
                     f"{c2[0]:.1f},{c2[1]:.1f} {s1[0]:.1f},{s1[1]:.1f}",
                     color, width, dash, marker)
            tip = P(ru + 30 * k, 0)
            svg._box(min(c1[0], c2[0], x1) - 4, min(c1[1], c2[1], y1) - 4,
                     max(c1[0], c2[0], x1) + 4, max(c1[1], c2[1], y1) + 4)
            if w is not None:
                svg.text(tip[0] + ux * 10, tip[1] + uy * 10 + 5, w, 13, PAL["teal"], bg=True)
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
            sx1, sy1, _, _ = _shorten(x1, y1, cx, cy, ru, 0)
            _, _, sx2, sy2 = _shorten(cx, cy, x2, y2, 0, rv + (2 if directed else 0))
            svg.path(f"M{sx1:.1f},{sy1:.1f} Q{cx:.1f},{cy:.1f} {sx2:.1f},{sy2:.1f}",
                     color, width, dash, marker)
            lx, ly = mx + nx * bend, my + ny * bend
            svg._box(min(x1, x2, cx), min(y1, y2, cy), max(x1, x2, cx), max(y1, y2, cy))
        else:
            sx1, sy1, sx2, sy2 = _shorten(x1, y1, x2, y2, ru, rv + (2 if directed else 0))
            svg.line(sx1, sy1, sx2, sy2, color, width, dash, marker)
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
            # dos aristas que se cruzan en su punto medio: el peso se corre sobre la arista
            if w is not None and any(math.hypot(lx - a, ly - b) < 22 for a, b in used_labels):
                lx, ly = x1 + (x2 - x1) * 0.3, y1 + (y2 - y1) * 0.3
        if w is not None:
            used_labels.append((lx, ly))
            wst = weight_style.get((u, v)) or (None if directed else weight_style.get((v, u)))
            wc = {None: PAL["teal"], "new": PAL["new"], "dim": "#9a9a9a",
                  "tree": PAL["teal"]}.get(wst, PAL["teal"])
            svg.text(lx, ly + 5, w, 14, wc, bold=(wst in ("new", "tree")), bg=True)

    for v, (x, y) in pos.items():
        st = node_style.get(v, "plain")
        t = node_text.get(v, v)
        has_lab = v in labels and labels[v] != ""
        ls = label_style.get(v)
        lc = PAL["new"] if ls == "new" else ("#9a9a9a" if ls == "dim" else PAL["ink"])
        if dots:
            fill, stroke, dr, nc = DOT_STYLES[st]
            svg.circle(x, y, dr, fill, stroke, 1.2)
            lp = label_pos.get(v)
            if v in name_pos:
                nd = name_pos[v]
            else:
                nd = label_dirs(pos, edges, v, avoid=(lp,) if (lp and has_lab) else ())[0]
            _place(svg, x, y, nd, t, font, nc, bold=st in ("new", "newgray", "newblack", "hl"),
                   off=dr + 5)
            if has_lab:
                where = lp or label_dirs(pos, edges, v, avoid=(nd,))[0]
                # Bedoya escribe las etiquetas de los algoritmos en rojo
                col = PAL["new"] if ls in (None, "new") else lc
                _place(svg, x, y, where, labels[v], label_font, col, bold=(ls == "new"),
                       off=dr + 6)
            continue
        fill, stroke, tc, width = NODE_STYLES[st]
        svg.circle(x, y, r, fill, stroke, width)
        size = font if len(str(t)) <= 2 else max(10, font - 2 * (len(str(t)) - 2))
        svg.text(x, y + size * 0.35, t, size, tc, bold=st.startswith("new") or st == "hl")
        if has_lab:
            where = label_pos.get(v, "above")
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
        fill = "#ffe3e3" if isnew else (PAL["white"] if isdim else PAL["soft"])
        stroke = PAL["new"] if isnew else (PAL["dim"] if isdim else PAL["border"])
        svg.rect(tx, y, w, 32, fill, stroke, 2.2 if isnew else 1.2)
        col = PAL["new"] if isnew else ("#9a9a9a" if isdim else PAL["ink"])
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


def nary_layout(t, dx=50, dy=64, gap=0.5):
    """t = (etiqueta, [hijos]). Hojas consecutivas, padres centrados.

    Entre hojas de padres distintos se deja 'gap' columnas extra, para que los
    subárboles hermanos no se amontonen.
    """
    pos, edges, keys = {}, [], {}
    counter = [0.0]
    ids = [0]
    last_parent = [None]

    def rec(node, depth, parent):
        lab, ch = node
        my = f"n{ids[0]}"
        ids[0] += 1
        keys[my] = lab
        kids = [rec(c, depth + 1, my) for c in ch]
        if kids:
            xs = [pos[k][0] for k in kids]
            pos[my] = ((min(xs) + max(xs)) / 2, depth * dy)
            for k in kids:
                edges.append((my, k))
        else:
            if last_parent[0] is not None and last_parent[0] != parent:
                counter[0] += gap
            pos[my] = (counter[0] * dx, depth * dy)
            counter[0] += 1
            last_parent[0] = parent
        return my

    root = rec(t, 0, None)
    return pos, edges, keys, root


def compact_nary_layout(t, dx=50, dy=64):
    """Como nary_layout, pero cada subárbol se arrima a su hermano hasta quedar a dx en el
    nivel donde más se acercan. Una hoja poco profunda ya no ocupa una columna entera."""
    edges, keys = [], {}
    ids = [0]

    def rec(node):
        # devuelve (id, x relativa y nivel de cada nodo, contorno izquierdo y derecho)
        lab, ch = node
        my = f"n{ids[0]}"
        ids[0] += 1
        keys[my] = lab
        if not ch:
            return my, {my: (0, 0)}, [], []
        rel, left, right, xs = {}, [], [], []
        for c in ch:
            cid, crel, cl, cr = rec(c)
            cl, cr = [0] + cl, [0] + cr
            s = max((right[i] - cl[i] + dx for i in range(min(len(right), len(cl)))), default=0)
            for k, (x, d) in crel.items():
                rel[k] = (x + s, d)
            left += [v + s for v in cl[len(left):]]
            right = [v + s for v in cr] + right[len(cr):]
            xs.append(s)
            edges.append((my, cid))
        mid = (xs[0] + xs[-1]) / 2
        rel = {k: (x - mid, d + 1) for k, (x, d) in rel.items()}
        rel[my] = (0, 0)
        return my, rel, [v - mid for v in left], [v - mid for v in right]

    root, rel, _, _ = rec(t)
    minx = min(x for x, _ in rel.values())
    pos = {k: (x - minx, d * dy) for k, (x, d) in rel.items()}
    return pos, edges, keys, root
