from common import *
from tviz import (from_tuple, draw, height, nodes, layout, halo, ring, badge, level_lines,
                  parent_map)

VIC = (10, (15, (25, (7, None, None), (6, None, None)), None), (-6, None, (18, None, None)))


# Árbol de Vargas (recorridos A..J) y el árbol de búsqueda de Bedoya
VV = ("A", ("C", ("D", ("F", None, None), None), ("G", ("E", None, None), ("J", None, None))),
      ("B", ("H", ("I", None, None), None), None))
BED = (24, (12, (7, (4, (1, None, None), (5, None, None)), (9, (8, None, None), (10, None, None))),
            (19, (16, (13, None, None), (18, None, None)), (21, None, None))),
       (43, (32, (28, (26, None, None), (29, None, None)), (38, (33, None, None), (42, None, None))),
            (48, (45, None, None), (51, (50, None, None), (53, None, None)))))


def preorder(n):
    return [] if n is None else [n] + preorder(n.left) + preorder(n.right)


def postorder(n):
    return [] if n is None else postorder(n.left) + postorder(n.right) + [n]


# Cinco ejemplos, de muy fácil a difícil: la misma lista de preguntas sobre árboles cada
# vez más grandes. B(k, izq, der).
def B(k, l=None, r=None):
    return (k, l, r)


NIVELES = ["muy fácil", "fácil", "medio", "medio", "difícil"]
EJEMPLOS = [
    B(8, B(4), B(9)),
    B(6, B(3, B(1), B(5)), B(9)),
    B(20, B(10, B(5), B(15)), B(30, None, B(40))),
    B(50, B(30, B(20), B(40)), B(70, B(60), B(80))),
    B(40, B(20, B(10, B(5), B(15)), B(30, B(25), B(35))),
      B(60, B(50, B(45)), B(70, B(65), B(80, B(75), B(90))))),
]


def _l(xs):
    return ", ".join(f"${x}$" for x in xs)


def ejemplo(p, i, t):
    root = from_tuple(t)
    ns_all = nodes(root)
    pre = preorder(root)
    leaves = [n.key for n in pre if n.left is None and n.right is None]
    inner = [n.key for n in pre if n.left or n.right]
    one = [n.key for n in pre if (n.left is None) != (n.right is None)]
    by_key = {n.key: n for n in pre}
    h = height(root)
    depth = {}

    def rec(n, d):
        if n is not None:
            depth[n.key] = d
            rec(n.left, d + 1)
            rec(n.right, d + 1)
    rec(root, 0)
    # rama más larga (la primera de izquierda a derecha)
    branch, x = [], root
    while x is not None:
        branch.append(x.key)
        # el hijo más alto; en un empate, el izquierdo
        x = max((c for c in (x.left, x.right) if c), key=height, default=None)
    D = dict(dx=48)
    pref = f"ej{i}"
    tabs = []

    def add(svg, txt):
        tabs.append(f"![Ejemplo {i}, paso {len(tabs) + 1}]({p.img(f'{pref}-{len(tabs) + 1:02d}', svg)})"
                    f"\n\n> {txt}")

    head = (f"**Ejemplo {i} ({NIVELES[i - 1]}).** Para este árbol, ¿cuáles son las hojas? ¿Cuál es "
            f"su altura y su peso? ¿Es completo? ¿Es lleno?\n\n"
            f"![Árbol del ejemplo {i}]({p.img(f'{pref}-00', draw(root, **D))})")
    ns = {k: "goal" for k in leaves}
    ns.update({k: "hl" for k in inner})
    add(draw(root, node_style=ns, **D),
        f"**Hojas** (en verde, sin hijos): {_l(leaves)}. **No terminales** (en amarillo): {_l(inner)}.")
    es = {(a, b): "path" for a, b in zip(branch, branch[1:])}
    add(draw(root, node_style={k: "hl" for k in branch}, edge_style=es,
             under=lambda svg, pos: level_lines(svg, pos), **D),
        f"Los niveles van de $0$ (la raíz) a ${h - 1}$. La rama más larga, "
        f"{' → '.join(f'${k}$' for k in branch)}, tiene ${h}$ nodos: la **altura** es ${h}$.")
    add(draw(root, node_style={n.key: "tree" for n in pre},
             over=lambda svg, pos: [badge(svg, *pos[n.key], j + 1) for j, n in enumerate(pre)], **D),
        f"Se cuentan los nodos: el **peso** es ${len(ns_all)}$.")
    if one:
        def over(svg, pos):
            for k in one:
                x, y = pos[k]
                ring(svg, x, y)
                # el rótulo va del lado del hijo que falta, donde no hay aristas
                left_missing = by_key[k].left is None
                svg.text(x + (-27 if left_missing else 27), y + 4, "un solo hijo", 12, PAL["new"],
                         anchor="end" if left_missing else "start", bold=True)
        add(draw(root, node_style={k: "bad" for k in one}, over=over, **D),
            f"**¿Completo?** No: {_l(one)} {'es no terminal' if len(one) == 1 else 'son no terminales'} "
            f"con un solo subárbol no vacío. En un árbol completo cada no terminal tiene "
            f"**exactamente dos** hijos.")
    else:
        add(draw(root, node_style={k: "goal" for k in inner}, **D),
            f"**¿Completo?** Sí: cada no terminal ({_l(inner)}) tiene exactamente dos hijos.")
    lvl = sorted({depth[k] for k in leaves})
    if one:
        why = "no es completo, así que tampoco puede ser lleno"
        if len(lvl) > 1:
            why += " (además, sus hojas están en distintos niveles: en rojo, las que no están en el último)"
    elif len(lvl) > 1:
        why = (f"es completo, pero sus hojas están en los niveles {_l(lvl)}: no todas están en el "
               f"mismo nivel (en rojo, las que no están en el último)")
    else:
        why = f"es completo y todas sus hojas están en el nivel ${lvl[0]}$"
    full = not one and len(lvl) == 1

    def over(svg, pos):
        for k in leaves:
            if depth[k] != h - 1:
                ring(svg, *pos[k])
    ls = {k: ("goal" if depth[k] == h - 1 else "bad") for k in leaves}
    add(draw(root, node_style=ls, under=lambda svg, pos: level_lines(svg, pos), over=over, **D),
        f"**¿Lleno?** {'Sí' if full else 'No'}: {why}. Con altura ${h}$ caben a lo sumo "
        f"$2^{h} - 1 = {2 ** h - 1}$ nodos y tiene ${len(ns_all)}$"
        + ("." if full else f": le faltan ${2 ** h - 1 - len(ns_all)}$ para estar lleno."))
    return f"{head}\n\n" + steps("Paso a paso", tabs)


def build():
    p = Page("Unidad4-EstructurasRecursivas/ArbolesBinarios")
    root = from_tuple(VIC)
    p.put("fig-ejemplo", f"![Árbol binario de ejemplo]({p.img('ejemplo', draw(root))})")

    # izquierda y derecha importan
    a = from_tuple(("a", ("b", None, None), None))
    b = from_tuple(("a", None, ("b", None, None)))
    p.put("fig-izq", f"![b como hijo izquierdo]({p.img('izq', draw(a))})")
    p.put("fig-der", f"![b como hijo derecho]({p.img('der', draw(b))})")

    # completo / lleno / ninguno
    comp = from_tuple(("a", ("b", ("d", None, None), ("e", None, None)), ("c", None, None)))
    lleno = from_tuple(("a", ("b", ("d", None, None), ("e", None, None)),
                        ("c", ("f", None, None), ("g", None, None))))
    nada = from_tuple(("a", ("b", None, ("d", None, None)), ("c", None, None)))
    p.put("fig-completo", f"![Completo]({p.img('completo', draw(comp, caption='Completo, no lleno'))})")
    p.put("fig-lleno", f"![Lleno]({p.img('lleno', draw(lleno, caption='Lleno'))})")
    p.put("fig-ninguno", f"![Ni completo ni lleno]({p.img('ninguno', draw(nada, caption='Ni completo ni lleno'))})")

    # altura y peso de abajo hacia arriba (postorden)
    order = postorder(root)
    h, w = {}, {}
    tabs = []
    for k, n in enumerate(order):
        hl_ = height(n.left)
        hr = height(n.right)
        h[n.key] = 1 + max(hl_, hr)
        w[n.key] = len(nodes(n))
        labels = {kk: f"h={h[kk]}, p={w[kk]}" for kk in h}
        ls = {n.key: "new"}
        ns = {kk: "tree" for kk in h}
        ns[n.key] = "hl"
        svg = draw(root, node_style=ns, labels=labels, label_style=ls, dx=62)
        img = p.img(f"altura-{k:02d}", svg)
        if n.left is None and n.right is None:
            txt = (f"> ${n.key}$ es hoja: sus dos subárboles son vacíos (altura $0$, peso $0$). "
                   f"$h = 1 + \\max(0, 0) = 1$, $p = 1 + 0 + 0 = 1$.")
        else:
            li = f"{h[n.left.key]}" if n.left else "0"
            ri = f"{h[n.right.key]}" if n.right else "0"
            lp = f"{w[n.left.key]}" if n.left else "0"
            rp = f"{w[n.right.key]}" if n.right else "0"
            txt = (f"> ${n.key}$: ya se conocen sus subárboles. "
                   f"$h = 1 + \\max({li}, {ri}) = {h[n.key]}$, $p = 1 + {lp} + {rp} = {w[n.key]}$.")
        tabs.append(f"![Altura y peso, paso {k + 1}]({img})\n\n{txt}")
    tabs[1] += "\n\n> **¿Por qué se calcula primero $7$ y $6$, y no $10$?**"
    tabs[2] += ("\n\n> Porque la altura y el peso de un nodo **dependen** de los de sus hijos. Hay "
                "que resolver primero los subárboles: es la recursión regresando desde las hojas.")
    p.put("altura-steps", steps("Altura (h) y peso (p) de cada subárbol", tabs))

    # Máximo número de nodos por nivel
    full4 = from_tuple((1, (2, (4, (8, None, None), (9, None, None)), (5, (10, None, None), (11, None, None))),
                        (3, (6, (12, None, None), (13, None, None)), (7, (14, None, None), (15, None, None)))))
    p.put("fig-full4", f"![Árbol binario lleno de altura 4]({p.img('lleno4', draw(full4, dx=34))})")
    for i, t in enumerate(EJEMPLOS, 1):
        p.put(f"ej{i}", ejemplo(p, i, t))
    p.assemble("index.md")

    # Ejercicios
    ex = from_tuple(("M", ("F", ("B", None, None), ("H", ("G", None, None), None)),
                     ("T", ("P", None, ("R", None, None)), ("W", None, None))))
    p.put("fig-ex1", f"![Árbol binario del ejercicio]({p.img('ex1', draw(ex))})")
    p.put("ex1-peso", str(len(nodes(ex))))
    p.put("ex1-alt", str(height(ex)))
    p.put("ex1-hojas", ", ".join(n.key for n in nodes(ex) if n.left is None and n.right is None))
    for key, t in (("vv", VV), ("bed", BED)):
        r = from_tuple(t)
        p.put(f"fig-{key}", f"![Árbol binario]({p.img(key, draw(r, dx=44, compact=True) if key == 'bed' else draw(r))})")
        par, lev = {}, {}

        def rec(n, pa, d):
            if n is None:
                return
            par[n.key], lev[n.key] = pa, d
            rec(n.left, n.key, d + 1)
            rec(n.right, n.key, d + 1)
        rec(r, None, 0)
        allnodes = nodes(r)
        for n in allnodes:
            kids = [c.key for c in (n.left, n.right) if c is not None]
            p.put(f"{key}-padre-{n.key}", f"${par[n.key]}$" if par[n.key] is not None else "—")
            p.put(f"{key}-hijos-{n.key}", ", ".join(f"${k}$" for k in kids) or "ninguno")
            p.put(f"{key}-nivel-{n.key}", f"${lev[n.key]}$")
        pre = preorder(r)
        p.put(f"{key}-hojas", ", ".join(f"${n.key}$" for n in pre if n.left is None and n.right is None))
        p.put(f"{key}-internos", ", ".join(f"${n.key}$" for n in pre if n.left or n.right))
        p.put(f"{key}-un-hijo", ", ".join(f"${n.key}$" for n in pre if (n.left is None) != (n.right is None)))
        p.put(f"{key}-alt", f"${height(r)}$")
        p.put(f"{key}-peso", f"${len(allnodes)}$")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
