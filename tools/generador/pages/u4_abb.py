from common import *
from tviz import (from_tuple, draw, bst_insert, bst_build, search_path, parent_map, find,
                  copy_tree, nodes, height, N, halo, ring, badge)

# Árbol de Bedoya: las 27 llaves de la bolsa, organizadas
BED_KEYS = [24, 12, 43, 7, 19, 32, 48, 4, 9, 16, 21, 28, 38, 45, 51, 1, 5, 8, 10, 13, 18, 26, 29,
            33, 42, 50, 53]
BOLSA = [28, 38, 8, 7, 12, 19, 32, 4, 9, 16, 21, 1, 5, 45, 10, 33, 42, 50, 53, 13, 18, 26, 29,
         24, 43, 48, 51]
# Árboles de las diapositivas de Aristizábal (las llaves repetidas llevan espacios para
# distinguir los nodos; el espacio no se ve en el dibujo)
DEF_AND = ("20", ("1", None, None), ("30", ("24", ("21", None, None), ("26", None, None)),
                                     ("34", None, None)))
MINMAX = ("5", ("4", ("4 ", ("1", None, None), (" 4", None, None)), None),
          ("7", ("6", ("5 ", None, None), ("7 ", None, None)), ("8", None, None)))
SUCC_AND = ("8", ("7", ("4", ("1", None, None), ("6", None, None)), None),
            ("10", ("9", ("8 ", None, None), ("10 ", None, None)), ("12", None, None)))
INS_AND = [8, 4, 10, 3, 7, 12, 1]
CASO1 = [12, 10, 16, 3, 11, 13, 20, 1, 5]
CASO23 = [12, 10, 16, 3, 13, 18, 1, 5]


def path_style(path, last_style="hl"):
    ns = {k: "hl" for k in path}
    es = {(a, b): "path" for a, b in zip(path, path[1:])}
    if path:
        ns[path[-1]] = last_style
    return ns, es


def succ(root, k):
    x = find(root, k)
    par = parent_map(root)
    if x.right is not None:
        y = x.right
        while y.left is not None:
            y = y.left
        return y.key
    y = par[x.key]
    while y is not None and x is y.right:
        x, y = y, par[y.key]
    return None if y is None else y.key


def pred(root, k):
    x = find(root, k)
    par = parent_map(root)
    if x.left is not None:
        y = x.left
        while y.right is not None:
            y = y.right
        return y.key
    y = par[x.key]
    while y is not None and x is y.left:
        x, y = y, par[y.key]
    return None if y is None else y.key


def delete(root, k):
    """TREE-DELETE: devuelve la raíz nueva y el caso."""
    z = find(root, k)
    par = parent_map(root)
    nch = (z.left is not None) + (z.right is not None)
    if nch == 2:
        s = succ(root, k)
        root, _ = delete(root, s)
        find(root, k).key = s
        return root, 3
    child = z.left or z.right
    p = par[k]
    if p is None:
        return child, nch + 1
    if p.left is z:
        p.left = child
    else:
        p.right = child
    return root, nch + 1


# Cinco ejemplos, de muy fácil a difícil: construir el ABB y luego buscar o borrar.
NIVELES = ["muy fácil", "fácil", "medio", "medio", "difícil"]
EJEMPLOS = [
    dict(keys=[5, 3, 8], ops=[("buscar", 8)]),
    dict(keys=[50, 30, 70, 20, 40, 60], ops=[("buscar", 40), ("buscar", 65)]),
    dict(keys=[45, 25, 65, 15, 35, 55, 75, 30], ops=[("borrar", 15), ("borrar", 35)]),
    dict(keys=[40, 20, 60, 10, 30, 50, 70, 25, 35, 65], ops=[("borrar", 20)], compacto=True),
    dict(keys=[50, 30, 80, 20, 40, 70, 90, 35, 45, 60, 75, 65, 85], ops=[("borrar", 50)],
         compacto=True),
]


def _cmp(k, x):
    return f"{k} {'<' if k < x else '>'} {x}"


def _side(k, x):
    return "izquierda" if k < x else "derecha"


def _ring(keys):
    def over(svg, pos):
        for k in keys:
            ring(svg, *pos[k])
    return over


def ejemplo(p, i, ex):
    pref = f"ej{i}"
    tabs = []

    def add(svg, txt):
        tabs.append(f"![Ejemplo {i}, paso {len(tabs) + 1}]({p.img(f'{pref}-{len(tabs):02d}', svg)})"
                    f"\n\n> {txt}")

    keys = ex["keys"]
    acc = {"buscar": "busque", "borrar": "borre"}
    tail = " y ".join(f"{acc[op]} ${k}$" for op, k in ex["ops"])
    head = (f"**Ejemplo {i} ({NIVELES[i - 1]}).** Inserte, en este orden, "
            f"{', '.join(f'${k}$' for k in keys)} en un ABB vacío; luego {tail}.")
    t = None
    if ex.get("compacto"):
        t = bst_build(keys)
        order = {k: j + 1 for j, k in enumerate(keys)}
        add(draw(t, node_style={k: "tree" for k in keys},
                 over=lambda svg, pos: [badge(svg, *pos[k], order[k]) for k in keys]),
            f"Se insertan, en este orden, {', '.join(f'${k}$' for k in keys)}, con el mismo método "
            f"de los ejemplos anteriores: se compara con cada nodo desde la raíz y se baja a la "
            f"izquierda si es menor o a la derecha si es mayor. El número junto a cada nodo es su "
            f"orden de llegada: un nodo siempre llega **después** que su padre.")
    else:
        for k in keys:
            if t is None:
                t = N(k)
                add(draw(t, node_style={k: "new"}, over=_ring([k])),
                    f"Insertar ${k}$: el árbol está vacío, ${k}$ es la **raíz**.")
                continue
            path = search_path(t, k)[0]
            t, _ = bst_insert(t, k)
            ns = {x: "hl" for x in path}
            ns[k] = "new"
            es = {(a, b): "path" for a, b in zip(path, path[1:] + [k])}
            labels = {x: _cmp(k, x) for x in path}
            steps_txt = "; ".join(f"${_cmp(k, x)}$ → {_side(k, x)}" for x in path)
            add(draw(t, node_style=ns, edge_style=es, labels=labels, over=_ring([k])),
                f"Insertar ${k}$: {steps_txt}. Ese lugar está vacío: ${k}$ queda como hijo "
                f"**{'izquierdo' if k < path[-1] else 'derecho'}** de ${path[-1]}$.")
    for op, k in ex["ops"]:
        if op == "buscar":
            path, found = search_path(t, k)
            ns = {x: "hl" for x in path}
            es = {(a, b): "path" for a, b in zip(path, path[1:])}
            labels = {x: _cmp(k, x) for x in path if x != k}
            steps_txt = "; ".join(f"${_cmp(k, x)}$ → {_side(k, x)}" for x in path if x != k)
            if found:
                ns[k] = "goal"
                add(draw(t, node_style=ns, edge_style=es, labels=labels, over=_ring([k])),
                    f"Buscar ${k}$: {steps_txt + '; ' if steps_txt else ''}${k} = {k}$: "
                    f"**encontrado** con ${len(path)}$ comparaciones, sin mirar el resto del árbol.")
            else:
                last = path[-1]
                add(draw(t, node_style=ns, edge_style=es, labels=labels,
                         ghost=(last, "L" if k < last else "R", "nil")),
                    f"Buscar ${k}$: {steps_txt}. Ese subárbol es vacío (`nil`): **${k}$ no está** "
                    f"en el árbol. Bastaron ${len(path)}$ comparaciones para saberlo.")
        else:
            z = find(t, k)
            par = parent_map(t)
            nch = (z.left is not None) + (z.right is not None)
            pz = par[k]
            if nch == 0:
                add(draw(t, node_style={k: "bad"}, over=_ring([k])),
                    f"Borrar ${k}$: es **hoja** (caso 1). Basta con quitarla: su padre, "
                    f"${pz.key}$, pasa a apuntar a `nil`.")
                t, _ = delete(t, k)
                add(draw(t, node_style={pz.key: "hl"}),
                    f"${pz.key}$ se quedó sin hijo {'izquierdo' if k < pz.key else 'derecho'}. "
                    f"Nada más cambió.")
            elif nch == 1:
                ch = z.left or z.right
                add(draw(t, node_style={k: "bad"},
                         under=lambda svg, pos: halo(svg, pos, ch, "orange", "sube"),
                         over=_ring([k])),
                    f"Borrar ${k}$: tiene **un solo hijo**, ${ch.key}$ (caso 2). Se separa ${k}$ y "
                    f"su padre, ${pz.key}$, pasa a apuntar a ${ch.key}$, que sube con todo su "
                    f"subárbol.")
                t, _ = delete(t, k)
                es = {(pz.key, ch.key): "new"}
                add(draw(t, node_style={ch.key: "new"}, edge_style=es),
                    f"Sigue siendo ABB: todo lo que colgaba de ${k}$ estaba del mismo lado de "
                    f"${pz.key}$ que ${k}$.")
            else:
                sk = succ(t, k)
                path = [k]
                y = z.right
                while y is not None:
                    path.append(y.key)
                    y = y.left
                es = {(a, b): "path" for a, b in zip(path, path[1:])}
                add(draw(t, node_style={k: "bad", sk: "goal"}, edge_style=es,
                         under=lambda svg, pos: halo(svg, pos, z.right, "orange",
                                                     f"subárbol derecho de {k}"),
                         over=_ring([k, sk])),
                    f"Borrar ${k}$: tiene **dos hijos** (caso 3). Su lugar lo toma su **sucesor**, el "
                    f"mínimo del subárbol derecho: se baja a la derecha una vez y luego a la "
                    f"izquierda hasta el final, {' → '.join(f'${x}$' for x in path)}. El sucesor es "
                    f"${sk}$: mayor que todo lo de la izquierda de ${k}$ y menor que todo lo demás "
                    f"de la derecha.")
                sn = find(t, sk)
                if sn.right is not None:
                    sp = par[sk]
                    add(draw(t, node_style={sk: "bad", sn.right.key: "hl"},
                             under=lambda svg, pos: halo(svg, pos, sn.right, "orange", "sube"),
                             over=_ring([sk])),
                        f"Primero se separa ${sk}$ de donde está. No tiene hijo izquierdo (es un "
                        f"mínimo), pero sí derecho, ${sn.right.key}$: es el caso 2, ${sn.right.key}$ "
                        f"sube y queda colgando de ${sp.key}$.")
                t, _ = delete(t, k)
                add(draw(t, node_style={sk: "new"}, over=_ring([sk])),
                    f"La llave ${sk}$ reemplaza a ${k}$. El árbol tiene un nodo menos y sigue "
                    f"siendo ABB.")
    r = t
    ino = [n.key for n in nodes(r)]

    def under(svg, pos):
        halo(svg, pos, r.left, "blue", f"menores que {r.key}")
        halo(svg, pos, r.right, "orange", f"mayores que {r.key}")

    def over(svg, pos):
        ring(svg, *pos[r.key])
        ys = max(y for _, y in pos.values()) + 62
        x0 = min(x for x, _ in pos.values()) - 10
        draw_panel(svg, x0, ys, "Inorden:", [str(k) for k in ino], cell=30, wrap=12)
    add(draw(r, under=under, over=over),
        f"**¿Es ABB?** Todo lo que está a la izquierda de la raíz ${r.key}$ es menor y todo lo de la "
        f"derecha es mayor, y lo mismo pasa en cada subárbol. Comprobación rápida: el inorden sale "
        f"ordenado, {', '.join(f'${k}$' for k in ino)}.")
    assert ino == sorted(ino)
    return f"{head}\n\n" + steps("Paso a paso", tabs)


# El ABB de las 27 llaves es ancho: se dibuja compacto para que se vea a buen tamaño.
BIG = dict(dx=44, compact=True)


def build():
    p = Page("Unidad4-EstructurasRecursivas/ArbolesBinariosBusqueda")
    bed = bst_build(BED_KEYS)

    # La bolsa
    svg = SVG()
    svg.polygon([(-14, -20), (186, -20), (196, 320), (-24, 320)], "#e9d3ac", "#9c7a43", 1.4)
    cells = [(0, j) for j in range(3)] + [(r, j) for r in range(1, 7) for j in range(4)]
    for k, (r, j) in zip(BOLSA, cells):
        x, y = 22 + j * 44 + (22 if r == 0 else 0), 14 + r * 43
        svg.circle(x, y, 17, "#f5ead6", PAL["ink"], 1.2)
        svg.text(x, y + 5, k, 14)
    p.put("fig-bolsa", f"![Bolsa con 27 llaves]({p.img('bolsa', svg)})")
    p.put("fig-bed", f"![ABB con las 27 llaves]({p.img('bed', draw(bed, **BIG))})")

    def search_tabs(prefix, root, k):
        path, found = search_path(root, k)
        tabs = []
        for i in range(len(path)):
            ns, es = path_style(path[:i + 1])
            x = path[i]
            if x == k:
                ns[x] = "goal"
                txt = f"> ${k} = {x}$: **encontrado**, con {i + 1} comparaciones."
            elif k < x:
                txt = f"> ${k} < {x}$: se sigue por el subárbol **izquierdo**."
            else:
                txt = f"> ${k} > {x}$: se sigue por el subárbol **derecho**."
            ghost = None
            if not found and i == len(path) - 1:
                ghost = (x, "L" if k < x else "R", "nil")
                txt += f" Pero ese subárbol es vacío: **${k}$ no está** en el árbol."
            svg = draw(root, node_style=ns, edge_style=es, ghost=ghost, **BIG)
            tabs.append(f"![Buscar {k}, paso {i + 1}]({p.img(f'{prefix}-{i:02d}', svg)})\n\n{txt}")
        return steps(f"TREE-SEARCH(raíz, {k})", tabs)

    p.put("buscar-45", search_tabs("buscar45", bed, 45))
    p.put("buscar-11", search_tabs("buscar11", bed, 11))

    # Búsqueda binaria en una lista (Vargas)
    arr = [1, 2, 5, 6, 10, 22, 26, 32, 40, 50]
    lo, hi, k = 0, len(arr) - 1, 6
    tabs = []
    while lo <= hi:
        mid = (lo + hi) // 2
        svg = SVG()
        dim = [i for i in range(len(arr)) if i < lo or i > hi]
        draw_panel(svg, 0, 0, "Lista:", [str(x) for x in arr], new=[mid], dim=dim, cell=34)
        img = p.img(f"binaria-{len(tabs):02d}", svg)
        if arr[mid] == k:
            txt = f"> La mitad es ${arr[mid]}$: **es el buscado**. Se hicieron {len(tabs) + 1} comparaciones."
        elif k < arr[mid]:
            txt = f"> La mitad es ${arr[mid]}$. Como $6 < {arr[mid]}$, se descarta la mitad derecha."
        else:
            txt = f"> La mitad es ${arr[mid]}$. Como $6 > {arr[mid]}$, se descarta la mitad izquierda."
        tabs.append(f"![Búsqueda binaria, paso {len(tabs) + 1}]({img})\n\n{txt}")
        if arr[mid] == k:
            break
        if k < arr[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    p.put("binaria", steps("Búsqueda binaria de 6", tabs))

    # Definiciones
    defb = bst_build([10, 7, 14, 4, 8, 12])
    defa = from_tuple(DEF_AND)
    svg_b = draw(defb)
    svg_a = draw(defa)
    p.put("fig-def-bed", f"![ABB con llaves 10, 7, 14, 4, 8, 12]({p.img('def-bed', svg_b)})")
    p.put("fig-def-and", f"![ABB con raíz 20]({p.img('def-and', svg_a)})")

    # Mínimo y máximo (árbol con llaves repetidas)
    mm = from_tuple(MINMAX)
    p.put("fig-minmax", f"![ABB con llaves repetidas]({p.img('minmax', draw(mm))})")
    for name, side in (("min", "left"), ("max", "right")):
        path = []
        x = mm
        while x is not None:
            path.append(x.key)
            x = getattr(x, side)
        ns, es = path_style(path, "goal")
        p.put(f"fig-{name}", f"![{name}]({p.img(name, draw(mm, node_style=ns, edge_style=es))})")

    # Sucesor de 19 (mínimo del derecho) y de 21 (sube)
    par = parent_map(bed)

    def succ_tabs(prefix, k):
        x = find(bed, k)
        tabs = []
        ns = {k: "hl"}
        if x.right is not None:
            tabs.append((dict(ns), {}, f"> ${k}$ tiene subárbol derecho: el sucesor es el "
                                       f"**mínimo** de ese subárbol (`TREE-MINIMUM(right[x])`)."))
            y = x.right
            path = [k]
            while y is not None:
                path.append(y.key)
                y = y.left
            ns2, es2 = path_style(path, "goal")
            tabs.append((ns2, es2, f"> Se baja a la derecha una vez y luego a la izquierda hasta "
                                   f"el final: el sucesor de ${k}$ es ${path[-1]}$."))
        else:
            tabs.append((dict(ns), {}, f"> ${k}$ **no** tiene subárbol derecho. Hay que subir "
                                       f"mientras se llegue desde un hijo **derecho**."))
            path = [k]
            y = par[k]
            cur = x
            while y is not None and cur is y.right:
                path.append(y.key)
                ns2, _ = path_style(path)
                es2 = {(b, a): "path" for a, b in zip(path, path[1:])}
                tabs.append((ns2, es2, f"> ${cur.key}$ es hijo **derecho** de ${y.key}$: se sigue "
                                       f"subiendo."))
                cur, y = y, par[y.key]
            path.append(y.key)
            ns2, _ = path_style(path, "goal")
            es2 = {(b, a): "path" for a, b in zip(path, path[1:])}
            tabs.append((ns2, es2, f"> ${cur.key}$ es hijo **izquierdo** de ${y.key}$: el "
                                   f"sucesor de ${k}$ es ${y.key}$."))
        out = []
        for i, (ns_, es_, txt) in enumerate(tabs):
            svg = draw(bed, node_style=ns_, edge_style=es_, **BIG)
            out.append(f"![Sucesor de {k}, paso {i + 1}]({p.img(f'{prefix}-{i:02d}', svg)})\n\n{txt}")
        return steps(f"TREE-SUCCESSOR({k})", out)

    p.put("succ-19", succ_tabs("succ19", 19))
    p.put("succ-21", succ_tabs("succ21", 21))

    # TREE-INSERT(z) con key[z] = 5, con la traza de y y x
    t = bst_build(INS_AND)
    path = search_path(t, 5)[0]
    rows = [["inicio", "NIL", "8", ""]]
    tabs = []
    svg = draw(t, node_style={8: "hl"})
    tabs.append(f"![TREE-INSERT, inicio]({p.img('ins-00', svg)})\n\n> Líneas 1 y 2: $y = $ NIL, "
                f"$x = $ la raíz $8$.\n\n" + md_table(["Iteración", "y", "x", "Comparación"], rows))
    for i, xk in enumerate(path):
        child = find(t, xk).left if 5 < xk else find(t, xk).right
        nx = child.key if child else "NIL"
        rows.append([str(i + 1), str(xk), str(nx), f"${5} {'<' if 5 < xk else '>'} {xk}$"])
        ns, es = path_style(path[:i + 1])
        ghost = None if child else (xk, "L" if 5 < xk else "R", "nil")
        svg = draw(t, node_style=ns, edge_style=es, ghost=ghost)
        rr = [r[:] for r in rows]
        rr[-1] = [hl(c) if c and not c.startswith("$") else c for c in rr[-1]]
        txt = (f"> $y = {xk}$. Como $5 {'<' if 5 < xk else '>'} {xk}$, $x$ baja al hijo "
               f"**{'izquierdo' if 5 < xk else 'derecho'}**: $x = $ {nx}.")
        tabs.append(f"![TREE-INSERT, iteración {i + 1}]({p.img(f'ins-{i + 1:02d}', svg)})\n\n{txt}\n\n"
                    + md_table(["Iteración", "y", "x", "Comparación"], rr))
    t, _ = bst_insert(t, 5)
    ns, es = path_style(path)
    ns[5] = "new"
    es[(path[-1], 5)] = "new"
    svg = draw(t, node_style=ns, edge_style=es)
    tabs.append(f"![TREE-INSERT, final]({p.img(f'ins-{len(path) + 1:02d}', svg)})\n\n> $x$ es NIL: "
                f"termina el ciclo. Línea 8: $p[z] = y = {path[-1]}$. Como $5 < {path[-1]}$, "
                f"$z$ queda como hijo **izquierdo** de ${path[-1]}$ (línea 12).")
    p.put("insertar", steps("TREE-INSERT(T, z) con key[z] = 5", tabs))

    deg = bst_build([1, 2, 3, 4, 5])
    p.put("fig-degenerado", f"![Árbol degenerado]({p.img('degenerado', draw(deg))})")

    # Eliminación: los tres casos con los árboles de Aristizábal
    t1 = bst_build(CASO1)
    after1, _ = delete(copy_tree(t1), 5)
    tabs = [f"![Caso 1]({p.img('caso1-0', draw(t1, node_style={5: 'bad', 3: 'hl'}))})\n\n> $z = 5$ "
            f"es hoja.",
            f"![Caso 1, resultado]({p.img('caso1-1', draw(after1, node_style={3: 'hl'}))})\n\n> El "
            f"padre de $z$ debe ahora apuntar a `nil`: $3$ se queda sin hijo derecho."]
    p.put("caso1", steps("Caso 1: borrar 5", tabs))
    t2 = bst_build(CASO23)
    after2, _ = delete(copy_tree(t2), 10)
    tabs = [f"![Caso 2]({p.img('caso2-0', draw(t2, node_style={10: 'bad', 3: 'hl'}))})\n\n> $z = 10$ "
            f"tiene un solo hijo, $3$.",
            f"![Caso 2, resultado]({p.img('caso2-1', draw(after2, node_style={3: 'new'}, edge_style={(12, 3): 'new'}))})"
            f"\n\n> Se separa $z$ del árbol: su padre, $12$, pasa a apuntar a su único hijo, $3$, "
            f"que sube con todo su subárbol. Sigue siendo un ABB: todo lo que estaba debajo de "
            f"$10$ era menor que $12$."]
    p.put("caso2", steps("Caso 2: borrar 10", tabs))
    after3, _ = delete(copy_tree(t2), 12)
    tabs = [f"![Caso 3]({p.img('caso3-0', draw(t2, node_style={12: 'bad'}))})\n\n> $z = 12$ tiene "
            f"dos hijos. **¿Cuál de los nodos restantes debería ocupar el lugar del nodo a borrar?**",
            f"![Caso 3, sucesor]({p.img('caso3-1', draw(t2, node_style={12: 'bad', 16: 'hl', 13: 'goal'}, edge_style={(12, 16): 'path', (16, 13): 'path'}))})"
            f"\n\n> Su **sucesor** $y = 13$, el mínimo del subárbol derecho: es mayor que todo lo de "
            f"la izquierda de $12$ y menor que todo lo demás de la derecha. El sucesor no tiene "
            f"hijo izquierdo, así que separarlo es el caso 1 o el caso 2.",
            f"![Caso 3, resultado]({p.img('caso3-2', draw(after3, node_style={13: 'new'}))})\n\n> Se "
            f"separa (elimina) su sucesor $y$ del árbol y se reemplaza el contenido de $z$ con el "
            f"de $y$: la raíz ahora tiene la llave $13$."]
    p.put("caso3", steps("Caso 3: borrar 12", tabs))
    for i, ex in enumerate(EJEMPLOS, 1):
        p.put(f"ej{i}", ejemplo(p, i, ex))
    p.assemble("index.md")

    # Ejercicios 1 y 2: estructura dada
    est1 = bst_build([12, 7, 23, 3, 9, 17, 25])
    est2 = bst_build([25, 10, 38, 7, 17, 29, 42, 3, 8, 14, 21, 27, 34])

    def blank(root, keep=()):
        k = [0]

        def rec(n):
            if n is None:
                return None
            k[0] += 1
            lab = n.key if n.key in keep else " " * k[0]
            return N(lab, rec(n.left), rec(n.right))
        return rec(root)
    p.put("fig-est1", f"![Estructura]({p.img('est1', draw(blank(est1)))})")
    p.put("fig-est1-sol", f"![Solución]({p.img('est1-sol', draw(est1))})")
    p.put("fig-est2", f"![Estructura]({p.img('est2', draw(blank(est2, keep=(25, 17)), dx=34))})")
    p.put("fig-est2-sol", f"![Solución]({p.img('est2-sol', draw(est2, dx=34))})")
    words = ["ipod touch", "ipad", "playstation", "apple tv", "iphone", "nintendo wii", "smart tv"]
    tw = bst_build(words)
    assert [n.key for n in nodes(tw)] == sorted(words)
    tw, _ = bst_insert(tw, "kindle")

    def as_nary(n):
        return (n.key, [as_nary(c) for c in (n.left, n.right) if c is not None])
    pos, E = tree_pos(as_nary(tw), 70, 58)
    p.put("fig-ex3-sol", gfig(p, "ex3-sol", pos, E, node_style={"kindle": "new"},
                              edge_style={("nintendo wii", "kindle"): "new"}))
    st = from_tuple(SUCC_AND)
    p.put("fig-ex4", f"![ABB con llaves repetidas]({p.img('ex4', draw(st))})")
    for k in (10, 29, 42):
        p.put(f"ex5-s{k}", f"${succ(bed, k)}$")
    for k in (24, 32):
        p.put(f"ex5-p{k}", f"${pred(bed, k)}$")
    # Ejercicio 6: trazas de TREE-INSERT
    t = bst_build(INS_AND + [5])
    parts = []
    for k in (6, 11):
        path = search_path(t, k)[0]
        rows = [["inicio", "NIL", str(path[0])]]
        for i, xk in enumerate(path):
            child = find(t, xk).left if k < xk else find(t, xk).right
            rows.append([str(i + 1), str(xk), str(child.key) if child else "NIL"])
        last = path[-1]
        side = "izquierdo" if k < last else "derecho"
        parts.append(f"Insertar ${k}$:\n\n" + md_table(["Iteración", "y", "x"], rows)
                     + f"\n\n${k}$ queda como hijo **{side}** de ${last}$.")
        t, _ = bst_insert(t, k)
    parts.append(f"![Árbol final]({p.img('ex6-sol', draw(t, node_style={6: 'new', 11: 'new'}))})")
    p.put("ex6-sol", "\n\n".join(parts))
    # Ejercicio 7
    t = bst_build(BED_KEYS)
    cases = []
    for k in (1, 4, 24):
        t, c = delete(t, k)
        cases.append(c)
    assert cases == [1, 2, 3]
    p.put("ex7-sol", f"![Árbol final]({p.img('ex7-sol', draw(t, node_style={26: 'new', 5: 'new'}, **BIG))})")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
