from common import *
from tviz import from_tuple, draw, halo, ring, badge, parent_map, nodes, layout

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
    parts = []
    for t in trees:
        pos, E = gpos(t, dx, 54)
        svg = SVG()
        draw_graph(svg, pos, E)
        parts.append(svg)
    return f"![{', '.join(caps)}]({p.img(name, tile(parts, gap, caps=caps))})"


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


# Cinco ejemplos por recorrido, de muy fácil a difícil. B(k, izq, der); "·" no se usa:
# un hijo ausente es None. Las letras no siguen el orden alfabético para que el dibujo no
# delate el resultado.
def B(k, l=None, r=None):
    return (k, l, r)


EJ = {
    "pre": [B("k", B("m"), B("d")),
            B("f", B("c", B("a"), B("g")), B("e")),
            B("d", B("h", B("b")), B("k", B("e"), B("a", B("m")))),
            B("g", B("c", B("f", None, B("j")), B("b")), B("m", B("h", B("l"), B("n")))),
            B("p", B("e", B("k", B("a")), B("r", B("n", B("c"), B("s")))),
              B("b", B("t", None, B("h", B("f"))), B("q", None, B("m"))))],
    "in": [B("n", B("r"), B("g")),
           B("e", B("b", B("d"), B("h")), B("c")),
           B("k", B("d", None, B("f")), B("p", B("j", B("a")), B("s"))),
           B("h", B("c", B("e", None, B("b")), B("g", B("n"))), B("r", None, B("l", B("t")))),
           B("a", B("q", B("f", None, B("m", B("k"))), B("z", B("e"))),
             B("d", B("n", None, B("w")), B("j", B("h", None, B("c")), B("y"))))],
    "post": [B("c", B("f"), B("h")),
             B("m", B("a", B("k"), B("d")), B("p")),
             B("b", B("g", None, B("e", B("c"))), B("n", B("f"), B("h"))),
             B("t", B("j", B("a", B("d")), B("k")), B("r", None, B("w", B("e"), B("q")))),
             B("h", B("c", B("m", None, B("b", B("s"))), B("g", B("f"))),
               B("r", B("e", None, B("x")), B("a", B("p", B("k")), B("v"))))],
}
REGLA = {"pre": "raíz, subárbol izquierdo, subárbol derecho",
         "in": "subárbol izquierdo, raíz, subárbol derecho",
         "post": "subárbol izquierdo, subárbol derecho, raíz"}


def _lst(ns):
    return ", ".join(f"${n.key}$" for n in ns)


def _why(kind, x, k, order, par):
    """Por qué x es el nodo número k + 1 del recorrido."""
    pa = par[x.key]
    if kind == "pre":
        if pa is None:
            return f"Se empieza por la raíz ${x.key}$: en preorden la raíz va **primero**."
        if pa.left is x:
            return (f"${x.key}$ es la raíz del subárbol **izquierdo** de ${pa.key}$: se visita "
                    f"apenas se entra a ese subárbol, antes que sus hijos.")
        prev = (f"se terminó el subárbol izquierdo de ${pa.key}$" if pa.left is not None
                else f"${pa.key}$ no tiene subárbol izquierdo")
        return (f"Como {prev}, sigue el **derecho**, que empieza por su raíz ${x.key}$.")
    if kind == "in":
        if x.left is not None:
            return (f"Todo el subárbol izquierdo de ${x.key}$ ({_lst(border(x.left, 'in'))}) ya se "
                    f"recorrió: ahora toca ${x.key}$.")
        if k == 0:
            chain = []
            y = x
            while y is not None:
                chain.append(y.key)
                y = par[y.key]
            return (f"Se baja siempre por la izquierda desde la raíz: "
                    f"{' → '.join(f'${c}$' for c in reversed(chain))}. ${x.key}$ no tiene subárbol "
                    f"izquierdo: es el **primero**.")
        return f"${x.key}$ no tiene subárbol izquierdo: se visita de inmediato."
    if x.left is None and x.right is None:
        if k == 0:
            chain = []
            y = x
            while y is not None:
                chain.append(y.key)
                y = par[y.key]
            return (f"Se baja por los subárboles izquierdos hasta la primera hoja: "
                    f"{' → '.join(f'${c}$' for c in reversed(chain))}. Las hojas no tienen nada "
                    f"pendiente debajo: ${x.key}$ va **primero**.")
        return f"${x.key}$ es hoja: no tiene subárboles pendientes, se visita."
    parts = []
    if x.left is not None:
        parts.append(f"el izquierdo ({_lst(border(x.left, 'post'))})")
    if x.right is not None:
        parts.append(f"el derecho ({_lst(border(x.right, 'post'))})")
    tail = " Es la raíz: va de **última**." if par[x.key] is None else ""
    return f"Ya se recorrieron sus subárboles, {' y '.join(parts)}: ahora sí ${x.key}$.{tail}"


def ejemplo_recorrido(p, prefix, t, kind):
    root = from_tuple(t)
    order = border(root, kind)
    par = parent_map(root)
    nm = NAMES[kind].capitalize()

    def panel(svg, pos, k):
        ys = max(y for _, y in pos.values()) + 64
        x0 = min(x for x, _ in pos.values()) - 10
        draw_panel(svg, x0, ys, f"{nm}:", [n.key for n in order[:k + 1]], new=[k], cell=30, wrap=12)

    head = f"![Árbol del ejemplo]({p.img(f'{prefix}-00', draw(root, dx=46))})"
    tabs = []
    for k, x in enumerate(order):
        done = order[:k + 1]

        def under(svg, pos, x=x):
            if kind == "pre":
                halo(svg, pos, x, "red", f"subárbol de {x.key}")
            elif kind == "in":
                halo(svg, pos, x.left, "blue", "izq. ✓")
            else:
                halo(svg, pos, x.left, "blue", "izq. ✓")
                halo(svg, pos, x.right, "orange", "der. ✓")

        def over(svg, pos, k=k, x=x, done=done):
            ring(svg, *pos[x.key])
            for i, n in enumerate(done):
                badge(svg, *pos[n.key], i + 1, PAL["new"] if i == k else PAL["teal"],
                      r=19 if i == k else 15)
            panel(svg, pos, k)
        ns = {n.key: "tree" for n in done}
        ns[x.key] = "new"
        svg = draw(root, node_style=ns, dx=46, under=under, over=over)
        txt = _why(kind, x, k, order, par)
        if k == len(order) - 1:
            txt += f"\n\n> **{nm}:** {seq(n.key for n in order)}."
        tabs.append(f"![{NAMES[kind]}, paso {k + 1}]({p.img(f'{prefix}-{k + 1:02d}', svg)})\n\n> {txt}")
    return head, tabs, [n.key for n in order]


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
    for kind in ("pre", "in", "post"):
        for i, t in enumerate(EJ[kind]):
            head, tabs, order = ejemplo_recorrido(p, f"ej{kind}{i + 1}", t, kind)
            # verificación independiente con el recorrido de los árboles n-arios
            def as_gen(t):
                return None if t is None else (t[0], [as_gen(t[1]), as_gen(t[2])]
                                               if (t[1] or t[2]) else [])
            assert order == gorder(as_gen(t), kind), (kind, i)
            p.put(f"ej-{kind}-{i + 1}",
                  f"**Ejemplo {i + 1}.** Recorra el árbol en {NAMES[kind]} "
                  f"({REGLA[kind]}).\n\n{head}\n\n" + steps("Paso a paso", tabs))
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

    parts = []
    rows = []
    for t, txt in zip(EX4, EX4_TXT):
        r = from_tuple(t)
        parts.append(draw(r, font=17))
        pre = " ".join(n.key.strip() for n in border(r, "pre"))
        post = " ".join(n.key.strip() for n in border(r, "post"))
        rows.append(f"| ${txt}$ | `{pre}` | `{post}` |")
    p.put("fig-ex4", f"![Árboles de las tres expresiones]({p.img('ex4', tile(parts, caps=['a)', 'b)', 'c)']))})")
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
