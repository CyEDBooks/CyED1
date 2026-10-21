from common import *
from tviz import from_tuple, draw, height, nodes, layout

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
