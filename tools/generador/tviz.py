"""Árboles binarios: ABB, AVL, recorridos y su dibujo paso a paso."""
from common import *
from figlib import _shorten, NODE_STYLES


class N:
    __slots__ = ("key", "left", "right")

    def __init__(self, key, left=None, right=None):
        self.key, self.left, self.right = key, left, right


def copy_tree(n):
    return None if n is None else N(n.key, copy_tree(n.left), copy_tree(n.right))


def height(n):
    """Altura en nodos (árbol vacío = 0, hoja = 1), como en las diapositivas."""
    return 0 if n is None else 1 + max(height(n.left), height(n.right))


def fb(n):
    return height(n.right) - height(n.left)


def nodes(n):
    return [] if n is None else nodes(n.left) + [n] + nodes(n.right)


def from_tuple(t):
    if t is None:
        return None
    k, l, r = t
    return N(k, from_tuple(l), from_tuple(r))


def layout(root, dx=44, dy=62):
    pos, edges = {}, []
    i = [0]

    def rec(n, d):
        if n is None:
            return
        rec(n.left, d + 1)
        pos[n.key] = (i[0] * dx, d * dy)
        i[0] += 1
        rec(n.right, d + 1)
        for ch in (n.left, n.right):
            if ch is not None:
                edges.append((n.key, ch.key))
    rec(root, 0)
    return pos, edges


def compact_layout(root, dx=44, dy=62):
    """Como layout, pero cada subárbol se arrima al de al lado hasta quedar a dx en su nivel
    más cercano, y el padre queda centrado sobre sus hijos. Mucho más angosto en árboles
    grandes; ya no hay una columna por nodo."""
    def rec(n):
        # devuelve (x relativa de cada llave con la raíz en 0, contorno izquierdo y derecho por nivel)
        subs = [(c, rec(c)) for c in (n.left, n.right) if c is not None]
        if not subs:
            return {n.key: (0, 0)}, [0], [0]
        if len(subs) == 2:
            (_, (pl, ll, rl)), (_, (pr, lr, rr)) = subs
            off = max(rl[i] - lr[i] + dx for i in range(min(len(rl), len(lr))))
            sl, sr = -off / 2, off / 2
        else:
            c, (pl, ll, rl) = subs[0]
            sl = -dx / 2 if c is n.left else dx / 2
            pr, lr, rr, sr = {}, [], [], 0
        pos = {n.key: (0, 0)}
        for p_, s in ((pl, sl), (pr, sr)):
            for k, (x, d) in p_.items():
                pos[k] = (x + s, d + 1)
        depth = max(len(ll), len(lr))
        left = [0] + [min(v for v in (ll[i] + sl if i < len(ll) else None,
                                      lr[i] + sr if i < len(lr) else None) if v is not None)
                      for i in range(depth)]
        right = [0] + [max(v for v in (rl[i] + sl if i < len(rl) else None,
                                       rr[i] + sr if i < len(rr) else None) if v is not None)
                       for i in range(depth)]
        return pos, left, right

    rel, _, _ = rec(root)
    minx = min(x for x, _ in rel.values())
    pos = {k: ((x - minx), d * dy) for k, (x, d) in rel.items()}
    edges = [(n.key, c.key) for n in nodes(root) for c in (n.left, n.right) if c is not None]
    return pos, edges


def draw(root, node_style=None, edge_style=None, labels=None, label_style=None, r=15,
         panel=None, caption=None, dx=40, dy=56, label_side="right", font=13, ghost=None,
         compact=False):
    """Dibuja un árbol binario. ghost = (clave_padre, 'L'|'R', texto) para un hueco.
    compact: usa compact_layout (para árboles grandes)."""
    svg = SVG()
    if root is None:
        svg.rect(0, 0, 120, 40, PAL["soft"], PAL["border"])
        svg.text(60, 26, "árbol vacío", 13, PAL["muted"])
        return svg
    pos, edges = (compact_layout if compact else layout)(root, dx, dy)
    node_style = node_style or {}
    edge_style = edge_style or {}
    labels = labels or {}
    label_style = label_style or {}
    for a, b in edges:
        st = edge_style.get((a, b), "plain")
        color, width, dash = EDGE_STYLES_T[st]
        x1, y1, x2, y2 = _shorten(*pos[a], *pos[b], r, r)
        svg.line(x1, y1, x2, y2, color, width, dash)
    if ghost:
        pk, side, txt = ghost
        x, y = pos[pk]
        gx, gy = x + (-dx * 0.7 if side == "L" else dx * 0.7), y + dy
        x1, y1, x2, y2 = _shorten(x, y, gx, gy, r, r)
        svg.line(x1, y1, x2, y2, PAL["new"], 2.4, "5,4")
        svg.circle(gx, gy, r, "#ffe3e3", PAL["new"], 2.4)
        svg.text(gx, gy + 5, txt, font, PAL["new"], bold=True)
    for k, (x, y) in pos.items():
        st = node_style.get(k, "plain")
        fill, stroke, tc, width = NODE_STYLES[st]
        svg.circle(x, y, r, fill, stroke, width)
        t = str(k)
        size = font if len(t) <= 2 else max(10, font - (len(t) - 2))
        svg.text(x, y + size * 0.35, t, size, tc, bold=st in ("new", "hl", "bad"))
        if k in labels and labels[k] != "":
            ls = label_style.get(k)
            col = PAL["new"] if ls == "new" else (PAL["bad"] if ls == "bad" else PAL["teal"])
            if label_side == "right":
                svg.text(x + r + 3, y - r + 5, labels[k], 13, col, anchor="start", bold=ls is not None)
            else:
                svg.text(x, y + r + 15, labels[k], 13, col, bold=ls is not None)
    if panel:
        ys = max(y for _, y in pos.values()) + 48
        x0 = min(x for x, _ in pos.values()) - 10
        title, items, new = panel
        draw_panel(svg, x0, ys, title, items, new=new, cell=30, wrap=12)
    if caption:
        ys = max(y for _, y in pos.values()) + (100 if panel else 44)
        x0 = min(x for x, _ in pos.values()) - 10
        svg.text(x0, ys, caption, 13, PAL["muted"], anchor="start")
    return svg


EDGE_STYLES_T = {"plain": (PAL["ink"], 1.2, None), "new": (PAL["new"], 3.0, None),
                 "path": (PAL["new"], 3.0, None), "dim": (PAL["dim"], 1.3, None),
                 "tree": (PAL["teal"], 2.6, None)}


# ABB
def bst_insert(root, k):
    path = []
    if root is None:
        return N(k), path
    x = root
    while True:
        path.append(x.key)
        if k < x.key:
            if x.left is None:
                x.left = N(k)
                break
            x = x.left
        else:
            if x.right is None:
                x.right = N(k)
                break
            x = x.right
    return root, path


def bst_build(keys):
    root = None
    for k in keys:
        root, _ = bst_insert(root, k)
    return root


def search_path(root, k):
    path = []
    x = root
    while x is not None and x.key != k:
        path.append(x.key)
        x = x.left if k < x.key else x.right
    if x is not None:
        path.append(x.key)
    return path, x is not None


def parent_map(root):
    par = {}

    def rec(n, p):
        if n is None:
            return
        par[n.key] = p
        rec(n.left, n)
        rec(n.right, n)
    rec(root, None)
    return par


def find(root, k):
    x = root
    while x is not None and x.key != k:
        x = x.left if k < x.key else x.right
    return x


# AVL
def rot_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    return y


def rot_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    return x


def avl_insert_trace(root, k):
    """Inserta k como en un ABB y rebalancea de abajo hacia arriba.

    Devuelve la raíz final y la lista de pasos (árbol, descripción, resaltados).
    """
    snaps = []
    root = copy_tree(root)
    root, path = bst_insert(root, k)
    snaps.append(dict(tree=copy_tree(root), kind="insert", key=k, path=path))
    # recorrer el camino de abajo hacia arriba
    for pk in reversed(path):
        par = parent_map(root)
        p = find(root, pk)
        f = fb(p)
        if abs(f) <= 1:
            continue
        snaps.append(dict(tree=copy_tree(root), kind="unbalanced", key=pk, fb=f))
        q = p.right if f == 2 else p.left
        fq = fb(q)
        if f == 2:
            if fq >= 0:
                case = "A" if fq == 1 else "B"
                new = rot_left(p)
                rots = [("izquierda", p.key)]
            else:
                case = "C"
                p.right = rot_right(q)
                snaps.append(dict(tree=None, kind="rot1", key=q.key))
                tmp_parent = par[p.key]
                new = rot_left(p)
                rots = [("derecha", q.key), ("izquierda", p.key)]
        else:
            if fq <= 0:
                case = "D" if fq == -1 else "E"
                new = rot_right(p)
                rots = [("derecha", p.key)]
            else:
                case = "F"
                p.left = rot_left(q)
                snaps.append(dict(tree=None, kind="rot1", key=q.key))
                new = rot_right(p)
                rots = [("izquierda", q.key), ("derecha", p.key)]
        pp = par[pk]
        if pp is None:
            root = new
        elif pp.left is p:
            pp.left = new
        else:
            pp.right = new
        # árbol intermedio de la rotación doble
        snaps = [s for s in snaps if s["kind"] != "rot1"]
        snaps.append(dict(tree=copy_tree(root), kind="rotated", key=pk, case=case, rots=rots,
                          fq=fq, newroot=new.key))
        break  # en la inserción basta un rebalanceo
    return root, snaps


def double_rotation_middle(root, pk, case):
    """Árbol después de la primera rotación de un caso C o F (para mostrarlo)."""
    root = copy_tree(root)
    p = find(root, pk)
    if case == "C":
        p.right = rot_right(p.right)
    else:
        p.left = rot_left(p.left)
    return root


def _rebalance_at(root, p, par):
    """Rebalancea el subárbol con raíz p (|fb(p)| = 2). Devuelve raíz, datos del paso."""
    f = fb(p)
    q = p.right if f == 2 else p.left
    fq = fb(q)
    mid = None
    if f == 2:
        if fq >= 0:
            case = "A" if fq == 1 else "B"
            new = rot_left(p)
            rots = [("izquierda", p.key)]
        else:
            case = "C"
            p.right = rot_right(q)
            mid = True
            new = rot_left(p)
            rots = [("derecha", q.key), ("izquierda", p.key)]
    else:
        if fq <= 0:
            case = "D" if fq == -1 else "E"
            new = rot_right(p)
            rots = [("derecha", p.key)]
        else:
            case = "F"
            p.left = rot_left(q)
            mid = True
            new = rot_right(p)
            rots = [("izquierda", q.key), ("derecha", p.key)]
    pp = par.get(p.key)
    if pp is None:
        root = new
    elif pp.left is p:
        pp.left = new
    else:
        pp.right = new
    return root, dict(case=case, rots=rots, fq=fq, newroot=new.key, q=q.key)


def avl_delete_trace(root, k):
    """Borra k como en un ABB (con el sucesor si tiene dos hijos) y rebalancea todos los
    nodos desbalanceados desde el padre del nodo que salió hasta la raíz."""
    snaps = []
    root = copy_tree(root)
    z = find(root, k)
    y = z
    if z.left is not None and z.right is not None:
        y = z.right
        while y.left is not None:
            y = y.left
    par = parent_map(root)
    py = par[y.key]
    x = y.left if y.left is not None else y.right
    if py is None:
        root = x
    elif py.left is y:
        py.left = x
    else:
        py.right = x
    succ_key = None
    if y is not z:
        succ_key = y.key
        z.key = y.key
    start = py.key if py is not None else None
    snaps.append(dict(tree=copy_tree(root), kind="delete", key=k, succ=succ_key, start=start,
                      nchildren=(0 if (z.left is None and z.right is None and y is z) else None)))
    if py is None:
        return root, snaps
    # camino de la raíz al padre del nodo que salió (objetos, para seguirlos tras rotar)
    path = []
    cur = root
    while cur is not None:
        path.append(cur)
        if cur is py:
            break
        cur = cur.left if py.key < cur.key else cur.right
    for node in reversed(path):
        if abs(fb(node)) <= 1:
            continue
        par = parent_map(root)
        before = copy_tree(root)
        f = fb(node)
        qn = node.right if f == 2 else node.left
        snaps.append(dict(tree=before, kind="unbalanced", key=node.key, fb=f))
        pk = node.key
        root, info = _rebalance_at(root, node, par)
        snaps.append(dict(tree=copy_tree(root), kind="rotated", key=pk, before=before, **info))
    return root, snaps


def avl_insert(root, k):
    """Inserción AVL sin traza (para construir árboles de partida)."""
    root, _ = avl_insert_trace(root, k)
    return root
