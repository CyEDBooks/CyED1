from common import *
from figlib import nary_layout, text_width

# Árboles de las diapositivas de Bedoya (la letra es el nombre del nodo).
T0 = ("a", [("b", [("f", [])]), ("c", [("g", [("n", [])]), ("h", [])]),
            ("d", [("i", []), ("j", []), ("k", [("o", [("r", []), ("s", [])])])]),
            ("e", [("l", []), ("m", [("p", []), ("q", [])])])])
T1 = ("a", [("b", [("d", [("h", []), ("i", [])]), ("e", [("j", []), ("k", [("n", []), ("o", [])])])]),
            ("c", [("f", []), ("g", [("l", [("p", []), ("q", [])]), ("m", [("r", []), ("s", [])])])])])
T2 = ("a", [("b", [("e", [("k", []), ("m", [])]), ("f", [])]), ("c", [("g", []), ("h", [])]),
            ("d", [("i", []), ("j", [("n", [])])])])
T3 = ("a", [("b", [("e", [("m", []), ("n", [])]), ("f", []), ("g", []),
                   ("h", [("o", [("q", []), ("r", [])])])]),
            ("c", []), ("d", [("i", []), ("j", [("p", [])]), ("k", [])])])

L = ("·", [])  # hoja sin nombre


def info(t):
    parent, children, depth = {}, {}, {}

    def rec(node, p, d):
        lab, ch = node
        parent[lab] = p
        children[lab] = [c[0] for c in ch]
        depth[lab] = d
        for c in ch:
            rec(c, lab, d + 1)
    rec(t, None, 0)
    return parent, children, depth


def mlist(xs):
    return ", ".join(f"${x}$" for x in xs)


def put_info(p, key, t):
    par, ch, dep = info(t)
    leaves = [v for v in preorder(t) if not ch[v]]
    internal = [v for v in preorder(t) if ch[v]]
    p.put(f"{key}-hojas", mlist(leaves))
    p.put(f"{key}-nhojas", str(len(leaves)))
    p.put(f"{key}-internos", mlist(internal))
    p.put(f"{key}-alt", f"${max(dep.values()) + 1}$")
    p.put(f"{key}-peso", f"${len(ch)}$")
    p.put(f"{key}-orden", f"${max(len(c) for c in ch.values())}$")
    for v in ch:
        p.put(f"{key}-padre-{v}", f"${par[v]}$" if par[v] else "—")
        p.put(f"{key}-hijos-{v}", mlist(ch[v]) or "ninguno")
        p.put(f"{key}-prof-{v}", f"${dep[v]}$")
        p.put(f"{key}-ar-{v}", f"${len(ch[v])}$")


def preorder(t):
    lab, ch = t
    out = [lab]
    for c in ch:
        out += preorder(c)
    return out


def tsvg(t, dx=40, dy=56, **kw):
    pos, E = tree_pos(t, dx, dy)
    svg = SVG()
    draw_graph(svg, pos, E, **kw)
    return svg, pos, E


def tfig(p, name, t, alt="Árbol", **kw):
    svg, _, _ = tsvg(t, **kw)
    return f"![{alt}]({p.img(name, svg)})"


def utree(t):
    """Árbol sin nombres: da un nombre interno distinto a cada nodo."""
    k = [0]

    def rec(n):
        k[0] += 1
        return (f"u{k[0]}", [rec(c) for c in n[1]])
    return rec(t)


def ufig_row(p, name, trees, caps, dx=24, dy=46, gap=70):
    """Varios árboles sin nombres, uno al lado del otro, con su rótulo."""
    parts = []
    for t in trees:
        pos, E = tree_pos(utree(t), dx, dy)
        svg = SVG()
        draw_graph(svg, pos, E, node_text={v: "" for v in pos})
        parts.append(svg)
    return f"![{', '.join(caps)}]({p.img(name, tile(parts, gap, caps=caps))})"


def gcap(svg, pos, cap, dy=34):
    xs = [x for x, _ in pos.values()]
    svg.text((min(xs) + max(xs)) / 2, max(y for _, y in pos.values()) + dy, cap, 14, PAL["ink"])


def graph_row(p, name, items, gap=80, **kw):
    """items: lista de (pos, aristas, rótulo, estilos de arista)."""
    parts = []
    for pos, E, _, es in items:
        svg = SVG()
        draw_graph(svg, pos, E, edge_style=es, **kw)
        parts.append(svg)
    caps = [it[2] for it in items]
    return f"![{name}]({p.img(name, tile(parts, gap, caps=caps))})"


GRID = scale({"a": (0, 0), "b": (1, 0), "c": (0, 1), "d": (1, 1), "e": (0, 2), "f": (1, 2)}, 72)


def rooted(edges, r):
    adj = {}
    for x, y in edges:
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)

    def rec(v, par):
        return (v, [rec(w, v) for w in sorted(adj[v]) if w != par])
    return rec(r, None)


# Árboles de decisión: cada nodo es (texto, forma, [(rótulo de la rama, hijo), ...])
def draw_dtree(node, dx=110, dy=86, hl_path=(), shapes=None, compact=False):
    ids, labs, shp, kids, elab = {}, {}, {}, {}, {}
    k = [0]

    def rec(n):
        k[0] += 1
        me = f"n{k[0]}"
        labs[me], shp[me] = n[0], n[1]
        kids[me] = []
        ch = []
        for lab, c in n[2]:
            cid = rec(c)
            kids[me].append(cid)
            elab[(me, cid)] = lab
            ch.append((cid, []))
        return me
    root = rec(node)

    def as_t(v):
        return (v, [as_t(c) for c in kids[v]])
    pos, E = tree_pos(as_t(root), dx, dy, compact)
    hl = set(hl_path)
    svg = SVG()

    def half(v):
        t = labs[v]
        w = text_width(t, 13) / 2 + 10
        return (w, 13) if shp[v] != "text" else (w, 9)
    for a, b in E:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        on = a in hl and b in hl
        col, wd = (PAL["new"], 2.8) if on else (PAL["ink"], 1.1)
        svg.line(x1, y1 + half(a)[1], x2, y2 - half(b)[1], col, wd)
        mx, my = x1 + (x2 - x1) * 0.45, y1 + (y2 - y1) * 0.5
        left = x2 < x1 - 1
        right = x2 > x1 + 1
        svg.text(mx + (-6 if left else (6 if right else 6)), my, elab[(a, b)], 12,
                 PAL["new"] if on else PAL["muted"],
                 anchor="end" if left else "start", italic=True, bg=True)
    for v, (x, y) in pos.items():
        w, h = half(v)
        on = v in hl
        stroke = PAL["new"] if on else PAL["ink"]
        sw = 2.4 if on else 1.1
        if shp[v] == "box":
            svg.rect(x - w, y - h, 2 * w, 2 * h, "#fff2b3" if on else PAL["white"], stroke, sw, rx=2)
        elif shp[v] == "ellipse":
            svg.ellipse(x, y, w + 4, h + 2, "#fff2b3" if on else PAL["white"],
                        stroke if on else "#3a8ec9", sw)
        svg.text(x, y + 4.5, labs[v], 13, PAL["new"] if (on and shp[v] == "text") else PAL["ink"],
                 bold=on)
    return svg, pos


def leaf(t, shape="ellipse"):
    return (t, shape, [])


SORT3 = ("a : b", "box", [
    ("a > b", ("a : c", "box", [
        ("a > c", ("b : c", "box", [("b > c", leaf("a > b > c")), ("b < c", leaf("a > c > b"))])),
        ("a < c", leaf("c > a > b"))])),
    ("a < b", ("b : c", "box", [
        ("b > c", ("a : c", "box", [("a > c", leaf("b > a > c")), ("a < c", leaf("b > c > a"))])),
        ("b < c", leaf("c > b > a"))]))])

GOLF = ("Ambiente", "box", [
    ("soleado", ("Humedad", "box", [("alta", leaf("N", "box")), ("normal", leaf("P", "box"))])),
    ("nublado", leaf("P", "box")),
    ("lluvioso", ("Viento", "box", [("sí", leaf("N", "box")), ("no", leaf("P", "box"))]))])

CREDITO = ("¿Moroso?", "ellipse", [
    ("sí", leaf("No conceder", "text")),
    ("no", ("Ingresos (€/mes)", "ellipse", [
        ("< 600", leaf("No conceder", "text")),
        ("600-1200", ("¿Trabajo fijo?", "ellipse", [("sí", leaf("Conceder", "text")),
                                                     ("no", leaf("No conceder", "text"))])),
        ("> 1200", leaf("Conceder", "text"))]))])

GOLF_ROWS = [
    ("soleado", "alta", "alta", "no", "N"), ("soleado", "alta", "alta", "sí", "N"),
    ("nublado", "alta", "alta", "no", "P"), ("lluvia", "media", "alta", "no", "P"),
    ("lluvia", "baja", "normal", "no", "P"), ("lluvia", "baja", "normal", "sí", "N"),
    ("nublado", "baja", "normal", "sí", "P"), ("soleado", "media", "alta", "no", "N"),
    ("soleado", "baja", "normal", "no", "P"), ("lluvia", "media", "normal", "no", "P"),
    ("soleado", "media", "normal", "sí", "P"), ("nublado", "media", "alta", "sí", "P"),
    ("nublado", "alta", "normal", "no", "P"), ("lluvia", "media", "alta", "sí", "N")]


def golf_tree_decides(row):
    amb, _, hum, vie, _ = row
    if amb == "soleado":
        return "N" if hum == "alta" else "P"
    if amb == "nublado":
        return "P"
    return "N" if vie == "sí" else "P"


def build():
    p = Page("Unidad4-EstructurasRecursivas/Arboles")

    # ¿Es un árbol? (introducción)
    intro = [
        [("a", "c"), ("b", "c"), ("c", "d"), ("c", "f"), ("e", "f")],
        [("a", "b"), ("b", "d"), ("a", "c"), ("c", "d"), ("c", "e"), ("c", "f")],
        [("a", "c"), ("a", "f"), ("b", "e"), ("d", "f"), ("e", "f")],
    ]
    p.put("fig-intro", graph_row(p, "intro", [(GRID, intro[0], "1", {}), (GRID, intro[1], "2", {}),
                                              (GRID, intro[2], "3", {})]))
    cyc = {("a", "b"): "new", ("b", "d"): "new", ("c", "d"): "new", ("a", "c"): "new"}
    p.put("fig-intro-sol", graph_row(p, "intro-sol", [(GRID, intro[1], "", cyc)]))

    # Árbol con raíz: el mismo árbol con raíces c, a y e
    Tg = intro[0]
    tabs = []
    svg = SVG()
    draw_graph(svg, GRID, Tg)
    tabs.append(f"![Árbol]({p.img('raiz-0', svg)})\n\n> Un árbol: conexo y sin circuitos.")
    for i, r in enumerate(["c", "a", "e"], 1):
        svg, pos, _ = tsvg(rooted(Tg, r), 50, 58, node_style={r: "hl"})
        gcap(svg, pos, f"Árbol con raíz en {r}")
        tabs.append(f"![Árbol con raíz en {r}]({p.img(f'raiz-{i}', svg)})\n\n"
                    f"> Se escoge ${r}$ como raíz: se toma ${r}$ y se dejan colgar los demás "
                    f"vértices, cada uno debajo del vértice por el que se llega a él desde ${r}$.")
    p.put("raiz-steps", steps("El mismo árbol con raíces distintas", tabs, dropdown=False))

    # Estructura recursiva: e con subárboles a1 ... an
    svg = SVG()
    svg.circle(0, 0, 15, PAL["white"], PAL["ink"], 1.3)
    svg.text(0, 5, "e", 14)
    for x, lab in ((-110, "a₁"), (0, "aᵢ"), (110, "aₙ")):
        svg.line(0, 15, x, 78, PAL["ink"], 1.2)
        svg.polygon([(x, 78), (x - 30, 140), (x + 30, 140)], PAL["white"], PAL["ink"], 1.2)
        svg.text(x, 128, lab, 15)
    for x in (-55, 55):
        svg.text(x, 118, "...", 16)
    p.put("fig-recursivo", f"![Un elemento con sus subárboles]({p.img('recursivo', svg)})")

    # Terminología, paso a paso sobre T0
    pos, E = tree_pos(T0, 42, 58)
    par, ch, dep = info(T0)
    leaves = [v for v in pos if not ch[v]]
    internal = [v for v in pos if ch[v]]

    def tstep(name, ns=None, es=None, labels=None, extra=None):
        svg = SVG()
        draw_graph(svg, pos, E, node_style=ns or {}, edge_style=es or {}, labels=labels or {},
                   label_style={v: "new" for v in (labels or {})})
        if extra:
            extra(svg)
        return p.img(name, svg)
    tabs = []
    tabs.append(f"![Raíz]({tstep('term-0', {'a': 'hl'})})\n\n> $a$ es la **raíz** del árbol: el "
                f"nodo inicial, el único sin padre.")
    tabs.append(f"![Hojas]({tstep('term-1', {v: 'hl' for v in leaves})})\n\n> "
                f"{mlist(leaves)} son las **hojas** del árbol: no tienen hijos.")
    tabs.append(f"![Nodos internos]({tstep('term-2', {v: 'hl' for v in internal})})\n\n> "
                f"{mlist(internal)} son los **nodos internos**: tienen al menos un hijo.")
    r1, r2 = ["a", "b", "f"], ["a", "d", "k", "o", "s"]
    es = {(x, y): "new" for r in (r1, r2) for x, y in zip(r, r[1:])}
    tabs.append(f"![Ramas]({tstep('term-3', {v: 'hl' for v in r1 + r2}, es)})\n\n> Un camino "
                f"desde la raíz hasta una hoja es una **rama**: $a \\to b \\to f$ y "
                f"$a \\to d \\to k \\to o \\to s$ son dos de las ${len(leaves)}$ ramas.")
    tabs.append(f"![Padre e hijos]({tstep('term-4', {'a': 'hl', 'b': 'hl', 'c': 'new', 'd': 'new', 'e': 'new', 'f': 'new'}, {('a', 'b'): 'new', ('a', 'c'): 'new', ('a', 'd'): 'new', ('a', 'e'): 'new', ('b', 'f'): 'new'})})\n\n"
                f"> $a$ es el **padre** de $b, c, d, e$, y $b$ es el padre de $f$. $b, c, d, e$ son "
                f"los **hijos** de $a$ (sus descendientes directos); $f$ es el hijo de $b$.")

    def levels(svg):
        x0 = min(x for x, _ in pos.values()) - 30
        for d in range(max(dep.values()) + 1):
            svg.text(x0, d * 58 + 5, f"Profundidad {d}", 12, PAL["teal"], anchor="end")
    tabs.append(f"![Profundidad]({tstep('term-5', extra=levels)})\n\n> La **profundidad** de un nodo "
                f"es la longitud del camino desde la raíz: $a$ tiene profundidad $0$; $b, c, d, e$, "
                f"profundidad $1$; $o$, profundidad $3$; $r$ y $s$, profundidad $4$.")
    ar = {v: str(len(ch[v])) for v in pos}
    tabs.append(f"![Aridad]({tstep('term-6', labels=ar)})\n\n> Cada nodo tiene una **aridad** u "
                f"**orden**: la cantidad de hijos. La de $a$ es $4$, la de $d$ es $3$, la de $g$ es "
                f"$1$ y la de cualquier hoja es $0$.")
    p.put("term-steps", steps("Terminología sobre un árbol", tabs, dropdown=False))
    put_info(p, "t0", T0)

    # Pregunta de terminología (T1) y ejercicios (T2, T3)
    for key, t in (("t1", T1), ("t2", T2), ("t3", T3)):
        p.put(f"fig-{key}", tfig(p, f"term-{key}", t, dx=40))
        put_info(p, key, t)

    # Aridad y n-arios
    bin_c = ("·", [("·", [("·", [L, L]), ("·", [L, L])]), ("·", [L, ("·", [L, L])])])
    tri = ("·", [("·", [L, L, L]), ("·", [("·", [L])]), ("·", [L, L])])
    p.put("fig-aridad", ufig_row(p, "aridad", [bin_c, tri], ["", ""]))
    n1a = ("·", [("·", [("·", [L, L]), L]), L])
    n1b = ("·", [("·", [("·", [L, L]), L, L]), L, ("·", [L, L])])
    p.put("fig-nar-1", ufig_row(p, "nar-1", [n1a, n1b], ["a)", "b)"]))
    p.put("fig-nar-1-sol", ufig_row(p, "nar-1-sol", [n1a, n1b],
                                    ["Árbol binario completo", "Árbol 3-ario"]))
    n2a = ("·", [("·", [L, L]), ("·", [("·", [L, L])])])
    n2b = ("·", [("·", [("·", [L, L, L]), L, L]), ("·", [L, L, L]), L])
    n3a = ("·", [("·", [L] * 5), L, L, L, ("·", [L] * 5)])
    n3b = ("·", [("·", [L, ("·", [L, L]), L]), ("·", [L, L, L, L])])
    p.put("fig-nar-2", ufig_row(p, "nar-2", [n2a, n2b], ["a)", "b)"]))
    p.put("fig-nar-3", ufig_row(p, "nar-3", [n3a, n3b], ["c)", "d)"], dx=20))

    # Subárboles de T1
    pos1, E1 = tree_pos(T1, 40, 56)

    def desc(t, v):
        lab, chs = t
        if lab == v:
            return preorder(t)
        for c in chs:
            r = desc(c, v)
            if r:
                return r
        return []
    tabs = []
    svg = SVG()
    draw_graph(svg, pos1, E1)
    gcap(svg, pos1, "Árbol T")
    tabs.append(f"![Árbol T]({p.img('sub-0', svg)})\n\n> El árbol $T$.")
    for i, v in enumerate(["c", "d", "b"], 1):
        sub = set(desc(T1, v))
        svg = SVG()
        draw_graph(svg, pos1, E1, node_style={x: ("hl" if x == v else "tree") for x in sub},
                   edge_style={(x, y): "tree" for x, y in E1 if x in sub})
        gcap(svg, pos1, f"Subárbol de T con raíz en {v}")
        extra = (" Es un subárbol de un solo nivel: $d$ y sus dos hojas." if v == "d" else "")
        tabs.append(f"![Subárbol con raíz en {v}]({p.img(f'sub-{i}', svg)})\n\n> El subárbol con "
                    f"raíz en ${v}$ tiene a ${v}$ y a todos sus descendientes: "
                    f"{mlist(desc(T1, v))}.{extra}")
    p.put("sub-steps", steps("Subárboles de T", tabs, dropdown=False))

    def subt(t, v):
        if t[0] == v:
            return t
        for c in t[1]:
            r = subt(c, v)
            if r:
                return r
    parts = []
    for v in ("e", "g"):
        pos, E = tree_pos(subt(T1, v), 40, 56)
        svg = SVG()
        draw_graph(svg, pos, E, node_style={v: "hl"})
        parts.append(svg)
    caps = [f"Subárbol con raíz en {v}" for v in ("e", "g")]
    p.put("fig-ex6", f"![Subárboles con raíz en e y en g]({p.img('ex6', tile(parts, 110, caps=caps))})")

    # Árboles de decisión
    svg, _ = draw_dtree(SORT3, compact=True)
    p.put("fig-decision", f"![Árbol de decisión para ordenar tres elementos]({p.img('decision', svg)})")
    # a = 1, b = 7, c = 5: a < b, b > c, a < c
    path_ids = ["n1", "n7", "n8", "n10"]
    texts = ["Se compara $a$ con $b$: $1 < 7$, se baja por la rama $a < b$.",
             "Se compara $b$ con $c$: $7 > 5$, se baja por la rama $b > c$.",
             "Se compara $a$ con $c$: $1 < 5$, se baja por la rama $a < c$.",
             "Se llega a la hoja $b > c > a$: el orden es $a, c, b$ $(1, 5, 7)$. Hicieron falta "
             "$3$ comparaciones."]
    tabs = []
    for i in range(len(path_ids)):
        svg, _ = draw_dtree(SORT3, hl_path=path_ids[:i + 1], compact=True)
        tabs.append(f"![Decisión, paso {i + 1}]({p.img(f'decision-{i}', svg)})\n\n> {texts[i]}")
    p.put("decision-steps", steps("a = 1, b = 7, c = 5", tabs))
    rows = [list(r) for r in GOLF_ROWS]
    assert all(golf_tree_decides(r) == r[4] for r in GOLF_ROWS)
    p.put("golf-tabla", md_table(["Ambiente", "Temp.", "Humedad", "Viento", "Clase"], rows))
    svg, _ = draw_dtree(GOLF, dx=92, dy=84)
    p.put("fig-golf", f"![Árbol de decisión para jugar golf]({p.img('golf', svg)})")
    svg, _ = draw_dtree(CREDITO, dx=105, dy=86)
    p.put("fig-credito", f"![Árbol de decisión para aprobar un crédito]({p.img('credito', svg)})")

    # Ejercicios: ¿es árbol?
    s1 = [[("a", "b"), ("a", "c"), ("a", "d"), ("b", "e"), ("c", "f"), ("d", "e")],
          [("a", "d"), ("b", "c"), ("c", "d"), ("c", "f"), ("d", "e")],
          [("a", "f"), ("b", "e"), ("b", "d"), ("c", "e")]]
    p.put("fig-ex1", graph_row(p, "ex1", [(GRID, E, c, {}) for E, c in zip(s1, ["a)", "b)", "c)"])]))
    p.put("fig-ex1-b", tfig(p, "ex1-b", rooted(s1[1], "c"), dx=46, node_style={"c": "hl"}))
    g1 = scale({"a": (1.5, 0), "f": (0, 1.3), "d": (1.0, 1.3), "b": (1.7, 1.3), "c": (2.5, 1.3),
                "e": (0, 2.2)}, 62)
    g1e = [("a", "f"), ("a", "d"), ("a", "b"), ("a", "c"), ("f", "e"), ("e", "d")]
    g2 = scale({"a": (0.6, 0), "d": (0.6, 0.9), "c": (0.2, 1.6), "e": (1.2, 1.6), "b": (-0.3, 2.4),
                "f": (0.8, 2.4)}, 62)
    g2e = [("a", "d"), ("d", "c"), ("d", "e"), ("c", "b"), ("c", "f"), ("b", "f")]
    g3t = ("a", [("b", [("d", [])]), ("c", [("e", [("g", [])]), ("f", [("h", []), ("i", [])])])])
    g3, g3e = tree_pos(g3t, 40, 52)
    p.put("fig-ex2", graph_row(p, "ex2", [(g1, g1e, "a)", {}), (g2, g2e, "b)", {}),
                                          (g3, g3e, "c)", {})]))

    p.assemble("index.md")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
