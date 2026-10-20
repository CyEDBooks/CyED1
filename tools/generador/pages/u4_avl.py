from common import *
from tviz import (from_tuple, draw, nodes, fb, height, avl_insert_trace, double_rotation_middle,
                  copy_tree, find, rot_left, bst_build, N)


def fbl(root, newk=None, bad=None):
    labels, ls = {}, {}
    for n in nodes(root):
        f = fb(n)
        labels[n.key] = {0: "0"}.get(f, f"{f:+d}".replace("-", "−"))
        if abs(f) > 1:
            ls[n.key] = "bad"
    return labels, ls


def avl_tabs(p, prefix, seq, start=None, show_all=True):
    root = start
    out = []
    k_img = 0
    for k in seq:
        root_after, snaps = avl_insert_trace(root, k)
        for s in snaps:
            t = s["tree"]
            labels, ls = fbl(t)
            if s["kind"] == "insert":
                ns = {x: "hl" for x in s["path"]}
                ns[k] = "new"
                es = {(a, b): "path" for a, b in zip(s["path"], s["path"][1:] + [k])}
                txt = f"> Insertar ${k}$ como en un ABB" + (
                    f" (camino: {', '.join(map(str, s['path']))})." if s["path"] else ": es la raíz.")
                if len(snaps) == 1:
                    txt += " Todos los factores de balanceo están entre $-1$ y $1$: sigue siendo AVL."
                img = draw(t, node_style=ns, edge_style=es, labels=labels, label_style=ls)
            elif s["kind"] == "unbalanced":
                ns = {s["key"]: "bad"}
                q = find(t, s["key"]).right if s["fb"] == 2 else find(t, s["key"]).left
                ns[q.key] = "hl"
                txt = (f"> Subiendo por el camino, el primer nodo desbalanceado es $p = {s['key']}$, "
                       f"con $fb(p) = {s['fb']:+d}$. Su hijo del lado más alto es $q = {q.key}$, con "
                       f"$fb(q) = {fb(q):+d}$.").replace("+-", "-")
                img = draw(t, node_style=ns, labels=labels, label_style=ls)
                unb = s
            else:
                if s["case"] in ("C", "F"):
                    mid = double_rotation_middle(unb["tree"], unb["key"], s["case"])
                    l2, ls2 = fbl(mid)
                    r1 = s["rots"][0]
                    img_mid = draw(mid, node_style={r1[1]: "hl"}, labels=l2, label_style=ls2)
                    path = p.img(f"{prefix}-{k_img:02d}", img_mid)
                    k_img += 1
                    out.append(f"![AVL, paso {len(out) + 1}]({path})\n\n> **Caso {s['case']}:** $fb(q)$ "
                               f"tiene signo contrario a $fb(p)$. Primero se rota $q = {r1[1]}$ hacia la "
                               f"**{r1[0]}**: ahora el desbalance queda «en línea».")
                    r2 = s["rots"][1]
                    txt = (f"> Luego se rota $p = {r2[1]}$ hacia la **{r2[0]}**. La nueva raíz del "
                           f"subárbol es ${s['newroot']}$ y el árbol vuelve a ser AVL.")
                else:
                    r1 = s["rots"][0]
                    txt = (f"> **Caso {s['case']}:** $fb(q)$ tiene el mismo signo que $fb(p)$ (o es $0$). "
                           f"Una rotación de $p = {r1[1]}$ hacia la **{r1[0]}** basta: la nueva raíz "
                           f"del subárbol es ${s['newroot']}$.")
                img = draw(t, node_style={s["newroot"]: "new"}, labels=labels, label_style=ls)
            path = p.img(f"{prefix}-{k_img:02d}", img)
            k_img += 1
            out.append(f"![AVL, paso {len(out) + 1}]({path})\n\n{txt}")
        root = root_after
    return out, root


def build():
    p = Page("Unidad4-EstructurasRecursivas/ArbolesAVL")

    deg = bst_build([1, 2, 3, 4, 5, 6, 7])
    p.put("fig-cadena", f"![Cadena]({p.img('cadena', draw(deg, dx=36))})")

    # ¿Es AVL?
    cands = [
        ("es-1", (8, (4, (2, None, None), (6, None, None)), (10, None, (12, None, None)))),
        ("es-2", (8, (4, (2, (1, None, None), None), (6, None, None)), (10, None, None))),
        ("es-3", (8, (4, (2, (1, None, None), (3, None, None)), (6, None, None)), (10, (9, None, None), None))),
        ("es-4", (8, (4, None, None), (12, (10, None, None), (14, None, (16, None, None))))),
    ]
    for i, (name, t) in enumerate(cands):
        r = from_tuple(t)
        p.put("fig-" + name, f"![{name}]({p.img(name, draw(r, caption='abcd'[i] + ')'))})")
        labels, ls = fbl(r)
        p.put("fig-" + name + "-sol", f"![{name}]({p.img(name + '-sol', draw(r, labels=labels, label_style=ls))})")

    # Rotaciones genéricas
    before = from_tuple(("x", ("α", None, None), ("y", ("β", None, None), ("γ", None, None))))
    after = from_tuple(("y", ("x", ("α", None, None), ("β", None, None)), ("γ", None, None)))
    gst = {"α": "ghost", "β": "tree", "γ": "ghost"}
    p.put("fig-rot-antes", f"![Antes]({p.img('rot-antes', draw(before, node_style={**gst, 'x': 'hl', 'y': 'plain'}, caption='x con hijo derecho y'))})")
    p.put("fig-rot-despues", f"![Después]({p.img('rot-despues', draw(after, node_style={**gst, 'x': 'hl', 'y': 'plain'}, caption='después de LEFT-ROTATE(x)'))})")

    # Ejemplos de inserción
    st, _ = avl_tabs(p, "ej1", [3, 2, 1])
    p.put("ej1", steps("Insertar 3, 2, 1", st))
    st, _ = avl_tabs(p, "ej2", [1, 2, 3, 4, 5, 6, 7])
    p.put("ej2", steps("Insertar 1, 2, 3, 4, 5, 6, 7", st))
    base = None
    for k in [50, 20, 70, 10, 30]:
        base, _ = avl_insert_trace(base, k)
    labels, ls = fbl(base)
    p.put("fig-ej3-base", f"![AVL inicial]({p.img('ej3-base', draw(base, labels=labels))})")
    st, _ = avl_tabs(p, "ej3", [25], start=base)
    p.put("ej3", steps("AVL-INSERT(T, 25)", st))
    st, _ = avl_tabs(p, "ej4", [10, 30, 20])
    p.put("ej4", steps("Insertar 10, 30, 20", st))

    # Eliminación con caso B
    t = from_tuple((2, (1, None, None), (4, (3, None, None), (5, None, None))))
    tabs = []
    labels, ls = fbl(t)
    tabs.append((copy_tree(t), {1: "bad"}, labels, ls, "> Se elimina $1$ como en un ABB (es una hoja)."))
    t.left = None
    labels, ls = fbl(t)
    tabs.append((copy_tree(t), {2: "bad", 4: "hl"}, labels, ls,
                 "> $fb(2) = 2 - 0 = +2$: desbalanceado. Su hijo derecho $q = 4$ tiene $fb(q) = 0$. "
                 "Es el **caso B**, que solo aparece al eliminar."))
    t = rot_left(t)
    labels, ls = fbl(t)
    tabs.append((copy_tree(t), {4: "new"}, labels, ls,
                 "> Se rota $2$ hacia la izquierda. Ahora $fb(4) = -1$: balanceado. A diferencia de la "
                 "inserción, al eliminar la altura del subárbol puede bajar y hay que **seguir "
                 "subiendo** y revisando ancestros."))
    out = []
    for i, (tt, ns, labels, ls, txt) in enumerate(tabs):
        out.append(f"![Eliminar, paso {i + 1}]({p.img(f'del-{i:02d}', draw(tt, node_style=ns, labels=labels, label_style=ls))})\n\n{txt}")
    p.put("eliminar", steps("Eliminar 1", out))
    p.assemble("index.md")

    # ejercicios
    root = None
    for k in [10, 20, 30, 40, 50, 25]:
        root, _ = avl_insert_trace(root, k)
    labels, ls = fbl(root)
    p.put("ex1-sol", f"![Resultado]({p.img('ex1-sol', draw(root, labels=labels))})")
    root2 = None
    cases = []
    for k in [15, 20, 24, 10, 13, 7, 30, 36, 25]:
        root2, sn = avl_insert_trace(root2, k)
        for s in sn:
            if s["kind"] == "rotated":
                cases.append(f"al insertar ${k}$: caso {s['case']} en ${s['key']}$")
    labels, _ = fbl(root2)
    p.put("ex2-sol", f"![Resultado]({p.img('ex2-sol', draw(root2, labels=labels))})")
    p.put("ex2-casos", "; ".join(cases))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
