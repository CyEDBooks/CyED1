from common import *
from tviz import from_tuple, draw

LET = ("A", ("C", ("D", ("F", None, None), None), ("G", ("E", None, None), ("J", None, None))),
       ("B", ("H", ("I", None, None), None), None))
NAR = ("a", [("b", [("e", []), ("f", []), ("g", [])]), ("c", []),
             ("d", [("h", []), ("i", []), ("j", [])])])
EXPR = ("+", ("↑", ("+ ", ("x", None, None), ("y", None, None)), ("2", None, None)),
        ("/", ("−", ("x ", None, None), ("4", None, None)), ("3", None, None)))


def order(n, kind):
    if n is None:
        return []
    l, r = order(n.left, kind), order(n.right, kind)
    return {"pre": [n] + l + r, "in": l + [n] + r, "post": l + r + [n]}[kind]


NAMES = {"pre": "preorden", "in": "inorden", "post": "postorden"}
RULE = {"pre": "raíz → izquierdo → derecho", "in": "izquierdo → raíz → derecho",
        "post": "izquierdo → derecho → raíz"}


def traversal_steps(p, prefix, root, kind, why=None):
    seq = order(root, kind)
    tabs = []
    for k in range(len(seq)):
        visited = seq[:k + 1]
        ns = {n.key: "tree" for n in visited}
        ns[seq[k].key] = "hl"
        labels = {n.key: str(i + 1) for i, n in enumerate(visited)}
        ls = {seq[k].key: "new"}
        items = [n.key.strip() for n in visited]
        svg = draw(root, node_style=ns, labels=labels, label_style=ls,
                   panel=(NAMES[kind] + ":", items, [k]))
        img = p.img(f"{prefix}-{k:02d}", svg)
        txt = ""
        if why and k in why:
            txt = "\n\n> " + why[k]
        tabs.append(f"![{NAMES[kind]}, paso {k + 1}]({img}){txt}")
    seqtxt = " – ".join(n.key.strip() for n in seq)
    return steps(f"Recorrido en {NAMES[kind]} ({RULE[kind]})", tabs), seqtxt


def nary_order(t, kind):
    lab, ch = t
    if not ch:
        return [lab]
    if kind == "pre":
        out = [lab]
        for c_ in ch:
            out += nary_order(c_, kind)
    elif kind == "post":
        out = []
        for c_ in ch:
            out += nary_order(c_, kind)
        out.append(lab)
    else:
        out = nary_order(ch[0], kind) + [lab]
        for c_ in ch[1:]:
            out += nary_order(c_, kind)
    return out


def eval_postfix(tokens):
    st = []
    rows = []
    for t in tokens:
        if t in "+−*/↑":
            b = st.pop()
            a = st.pop()
            v = {"+": a + b, "−": a - b, "*": a * b, "/": a / b, "↑": a ** b}[t]
            v = int(v) if v == int(v) else v
            st.append(v)
            rows.append((t, f"saca {b} y {a}; {a} {t} {b} = {v}", list(st)))
        else:
            st.append(int(t))
            rows.append((t, "es número: se apila", list(st)))
    return rows


def reduce_prefix(tokens):
    """Reducción al estilo de las diapositivas: el operador más a la derecha
    que tenga dos números a continuación se reemplaza por su resultado."""
    toks = list(tokens)
    lines = [" ".join(toks)]
    while len(toks) > 1:
        for i in range(len(toks) - 3, -1, -1):
            if toks[i] in "+−*/↑" and toks[i + 1] not in "+−*/↑" and toks[i + 2] not in "+−*/↑":
                a, b = int(toks[i + 1]), int(toks[i + 2])
                v = {"+": a + b, "−": a - b, "*": a * b, "/": a // b, "↑": a ** b}[toks[i]]
                toks[i:i + 3] = [str(v)]
                break
        lines.append(" ".join(toks))
    return lines


def build():
    p = Page("Unidad4-EstructurasRecursivas/RecorridosArboles")
    mini = from_tuple(("a", ("b", None, None), ("c", None, None)))
    p.put("fig-mini", f"![Árbol de tres nodos]({p.img('mini', draw(mini))})")

    root = from_tuple(LET)
    p.put("fig-let", f"![Árbol binario A..J]({p.img('letras', draw(root))})")
    st, s = traversal_steps(p, "pre", root, "pre",
                            why={1: "Después de $A$ se recorre **todo** el subárbol izquierdo (el de "
                                    "$C$) en preorden, antes de tocar el derecho.",
                                 4: "Terminó el subárbol de $D$; se sigue con el subárbol derecho de "
                                    "$C$, que empieza en $G$."})
    p.put("pre", st)
    p.put("pre-seq", s)
    st, s = traversal_steps(p, "in", root, "in",
                            why={0: "$F$ es el primero: hay que bajar por la izquierda hasta donde se "
                                    "pueda antes de visitar cualquier raíz.",
                                 6: "Se visita $A$ solo cuando ya se recorrió todo su subárbol "
                                    "izquierdo."})
    p.put("in", st)
    p.put("in-seq", s)
    st, s = traversal_steps(p, "post", root, "post",
                            why={9: "La raíz $A$ es siempre la **última** en postorden."})
    p.put("post", st)
    p.put("post-seq", s)

    # n-ario (Bedoya)
    pos, E = tree_pos(NAR, 50, 60)
    p.put("fig-nar", gfig(p, "nario", pos, E))
    for k in ("pre", "in", "post"):
        p.put(f"nar-{k}", " – ".join(nary_order(NAR, k)))

    # Expresión: construcción por niveles
    ex = from_tuple(EXPR)
    lvls = {}

    def depth(n, d):
        if n is None:
            return
        lvls[n.key] = d
        depth(n.left, d + 1)
        depth(n.right, d + 1)
    depth(ex, 0)
    tabs = []
    texts = [
        "> El operador que se evalúa **último** es el $+$ central: $\\big((x+y)↑2\\big) \\mathbin{\\mathbf{+}} \\big((x-4)/3\\big)$. Es la raíz.",
        "> Su operando izquierdo es $(x+y)↑2$ (raíz $↑$) y el derecho es $(x-4)/3$ (raíz $/$).",
        "> Se repite en cada operando: $x+y$, el exponente $2$, $x-4$ y el divisor $3$.",
        "> Las hojas son siempre **operandos** (variables o números); los nodos internos, **operadores**.",
    ]
    for d in range(4):
        def prune(n):
            if n is None or lvls[n.key] > d:
                return None
            from tviz import N
            return N(n.key, prune(n.left), prune(n.right))
        t = prune(ex)
        ns = {k: ("new" if lvls[k] == d else "plain") for k in lvls if lvls[k] <= d}
        tabs.append(f"![Árbol de expresión, paso {d + 1}]({p.img(f'expr-{d:02d}', draw(t, node_style=ns))})\n\n{texts[d]}")
    p.put("expr-steps", steps("Construir el árbol de ((x+y)↑2)+((x−4)/3)", tabs))
    p.put("fig-expr", f"![Árbol de expresión]({p.img('expr', draw(ex))})")
    p.put("expr-pre", " ".join(n.key.strip() for n in order(ex, "pre")))
    p.put("expr-post", " ".join(n.key.strip() for n in order(ex, "post")))

    # Evaluación posfija con pila
    rows = eval_postfix("8 6 − 3 ↑ 10 7 2 − / +".split())
    tabs = []
    acc = []
    for k, (tok, accion, pila) in enumerate(rows):
        acc.append([f"`{tok}`", accion, " ".join(str(x) for x in pila)])
        rr = [r[:] for r in acc]
        rr[-1] = [hl(tok), hl(accion), hl(" ".join(str(x) for x in pila))]
        tabs.append(md_table(["Símbolo", "Acción", "Pila (tope a la derecha)"], rr))
    tabs[-1] += f"\n\n> Al final la pila tiene un solo valor: **{rows[-1][2][0]}**."
    p.put("post-eval", steps("Evaluar 8 6 − 3 ↑ 10 7 2 − / + con una pila", tabs))
    lines = reduce_prefix("+ − * 2 3 5 / ↑ 2 3 4".split())
    tabs = []
    for k in range(len(lines)):
        body = "\n".join((f"- **`{l}`** ←" if i == k else f"- `{l}`") for i, l in enumerate(lines[:k + 1]))
        tabs.append(body)
    tabs[0] += "\n\n> Se busca el operador **más a la derecha** que esté seguido de dos números."
    p.put("pre-eval", steps("Evaluar + − * 2 3 5 / ↑ 2 3 4", tabs))
    p.put("pre-eval-res", lines[-1])
    p.assemble("index.md")

    # ejercicios
    ex2 = from_tuple(("+", ("↑", ("−", ("8", None, None), ("6", None, None)), ("3", None, None)),
                      ("/", ("10", None, None), ("− ", ("7", None, None), ("2", None, None)))))
    p.put("fig-ex2", f"![Árbol de expresión del ejercicio]({p.img('ex2', draw(ex2))})")
    p.put("ex2-pre", " ".join(n.key.strip() for n in order(ex2, "pre")))
    p.put("ex2-post", " ".join(n.key.strip() for n in order(ex2, "post")))
    tr = from_tuple(("50", ("30", ("20", None, None), ("40", ("35", None, None), None)),
                     ("70", ("60", None, None), ("80", None, ("90", None, None)))))
    p.put("fig-ex1", f"![Árbol binario del ejercicio]({p.img('ex1', draw(tr))})")
    for k in ("pre", "in", "post"):
        p.put(f"ex1-{k}", " – ".join(n.key for n in order(tr, k)))
    lines = reduce_prefix("/ − + + 4 3 13 5 − ↑ − 6 4 3 3".split())
    p.put("ex3-lines", "\n".join(f"- `{l}`" for l in lines))
    rows = eval_postfix("7 2 3 * − 4 ↑ 9 3 / +".split())
    p.put("ex4-res", str(rows[-1][2][0]))
    p.put("ex4-rows", md_table(["Símbolo", "Pila"], [[f"`{t}`", " ".join(str(x) for x in s)] for t, _, s in rows]))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
