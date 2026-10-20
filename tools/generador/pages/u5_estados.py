from common import *
from algos import tree_search, explicit_tree, minimax
from sviz import layout, search_step_svg, draw_board
from figlib import NODE_STYLES, _shorten

T1 = ("A", [("B", [("E", []), ("F", [("K", []), ("L", [])])]),
            ("C", [("G", []), ("H", [])]),
            ("D", [("I", [("M", [])]), ("J", [])])])
T2 = ("A", [("B", [("D", [("H", []), ("I", [])]), ("E", [])]),
            ("C", [("F", [("J", []), ("K", [])]), ("G", [("L", [])])])])

ROM = [("Arad", "Zerind", 75), ("Arad", "Sibiu", 140), ("Arad", "Timisoara", 118),
       ("Zerind", "Oradea", 71), ("Oradea", "Sibiu", 151), ("Timisoara", "Lugoj", 111),
       ("Lugoj", "Mehadia", 70), ("Mehadia", "Drobeta", 75), ("Drobeta", "Craiova", 120),
       ("Craiova", "Rimnicu", 146), ("Craiova", "Pitesti", 138), ("Sibiu", "Fagaras", 99),
       ("Sibiu", "Rimnicu", 80), ("Rimnicu", "Pitesti", 97), ("Fagaras", "Bucarest", 211),
       ("Pitesti", "Bucarest", 101)]
ROM_SH = {"Arad": "Ara", "Zerind": "Zer", "Oradea": "Ora", "Sibiu": "Sib", "Timisoara": "Tim",
          "Lugoj": "Lug", "Mehadia": "Meh", "Drobeta": "Dro", "Craiova": "Cra", "Rimnicu": "Rim",
          "Fagaras": "Fag", "Pitesti": "Pit", "Bucarest": "Buc"}
ROM_POS = scale({"Oradea": (0.9, 0), "Zerind": (0.4, 0.8), "Arad": (0, 1.7), "Sibiu": (1.9, 1.5),
                 "Fagaras": (3.3, 1.5), "Timisoara": (0.1, 2.9), "Rimnicu": (2.3, 2.5),
                 "Lugoj": (1.0, 3.4), "Pitesti": (3.3, 3.1), "Mehadia": (1.0, 4.2),
                 "Bucarest": (4.5, 3.6), "Drobeta": (0.9, 5.0), "Craiova": (2.6, 4.8)}, 95)


def letters_steps(p, prefix, tree, goals, mode, draw=True):
    succ = explicit_tree(tree)
    nodes, exp, goal, snaps = tree_search(tree[0], succ, lambda s: s in goals, mode, "none")
    # posiciones con el árbol COMPLETO para que nada se mueva entre pasos
    full_nodes, _, _, _ = tree_search(tree[0], succ, lambda s: False, "bfs", "none")
    fpos, fch = layout(full_nodes, 56, 66)
    pos = {}
    for n in nodes:
        # emparejar por etiqueta (las etiquetas son únicas)
        fid = next(f["id"] for f in full_nodes if f["state"] == n["state"])
        pos[n["id"]] = fpos[fid]
    title = "Cola:" if mode == "bfs" else "Pila:"
    out = []
    rows = []
    for k, sn in enumerate(snaps):
        upto = max([0] + [i for s in snaps[:k + 1] for i in s["created"]])
        svg = search_step_svg(nodes, pos, None, sn, upto, lambda n: n["state"],
                              frontier_title=title)
        # marcar metas con doble borde
        for n in nodes:
            if n["id"] <= upto and n["state"] in goals:
                x, y = pos[n["id"]]
                svg.circle(x, y, 24, "none", PAL["goal"], 1.6)
        img = p.img(f"{prefix}-{k:02d}", svg) if draw else ""
        body = [f"![Paso {k + 1}]({img})", ""]
        fr = " ".join(nodes[i]["state"] for i in sn["frontier"])
        if k == 0:
            body.append(f"> Se crea el nodo raíz {tree[0]} y se mete en la {'cola' if mode == 'bfs' else 'pila'}. "
                        f"Las metas ({' y '.join(sorted(goals))}) tienen doble borde verde.")
            rows.append([fr or "∅", "—"])
        else:
            cur = nodes[sn["current"]]["state"]
            if sn.get("goal"):
                body.append(f"> Se extrae **{cur}** y se expande: **es meta**. La búsqueda termina "
                            f"y no se crean sus hijos.")
                rows.append([fr or "∅", f"Extraer {cur}: es meta"])
            elif sn["created"]:
                kids = ", ".join(nodes[i]["state"] for i in sn["created"])
                where = "al final de la cola" if mode == "bfs" else "al tope de la pila"
                body.append(f"> Se extrae **{cur}** y se expande: no es meta, así que se crean sus "
                            f"hijos {kids} y se meten {where}.")
                rows.append([fr or "∅", f"Extraer {cur}, meter hijos de {cur}"])
            else:
                body.append(f"> Se extrae **{cur}** y se expande: no es meta y no tiene hijos.")
                rows.append([fr or "∅", f"Extraer {cur}"])
        rows_hl = [r[:] for r in rows]
        rows_hl[-1] = [hl(rows_hl[-1][0]), hl(rows_hl[-1][1])]
        body += ["", md_table(["Estado de la " + ("cola" if mode == "bfs" else "pila"), "Iteración"],
                              rows_hl)]
        out.append("\n".join(body))
    created = [n["state"] for n in nodes]
    expanded = [nodes[i]["state"] for i in exp]
    return out, nodes[goal]["state"] if goal is not None else None, created, expanded


def jarras_succ(s):
    a, b = s
    out = [("Llenar 4", (4, b)), ("Llenar 3", (a, 3)), ("Vaciar 4", (0, b)), ("Vaciar 3", (a, 0))]
    t = min(a, 3 - b)
    out.append(("4→3", (a - t, b + t)))
    t = min(b, 4 - a)
    out.append(("3→4", (a + t, b - t)))
    return [(o, x) for o, x in out if x != s]


def puzzle_succ(b):
    b = [list(r) for r in b]
    i, j = next((i, j) for i in range(3) for j in range(3) if b[i][j] == 0)
    out = []
    for op, di, dj in (("↑", -1, 0), ("↓", 1, 0), ("←", 0, -1), ("→", 0, 1)):
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            c = [r[:] for r in b]
            c[i][j], c[ni][nj] = c[ni][nj], 0
            out.append((op, tuple(tuple(r) for r in c)))
    return out


GOAL = ((1, 2, 3), (4, 5, 6), (7, 8, 0))


def build():
    p = Page("Unidad5-Grafos/BusquedaEspacioEstados")

    # jarras: árbol completo por BFS (sin repetir estados)
    nodes, exp, goal, snaps = tree_search((0, 0), jarras_succ, lambda s: s[0] == 2, "bfs", "global")
    pos, ch = layout(nodes, 58, 70)
    lab = lambda n: f"{n['state'][0]},{n['state'][1]}"
    out = []
    for k, sn in enumerate(snaps):
        upto = max([0] + [i for s in snaps[:k + 1] for i in s["created"]])
        svg = search_step_svg(nodes, pos, ch, sn, upto, lab, r=21, show_ops=False)
        img = p.img(f"jarras-{k:02d}", svg)
        body = [f"![Jarras, paso {k + 1}]({img})", ""]
        if k == 0:
            body.append("> El estado inicial es $(0,0)$: las dos jarras vacías.")
        else:
            cur = nodes[sn["current"]]
            if sn.get("goal"):
                body.append(f"> Se expande $({lab(cur)})$: la jarra de 4 tiene **2 litros**. Es meta.")
            elif sn["created"]:
                kids = ", ".join(f"$({lab(nodes[i])})$ ({nodes[i]['op']})" for i in sn["created"])
                body.append(f"> Se expande $({lab(cur)})$ y se crean los estados nuevos: {kids}.")
            else:
                body.append(f"> Se expande $({lab(cur)})$: todos sus sucesores ya fueron creados antes. "
                            f"No se crea nada.")
        out.append("\n".join(body))
    p.put("jarras", steps("Búsqueda por amplitud en el problema de las jarras", out))
    path = []
    g = goal
    while g is not None:
        path.append(nodes[g])
        g = nodes[g]["parent"]
    path = path[::-1]
    p.put("jarras-sol", " → ".join(
        (f"$({lab(n)})$" if n["op"] is None else f"**{n['op']}** $({lab(n)})$") for n in path))
    p.put("jarras-n", str(len(nodes)))

    # árbol de letras: BFS y DFS
    st, g1, cr, ex = letters_steps(p, "t1-bfs", T1, {"G", "L"}, "bfs")
    p.put("t1-bfs", steps("Búsqueda preferente por amplitud", st))
    p.put("t1-bfs-res", f"Encuentra la meta **{g1}**. Nodos creados: {', '.join(cr)}. "
                        f"Nodos expandidos: {', '.join(ex)}.")
    st, g2, cr, ex = letters_steps(p, "t1-dfs", T1, {"G", "L"}, "dfs")
    p.put("t1-dfs", steps("Búsqueda preferente por profundidad", st))
    p.put("t1-dfs-res", f"Encuentra la meta **{g2}**. Nodos creados: {', '.join(cr)}. "
                        f"Nodos expandidos: {', '.join(ex)}.")

    # 8-puzzle
    start = ((1, 2, 3), (4, 0, 6), (7, 5, 8))
    nodes, exp, goal, snaps = tree_search(start, puzzle_succ, lambda s: s == GOAL, "bfs", "path")
    pos, ch = layout(nodes, 74, 96)
    out = []
    for k, sn in enumerate(snaps):
        upto = max([0] + [i for s in snaps[:k + 1] for i in s["created"]])
        svg = search_step_svg(nodes, pos, ch, sn, upto, None, kind="board", show_ops=True)
        img = p.img(f"puzzle-{k:02d}", svg)
        body = [f"![8-puzzle, paso {k + 1}]({img})", ""]
        if k == 0:
            body.append("> Estado inicial. Los operadores mueven el **espacio** en el orden "
                        "↑, ↓, ←, →.")
        else:
            cur = nodes[sn["current"]]
            op = f" (se llegó con {cur['op']})" if cur["op"] else ""
            if sn.get("goal"):
                body.append(f"> Se expande el nodo{op}: es la configuración meta. Termina.")
            else:
                ops = ", ".join(nodes[i]["op"] for i in sn["created"])
                body.append(f"> Se expande el nodo{op}: no es meta; se crean sus hijos con {ops}. "
                            f"No se crea el hijo que devolvería al estado del padre.")
        out.append("\n".join(body))
    p.put("puzzle", steps("Búsqueda por amplitud en el 8-puzzle", out))
    p.put("puzzle-n", f"{len(nodes)} nodos creados y {len(exp)} expandidos")
    svg = SVG()
    draw_board(svg, 0, 0, start, cell=26)
    svg.text(0, 56, "Inicial", 13, PAL["muted"])
    draw_board(svg, 130, 0, GOAL, "goal", cell=26)
    svg.text(130, 56, "Meta", 13, PAL["muted"])
    p.put("fig-puzzle", f"![8-puzzle inicial y meta]({p.img('puzzle-ini', svg)})")

    # NIM con 4 fichas
    nim = [dict(id=0, state=4, parent=None, op=None, depth=0)]
    frontier = [0]
    while frontier:
        v = frontier.pop(0)
        for k in (1, 2, 3):
            if k <= nim[v]["state"]:
                nid = len(nim)
                nim.append(dict(id=nid, state=nim[v]["state"] - k, parent=v, op=f"−{k}",
                                depth=nim[v]["depth"] + 1))
                frontier.append(nid)
    pos, ch = layout(nim, 58, 80)
    # J1 juega en profundidad par. Hoja (0 fichas): el que debería jugar gana.
    val, order = minimax(nim, ch, lambda v, maxi: +1 if maxi else -1)
    maxd = max(n["depth"] for n in nim)
    out = []

    def nim_svg(visible_depth, valued, newv):
        svg = SVG()
        for n in nim:
            if n["parent"] is not None and n["depth"] <= visible_depth:
                (x1, y1), (x2, y2) = pos[n["parent"]], pos[n["id"]]
                sx1, sy1, sx2, sy2 = _shorten(x1, y1, x2, y2, 17, 17)
                svg.line(sx1, sy1, sx2, sy2, PAL["muted"], 1.3)
                lx, ly = x1 + (x2 - x1) * 0.42, y1 + (y2 - y1) * 0.42
                svg.text(lx + (6 if x2 > x1 else (-6 if x2 < x1 else 6)), ly + 4, n["op"], 10,
                         PAL["muted"], anchor="start" if x2 >= x1 else "end", bg=True)
        for n in nim:
            if n["depth"] > visible_depth:
                continue
            x, y = pos[n["id"]]
            i = n["id"]
            if i in valued:
                st = "goal" if val[i] > 0 else "bad"
                if i in newv:
                    st = "hl"
            else:
                st = "new" if (n["depth"] == visible_depth and not valued) else "plain"
            fill, stroke, tc, width = NODE_STYLES[st]
            svg.circle(x, y, 16, fill, stroke, width)
            svg.text(x, y + 5, n["state"], 13, tc, bold=(st in ("new", "hl")))
            if i in valued:
                svg.text(x + 20, y - 12, "+1" if val[i] > 0 else "−1", 11,
                         PAL["new"] if i in newv else (PAL["goal"] if val[i] > 0 else PAL["bad"]),
                         bold=i in newv)
        x0 = min(x for x, _ in pos.values()) - 30
        for d in range(min(visible_depth, maxd) + 1):
            svg.text(x0, d * 80 + 5, "J1" if d % 2 == 0 else "J2", 12, PAL["muted"], anchor="end",
                     bold=True)
        return svg

    for d in range(maxd + 1):
        img = p.img(f"nim-{len(out):02d}", nim_svg(d, set(), set()))
        cnt = sum(1 for n in nim if n["depth"] == d)
        if d == 0:
            txt = "> La raíz: hay 4 fichas y juega J1."
        else:
            txt = (f"> Nivel {d}: juega {'J1' if d % 2 == 0 else 'J2'}. Se agregan los {cnt} estados "
                   f"posibles; cada arista dice cuántas fichas se tomaron.")
        out.append(f"![NIM, paso {len(out) + 1}]({img})\n\n{txt}")
    leaves = {n["id"] for n in nim if not ch.get(n["id"])}
    img = p.img(f"nim-{len(out):02d}", nim_svg(maxd, leaves, leaves))
    out.append(f"![NIM, paso {len(out) + 1}]({img})\n\n> Las hojas tienen $0$ fichas: el jugador "
               "anterior tomó la última y **perdió**. Si en la hoja le toca a J1, J1 gana ($+1$); si "
               "le toca a J2, J1 pierde ($-1$).")
    valued = set(leaves)
    for v in order:
        if v in leaves:
            continue
        valued.add(v)
        n = nim[v]
        who = "J1" if n["depth"] % 2 == 0 else "J2"
        kids = ", ".join(("+1" if val[c] > 0 else "−1") for c in ch[v])
        rule = "el **máximo**" if who == "J1" else "el **mínimo**"
        img = p.img(f"nim-{len(out):02d}", nim_svg(maxd, valued, {v}))
        out.append(f"![NIM, paso {len(out) + 1}]({img})\n\n> Nodo con {n['state']} fichas, juega "
                   f"{who}. Sus hijos valen {kids}; {who} escoge {rule}: "
                   f"${'+1' if val[v] > 0 else '-1'}$.")
    p.put("nim", steps("Árbol del juego NIM con 4 fichas", out))
    p.put("nim-raiz", "+1" if val[0] > 0 else "−1")
    best = [c for c in ch[0] if val[c] == val[0]]
    p.put("nim-jugada", ", ".join(f"tomar {4 - nim[c]['state']}" for c in best))
    p.put("nim-n", str(len(nim)))

    p.assemble("index.md")

    # ejercicios
    st, g1, cr, ex = letters_steps(p, "t2-bfs", T2, {"I", "F"}, "bfs", draw=False)
    p.put("t2-bfs-res", f"Encuentra **{g1}**. Creados: {', '.join(cr)}. Expandidos: {', '.join(ex)}.")
    st, g2, cr, ex = letters_steps(p, "t2-dfs", T2, {"I", "F"}, "dfs", draw=False)
    p.put("t2-dfs-res", f"Encuentra **{g2}**. Creados: {', '.join(cr)}. Expandidos: {', '.join(ex)}.")
    full, _, _, _ = tree_search("A", explicit_tree(T2), lambda s: False, "bfs", "none")
    fpos, _ = layout(full, 56, 66)
    svg = SVG()
    for n in full:
        if n["parent"] is not None:
            (x1, y1), (x2, y2) = fpos[n["parent"]], fpos[n["id"]]
            svg.line(x1, y1 + 21, x2, y2 - 21, PAL["muted"], 1.5)
    for n in full:
        x, y = fpos[n["id"]]
        svg.circle(x, y, 20, PAL["white"], PAL["ink"], 1.6)
        svg.text(x, y + 5, n["state"], 14)
        if n["state"] in ("I", "F"):
            svg.circle(x, y, 24, "none", PAL["goal"], 1.6)
    p.put("fig-t2", f"![Árbol de búsqueda con metas I y F]({p.img('t2', svg)})")

    V = [ROM_SH[v] for v in ROM_POS]
    E = [(ROM_SH[a], ROM_SH[b], w) for a, b, w in ROM]
    POS = {ROM_SH[k]: v for k, v in ROM_POS.items()}
    svg = SVG()
    draw_graph(svg, POS, E, False, r=21)
    p.put("fig-rom", f"![Mapa de Rumania]({p.img('rumania', svg)})")
    adj = {}
    for a, b, _ in E:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    orden = ["Ara", "Zer", "Ora", "Sib", "Tim", "Lug", "Meh", "Dro", "Cra", "Rim", "Fag", "Pit", "Buc"]
    succ = lambda s: [(None, x) for x in sorted(adj[s], key=orden.index)]
    nodes, exp, goal, snaps = tree_search("Sib", succ, lambda s: s == "Buc", "bfs", "path")
    p.put("rom-exp", ", ".join(nodes[i]["state"] for i in exp))
    path = []
    g = goal
    while g is not None:
        path.append(nodes[g]["state"])
        g = nodes[g]["parent"]
    p.put("rom-path", " → ".join(path[::-1]))
    p.put("rom-n", str(len(nodes)))
    nodes2, exp2, goal2, _ = tree_search("Sib", succ, lambda s: s == "Buc", "bfs", "none")
    p.put("rom-n2", str(len(nodes2)))
    p.put("rom-exp2", str(len(exp2)))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
