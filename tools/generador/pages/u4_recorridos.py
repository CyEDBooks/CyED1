from common import *
from tviz import from_tuple, draw

# Árboles de Bedoya. Un hijo puede ser None para dejar el hueco del lado vacío:
# ("h", [None, ("j", [])]) es h con un único hijo j a la derecha.
TA = ("e", [("f", [("a", []), ("d", [("c", []), ("g", [])])]), ("b", [("h", []), ("i", [])])])
TB = ("c", [("b", [("e", [("i", []), ("a", [])]), ("h", [None, ("j", [])])]),
            ("g", [("f", []), ("d", [("k", []), ("m", [])])])])
TC = ("a", [("b", [("d", [("h", []), ("i", [])]), ("e", [("j", []), ("k", [("n", []), ("o", [])])])]),
            ("c", [("f", []), ("g", [("l", [("p", []), ("q", [])]), ("m", [("r", []), ("s", [])])])])])
TD = ("e", [("c", [("h", [("k", []), ("m", [("p", []), ("q", [])])]),
                   ("i", [("n", [("r", []), ("o", [])]), None])]),
            ("d", [("f", []), ("g", [("j", [("a", []), ("b", [])]), None])])])
TE = ("a", [("b", [("e", []), ("f", []), ("g", [])]), ("c", []), ("d", [("h", []), ("i", []), ("j", [])])])
TF = ("a", [("b", [("e", [("j", []), ("k", [("n", []), ("o", []), ("p", [])])]), ("f", [])]), ("c", []),
            ("d", [("g", [("l", []), ("m", [])]), ("h", []), ("i", [])])])
T_OPEN = ("a", [("b", [("e", [("k", []), ("m", [("r", []), ("s", []), ("t", [])])]), ("f", []),
                       ("g", [("n", []), ("o", [])])]),
                ("c", []),
                ("d", [("h", [("p", []), ("q", [("u", []), ("v", []), ("w", [])])]), ("i", []), ("j", [])])])
# Árbol n-ario de las diapositivas de Aristizábal
T_AND = ("a", [("b", []), ("c", [("e", []), ("f", [])]),
               ("d", [("g", [("j", []), ("k", []), ("l", []), ("m", [])]), ("h", []), ("i", [])])])
T_SOLO = ("d", [("b", [("a", []), ("c", [])]), ("h", [None, ("j", [])])])

# Árbol binario de Vargas
VV = (10, (15, (25, (7, None, None), (6, None, None)), None), (-6, None, (18, None, None)))

EXPR = ("+", ("↑", ("+ ", ("x", None, None), ("y", None, None)), ("2", None, None)),
        ("/", ("−", ("x ", None, None), ("4", None, None)), ("3", None, None)))
OCHO = ("+", ("↑", ("−", ("8", None, None), ("6", None, None)), ("3", None, None)),
        ("/", ("10", None, None), ("− ", ("7", None, None), ("2", None, None))))
EX4 = [("/", ("+", ("x", None, None), ("5", None, None)), ("−", ("x ", None, None), ("3", None, None))),
       ("*", ("+", ("x", None, None), ("/", ("y", None, None), ("z", None, None))), ("3", None, None)),
       ("+", ("x", None, None), ("/", ("y", None, None), ("+ ", ("x ", None, None), ("3", None, None))))]
EX4_TXT = ["(x+5)/(x-3)", "(x+(y/z))*3", "x+(y/(x+3))"]


def kids(t):
    return [c for c in t[1] if c is not None]


def gorder(t, kind):
    """Recorrido de un árbol (n-ario, o binario con huecos None)."""
    if t is None:
        return []
    lab, ch = t
    if kind == "pre":
        return [lab] + [x for c in ch for x in gorder(c, kind)]
    if kind == "post":
        return [x for c in ch for x in gorder(c, kind)] + [lab]
    if not ch:
        return [lab]
    return gorder(ch[0], kind) + [lab] + [x for c in ch[1:] for x in gorder(c, kind)]


def levels(t):
    out, q = [], [t]
    while q:
        n = q.pop(0)
        out.append(n[0])
        q += kids(n)
    return out


def gpos(t, dx=40, dy=56):
    """Posiciones dejando el hueco de los hijos None."""
    k = [0]

    def fill(n):
        if n is None:
            k[0] += 1
            return (f"_hueco{k[0]}", [])
        return (n[0], [fill(c) for c in n[1]])
    pos, E = tree_pos(fill(t), dx, dy)
    pos = {v: xy for v, xy in pos.items() if not v.startswith("_hueco")}
    E = [(a, b) for a, b in E if not b.startswith("_hueco")]
    return pos, E


def seq(xs):
    return " – ".join(str(x).strip() for x in xs)


NAMES = {"pre": "preorden", "in": "inorden", "post": "postorden"}
PASOS = {"pre": ("r", "T₁", "T₂"), "in": ("T₁", "r", "T₂"), "post": ("T₁", "T₂", "r")}


def subtree_nodes(t):
    return [t[0]] + [x for c in kids(t) for x in subtree_nodes(c)]


def traversal_steps(p, prefix, t, kind, why=None):
    pos, E = gpos(t, 46, 62)
    order = gorder(t, kind)
    tabs = []
    # Paso 0: la regla, con T1 y T2 encerrados
    svg = SVG()
    draw_graph(svg, pos, E, node_style={t[0]: "hl"})
    t1, t2 = kids(t)
    for sub, nm in ((t1, "T₁"), (t2, "T₂")):
        xs = [pos[v][0] for v in subtree_nodes(sub)]
        ys = [pos[v][1] for v in subtree_nodes(sub)]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        rx, ry = (max(xs) - min(xs)) / 2 + 26, (max(ys) - min(ys)) / 2 + 24
        svg.ellipse(cx, cy, rx, ry, "none", PAL["new"], 1.2, "5,4")
        svg.text(cx + rx * 0.75, cy - ry - 2, nm, 15, PAL["new"])
    x0 = max(x for x, _ in pos.values()) + 60
    for i, nm in enumerate(PASOS[kind]):
        svg.text(x0, 20 + 26 * i, f"Paso {i + 1}: {nm if nm != 'r' else 'visitar r'}", 14,
                 PAL["ink"], anchor="start")
    rule = {"pre": "la raíz, luego $T_1$ completo en preorden y luego $T_2$ en preorden",
            "in": "$T_1$ completo en inorden, luego la raíz y luego $T_2$ en inorden",
            "post": "$T_1$ completo en postorden, luego $T_2$ en postorden y al final la raíz"}[kind]
    tabs.append(f"![Recorrido en {NAMES[kind]}: la regla]({p.img(f'{prefix}-regla', svg)})\n\n"
                f"> La raíz es ${t[0]}$, con subárboles $T_1$ (raíz ${t1[0]}$) y $T_2$ (raíz ${t2[0]}$). "
                f"En {NAMES[kind]} se recorre {rule}. Dentro de cada subárbol se aplica la **misma** "
                f"regla.")
    for k in range(len(order)):
        visited = order[:k + 1]
        ns = {v: "tree" for v in visited}
        ns[order[k]] = "new"
        labels = {v: str(i + 1) for i, v in enumerate(visited)}
        svg = SVG()
        draw_graph(svg, pos, E, node_style=ns, labels=labels,
                   label_style={v: ("new" if v == order[k] else "dim") for v in visited})
        ys = max(y for _, y in pos.values()) + 50
        x0 = min(x for x, _ in pos.values()) - 10
        draw_panel(svg, x0, ys, f"Recorrido en {NAMES[kind]}:", visited, new=[k])
        txt = f"\n\n> {why[k]}" if why and k in why else ""
        tabs.append(f"![{NAMES[kind]}, paso {k + 1}]({p.img(f'{prefix}-{k:02d}', svg)}){txt}")
    return steps(f"Recorrido en {NAMES[kind]}", tabs), seq(order)


def tree_row(p, name, trees, caps, dx=38, gap=80):
    svg = SVG()
    x0 = 0
    for t, cap in zip(trees, caps):
        pos, E = gpos(t, dx, 54)
        minx = min(x for x, _ in pos.values())
        pos = {v: (x - minx + x0, y) for v, (x, y) in pos.items()}
        draw_graph(svg, pos, E)
        xs = [x for x, _ in pos.values()]
        svg.text((min(xs) + max(xs)) / 2, max(y for _, y in pos.values()) + 36, cap, 14)
        x0 = max(xs) + gap
    return f"![{', '.join(caps)}]({p.img(name, svg)})"


def border(n, kind):
    if n is None:
        return []
    l, r = border(n.left, kind), border(n.right, kind)
    return {"pre": [n] + l + r, "in": l + [n] + r, "post": l + r + [n]}[kind]


OPS = "+−*/↑"


def apply(op, a, b):
    v = {"+": a + b, "−": a - b, "*": a * b, "/": a / b, "↑": a ** b}[op]
    return int(v) if v == int(v) else v


def reduce_prefix(tokens):
    """Regla de las diapositivas: el operador más a la derecha seguido de dos números."""
    toks = list(tokens)
    lines = [" ".join(toks)]
    while len(toks) > 1:
        for i in range(len(toks) - 3, -1, -1):
            if toks[i] in OPS and toks[i + 1] not in OPS and toks[i + 2] not in OPS:
                toks[i:i + 3] = [str(apply(toks[i], int(toks[i + 1]), int(toks[i + 2])))]
                break
        lines.append(" ".join(toks))
    return lines


def reduce_postfix(tokens):
    """El operador más a la izquierda precedido de dos números."""
    toks = list(tokens)
    lines = [" ".join(toks)]
    while len(toks) > 1:
        for i in range(2, len(toks)):
            if toks[i] in OPS and toks[i - 1] not in OPS and toks[i - 2] not in OPS:
                toks[i - 2:i + 1] = [str(apply(toks[i], int(toks[i - 2]), int(toks[i - 1])))]
                break
        lines.append(" ".join(toks))
    return lines


def reduction_tabs(lines, first_note):
    tabs = []
    for k in range(len(lines)):
        body = "\n".join((f"- **`{l}`** ←" if i == k else f"- `{l}`")
                         for i, l in enumerate(lines[:k + 1]))
        tabs.append(body)
    tabs[0] += f"\n\n> {first_note}"
    tabs[-1] += f"\n\n> Queda un solo número: el valor es **{lines[-1]}**."
    return tabs


# Resultados que dan las diapositivas de Bedoya, para verificar los árboles.
BEDOYA = {
    ("TA", "pre"): "efadcgbhi", ("TA", "in"): "afcdgehbi", ("TA", "post"): "acgdfhibe",
    ("TB", "pre"): "cbeiahjgfdkm", ("TB", "in"): "ieabhjcfgkdm", ("TB", "post"): "iaejhbfkmdgc",
    ("TC", "pre"): "abdhiejknocfglpqmrs", ("TC", "in"): "hdibjenkoafcplqgrms",
    ("TC", "post"): "hidjnokebfpqlrsmgca",
    ("TD", "pre"): "echkmpqinrodfgjab", ("TD", "in"): "khpmqcrnoiefdajbg",
    ("TD", "post"): "kpqmhronicfabjgde",
    ("TE", "pre"): "abefgcdhij", ("TE", "in"): "ebfgachdij", ("TE", "post"): "efgbchijda",
    ("TF", "pre"): "abejknopfcdglmhi", ("TF", "in"): "jenkopbfaclgmdhi",
    ("TF", "post"): "jnopkefbclmghida",
}


def build():
    for (name, kind), want in BEDOYA.items():
        got = "".join(gorder(globals()[name], kind))
        assert got == want, (name, kind, got, want)
    p = Page("Unidad4-EstructurasRecursivas/RecorridosArboles")
    mini = from_tuple(("a", ("b", None, None), ("c", None, None)))
    p.put("fig-mini", f"![Árbol de tres nodos]({p.img('mini', draw(mini))})")

    st, s = traversal_steps(p, "pre", TA, "pre",
                            why={1: "Después de $e$ se recorre **todo** $T_1$ en preorden: su raíz "
                                    "$f$ primero.",
                                 5: "Terminó $T_1$. Ahora se recorre $T_2$, que empieza en su raíz "
                                    "$b$."})
    p.put("pre", st)
    p.put("pre-seq", s)
    st, s = traversal_steps(p, "in", TA, "in",
                            why={0: "$a$ es el primero: se baja por el primer subárbol hasta donde se "
                                    "pueda antes de visitar cualquier raíz.",
                                 5: "Se visita $e$ solo cuando ya se recorrió todo $T_1$."})
    p.put("in", st)
    p.put("in-seq", s)
    st, s = traversal_steps(p, "post", TA, "post",
                            why={4: "$f$ va después de todo su subárbol: $a$, y luego $c, g, d$.",
                                 8: "La raíz $e$ es siempre la **última** en postorden."})
    p.put("post", st)
    p.put("post-seq", s)
    p.put("niveles", seq(levels(TA)))

    pos, E = gpos(T_SOLO, 46, 60)
    svg = SVG()
    draw_graph(svg, pos, E)
    p.put("fig-solo", f"![h con un solo hijo a la derecha]({p.img('solo', svg)})")
    p.put("solo-in", seq(gorder(T_SOLO, "in")))

    pos, E = gpos(T_AND, 46, 60)
    p.put("fig-nar", gfig(p, "nario", pos, E))
    for k in ("pre", "in", "post"):
        p.put(f"nar-{k}", seq(gorder(T_AND, k)))

    # Expresión: construcción de abajo hacia arriba, como en las diapositivas
    from tviz import N
    parts = [
        (("+ ", ("x", None, None), ("y", None, None)), "Se empieza por los paréntesis de adentro: $x+y$."),
        (("↑", ("+ ", ("x", None, None), ("y", None, None)), ("2", None, None)),
         "$(x+y)↑2$: el árbol de $x+y$ es el operando izquierdo de $↑$."),
        (("−", ("x ", None, None), ("4", None, None)), "Por el otro lado, $x-4$."),
        (("/", ("−", ("x ", None, None), ("4", None, None)), ("3", None, None)),
         "$(x-4)/3$: el árbol de $x-4$ es el operando izquierdo de $/$."),
        (EXPR, "El $+$ del centro se evalúa **último**: es la raíz, con los dos árboles como "
               "subárboles."),
    ]
    tabs = []
    for d, (t, txt) in enumerate(parts):
        tr = from_tuple(t)
        tabs.append(f"![Árbol de expresión, paso {d + 1}]({p.img(f'expr-{d:02d}', draw(tr, node_style={tr.key: 'new'}, font=17))})\n\n> {txt}")
    p.put("expr-steps", steps("Árbol de ((x+y)↑2)+((x−4)/3)", tabs))
    ex = from_tuple(EXPR)
    p.put("expr-pre", " ".join(n.key.strip() for n in border(ex, "pre")))
    p.put("expr-post", " ".join(n.key.strip() for n in border(ex, "post")))

    ocho = from_tuple(OCHO)
    p.put("fig-ocho", f"![Árbol de expresión]({p.img('ocho', draw(ocho, font=17))})")
    pre8 = [n.key.strip() for n in border(ocho, "pre")]
    post8 = [n.key.strip() for n in border(ocho, "post")]
    p.put("ocho-pre", " ".join(pre8))
    p.put("ocho-post", " ".join(post8))
    lines = reduce_prefix(pre8)
    assert lines[-1] == "10"
    p.put("pre-eval", steps("Evaluar " + " ".join(pre8),
                            reduction_tabs(lines, "El operador más a la derecha seguido de dos "
                                                  "números es `− 7 2`: se reemplaza por $5$.")))
    lines = reduce_postfix(post8)
    assert lines[-1] == "10"
    p.put("post-eval", steps("Evaluar " + " ".join(post8),
                             reduction_tabs(lines, "El operador más a la izquierda precedido de "
                                                   "dos números es `8 6 −`: se reemplaza por $2$.")))
    p.assemble("index.md")

    # Ejercicios
    p.put("fig-ex1", tree_row(p, "ex1", [TB, TD, TC], ["a)", "b)", "c)"], dx=34))
    for key, t in (("ex1a", TB), ("ex1b", TD), ("ex1c", TC), ("ex2a", TE), ("ex2b", TF)):
        for k in ("pre", "in", "post"):
            p.put(f"{key}-{k}", seq(gorder(t, k)))
    p.put("fig-ex2", tree_row(p, "ex2", [TE, TF], ["a)", "b)"], dx=36))
    vv = from_tuple(VV)
    p.put("fig-ex3", f"![Árbol binario]({p.img('ex3', draw(vv))})")
    for k in ("pre", "in", "post"):
        p.put(f"ex3-{k}", seq(n.key for n in border(vv, k)))
    lv, q = [], [vv]
    while q:
        n = q.pop(0)
        lv.append(n.key)
        q += [c for c in (n.left, n.right) if c]
    p.put("ex3-niv", seq(lv))

    svg = SVG()
    x0 = 0
    rows = []
    for t, cap, txt in zip(EX4, ["a)", "b)", "c)"], EX4_TXT):
        r = from_tuple(t)
        sub = draw(r, font=17)
        # se copia el dibujo desplazado
        for it in sub.items:
            svg.items.append(f'<g transform="translate({x0 - sub.minx:.1f},0)">{it}</g>')
        svg._box(x0, sub.miny, x0 + sub.maxx - sub.minx, sub.maxy)
        svg.text(x0 + (sub.maxx - sub.minx) / 2, sub.maxy + 26, cap, 14)
        x0 += sub.maxx - sub.minx + 60
        pre = " ".join(n.key.strip() for n in border(r, "pre"))
        post = " ".join(n.key.strip() for n in border(r, "post"))
        rows.append(f"| ${txt}$ | `{pre}` | `{post}` |")
    p.put("fig-ex4", f"![Árboles de las tres expresiones]({p.img('ex4', svg)})")
    p.put("ex5-rows", "\n".join(rows))
    for key, expr, fn in (("ex6a", "+ − * 2 3 5 / ↑ 2 3 4", reduce_prefix),
                          ("ex6b", "/ − + + 4 3 13 5 − ↑ − 6 4 3 3", reduce_prefix),
                          ("ex7a", "7 2 3 * − 4 ↑ 9 3 / +", reduce_postfix),
                          ("ex7b", "2 3 ↑ 3 1 + / 4 ↑ 1 4 + 2 ↑ 5 / +", reduce_postfix)):
        lines = fn(expr.split())
        p.put(f"{key}-lines", "\n".join(f"- `{l}`" for l in lines))
        p.put(f"{key}-res", lines[-1])
    pos, E = gpos(T_OPEN, 36, 54)
    p.put("fig-ex9", gfig(p, "ex9", pos, E))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
