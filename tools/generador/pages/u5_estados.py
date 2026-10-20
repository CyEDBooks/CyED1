from common import *
from algos import tree_search, explicit_tree, minimax
from sviz import layout, search_step_svg, draw_board
from figlib import NODE_STYLES, _shorten

# Árboles de las diapositivas de Bedoya
T1 = ("H", [("A", [("D", [("K", []), ("L", [])]), ("E", [])]), ("B", [("F", [])]),
            ("C", [("G", []), ("J", [])])])
T2 = ("Z", [("W", [("P", [("K", []), ("L", [])])]), ("X", [("F", []), ("E", [("G", []), ("H", [])])]),
            ("T", [("A", []), ("C", [("D", []), ("I", [])]), ("B", [])])])
T3 = ("Z", [("W", [("P", [("Q", []), ("R", [])]), ("Y", [("K", []), ("L", [])])]),
            ("X", [("F", []), ("E", [("G", [])])]), ("T", [("A", []), ("C", [("D", []), ("I", [])])])])

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
    for op, di, dj in (("→", 0, 1), ("↓", 1, 0), ("←", 0, -1), ("↑", -1, 0)):
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            c = [r[:] for r in b]
            c[i][j], c[ni][nj] = c[ni][nj], 0
            out.append((op, tuple(tuple(r) for r in c)))
    return out


GOAL = ((1, 2, 3), (4, 5, 6), (7, 8, 0))


def grid_succ(walls, n_rows, n_cols, order):
    moves = {"←": (0, -1), "→": (0, 1), "↑": (-1, 0), "↓": (1, 0)}

    def succ(s):
        out = []
        for op in order:
            di, dj = moves[op]
            r, c = s[0] + di, s[1] + dj
            if 0 <= r < n_rows and 0 <= c < n_cols and (r, c) not in walls:
                out.append((op, (r, c)))
        return out
    return succ


def grid_fig(walls, n_rows, n_cols, start, goal, start_lab="", goal_lab=""):
    svg = SVG()
    cell = 34
    for j in range(n_cols):
        svg.text(40 + j * cell + cell / 2, 14, j, 13)
    for i in range(n_rows):
        svg.text(28, 26 + i * cell + cell / 2 + 4, i, 13, anchor="end")
        for j in range(n_cols):
            fill = PAL["white"]
            if (i, j) in walls:
                fill = "#9a9a9a"
            if (i, j) == start:
                fill = "#c00000" if not start_lab else "#b5e61d"
            if (i, j) == goal:
                fill = "#ffff00"
            svg.rect(40 + j * cell, 22 + i * cell, cell, cell, fill, PAL["ink"], 1.0, rx=0)
            lab = start_lab if (i, j) == start else (goal_lab if (i, j) == goal else "")
            if lab:
                svg.text(40 + j * cell + cell / 2, 22 + i * cell + cell / 2 + 4, lab, 11, PAL["ink"])
    return svg


def path_of(nodes, g):
    out = []
    while g is not None:
        out.append(nodes[g])
        g = nodes[g]["parent"]
    return out[::-1]


def search_tabs(p, prefix, nodes, exp, goal, snaps, lab, r=21, dx=62, dy=74, what="estado"):
    pos, ch = layout(nodes, dx, dy)
    out = []
    for k, sn in enumerate(snaps):
        upto = max([0] + [i for s_ in snaps[:k + 1] for i in s_["created"]])
        svg = search_step_svg(nodes, pos, ch, sn, upto, lab, r=r, show_ops=True)
        body = [f"![Paso {k + 1}]({p.img(f'{prefix}-{k:02d}', svg)})", ""]
        if k == 0:
            body.append(f"> Se crea el nodo raíz ${lab(nodes[0])}$ y se mete en la cola.")
        else:
            cur = nodes[sn["current"]]
            if sn.get("goal"):
                body.append(f"> Se expande ${lab(cur)}$: **es meta**. La búsqueda termina.")
            elif sn["created"]:
                kids = ", ".join(f"${lab(nodes[i])}$ ({nodes[i]['op']})" for i in sn["created"])
                body.append(f"> Se expande ${lab(cur)}$: no es meta; se crean {kids}.")
            else:
                body.append(f"> Se expande ${lab(cur)}$: no es meta y no tiene hijos nuevos.")
        out.append("\n".join(body))
    return out


# Tres en línea
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != " " and b[a] == b[c] == b[d]:
            return b[a]
    return None


def game_tree(board):
    nodes = [dict(id=0, state=board, parent=None, op=None, depth=0, move=None)]
    q = [0]
    while q:
        v = q.pop(0)
        b = nodes[v]["state"]
        if winner(b) or " " not in b:
            continue
        turn = "X" if nodes[v]["depth"] % 2 == 0 else "O"
        for i in range(9):
            if b[i] == " ":
                nb = b[:i] + turn + b[i + 1:]
                nodes.append(dict(id=len(nodes), state=nb, parent=v, op=None,
                                  depth=nodes[v]["depth"] + 1, move=i))
                q.append(len(nodes) - 1)
    return nodes


def game_value(nodes):
    ch = {}
    for n in nodes:
        if n["parent"] is not None:
            ch.setdefault(n["parent"], []).append(n["id"])

    def leaf(v, maxi):
        w = winner(nodes[v]["state"])
        return 1 if w == "X" else (-1 if w == "O" else 0)
    val, _ = minimax(nodes, ch, leaf)
    return val, ch


OUTCOME = {1: "Gana jugador1", -1: "Pierde jugador1", 0: "Empate"}


def draw_ttt(svg, x, y, b, newi=None, cell=15):
    x0, y0 = x - 1.5 * cell, y - 1.5 * cell
    for i in range(9):
        r, c = divmod(i, 3)
        svg.rect(x0 + c * cell, y0 + r * cell, cell, cell, PAL["white"], PAL["ink"], 0.8, rx=0)
        if b[i] != " ":
            svg.text(x0 + c * cell + cell / 2, y0 + r * cell + cell / 2 + 4.5, b[i].lower(), 12,
                     PAL["new"] if i == newi else PAL["ink"], bold=(i == newi), italic=(b[i] == "O"))


def game_svg(nodes, val=None, ch=None, dx=58, dy=92):
    pos, chl = layout(nodes, dx, dy)
    svg = SVG()
    for n in nodes:
        if n["parent"] is not None:
            (x1, y1), (x2, y2) = pos[n["parent"]], pos[n["id"]]
            svg.line(x1, y1 + 24, x2, y2 - 24, PAL["ink"], 1.0)
    for n in nodes:
        x, y = pos[n["id"]]
        draw_ttt(svg, x, y, n["state"], n["move"])
        if not chl.get(n["id"]):
            o = OUTCOME[game_value_leaf(n)]
            svg.text(x, y + 36, o.split()[0], 11, PAL["new"], bold=True)
            if " " in o:
                svg.text(x, y + 49, o.split()[1], 11, PAL["new"], bold=True)
        elif val is not None:
            svg.text(x + 28, y - 14, {1: "gana", -1: "pierde", 0: "empate"}[val[n["id"]]], 10,
                     PAL["teal"], anchor="start", italic=True)
    return svg


def game_value_leaf(n):
    w = winner(n["state"])
    return 1 if w == "X" else (-1 if w == "O" else 0)


CELL_NAMES = ["arriba a la izquierda", "arriba al centro", "arriba a la derecha",
              "en el centro a la izquierda", "en el centro", "en el centro a la derecha",
              "abajo a la izquierda", "abajo al centro", "abajo a la derecha"]


def build():
    p = Page("Unidad5-Grafos/BusquedaEspacioEstados")

    # Mapa de Rumania
    V = [ROM_SH[v] for v in ROM_POS]
    E = [(ROM_SH[a], ROM_SH[b], w) for a, b, w in ROM]
    POS = {ROM_SH[k]: v for k, v in ROM_POS.items()}
    full = {ROM_SH[k]: k for k in ROM_POS}
    svg = SVG()
    draw_graph(svg, POS, E, False, node_text=full, node_style={"Ara": "hl", "Buc": "goal"})
    p.put("fig-rom", f"![Mapa de Rumania]({p.img('rumania', svg)})")

    # Primeros niveles del árbol de búsqueda desde Arad
    adj = {}
    for a, b, _ in E:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    orden = ["Ara", "Zer", "Ora", "Sib", "Tim", "Lug", "Meh", "Dro", "Cra", "Rim", "Fag", "Pit", "Buc"]
    t_arad = ("Arad", [("Zerind", []), ("Sibiu", [("Arad ", []), ("Oradea", []), ("Rimnicu", []),
                                                  ("Fagaras", [])]), ("Timisoara", [])])
    pos_a, E_a = tree_pos(t_arad, 74, 64)
    svg = SVG()
    draw_graph(svg, pos_a, E_a, dots=True, node_style={"Arad": "green", "Sibiu": "green"},
               node_text={k: k.strip() for k in pos_a})
    p.put("fig-arbol-arad", f"![Árbol de búsqueda desde Arad]({p.img('arbol-arad', svg)})\n\n"
                            f"Se expandió Arad (sus hijos son las ciudades vecinas) y luego Sibiu. "
                            f"Uno de los hijos de Sibiu es otra vez Arad: el árbol de búsqueda "
                            f"puede repetir estados.")

    # 8-puzzle: formulación
    svg = SVG()
    draw_board(svg, 0, 0, ((6, 3, 7), (8, 1, 4), (2, 0, 5)), cell=26)
    draw_board(svg, 130, 0, GOAL, "goal", cell=26)
    svg.text(0, 56, "Un estado", 13, PAL["muted"])
    svg.text(130, 56, "Meta", 13, PAL["muted"])
    p.put("fig-puzzle", f"![8-puzzle: un estado y la meta]({p.img('puzzle-ini', svg)})")

    # Árbol de letras: amplitud y profundidad
    st, g1, cr, ex = letters_steps(p, "t1-bfs", T1, {"G", "L"}, "bfs")
    p.put("t1-bfs", steps("Búsqueda preferente por amplitud", st))
    p.put("t1-bfs-res", f"Encuentra la meta **{g1}**. Nodos creados: {', '.join(cr)}. "
                        f"Nodos expandidos: {', '.join(ex)}.")
    st, g2, cr, ex = letters_steps(p, "t1-dfs", T1, {"G", "L"}, "dfs")
    p.put("t1-dfs", steps("Búsqueda preferente por profundidad", st))
    p.put("t1-dfs-res", f"Encuentra la meta **{g2}**. Nodos creados: {', '.join(cr)}. "
                        f"Nodos expandidos: {', '.join(ex)}.")

    # Agente minero
    walls = {(1, 1), (1, 3), (1, 4), (2, 1), (3, 1), (3, 3), (4, 3)}
    succ = grid_succ(walls, 5, 5, ["←", "→", "↑", "↓"])
    nodes, exp, goal, snaps = tree_search((2, 2), succ, lambda s: s == (4, 4), "bfs", "path")
    p.put("fig-minero", f"![Mina]({p.img('minero-grid', grid_fig(walls, 5, 5, (2, 2), (4, 4)))})")
    lab = lambda n: f"({n['state'][0]},{n['state'][1]})"
    p.put("minero", steps("Búsqueda por amplitud del agente minero",
                          search_tabs(p, "minero", nodes, exp, goal, snaps, lab, r=22)))
    path = path_of(nodes, goal)
    assert [n["state"] for n in path] == [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4)]
    p.put("minero-res", f"El agente sigue el camino {' → '.join(lab(n) for n in path)}. "
                        f"Se crearon {len(nodes)} nodos y se expandieron {len(exp)}.")

    # 8-puzzle de Bedoya
    start = ((1, 0, 2), (4, 5, 3), (7, 8, 6))
    nodes, exp, goal, snaps = tree_search(start, puzzle_succ, lambda s: s == GOAL, "bfs", "path")
    pos, ch = layout(nodes, 74, 96)
    out = []
    for k, sn in enumerate(snaps):
        upto = max([0] + [i for s_ in snaps[:k + 1] for i in s_["created"]])
        svg = search_step_svg(nodes, pos, ch, sn, upto, None, kind="board", show_ops=True)
        body = [f"![8-puzzle, paso {k + 1}]({p.img(f'puzzle-{k:02d}', svg)})", ""]
        if k == 0:
            body.append("> Estado inicial: el espacio está arriba al centro.")
        else:
            cur = nodes[sn["current"]]
            op = f" (se llegó con {cur['op']})" if cur["op"] else ""
            if sn.get("goal"):
                body.append(f"> Se expande el nodo{op}: es la configuración meta. Termina.")
            else:
                ops = ", ".join(nodes[i]["op"] for i in sn["created"])
                body.append(f"> Se expande el nodo{op}: no es meta; se crean sus hijos con {ops}. "
                            f"No se crea el hijo que devolvería a un estado de la rama.")
        out.append("\n".join(body))
    p.put("puzzle", steps("Búsqueda por amplitud en el 8-puzzle", out))
    assert (len(nodes), len(exp)) == (19, 10)
    p.put("puzzle-n", f"{len(nodes)} nodos creados y {len(exp)} expandidos")

    # Tres en línea (Bedoya)
    g1 = "XXO" if False else " XOXXO O "
    tree = game_tree(g1)
    val, chg = game_value(tree)
    svg = SVG()
    draw_ttt(svg, 0, 0, g1, cell=26)
    p.put("fig-gato-ini", f"![Tablero inicial]({p.img('gato-ini', svg)})")
    p.put("gato", f"![Árbol de juego]({p.img('gato', game_svg(tree))})")
    best = [c for c in chg[0] if val[c] == val[0]]
    opts = "; ".join(f"X {CELL_NAMES[tree[c]['move']]}: el jugador 2 puede llevarlo a "
                     f"«{OUTCOME[val[c]].lower()}»" for c in chg[0])
    assert len(best) == 1
    p.put("gato-resp", f"Se analiza de las hojas hacia arriba. En cada jugada de O se supone que O "
                       f"escoge lo peor para el jugador 1: {opts}.\n\n"
                       f"![Árbol analizado]({p.img('gato-val', game_svg(tree, val, chg))})\n\n"
                       f"La mejor jugada es **X {CELL_NAMES[tree[best[0]]['move']]}**: asegura al "
                       f"menos un {OUTCOME[val[0]].lower()}. Con las otras dos, si O juega bien, el "
                       f"jugador 1 pierde.")

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
    val, order = minimax(nim, ch, lambda v, maxi: +1 if maxi else -1)
    maxd = max(n["depth"] for n in nim)
    out = []

    def nim_svg(visible_depth, valued, newv):
        svg = SVG()
        for n in nim:
            if n["parent"] is not None and n["depth"] <= visible_depth:
                (x1, y1), (x2, y2) = pos[n["parent"]], pos[n["id"]]
                sx1, sy1, sx2, sy2 = _shorten(x1, y1, x2, y2, 17, 17)
                svg.line(sx1, sy1, sx2, sy2, PAL["ink"], 1.1)
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

    # Ejercicios
    def tree_fig(name, t, goals):
        full, _, _, _ = tree_search(t[0], explicit_tree(t), lambda s: False, "bfs", "none")
        fpos, _ = layout(full, 54, 64)
        svg = SVG()
        for n in full:
            if n["parent"] is not None:
                (x1, y1), (x2, y2) = fpos[n["parent"]], fpos[n["id"]]
                sx1, sy1, sx2, sy2 = _shorten(x1, y1, x2, y2, 19, 19)
                svg.line(sx1, sy1, sx2, sy2, PAL["ink"], 1.1)
        for n in full:
            x, y = fpos[n["id"]]
            fill, stroke, tc, width = NODE_STYLES["green"]
            svg.circle(x, y, 18, fill, stroke, width)
            svg.text(x, y + 5, n["state"], 14)
            if n["state"] in goals:
                svg.circle(x, y, 22, "none", PAL["goal"], 1.6)
        return f"![Árbol con metas {' y '.join(sorted(goals))}]({p.img(name, svg)})"
    for key, t, goals in (("t2", T2, {"L", "D"}), ("t3", T3, {"L", "A"})):
        p.put(f"fig-{key}", tree_fig(key, t, goals))
        for mode in ("bfs", "dfs"):
            _, g, cr, ex = letters_steps(p, f"{key}-{mode}", t, goals, mode, draw=False)
            p.put(f"{key}-{mode}-res", f"Encuentra **{g}**. Creados: {', '.join(cr)}. "
                                       f"Expandidos: {', '.join(ex)}.")

    rsucc = lambda s: [(None, x) for x in sorted(adj[s], key=orden.index)]
    for key, origin in (("ara", "Ara"), ("rom", "Sib")):
        nodes, exp, goal, snaps = tree_search(origin, rsucc, lambda s: s == "Buc", "bfs", "path")
        p.put(f"{key}-exp", ", ".join(nodes[i]["state"] for i in exp))
        p.put(f"{key}-path", " → ".join(n["state"] for n in path_of(nodes, goal)))
        p.put(f"{key}-n", str(len(nodes)))
        if key == "ara":
            pos, ch = layout(nodes, 50, 64)
            svg = search_step_svg(nodes, pos, ch, snaps[-1], len(nodes) - 1, lambda n: n["state"],
                                  r=19, frontier_title="Cola:")
            p.put("fig-ara", f"![Árbol de búsqueda desde Arad]({p.img('arad-bfs', svg)})")

    # Ratón y queso (sin evitar devolverse)
    walls2 = {(0, 0), (0, 1), (0, 2), (0, 3), (2, 1), (2, 2)}
    succ2 = grid_succ(walls2, 4, 4, ["↑", "←", "→", "↓"])
    nodes, exp, goal, snaps = tree_search((3, 1), succ2, lambda s: s == (2, 0), "bfs", "none")
    p.put("fig-raton", f"![Cuadrícula]({p.img('raton-grid', grid_fig(walls2, 4, 4, (3, 1), (2, 0), 'ratón', 'queso'))})")
    pos, ch = layout(nodes, 62, 74)
    svg = search_step_svg(nodes, pos, ch, snaps[-1], len(nodes) - 1, lab, r=22, show_ops=True)
    path = path_of(nodes, goal)
    p.put("raton-sol", f"![Árbol de búsqueda]({p.img('raton-arbol', svg)})\n\nCamino: "
                       f"{' → '.join(lab(n) for n in path)}. Se crearon {len(nodes)} nodos y se "
                       f"expandieron {len(exp)}. Algunos hijos repiten el estado de su abuelo "
                       f"(volver a $(3,1)$), porque no se evita devolverse.")

    # Aspiradora (sin evitar devolverse)
    def asp_succ(s):
        pos_, l, r = s
        out = []
        for op in ("A", "D", "I"):
            if op == "A":
                nxt = (pos_, l and pos_ != 0, r and pos_ != 1)
            elif op == "D":
                nxt = (1, l, r)
            else:
                nxt = (0, l, r)
            if nxt != s:                     # un operador que no cambia nada no se aplica
                out.append((op, nxt))
        return out
    nodes, exp, goal, snaps = tree_search((0, True, True), asp_succ,
                                          lambda s: not s[1] and not s[2], "bfs", "none")
    pos, ch = layout(nodes, 74, 84)
    svg = SVG()
    for n in nodes:
        if n["parent"] is not None:
            (x1, y1), (x2, y2) = pos[n["parent"]], pos[n["id"]]
            svg.line(x1, y1 + 15, x2, y2 - 15, PAL["ink"], 1.0)
            svg.text((x1 + x2) / 2 + 6, (y1 + y2) / 2, n["op"], 12, PAL["muted"], anchor="start",
                     bg=True)
    for n in nodes:
        x, y = pos[n["id"]]
        st_, l, r = n["state"]
        for k, dirty in ((0, l), (1, r)):
            fill = "#fff2b3" if n["id"] == goal else ("#e8f5d9" if n["id"] in exp else PAL["white"])
            svg.rect(x - 30 + k * 30, y - 14, 30, 28, fill, PAL["ink"], 1.0, rx=0)
            if st_ == k:
                svg.text(x - 15 + k * 30, y + 1, "asp", 9, PAL["teal"], bold=True)
            if dirty:
                svg.text(x - 15 + k * 30, y + 11, "•••", 10, "#7a5230")
    p.put("aspiradora", f"![Árbol de búsqueda de la aspiradora]({p.img('aspiradora', svg)})")
    path = path_of(nodes, goal)
    ops = ", ".join(n["op"] for n in path[1:])
    p.put("aspiradora-res", f"La meta se encuentra con los operadores {ops} (profundidad "
                            f"{len(path) - 1}, costo $3 + 1 + 3 = 7$). Se crearon {len(nodes)} nodos "
                            f"y se expandieron {len(exp)}.")

    # Tres en línea: los otros dos tableros
    boards = ["XXOX  OO ", "XOO  XOX "]
    figs, sols = [], []
    for k, bd in enumerate(boards):
        svg = SVG()
        draw_ttt(svg, 0, 0, bd, cell=26)
        figs.append(f"![Tablero {'ab'[k]}]({p.img(f'gato-ej-{k}', svg)})")
        tree = game_tree(bd)
        val, chg = game_value(tree)
        best = [c for c in chg[0] if val[c] == val[0]]
        moves = " o ".join(f"X {CELL_NAMES[tree[c]['move']]}" for c in best)
        if val[0] < 0:
            msg = ("Ninguna jugada lo salva: tome la casilla que tome, si O juega bien, el jugador 1 "
                   "**pierde**. O amenaza con dos líneas a la vez.")
        else:
            msg = f"Con **{moves}** el jugador 1 asegura «{OUTCOME[val[0]].lower()}»."
        sols.append(f"{'ab'[k]}) {msg}\n\n"
                    f"![Árbol analizado]({p.img(f'gato-ej-{k}-val', game_svg(tree, val, chg))})")
    p.put("fig-gato-ej", "| a) | b) |\n|---|---|\n| " + " | ".join(figs) + " |")
    p.put("gato-ej-sol", "\n\n".join(sols))

    # Jarras: solo la solución
    nodes, exp, goal, snaps = tree_search((0, 0), jarras_succ, lambda s: s[0] == 2, "bfs", "global")
    path = path_of(nodes, goal)
    lj = lambda n: f"({n['state'][0]},{n['state'][1]})"
    p.put("jarras-sol", " → ".join((f"${lj(n)}$" if n["op"] is None else f"**{n['op']}** ${lj(n)}$")
                                   for n in path))
    p.put("jarras-n", str(len(nodes)))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
