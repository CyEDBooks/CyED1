from common import *
from tviz import (from_tuple, draw, bst_insert, bst_build, search_path, parent_map, find,
                  copy_tree, nodes, height, N)

CLRS = (15, (6, (3, (2, None, None), (4, None, None)), (7, None, (13, (9, None, None), None))),
        (18, (17, None, None), (20, None, None)))
SEQ = [12, 5, 18, 2, 9, 15, 19, 13, 17]


def path_style(path, last_style="hl"):
    ns = {k: "hl" for k in path}
    es = {(a, b): "path" for a, b in zip(path, path[1:])}
    if path:
        ns[path[-1]] = last_style
    return ns, es


def build():
    p = Page("Unidad4-EstructurasRecursivas/ArbolesBinariosBusqueda")

    # Búsqueda binaria en un arreglo
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

    # Árbol de ejemplo (CLRS)
    root = from_tuple(CLRS)
    p.put("fig-clrs", f"![Árbol binario de búsqueda]({p.img('clrs', draw(root))})")

    def search_tabs(prefix, k):
        path, found = search_path(root, k)
        tabs = []
        for i in range(len(path)):
            ns, es = path_style(path[:i + 1])
            x = path[i]
            if x == k:
                ns[x] = "goal"
                txt = f"> ${k} = {x}$: **encontrado**."
            elif k < x:
                txt = f"> ${k} < {x}$: se sigue por el subárbol **izquierdo**."
            else:
                txt = f"> ${k} > {x}$: se sigue por el subárbol **derecho**."
            ghost = None
            if not found and i == len(path) - 1:
                side = "L" if k < x else "R"
                ghost = (x, side, "nil")
                txt += f" Pero ese subárbol es vacío: **{k} no está** en el árbol."
            svg = draw(root, node_style=ns, edge_style=es, ghost=ghost)
            tabs.append(f"![Buscar {k}, paso {i + 1}]({p.img(f'{prefix}-{i:02d}', svg)})\n\n{txt}")
        return steps(f"TREE-SEARCH(raíz, {k})", tabs)

    p.put("buscar-13", search_tabs("buscar13", 13))
    p.put("buscar-14", search_tabs("buscar14", 14))

    # Mínimo y máximo
    for name, side in (("min", "left"), ("max", "right")):
        path = []
        x = root
        while x is not None:
            path.append(x.key)
            x = getattr(x, side)
        ns, es = path_style(path, "goal")
        p.put(f"fig-{name}", f"![{name}]({p.img(name, draw(root, node_style=ns, edge_style=es))})")

    # Sucesor de 13 (sube) y de 6 (mínimo del derecho)
    par = parent_map(root)

    def succ_tabs(prefix, k):
        x = find(root, k)
        tabs = []
        ns = {k: "hl"}
        if x.right is not None:
            tabs.append((dict(ns), {}, f"> ${k}$ tiene subárbol derecho: el sucesor es el **mínimo** de ese "
                                       f"subárbol."))
            y = x.right
            path = [k]
            while y is not None:
                path.append(y.key)
                y = y.left
            ns2, es2 = path_style(path, "goal")
            tabs.append((ns2, es2, f"> Se baja a la derecha una vez y luego a la izquierda hasta el "
                                   f"final: el sucesor de ${k}$ es ${path[-1]}$."))
        else:
            tabs.append((dict(ns), {}, f"> ${k}$ **no** tiene subárbol derecho. Hay que subir hasta "
                                       f"encontrar un ancestro del que $x$ esté en el subárbol "
                                       f"**izquierdo**."))
            path = [k]
            y = par[k]
            cur = x
            while y is not None and cur is y.right:
                path.append(y.key)
                ns2, es2 = path_style(path)
                es2 = {(b, a): "path" for a, b in zip(path, path[1:])}
                tabs.append((ns2, es2, f"> ${cur.key}$ es hijo **derecho** de ${y.key}$: se sigue "
                                       f"subiendo."))
                cur, y = y, par[y.key]
            if y is not None:
                path.append(y.key)
                ns2, es2 = path_style(path, "goal")
                es2 = {(b, a): "path" for a, b in zip(path, path[1:])}
                tabs.append((ns2, es2, f"> ${cur.key}$ es hijo **izquierdo** de ${y.key}$: el "
                                       f"sucesor de ${k}$ es ${y.key}$."))
        out = []
        for i, (ns_, es_, txt) in enumerate(tabs):
            svg = draw(root, node_style=ns_, edge_style=es_)
            out.append(f"![Sucesor de {k}, paso {i + 1}]({p.img(f'{prefix}-{i:02d}', svg)})\n\n{txt}")
        return steps(f"TREE-SUCCESSOR({k})", out)

    p.put("succ-6", succ_tabs("succ6", 6))
    p.put("succ-13", succ_tabs("succ13", 13))

    # Inserción paso a paso
    t = None
    tabs = []
    for i, k in enumerate(SEQ):
        before = copy_tree(t)
        t, path = bst_insert(t, k)
        if before is None:
            svg = draw(t, node_style={k: "new"})
            txt = f"> El árbol está vacío: ${k}$ es la raíz."
        else:
            ns, es = path_style(path)
            last = path[-1]
            side = "L" if k < last else "R"
            ns[k] = "new"
            es[(last, k)] = "new"
            svg = draw(t, node_style=ns, edge_style=es)
            comps = ", ".join(f"${k} {'<' if k < x else '>'} {x}$" for x in path)
            txt = (f"> Insertar ${k}$: {comps}. Se cuelga como hijo "
                   f"**{'izquierdo' if side == 'L' else 'derecho'}** de ${last}$.")
        tabs.append(f"![Insertar {k}]({p.img(f'ins-{i:02d}', svg)})\n\n{txt}")
    tabs[6] += "\n\n> **¿Dónde quedará $13$?**"
    p.put("insertar", steps("Insertar " + ", ".join(map(str, SEQ)), tabs))
    p.put("ins-inorden", ", ".join(str(n.key) for n in nodes(t)))

    # Caso degenerado
    deg = bst_build([1, 2, 3, 4, 5])
    p.put("fig-degenerado", f"![Árbol degenerado]({p.img('degenerado', draw(deg))})")

    # Eliminación: tres casos sobre el árbol construido
    t = bst_build(SEQ)
    tabs = []
    # caso 1: 9
    tabs.append((copy_tree(t), {9: "bad"}, {}, "> **Caso 1.** $9$ no tiene hijos: basta con que su "
                 "padre ($5$) apunte a `nil` en su lugar."))
    find(t, 5).right = None
    tabs.append((copy_tree(t), {5: "hl"}, {}, "> Se quitó $9$."))
    # caso 2: 5 (un hijo: 2)
    tabs.append((copy_tree(t), {5: "bad", 2: "hl"}, {}, "> **Caso 2.** $5$ tiene un solo hijo ($2$): "
                 "se separa $5$ y su padre ($12$) pasa a apuntar directamente a $2$."))
    find(t, 12).left = find(t, 2)
    tabs.append((copy_tree(t), {2: "new"}, {(12, 2): "new"}, "> $2$ ocupa el lugar de $5$. El "
                 "árbol sigue siendo de búsqueda: $2 < 12$."))
    # caso 3: 12 (dos hijos)
    tabs.append((copy_tree(t), {12: "bad"}, {}, "> **Caso 3.** $12$ tiene dos hijos. **¿Cuál de "
                 "los nodos restantes debería ocupar su lugar?**"))
    tabs.append((copy_tree(t), {12: "bad", 18: "hl", 15: "hl", 13: "goal"},
                 {(12, 18): "path", (18, 15): "path", (15, 13): "path"},
                 "> Su **sucesor**: el mínimo del subárbol derecho, $13$. Es mayor que todo lo de "
                 "la izquierda y menor que todo lo demás de la derecha. Además, el sucesor no tiene "
                 "hijo izquierdo, así que quitarlo es el caso 1 o el 2."))
    find(t, 15).left = None
    find(t, 12).key = 13
    tabs.append((copy_tree(t), {13: "new"}, {}, "> Se separa el sucesor $13$ y su llave reemplaza "
                 "la de $12$."))
    out = []
    for i, (tt, ns, es, txt) in enumerate(tabs):
        out.append(f"![Eliminar, paso {i + 1}]({p.img(f'del-{i:02d}', draw(tt, node_style=ns, edge_style=es))})\n\n{txt}")
    p.put("eliminar", steps("TREE-DELETE: los tres casos", out))
    p.put("del-inorden", ", ".join(str(n.key) for n in nodes(t)))
    p.assemble("index.md")

    # ejercicios
    words = ["mango", "fresa", "uva", "banano", "kiwi", "pera", "cereza", "lima"]
    tw = bst_build(words)
    p.put("ex1-fig", f"![ABB de frutas]({p.img('ex1-frutas', draw(tw, dx=62, r=27, font=13))})")
    p.put("ex1-inorden", ", ".join(n.key for n in nodes(tw)))
    p.put("ex1-alt", str(height(tw)))
    ex2 = from_tuple(CLRS)
    p.put("fig-ex2", f"![ABB de ejemplo]({p.img('ex2', draw(ex2))})")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
