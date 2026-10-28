"""Animaciones SVG de árboles y arreglos.

Una animación es una lista de cuadros (Frame). Cada cuadro dice dónde está cada nodo, con qué
estilo, qué etiqueta lleva y de quién es hijo. El SVG resultante desliza los nodos de un cuadro
al siguiente con SMIL (<animate>): funciona dentro de un <img>, sin JavaScript, y se repite
solo. El mismo cuadro se dibuja quieto con still(), para las pestañas «Paso 1, Paso 2, ...».

Los nodos, aristas y casillas se identifican por un id que se conserva entre cuadros: si un id
cambia de lugar, se desliza; si falta en un cuadro, se desvanece.
"""
import json

from figlib import SVG, PAL, NODE_STYLES, FONT, SCALE, text_width, esc, _shorten

R = 15            # radio de los nodos, como en tviz.draw
FONT_N = 13       # letra de las llaves

STYLES = dict(NODE_STYLES)
STYLES.update({
    # subárboles que se mueven en una rotación: A azul, B naranja, C verde, D/E morado
    "sa": ("#dde6fa", PAL["teal"], PAL["ink"], 1.8),
    "sb": ("#ffe8c7", "#b86a00", PAL["ink"], 1.8),
    "sc": ("#dcf2dc", PAL["goal"], PAL["ink"], 1.8),
    "sd": ("#e6d5f2", "#7030a0", PAL["ink"], 1.8),
    "out": ("#eeeeee", "#9a9a9a", "#8a8a8a", 1.1),
})
BOLD = {"new", "hl", "bad"}

# Casillas: (relleno, borde, texto, grosor)
CELL_STYLES = {
    "plain": ("#ffffff", "#ffffff", PAL["ink"], 0.0),
    "slot": (PAL["white"], PAL["border"], PAL["ink"], 1.2),
    "slot-out": ("#ececec", "#c4c4c4", PAL["ink"], 1.0),
    "txt": ("#ffffff", "#ffffff", PAL["ink"], 0.0),
    "txt-new": ("#ffffff", "#ffffff", PAL["new"], 0.0),
    "txt-goal": ("#ffffff", "#ffffff", PAL["goal"], 0.0),
    "txt-muted": ("#ffffff", "#ffffff", "#8a8a8a", 0.0),
    "box": ("#fff6f6", PAL["new"], PAL["new"], 1.6),
    "dim": ("#ececec", "#ececec", "#9a9a9a", 0.0),
}
for _k in ("new", "hl", "bad", "goal", "tree", "sa", "sb", "sc", "sd", "out"):
    CELL_STYLES[_k] = STYLES[_k]

EDGE = {"plain": (PAL["ink"], 1.2), "new": (PAL["new"], 3.0), "path": (PAL["new"], 3.0),
        "dim": (PAL["dim"], 1.3), "tree": (PAL["teal"], 2.6), "good": (PAL["goal"], 3.0),
        "bad": (PAL["bad"], 3.0), "hl": (PAL["orange"], 3.0)}

LABEL_COLORS = {None: PAL["teal"], "new": PAL["new"], "bad": PAL["bad"], "idx": "#7a7a7a",
                "goal": PAL["goal"]}


class Frame:
    def __init__(self, caption="", hold=None):
        self.caption = caption
        self.hold = hold          # segundos quieto; por defecto, según el largo del texto
        self.nodes = {}
        self.edges = {}
        self.cells = {}

    def node(self, nid, x, y, text, style="plain", label="", lstyle=None, lside="right",
             ring=False, shape="circle", hidden=False):
        """hidden: el nodo está en ese lugar pero no se ve (para que aparezca volando desde ahí)."""
        self.nodes[nid] = dict(x=x, y=y, text=str(text), style=style, label=str(label),
                               lstyle=lstyle, lside=lside, ring=ring, shape=shape, hidden=hidden)

    def edge(self, child, parent, style="plain"):
        self.edges[child] = (parent, style)

    def cell(self, cid, x, y, w, h, text, style="plain", size=14, hidden=False):
        self.cells[cid] = dict(x=x, y=y, w=w, h=h, text=str(text), style=style, size=size,
                               hidden=hidden)


def _label_xy(n):
    s = n["lside"]
    if s == "left":
        return -R - 4, -R + 5, "end"
    if s == "above":
        return 0, -R - 6, "middle"
    if s == "below":
        return 0, R + 15, "middle"
    return R + 4, -R + 5, "start"


TRI_H, TRI_W = 40, 24      # triángulo de un subárbol: alto y medio ancho


# Dibujo quieto de un cuadro
def still(fr, static=()):
    svg = SVG()
    for x, y, s, size, color, anchor, bold in static:
        svg.text(x, y, s, size, color, anchor=anchor, bold=bold)
    for cid, c in fr.cells.items():
        if c["hidden"]:
            continue
        fill, stroke, tc, w = CELL_STYLES[c["style"]]
        if w > 0 or fill != "#ffffff":
            svg.rect(c["x"], c["y"], c["w"], c["h"], fill, stroke, w)
        else:
            svg._box(c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"])
        svg.text(c["x"] + c["w"] / 2, c["y"] + c["h"] / 2 + c["size"] * 0.36, c["text"], c["size"],
                 tc, bold=c["style"] in BOLD or c["style"] in ("box", "txt-new"))
    for ch, (par, st) in fr.edges.items():
        a, b = fr.nodes[par], fr.nodes[ch]
        if a["hidden"] or b["hidden"]:
            continue
        color, w = EDGE[st]
        rb = 0 if b["shape"] == "tri" else R
        x1, y1, x2, y2 = _shorten(a["x"], a["y"], b["x"], b["y"], R, rb)
        svg.line(x1, y1, x2, y2, color, w)
    for nid, n in fr.nodes.items():
        if n["hidden"]:
            continue
        fill, stroke, tc, w = STYLES[n["style"]]
        x, y = n["x"], n["y"]
        if n["shape"] == "tri":
            svg.polygon([(x, y), (x - TRI_W, y + TRI_H), (x + TRI_W, y + TRI_H)], fill, stroke, w)
            svg.text(x, y + TRI_H - 9, n["text"], 14, tc)
        elif n["shape"] == "ghost":
            svg.ellipse(x, y, R, R, "#ffffff", PAL["new"], 1.8, "4,3")
            svg.text(x, y + 5, n["text"], FONT_N, PAL["new"], bold=True)
        else:
            svg.circle(x, y, R, fill, stroke, w)
            size = FONT_N if len(n["text"]) <= 2 else max(10, FONT_N - (len(n["text"]) - 2))
            svg.text(x, y + size * 0.35, n["text"], size, tc, bold=n["style"] in BOLD)
        if n["ring"]:
            svg.circle(x, y, R + 6, "none", PAL["new"], 2.2)
        if n["label"]:
            dx, dy, anchor = _label_xy(n)
            svg.text(x + dx, y + dy, n["label"], 13, LABEL_COLORS[n["lstyle"]], anchor=anchor,
                     bold=n["lstyle"] is not None and n["lstyle"] != "idx")
    return svg


# Línea de tiempo
MOVE = 0.9        # segundos que tarda el paso de un cuadro al siguiente
FADE = 0.45


def _hold(caption):
    return min(6.0, max(2.2, 1.0 + 0.05 * len(caption)))


class _Timeline:
    def __init__(self, holds, tail=1.8):
        self.S, self.E = [], []
        t = 0.0
        for i, h in enumerate(holds):
            self.S.append(t)
            if i == len(holds) - 1:
                h += tail
            self.E.append(t + h)
            t += h + MOVE
        self.J = self.E[-1] + FADE
        self.D = self.J + FADE

    def anim(self, attr, vals, tag="animate", extra=""):
        """<animate> de un atributo con un valor por cuadro (None: se repite el anterior)."""
        vals = list(vals)
        if all(v == vals[0] for v in vals):
            return ""
        pts = []
        for i, v in enumerate(vals):
            pts += [(self.S[i], v), (self.E[i], v)]
        pts += [(self.J, vals[-1]), (self.J + 0.002, vals[0]), (self.D, vals[0])]
        # quitar puntos intermedios repetidos
        out = [pts[0]]
        for k in range(1, len(pts) - 1):
            if pts[k][1] == out[-1][1] and pts[k][1] == pts[k + 1][1]:
                continue
            out.append(pts[k])
        out.append(pts[-1])
        kt = ";".join(f"{t / self.D:.4f}" for t, _ in out)
        vs = ";".join(str(v) for _, v in out)
        spl = ";".join("0.45 0 0.25 1" if (a[1] != b[1] and b[0] - a[0] > 0.05) else "0 0 1 1"
                       for a, b in zip(out, out[1:]))
        return (f'<{tag} attributeName="{attr}"{extra} dur="{self.D:.2f}s" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="{kt}" keySplines="{spl}" values="{vs}"/>')


def _f(v):
    return f"{v:.1f}"


def _fill_missing(seq):
    """Valores por cuadro con huecos (None): se rellenan con el vecino más cercano."""
    n = len(seq)
    out = list(seq)
    for i in range(n):
        if out[i] is None:
            for d in range(1, n):
                for j in (i - d, i + d):
                    if 0 <= j < n and seq[j] is not None:
                        out[i] = seq[j]
                        break
                if out[i] is not None:
                    break
    return out


def _wrap(s, width, size=14):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and text_width(t, size) > width:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines or [""]


def render(frames, static=(), min_w=420, title=""):
    """SVG animado (texto) de la lista de cuadros."""
    n = len(frames)
    tl = _Timeline([f.hold if f.hold is not None else _hold(f.caption) for f in frames])
    # caja: nodos, etiquetas, casillas y textos fijos de todos los cuadros
    xs, ys = [], []
    for f in frames:
        for nd in f.nodes.values():
            ext = TRI_H + 4 if nd["shape"] == "tri" else R + 8
            xs += [nd["x"] - R - 8, nd["x"] + R + 8]
            ys += [nd["y"] - R - 8, nd["y"] + ext]
            if nd["label"]:
                dx, dy, anchor = _label_xy(nd)
                w = text_width(nd["label"], 13)
                x0 = nd["x"] + dx - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
                xs += [x0, x0 + w]
                ys += [nd["y"] + dy - 13]
        for c in f.cells.values():
            w = max(c["w"], text_width(c["text"], c["size"]))
            cx = c["x"] + c["w"] / 2
            xs += [cx - w / 2, cx + w / 2]
            ys += [c["y"], c["y"] + c["h"]]
    for x, y, s, size, *_ in static:
        w = text_width(s, size)
        xs += [x - w / 2, x + w / 2]
        ys += [y - size, y + 4]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    if maxx - minx < min_w:
        pad = (min_w - (maxx - minx)) / 2
        minx, maxx = minx - pad, maxx + pad
    cw = maxx - minx
    caps = [_wrap(f.caption, cw - 46) for f in frames]
    nl = max(len(c) for c in caps)
    cap_y = maxy + 34
    total_h = cap_y + 20 * nl - miny + 6
    m = 14
    vx, vy, vw, vh = minx - m, miny - m, cw + 2 * m, total_h + 2 * m
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw * SCALE:.0f}" height="{vh * SCALE:.0f}" '
           f'viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}" font-family="{FONT}">']
    if title:
        out.append(f"<title>{esc(title)}</title>")
    out.append(f'<rect x="{vx:.1f}" y="{vy:.1f}" width="{vw:.1f}" height="{vh:.1f}" fill="#ffffff"/>')
    out.append(f'<line x1="{minx:.1f}" y1="{cap_y - 24:.1f}" x2="{maxx:.1f}" y2="{cap_y - 24:.1f}" '
               f'stroke="#dddddd" stroke-width="1"/>')
    # el ciclo se reinicia con un fundido
    out.append(f'<g><animate attributeName="opacity" dur="{tl.D:.2f}s" repeatCount="indefinite" '
               f'keyTimes="0;{tl.E[-1] / tl.D:.4f};{tl.J / tl.D:.4f};1" values="1;1;0;1"/>')
    for x, y, s, size, color, anchor, bold in static:
        fw = ' font-weight="bold"' if bold else ""
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
                   f'text-anchor="{anchor}"{fw}>{esc(s)}</text>')

    def present(seq):
        return [1 if (v is not None and not v["hidden"]) else 0 for v in seq]

    # casillas
    cids = list(dict.fromkeys(k for f in frames for k in f.cells))
    for cid in cids:
        seq = [f.cells.get(cid) for f in frames]
        op = present(seq)
        seq = _fill_missing(seq)
        c0 = seq[0]
        tx = tl.anim("transform", [f"{_f(c['x'])} {_f(c['y'])}" for c in seq], "animateTransform",
                     ' type="translate"')
        out.append(f'<g transform="translate({_f(c0["x"])} {_f(c0["y"])})" opacity="{op[0]}">{tx}'
                   f'{tl.anim("opacity", op)}')
        st = [CELL_STYLES[c["style"]] for c in seq]
        w, h = c0["w"], c0["h"]
        out.append(f'<rect x="0" y="0" width="{w:.1f}" height="{h:.1f}" rx="4" fill="{st[0][0]}" '
                   f'stroke="{st[0][1]}" stroke-width="{st[0][3]}">'
                   f'{tl.anim("fill", [s[0] for s in st])}{tl.anim("stroke", [s[1] for s in st])}'
                   f'{tl.anim("stroke-width", [s[3] for s in st])}</rect>')
        bold = all(c["style"] in BOLD or c["style"] in ("box", "txt-new") for c in seq)
        fw = ' font-weight="bold"' if bold else ""
        out.append(f'<text x="{w / 2:.1f}" y="{h / 2 + c0["size"] * 0.36:.1f}" font-size="{c0["size"]}" '
                   f'text-anchor="middle" fill="{st[0][2]}"{fw}>{esc(c0["text"])}'
                   f'{tl.anim("fill", [s[2] for s in st])}</text></g>')

    # aristas (una por hijo) debajo de los nodos
    nids = list(dict.fromkeys(k for f in frames for k in f.nodes))
    pos = {}
    for nid in nids:
        pos[nid] = _fill_missing([(f.nodes[nid]["x"], f.nodes[nid]["y"]) if nid in f.nodes else None
                                  for f in frames])
    for ch in dict.fromkeys(k for f in frames for k in f.edges):
        ends, cols, ws, op = [], [], [], []
        for i, f in enumerate(frames):
            e = f.edges.get(ch)
            if e is None:
                ends.append(None)
                cols.append(None)
                ws.append(None)
                op.append(0)
                continue
            par, st = e
            a, b = f.nodes[par], f.nodes[ch]
            rb = 0 if b["shape"] == "tri" else R
            ends.append(_shorten(a["x"], a["y"], b["x"], b["y"], R, rb))
            cols.append(EDGE[st][0])
            ws.append(EDGE[st][1])
            op.append(0 if (a["hidden"] or b["hidden"]) else 1)
        for i in range(n):        # sin padre: la arista se encoge sobre el hijo
            if ends[i] is None:
                cx, cy = pos[ch][i]
                ends[i] = (cx, cy - R, cx, cy - R)
        cols, ws = _fill_missing(cols), _fill_missing(ws)
        e0 = ends[0]
        anims = "".join(tl.anim(a, [_f(e[k]) for e in ends]) for k, a in enumerate(("x1", "y1", "x2", "y2")))
        out.append(f'<line x1="{_f(e0[0])}" y1="{_f(e0[1])}" x2="{_f(e0[2])}" y2="{_f(e0[3])}" '
                   f'stroke="{cols[0]}" stroke-width="{ws[0]}" opacity="{op[0]}">{anims}'
                   f'{tl.anim("stroke", cols)}{tl.anim("stroke-width", ws)}{tl.anim("opacity", op)}</line>')

    # nodos
    for nid in nids:
        seq = [f.nodes.get(nid) for f in frames]
        op = present(seq)
        seq = _fill_missing(seq)
        n0 = seq[0]
        tx = tl.anim("transform", [f"{_f(x)} {_f(y)}" for x, y in pos[nid]], "animateTransform",
                     ' type="translate"')
        x0, y0 = pos[nid][0]
        out.append(f'<g transform="translate({_f(x0)} {_f(y0)})" opacity="{op[0]}">{tx}{tl.anim("opacity", op)}')
        st = [STYLES[nd["style"]] for nd in seq]
        paint = (f'{tl.anim("fill", [s[0] for s in st])}{tl.anim("stroke", [s[1] for s in st])}'
                 f'{tl.anim("stroke-width", [s[3] for s in st])}')
        if n0["shape"] == "tri":
            out.append(f'<polygon points="0,0 {-TRI_W},{TRI_H} {TRI_W},{TRI_H}" fill="{st[0][0]}" '
                       f'stroke="{st[0][1]}" stroke-width="{st[0][3]}">{paint}</polygon>')
            out.append(f'<text x="0" y="{TRI_H - 9}" font-size="14" text-anchor="middle" '
                       f'fill="{st[0][2]}">{esc(n0["text"])}</text>')
        elif n0["shape"] == "ghost":
            out.append(f'<circle cx="0" cy="0" r="{R}" fill="#ffffff" stroke="{PAL["new"]}" '
                       f'stroke-width="1.8" stroke-dasharray="4,3"/>')
            out.append(f'<text x="0" y="5" font-size="{FONT_N}" text-anchor="middle" fill="{PAL["new"]}" '
                       f'font-weight="bold">{esc(n0["text"])}</text>')
        else:
            t = n0["text"]
            size = FONT_N if len(t) <= 2 else max(10, FONT_N - (len(t) - 2))
            out.append(f'<circle cx="0" cy="0" r="{R}" fill="{st[0][0]}" stroke="{st[0][1]}" '
                       f'stroke-width="{st[0][3]}">{paint}</circle>')
            out.append(f'<text x="0" y="{size * 0.35:.1f}" font-size="{size}" text-anchor="middle" '
                       f'fill="{st[0][2]}">{esc(t)}{tl.anim("fill", [s[2] for s in st])}</text>')
        rings = [1 if (nd["ring"] and o) else 0 for nd, o in zip(seq, op)]
        if any(rings):
            out.append(f'<circle cx="0" cy="0" r="{R + 6}" fill="none" stroke="{PAL["new"]}" '
                       f'stroke-width="2.2" opacity="{rings[0]}">{tl.anim("opacity", rings)}</circle>')
        labs = list(dict.fromkeys((nd["label"], nd["lstyle"], nd["lside"]) for nd in seq if nd["label"]))
        for lab in labs:
            vis = [1 if (nd["label"], nd["lstyle"], nd["lside"]) == lab and o else 0
                   for nd, o in zip(seq, op)]
            dx, dy, anchor = _label_xy(dict(lside=lab[2]))
            fw = ' font-weight="bold"' if lab[1] not in (None, "idx") else ""
            out.append(f'<text x="{dx}" y="{dy}" font-size="13" text-anchor="{anchor}" '
                       f'fill="{LABEL_COLORS[lab[1]]}" opacity="{vis[0]}"{fw}>{esc(lab[0])}'
                       f'{tl.anim("opacity", vis)}</text>')
        out.append("</g>")

    # pie: «i/n» y el texto del cuadro
    for i, (f, lines) in enumerate(zip(frames, caps)):
        vis = [1 if j == i else 0 for j in range(n)]
        parts = [f'<tspan font-weight="bold" fill="{PAL["new"]}">{i + 1}/{n}</tspan>']
        for k, ln in enumerate(lines):
            parts.append(f'<tspan x="{minx + 40:.1f}" y="{cap_y + 20 * k:.1f}">{esc(ln)}</tspan>')
        out.append(f'<text x="{minx:.1f}" y="{cap_y:.1f}" font-size="14" fill="{PAL["ink"]}" '
                   f'opacity="{vis[0]}">{"".join(parts)}{tl.anim("opacity", vis)}</text>')
    out.append("</g>")
    tl_js = json.dumps({"S": [round(t, 3) for t in tl.S], "E": [round(t, 3) for t in tl.E]})
    out.append(f"<script><![CDATA[\nvar TL = {tl_js};\n{PLAYER_JS}]]></script>")
    out.append("</svg>\n")
    return "\n".join(out)


# Reproductor. Dentro de un <img> (como en el libro) los scripts no corren: la animación se
# repite sola y no se ve ningún control. Abierto el SVG por sí solo, el script detiene el reloj
# de SMIL, lo maneja él y agrega una barra con reiniciar, cuadro anterior, reproducir/pausar,
# cuadro siguiente, velocidad y una barra de progreso en la que se puede hacer clic.
PLAYER_JS = r"""
(function () {
  var svg = document.documentElement;
  if (!svg.pauseAnimations || svg.getAttribute('data-player')) return;
  svg.setAttribute('data-player', '1');
  var NS = 'http://www.w3.org/2000/svg';
  var S = TL.S, E = TL.E, n = S.length, END = E[n - 1];
  var vb = svg.viewBox.baseVal, x0 = vb.x, y0 = vb.y, w = vb.width, h = vb.height, H = 58;
  svg.setAttribute('viewBox', x0 + ' ' + y0 + ' ' + w + ' ' + (h + H));
  svg.removeAttribute('width');
  svg.removeAttribute('height');
  svg.style.background = '#ffffff';
  svg.pauseAnimations();
  var t = 0, playing = true, rates = [0.5, 1, 2], ri = 1, last = null;
  var INK = '#111111', RED = '#d62020';
  function el(tag, at, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in at) e.setAttribute(k, at[k]);
    parent.appendChild(e);
    return e;
  }
  var bar = el('g', {}, svg), by = y0 + h + 6;
  el('rect', {x: x0, y: by - 2, width: w, height: H - 6, fill: '#f4f4f4'}, bar);
  function button(x, draw, fn, tip) {
    var b = el('g', {transform: 'translate(' + x + ',' + by + ')', style: 'cursor:pointer'}, bar);
    el('title', {}, b).textContent = tip;
    el('rect', {x: 0, y: 4, width: 34, height: 28, rx: 6, fill: '#ffffff', stroke: '#9a9a9a'}, b);
    var ic = el('g', {fill: INK}, b);
    draw(ic);
    b.addEventListener('click', function (ev) { ev.stopPropagation(); fn(); });
    return ic;
  }
  function path(g, d) { el('path', {d: d}, g); }
  var bx = x0 + 8;
  button(bx, function (g) { path(g, 'M7 11h3v14h-3z M19 11v14l-8-7z M28 11v14l-8-7z'); }, restart, 'Reiniciar (Inicio)');
  button(bx + 40, function (g) { path(g, 'M11 11h3v14h-3z M25 11v14l-10-7z'); }, prev, 'Cuadro anterior (←)');
  var pp = button(bx + 80, function () {}, toggle, 'Reproducir / pausar (espacio)');
  button(bx + 120, function (g) { path(g, 'M9 11v14l10-7z M20 11h3v14h-3z'); }, next, 'Cuadro siguiente (→)');
  var sp = el('g', {transform: 'translate(' + (bx + 160) + ',' + by + ')', style: 'cursor:pointer'}, bar);
  el('title', {}, sp).textContent = 'Velocidad';
  el('rect', {x: 0, y: 4, width: 42, height: 28, rx: 6, fill: '#ffffff', stroke: '#9a9a9a'}, sp);
  var spt = el('text', {x: 21, y: 23, 'font-size': 13, 'text-anchor': 'middle', fill: INK}, sp);
  sp.addEventListener('click', function (ev) { ev.stopPropagation(); ri = (ri + 1) % 3; draw(); });
  var px = bx + 212, pw = x0 + w - 8 - px - 56;
  var prog = el('g', {style: 'cursor:pointer'}, bar);
  el('rect', {x: px, y: by + 14, width: pw, height: 8, rx: 4, fill: '#dddddd'}, prog);
  for (var i = 1; i < n; i++)
    el('rect', {x: px + pw * S[i] / END - 0.5, y: by + 12, width: 1, height: 12, fill: '#9a9a9a'}, prog);
  var fill = el('rect', {x: px, y: by + 14, width: 0, height: 8, rx: 4, fill: RED}, prog);
  var cnt = el('text', {x: x0 + w - 10, y: by + 23, 'font-size': 13, 'text-anchor': 'end', fill: INK,
                        'font-weight': 'bold'}, bar);
  el('text', {x: x0 + w / 2, y: by + 46, 'font-size': 10.5, 'text-anchor': 'middle', fill: '#555555'}, bar)
    .textContent = 'Espacio: reproducir o pausar · ← →: cuadro a cuadro · clic en la barra: saltar';
  prog.addEventListener('click', function (ev) {
    var p = svg.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY;
    var q = p.matrixTransform(svg.getScreenCTM().inverse());
    t = Math.max(0, Math.min(END, (q.x - px) / pw * END)); playing = false; draw();
  });
  function frame() { var k = 0; for (var i = 0; i < n; i++) if (S[i] <= t + 1e-6) k = i; return k; }
  function go(k) { t = S[Math.max(0, Math.min(n - 1, k))]; playing = false; draw(); }
  function restart() { t = 0; playing = true; draw(); }
  function prev() { var k = frame(); go(t > S[k] + 0.3 ? k : k - 1); }
  function next() { go(frame() + 1); }
  function toggle() { if (!playing && t >= END) t = 0; playing = !playing; draw(); }
  function draw() {
    svg.setCurrentTime(t);
    fill.setAttribute('width', pw * t / END);
    cnt.textContent = (frame() + 1) + '/' + n;
    spt.textContent = rates[ri] + '×';
    while (pp.firstChild) pp.removeChild(pp.firstChild);
    if (playing) { path(pp, 'M11 11h4v14h-4z M19 11h4v14h-4z'); }
    else { path(pp, 'M12 10v16l13-8z'); }
  }
  function tick(now) {
    if (last !== null && playing) {
      t += (now - last) / 1000 * rates[ri];
      if (t >= END) { t = END; playing = false; }
      draw();
    }
    last = now;
    requestAnimationFrame(tick);
  }
  document.addEventListener('keydown', function (ev) {
    if (ev.key === ' ') { toggle(); ev.preventDefault(); }
    else if (ev.key === 'ArrowRight') next();
    else if (ev.key === 'ArrowLeft') prev();
    else if (ev.key === 'Home') restart();
  });
  draw();
  requestAnimationFrame(tick);
})();
"""


class AnimSVG:
    """Envoltorio con save(), para usarlo con Page.img como cualquier figura."""

    def __init__(self, frames, static=(), title="", min_w=420):
        self.frames, self.static, self.title, self.min_w = frames, static, title, min_w

    def save(self, path, **kw):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(self.frames, self.static, self.min_w, self.title))


def anim_block(page, name, frames, alt, static=(), min_w=420):
    """Figura animada lista para el markdown, con el enlace que la abre con controles."""
    path = page.img(name, AnimSVG(frames, static, alt, min_w))
    return (f"![{alt}]({path})\n\n"
            f"[▶ Abrir la animación con controles (reproducir, pausar, cuadro a cuadro)]({path})")


# Árboles binarios (tviz.N) como cuadros
def tree_frame(root, caption="", dx=40, dy=56, node_style=None, edge_style=None, labels=None,
               label_style=None, rings=(), label_side="away", ox=0, oy=0, fr=None):
    """Cuadro con el árbol en la disposición de tviz.layout (x por inorden): una rotación
    no mueve a nadie de columna, solo de nivel."""
    from tviz import layout
    fr = fr or Frame(caption)
    if root is None:
        return fr
    pos, edges = layout(root, dx, dy)
    node_style = node_style or {}
    edge_style = edge_style or {}
    labels = labels or {}
    label_style = label_style or {}
    par = {b: a for a, b in edges}
    for k, (x, y) in pos.items():
        side = label_side
        if side == "away":
            p = par.get(k)
            side = "left" if p is not None and pos[p][0] > x else "right"
        fr.node(k, x + ox, y + oy, k, node_style.get(k, "plain"), labels.get(k, ""),
                label_style.get(k), side, ring=k in rings)
    for a, b in edges:
        fr.edge(b, a, edge_style.get((a, b), "plain"))
    return fr
