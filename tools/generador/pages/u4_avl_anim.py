"""Animaciones de la página de árboles AVL: rotaciones que se deslizan, los casos A–F con sus
subárboles en color y la revisión «¿es AVL?» nodo por nodo."""
from common import *
from anim import Frame, anim_block, tree_frame
from tviz import (nodes, fb, height, find, avl_insert_trace, avl_delete_trace, double_rotation_middle,
                  copy_tree, bst_build, layout, from_tuple, N)


def fbtxt(f):
    return {0: "0"}.get(f, f"{f:+d}".replace("-", "−"))


def fbs(t):
    labels, ls = {}, {}
    for n in nodes(t):
        labels[n.key] = fbtxt(fb(n))
        if abs(fb(n)) > 1:
            ls[n.key] = "bad"
    return labels, ls


def keys(n):
    return [] if n is None else [x.key for x in nodes(n)]


def tf(t, cap, ns=None, es=None, rings=(), hold=None):
    labels, ls = fbs(t)
    fr = tree_frame(t, cap, node_style=ns, edge_style=es, labels=labels, label_style=ls, rings=rings)
    fr.hold = hold
    return fr


SUB = {"A": "sa", "B": "sb", "C": "sc", "D": "sb", "E": "sd"}
COLOR = {"A": "azul", "B": "naranja", "C": "verde", "D": "naranja", "E": "morado"}


def subtrees(t, pk, case):
    """Subárboles que se mueven en el rebalanceo de p: {nombre: raíz}, y q, r."""
    p = find(t, pk)
    if case in "AB":
        q = p.right
        return {"A": p.left, "B": q.left, "C": q.right}, q, None
    if case in "DE":
        q = p.left
        return {"A": p.right, "B": q.right, "C": q.left}, q, None
    if case == "C":
        q = p.right
        r = q.left
        return {"A": p.left, "D": r.left, "E": r.right, "C": q.right}, q, r
    q = p.left
    r = q.right
    return {"A": p.right, "D": r.right, "E": r.left, "C": q.left}, q, r


def colors(subs):
    return {k: SUB[name] for name, root in subs.items() for k in keys(root)}


def describe(subs):
    out = [f"{name} ({COLOR[name]})" for name, root in subs.items() if root is not None]
    return "subárboles " + ", ".join(out) if out else ""


ROT = {"izquierda": "LEFT", "derecha": "RIGHT"}


def rebalance_frames(snaps, frames):
    for a, b in zip(snaps[::2], snaps[1::2]):
        t, pk = a["tree"], a["key"]
        case = b["case"]
        subs, q, r = subtrees(t, pk, case)
        col = colors(subs)
        f, fq = fb(find(t, pk)), fb(q)
        ns = dict(col)
        ns.update({pk: "bad", q.key: "hl"})
        if r is not None:
            ns[r.key] = "hl"
        rots = " y luego ".join(f"{ROT[d]}-ROTATE({k})" for d, k in b["rots"])
        frames.append(tf(t, f"Subiendo, el primer nodo desbalanceado es p = {pk}, con fb(p) = {fbtxt(f)}. "
                         f"Su hijo del lado alto es q = {q.key}, con fb(q) = {fbtxt(fq)}: caso {case}, "
                         f"{rots}." + (f" En color, los {describe(subs)}." if describe(subs) else ""),
                         ns=ns, rings=(pk,)))
        if case in ("C", "F"):
            mid = double_rotation_middle(t, pk, case)
            d0, k0 = b["rots"][0]
            frames.append(tf(mid, f"{ROT[d0]}-ROTATE({k0}): r = {r.key} sube al lugar de q = {q.key}. "
                             f"Ahora p = {pk}, r = {r.key} y q = {q.key} están en línea, como en el caso "
                             f"{'A' if case == 'C' else 'D'}.", ns=ns, rings=(r.key,)))
        d1, k1 = b["rots"][-1]
        nr = b["newroot"]
        moved = [n for n in ("B", "D", "E") if subs.get(n) is not None]
        if len(moved) > 1:
            mv = f" Los subárboles {' y '.join(moved)} cambiaron de padre; el inorden no cambió."
        elif moved:
            mv = f" El subárbol {moved[0]} cambió de padre; el inorden no cambió."
        else:
            mv = " El inorden no cambió."
        ns2 = dict(col)
        ns2[nr] = "new"
        frames.append(tf(b["tree"], f"{ROT[d1]}-ROTATE({k1}): {nr} sube y {pk} baja a ser su hijo "
                         f"{'izquierdo' if d1 == 'izquierda' else 'derecho'}.{mv} Los factores vuelven a "
                         f"estar entre −1 y 1.", ns=ns2, rings=(nr,)))


def avl_frames(start, ops, intro=None):
    root = copy_tree(start)
    frames = []
    if root is not None:
        frames.append(tf(root, intro or "El árbol AVL de partida. Junto a cada nodo, su factor de balanceo."))
    for op, k in ops:
        if op == "i":
            after, snaps = avl_insert_trace(root, k)
            s0 = snaps[0]
            t, path = s0["tree"], s0["path"]
            ns = {x: "hl" for x in path}
            ns[k] = "new"
            es = {(a, b): "path" for a, b in zip(path, path[1:] + [k])}
            if not path:
                cap = f"Insertar {k}: el árbol está vacío, {k} es la raíz."
            else:
                cmp_ = ", ".join(f"{k} {'<' if k < x else '>'} {x}" for x in path)
                cap = (f"Insertar {k} como en un ABB ({cmp_}): queda como hijo "
                       f"{'izquierdo' if k < path[-1] else 'derecho'} de {path[-1]}.")
                cap += (" Todos los factores siguen entre −1 y 1." if len(snaps) == 1 else
                        " Un factor del camino quedó en ±2 (en rojo).")
            frames.append(tf(t, cap, ns=ns, es=es, rings=(k,)))
            rebalance_frames(snaps[1:], frames)
        else:
            z = find(root, k)
            if z.left is not None and z.right is not None:
                s = z.right
                path = [k]
                while s is not None:
                    path.append(s.key)
                    s = s.left
                sk = path[-1]
                frames.append(tf(root, f"Borrar {k} como en un ABB. Tiene dos hijos: lo reemplaza su "
                                 f"sucesor {sk}, el mínimo del subárbol derecho.",
                                 ns={k: "bad", sk: "goal"},
                                 es={(a, b): "path" for a, b in zip(path, path[1:])}, rings=(k, sk)))
            else:
                hijos = sum(c is not None for c in (z.left, z.right))
                frames.append(tf(root, f"Borrar {k} como en un ABB: "
                                 + ("es una hoja, simplemente sale." if hijos == 0 else
                                    "tiene un solo hijo, que sube a su lugar."),
                                 ns={k: "bad"}, rings=(k,)))
            after, snaps = avl_delete_trace(root, k)
            s0 = snaps[0]
            st = s0["start"]
            ns = {st: "hl"} if st is not None else {}
            if s0["succ"] is not None:
                ns[s0["succ"]] = "new"
            cap = (f"{s0['succ']} ocupa el lugar de {k}. " if s0["succ"] is not None else f"{k} salió. ")
            if st is not None:
                cap += (f"Desde {st}, el padre del nodo que salió, se suben revisando los factores."
                        + (" Todos siguen entre −1 y 1." if len(snaps) == 1 else " Hay un ±2 (en rojo)."))
            frames.append(tf(s0["tree"], cap, ns=ns, rings=(st,) if st is not None else ()))
            rebalance_frames(snaps[1:], frames)
        root = after
    frames.append(tf(root, "Resultado: todos los factores están en {−1, 0, 1} y el inorden sigue "
                     "ordenado. Es AVL.", ns={n.key: "goal" for n in nodes(root)}))
    return frames, root


def ops_anim(p, name, start, ops, alt, intro=None):
    frames, _ = avl_frames(start, ops, intro)
    return anim_block(p, name, frames, alt)


# Rotación genérica: x, y y los subárboles α, β, γ como triángulos
def rotation_anim(p):
    dx, dy = 46, 62

    def fr(cap, pos, par, ns):
        f = Frame(cap)
        for k, (cx, cy) in pos.items():
            f.node(k, cx * dx, cy * dy, k, ns.get(k, "plain"),
                   shape="tri" if k in "αβγ" else "circle")
        for c, pa in par.items():
            f.edge(c, pa)
        return f
    before = {"x": (1, 0), "α": (0, 1), "y": (3, 1), "β": (2, 2), "γ": (4, 2)}
    after = {"y": (3, 0), "x": (1, 1), "α": (0, 2), "β": (2, 2), "γ": (4, 1)}
    sty = {"α": "sa", "β": "sb", "γ": "sc"}
    f0 = fr("Antes: x tiene hijo derecho y. α, β y γ son subárboles cualesquiera.", before,
            {"α": "x", "y": "x", "β": "y", "γ": "y"}, sty)
    f1 = fr("LEFT-ROTATE(x): y sube, x baja a la izquierda y β (naranja) pasa de hijo izquierdo de y a "
            "hijo derecho de x. El inorden sigue siendo α, x, β, y, γ.", after,
            {"x": "y", "γ": "y", "α": "x", "β": "x"}, {**sty, "y": "new"})
    f2 = fr("RIGHT-ROTATE(y) deshace la rotación: x sube y β vuelve a ser hijo izquierdo de y.", before,
            {"α": "x", "y": "x", "β": "y", "γ": "y"}, {**sty, "x": "new"})
    return anim_block(p, "rot-anim", [f0, f1, f2], "Animación: LEFT-ROTATE(x) y RIGHT-ROTATE(y)")


# ¿Es AVL?
def check_frames(t):
    frames = [tf_plain(t, "¿Es AVL? Se revisan dos cosas: que sea ABB (el inorden sale ordenado) y que "
                          "cada nodo tenga |fb| ≤ 1.")]
    pos, _ = layout(t, 40, 56)
    ino = [n.key for n in nodes(t)]
    ybot = max(y for _, y in pos.values()) + 44
    x0 = min(x for x, _ in pos.values()) - 15
    badk = {ino[i + 1] for i in range(len(ino) - 1) if ino[i + 1] < ino[i]}
    badk |= {ino[i] for i in range(len(ino) - 1) if ino[i + 1] < ino[i]}
    bst = not badk

    def panel(f, mark):
        for i, k in enumerate(ino):
            st = ("bad" if k in badk else "goal") if mark else "slot"
            f.cell(f"io{k}", x0 + i * 34, ybot, 30, 28, k, st)
        f.cell("iolab", x0 - 64, ybot, 58, 28, "Inorden:", "txt-muted", size=12)
    f = tf_plain(t, "Inorden: " + ", ".join(map(str, ino)) + (". Sale ordenado ✓: es ABB." if bst else
                 f". No sale ordenado ✗: no es ABB, así que no puede ser AVL, aunque los factores estén bien."),
                 ns={k: "bad" for k in badk})
    panel(f, True)
    frames.append(f)
    # factores por niveles, de abajo hacia arriba
    depth = {k: round(y / 56) for k, (_, y) in pos.items()}
    labels, ls = {}, {}
    for d in range(max(depth.values()), -1, -1):
        lev = sorted(k for k in depth if depth[k] == d)
        parts = []
        for k in lev:
            n = find_any(t, k)
            f_ = fb(n)
            labels[k] = fbtxt(f_)
            if abs(f_) > 1:
                ls[k] = "bad"
            if n.left is None and n.right is None:
                continue
            parts.append(f"fb({k}) = {height(n.right)} − {height(n.left)} = {fbtxt(f_)}" +
                         (" ✗" if abs(f_) > 1 else ""))
        hojas = [k for k in lev if find_any(t, k).left is None and find_any(t, k).right is None]
        txt = f"Nivel {d}: "
        if hojas:
            txt += ("hojas " if len(hojas) > 1 else "hoja ") + ", ".join(map(str, hojas)) + ": fb = 0. "
        txt += "; ".join(parts) + ("." if parts else "")
        ns = {k: "hl" for k in lev}
        ns.update({k: "bad" for k in ls})
        if not bst:
            ns.update({k: "bad" for k in badk})
        f = tree_frame(t, txt, node_style=ns, labels=dict(labels), label_style=dict(ls))
        panel(f, True)
        frames.append(f)
    bal = not ls
    if bst and bal:
        verdict = "Sí es AVL: es ABB y todos los factores están en {−1, 0, 1}."
        ns = {n.key: "goal" for n in nodes(t)}
    else:
        why = []
        if not bst:
            why.append("no es ABB")
        if not bal:
            why.append("hay factores en ±2: " + ", ".join(f"fb({k}) = {labels[k]}" for k in ls))
        verdict = "No es AVL: " + " y ".join(why) + "."
        ns = {k: "bad" for k in list(ls) + (list(badk) if not bst else [])}
    f = tree_frame(t, verdict, node_style=ns, labels=labels, label_style=ls)
    panel(f, True)
    frames.append(f)
    return frames, bst, bal, labels, ls, badk


def tf_plain(t, cap, ns=None):
    return tree_frame(t, cap, node_style=ns)


def find_any(t, k):
    """find que no supone ABB (para revisar árboles que no lo son)."""
    for n in nodes(t):
        if n.key == k:
            return n


def fib_tree(h, keys_iter):
    """AVL mínimo de altura h, con llaves en inorden."""
    if h == 0:
        return None
    if h == 1:
        return N(next(keys_iter))
    left = fib_tree(h - 1, keys_iter)
    root = N(next(keys_iter))
    root.left = left
    root.right = fib_tree(h - 2, keys_iter)
    return root
