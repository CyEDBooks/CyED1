"""Convierte trazas de algoritmos en pasos (figura + tabla + texto)."""
from common import *
from algos import (bfs_trace, dfs_trace, dijkstra_trace, prim_trace, kruskal_trace,
                   floyd_trace, floyd_route, warshall_trace, path_to, adjacency, INF)


def _norm(d, n):
    return {(k if k >= 0 else n + k): v for k, v in (d or {}).items()}


def mv(v):
    """Vértice en modo matemático: nombres largos van en \\text{}."""
    v = str(v)
    if len(v) == 1 or v.isdigit() or v in ("∞",):
        return v
    return f"\\text{{{v}}}"


def _vlist(vs):
    vs = [f"${mv(v)}$" for v in vs]
    if len(vs) <= 1:
        return "".join(vs)
    return ", ".join(vs[:-1]) + " y " + vs[-1]


# BFS
def bfs_steps(page, prefix, vertices, pos, edges, s, directed=False, label_pos=None,
              questions=None, notes=None, table=True):
    adj = adjacency(vertices, edges, directed)
    snaps = bfs_trace(vertices, adj, s)
    questions = _norm(questions, len(snaps))
    notes = _norm(notes, len(snaps))
    out = []
    prev = None
    for i, sn in enumerate(snaps):
        ns, es, lab, lst = {}, {}, {}, {}
        for v in vertices:
            col = sn["color"][v]
            ns[v] = col
            lab[v] = fmt(sn["d"][v])
            if sn["pi"][v] is not None:
                es[(sn["pi"][v], v)] = "tree"
        for v in sn["new"]:
            ns[v] = "newgray"
            lst[v] = "new"
            if sn["pi"][v] is not None:
                es[(sn["pi"][v], v)] = "new"
        if sn["u"] is not None:
            ns[sn["u"]] = "newblack"
        svg = SVG()
        draw_graph(svg, pos, edges, directed, node_style=ns, edge_style=es, labels=lab,
                   label_style=lst, label_pos=label_pos)
        ys = max(y for _, y in pos.values()) + 52
        x0 = min(x for x, _ in pos.values()) - 10
        qnew = [k for k, v in enumerate(sn["Q"]) if v in sn["new"]]
        draw_panel(svg, x0, ys, "Q:", sn["Q"], new=qnew)
        path = page.img(f"{prefix}-{i:02d}", svg)
        body = [f"![BFS, paso {i + 1}]({path})", ""]
        if sn["kind"] == "init":
            body.append(f"> Todos los vértices empiezan blancos con $d = \\infty$. Se descubre el origen "
                        f"${mv(s)}$: se pinta de gris, ${mv(s)}.d = 0$ y se encola.")
        else:
            u = sn["u"]
            if sn["new"]:
                body.append(f"> Se extrae ${mv(u)}$ de la cola. Sus vecinos blancos {_vlist(sn['new'])} "
                            f"se descubren: quedan grises, con $d = {u}.d + 1 = {sn['d'][u] + 1}$ y "
                            f"$\\pi = {mv(u)}$, y se encolan. ${mv(u)}$ queda negro.")
            else:
                body.append(f"> Se extrae ${mv(u)}$ de la cola. No tiene vecinos blancos: no se descubre "
                            f"nada y ${mv(u)}$ queda negro.")
        if table:
            body.append("")
            header = ["", *[f"${mv(v)}$" for v in vertices]]
            rd = ["$d$"]
            rp = ["$\\pi$"]
            for v in vertices:
                dv = fmt(sn["d"][v])
                pv = sn["pi"][v] if sn["pi"][v] is not None else "NIL"
                if v in sn["new"]:
                    rd.append(hl(dv))
                    rp.append(hl(pv))
                else:
                    rd.append(dv)
                    rp.append(pv)
            body.append(md_table(header, [rd, rp]))
        if i in notes:
            body += ["", notes[i]]
        if i in questions:
            body += ["", f"> **{questions[i]}**"]
        out.append("\n".join(body))
        prev = sn
    return out, snaps


# DFS
def dfs_steps(page, prefix, vertices, pos, edges, directed=True, label_pos=None,
              roots=None, questions=None, notes=None, classify=True, curved=None):
    adj = adjacency(vertices, edges, directed)
    snaps = dfs_trace(vertices, adj, roots, directed)
    questions = _norm(questions, len(snaps))
    notes = _norm(notes, len(snaps))
    out = []
    for i, sn in enumerate(snaps):
        ns, es, lab, lst = {}, {}, {}, {}
        for v in vertices:
            ns[v] = sn["color"][v]
            dv = sn["d"].get(v)
            fv = sn["f"].get(v)
            lab[v] = "" if dv is None else (f"{dv}/{fv}" if fv else f"{dv}/")
        for (a, b), k in sn["cls"].items():
            es[(a, b)] = "tree" if k == "T" else "back"
        u = sn["u"]
        if sn["kind"] == "disc":
            ns[u] = "newgray"
            lst[u] = "new"
            if sn["edge"]:
                es[sn["edge"]] = "new"
        else:
            ns[u] = "newblack"
            lst[u] = "new"
        svg = SVG()
        draw_graph(svg, pos, edges, directed, node_style=ns, edge_style=es, labels=lab,
                   label_style=lst, label_pos=label_pos, curved=curved)
        if classify:
            # Etiqueta B/F/C sobre las aristas no-árbol ya clasificadas.
            for (a, b), k in sn["cls"].items():
                if k != "T":
                    (x1, y1), (x2, y2) = pos[a], pos[b]
                    if a == b:
                        svg.text(x1 + 24, y1 - 44, k, 13, PAL["muted"], bold=True, bg=True)
                    else:
                        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                        off = 14 if (b, a) not in sn["cls"] and not any(
                            e[0] == b and e[1] == a for e in edges) else 26
                        dx, dy = x2 - x1, y2 - y1
                        d = (dx * dx + dy * dy) ** 0.5
                        svg.text(mx - dy / d * off, my + dx / d * off + 5, k, 13, PAL["muted"],
                                 bold=True, bg=True)
        ys = max(y for _, y in pos.values()) + 52
        x0 = min(x for x, _ in pos.values()) - 10
        draw_panel(svg, x0, ys, "Grises (pila de llamadas):", sn["stack"],
                   new=[len(sn["stack"]) - 1] if sn["kind"] == "disc" else [])
        path = page.img(f"{prefix}-{i:02d}", svg)
        body = [f"![DFS, paso {i + 1}]({path})", ""]
        t = sn["time"]
        if sn["kind"] == "disc":
            if sn["edge"]:
                body.append(f"> Desde ${mv(sn['edge'][0])}$ se llega a ${mv(u)}$, que es blanco: tiempo "
                            f"${mv(t)}$, ${mv(u)}.d = {t}$, ${mv(u)}.\\pi = {mv(sn['edge'][0])}$. ${mv(u)}$ queda gris.")
            else:
                body.append(f"> Se inicia una búsqueda desde ${mv(u)}$: tiempo ${mv(t)}$, ${mv(u)}.d = {t}$. "
                            f"${mv(u)}$ queda gris.")
        else:
            body.append(f"> ${mv(u)}$ ya no tiene vecinos blancos: tiempo ${mv(t)}$, ${mv(u)}.f = {t}$. "
                        f"${mv(u)}$ queda negro y la búsqueda regresa.")
        if i in notes:
            body += ["", notes[i]]
        if i in questions:
            body += ["", f"> **{questions[i]}**"]
        out.append("\n".join(body))
    return out, snaps


# Dijkstra
def _lab(L, pred, v):
    return f"[{fmt(L[v])},{pred[v] if pred[v] is not None else '-'}]"


def dijkstra_steps(page, prefix, vertices, pos, edges, s, directed=False, label_pos=None,
                   questions=None, notes=None, target=None):
    adj = adjacency(vertices, edges, directed)
    snaps = dijkstra_trace(vertices, adj, s)
    questions = _norm(questions, len(snaps))
    notes = _norm(notes, len(snaps))
    out = []
    rows = []
    for i, sn in enumerate(snaps):
        ns, es, lab, lst, ws = {}, {}, {}, {}, {}
        for v in vertices:
            if v in sn["S"]:
                ns[v] = "black"
            if sn["L"][v] < INF:
                lab[v] = _lab(sn["L"], sn["pred"], v)
            if sn["pred"][v] is not None:
                es[(sn["pred"][v], v)] = "tree"
        u = sn["u"]
        if u is not None:
            ns[u] = "newblack"
            for v, _ in adj[u]:
                if v not in sn["S"]:
                    es[(u, v)] = "new" if v in sn["changed"] else "cand"
                    ws[(u, v)] = "new"
        for v in sn["changed"]:
            lst[v] = "new"
        svg = SVG()
        draw_graph(svg, pos, edges, directed, node_style=ns, edge_style=es, labels=lab,
                   label_style=lst, label_pos=label_pos, weight_style=ws)
        path = page.img(f"{prefix}-{i:02d}", svg)
        body = [f"![Dijkstra, paso {i + 1}]({path})", ""]
        if sn["kind"] == "init":
            body.append(f"> Se etiqueta el origen ${mv(s)}$ con $[0,-]$: distancia $0$, sin predecesor.")
        else:
            nb = [v for v, _ in adj[u] if v not in sn["S"]]
            txt = (f"> El vértice no permanente de menor etiqueta es ${mv(u)}$ con "
                   f"${fmt(sn['L'][u])}$: **${mv(u)}$ se vuelve permanente**.")
            if sn["changed"]:
                txt += (f" Se reetiquetan los vecinos {_vlist(sn['changed'])}, porque llegar por ${mv(u)}$ "
                        f"cuesta menos que su etiqueta anterior.")
            elif nb:
                txt += (f" Ningún vecino mejora: {_vlist(nb)} ya tienen una etiqueta menor o igual "
                        f"pasando por ${mv(u)}$.")
            else:
                txt += " No le quedan vecinos que no sean permanentes."
            body.append(txt)
        # tabla acumulada: una fila por iteración
        row = [str(i) if i else "inicio", f"${mv(u)}$" if u else "—"]
        for v in vertices:
            if v in sn["S"] and v != u:
                row.append("✓")
            else:
                cell = _lab(sn["L"], sn["pred"], v) if sn["L"][v] < INF else "∞"
                if v == u:
                    cell = f"**{cell}** ✓"
                row.append(hl(cell) if v in sn["changed"] else cell)
        rows.append(row)
        header = ["Iteración", "Permanente", *[f"${mv(v)}$" for v in vertices]]
        body += ["", md_table(header, rows)]
        if i in notes:
            body += ["", notes[i]]
        if i in questions:
            body += ["", f"> **{questions[i]}**"]
        out.append("\n".join(body))
    return out, snaps


def dijkstra_path_steps(page, prefix, vertices, pos, edges, snaps, s, t, directed=False,
                        label_pos=None):
    """Reconstrucción del camino siguiendo predecesores de t hacia s."""
    last = snaps[-1]
    L, pred = last["L"], last["pred"]
    chain = [t]
    while pred[chain[-1]] is not None:
        chain.append(pred[chain[-1]])
    out = []
    for k in range(1, len(chain) + 1):
        part = chain[:k]
        ns = {v: "black" for v in vertices}
        for v in part:
            ns[v] = "hl"
        es = {}
        for a, b in zip(part[1:], part):
            es[(a, b)] = "new"
        lab = {v: _lab(L, pred, v) for v in vertices if L[v] < INF}
        lst = {v: "new" for v in part}
        svg = SVG()
        draw_graph(svg, pos, edges, directed, node_style=ns, edge_style=es, labels=lab,
                   label_style=lst, label_pos=label_pos)
        path = page.img(f"{prefix}-{k:02d}", svg)
        v = part[-1]
        body = [f"![Camino mínimo, paso {k}]({path})", ""]
        if pred[v] is not None:
            body.append(f"> La etiqueta de ${mv(v)}$ es ${_lab(L, pred, v)}$: se llega a ${mv(v)}$ desde "
                        f"${mv(pred[v])}$.")
        else:
            body.append(f"> ${mv(v)}$ es el origen: no tiene predecesor. El camino, leído al revés, es "
                        f"${' \\to '.join(mv(x) for x in chain[::-1])}$ con costo ${fmt(L[t])}$.")
        out.append("\n".join(body))
    return out


# Prim
def _ekey(e):
    return f"\\{{{mv(e[0])},{mv(e[1])}\\}}"


def prim_steps(page, prefix, vertices, pos, edges, start, label_pos=None, notes=None,
               questions=None):
    snaps = prim_trace(vertices, edges, start)
    notes = _norm(notes, len(snaps))
    questions = _norm(questions, len(snaps))
    out = []
    total = 0
    for i, sn in enumerate(snaps):
        ns, es, ws = {}, {}, {}
        for v in vertices:
            ns[v] = "tree" if v in sn["inT"] else "plain"
        for e in sn["T"]:
            es[(e[0], e[1])] = "tree"
            ws[(e[0], e[1])] = "tree"
        for e in sn["cand"]:
            es[(e[0], e[1])] = "cand"
        ch = sn["chosen"]
        nv = None
        if ch:
            es[(ch[0], ch[1])] = "new"
            ws[(ch[0], ch[1])] = "new"
            if i == 1 and start is None:
                ns[ch[0]] = ns[ch[1]] = "hl"
            else:
                nv = ch[1] if ch[1] == sn["inT"][-1] else ch[0]
                ns[nv] = "hl"
            total += ch[2]
        elif start is not None:
            ns[start] = "hl"
        svg = SVG()
        draw_graph(svg, pos, edges, False, node_style=ns, edge_style=es, weight_style=ws)
        ys = max(y for _, y in pos.values()) + 50
        x0 = min(x for x, _ in pos.values()) - 10
        items = [f"{{{e[0]},{e[1]}}} {e[2]}" for e in sn["T"]]
        draw_panel(svg, x0, ys, "Árbol:", items, new=[len(items) - 1] if ch else [], cell=40,
                   mark=f"peso = {total}" if items else None)
        path = page.img(f"{prefix}-{i:02d}", svg)
        body = [f"![Prim, paso {i + 1}]({path})", ""]
        if not ch:
            if start is None:
                body.append("> Todas las aristas son candidatas. Se busca la de menor peso de todo el "
                            "grafo.")
            else:
                cand = ", ".join(f"${_ekey(e)}$ ({e[2]})" for e in sn["cand"])
                body.append(f"> Se empieza con el árbol que solo tiene a ${mv(start)}$. Las aristas "
                            f"candidatas (punteadas) son las que tienen un extremo en el árbol y el "
                            f"otro fuera: {cand}.")
        else:
            cand = sn["prev_cand"]
            minw = ch[2]
            ties = [e for e in cand if e[2] == minw and e != ch]
            if nv is None:
                txt = (f"> La arista de menor peso es ${_ekey(ch)}$ con peso ${ch[2]}$: se agrega al "
                       f"árbol. Ahora las candidatas (punteadas) son las aristas con un extremo en el "
                       f"árbol y el otro fuera.")
            else:
                txt = (f"> Entre las candidatas, la de menor peso es ${_ekey(ch)}$ con peso "
                       f"${ch[2]}$: se agrega al árbol junto con el vértice ${mv(nv)}$.")
            if ties:
                txt += (" Hay empate con " + ", ".join(f"${_ekey(e)}$" for e in ties) +
                        "; se escoge cualquiera (aquí, la primera en la lista).")
            body.append(txt)
            if len(sn["inT"]) == len(vertices):
                body.append("")
                body.append(f"> El árbol ya tiene $n-1 = {len(vertices) - 1}$ aristas: terminó. "
                            f"Peso total: ${total}$.")
        if i in notes:
            body += ["", notes[i]]
        if i in questions:
            body += ["", f"> **{questions[i]}**"]
        out.append("\n".join(body))
    return out, snaps


# Kruskal
def kruskal_steps(page, prefix, vertices, pos, edges, notes=None, questions=None):
    snaps = kruskal_trace(vertices, edges)
    notes = _norm(notes, len(snaps))
    questions = _norm(questions, len(snaps))
    out = []
    for i, sn in enumerate(snaps):
        ns, es, ws = {}, {}, {}
        inT = {v for e in sn["T"] for v in e[:2]}
        for v in vertices:
            ns[v] = "tree" if v in inT else "plain"
        for e in sn["T"]:
            es[(e[0], e[1])] = "tree"
            ws[(e[0], e[1])] = "tree"
        if sn["kind"] == "edge":
            e = sn["edge"]
            if sn["accepted"]:
                es[(e[0], e[1])] = "new"
                ws[(e[0], e[1])] = "new"
                ns[e[0]] = ns[e[1]] = "hl"
            else:
                es[(e[0], e[1])] = "reject"
        svg = SVG()
        draw_graph(svg, pos, edges, False, node_style=ns, edge_style=es, weight_style=ws)
        ys = max(y for _, y in pos.values()) + 50
        x0 = min(x for x, _ in pos.values()) - 10
        # lista ordenada de aristas, marcando procesadas
        items = []
        newi = []
        dim = []
        for k, e in enumerate(sn["order"]):
            items.append(f"{e[0]}{e[1]}:{e[2]}")
            if k == sn["i"]:
                newi.append(k)
            elif k < sn["i"]:
                dim.append(k)
        yb = draw_panel(svg, x0, ys, "Aristas ordenadas:", items, new=newi, dim=dim, cell=30,
                        wrap=6)
        comps = "  ".join("{" + ",".join(g) + "}" for g in sn["comps"])
        svg.text(x0, yb + 24, "Componentes: " + comps, 13, PAL["muted"], anchor="start")
        path = page.img(f"{prefix}-{i:02d}", svg)
        body = [f"![Kruskal, paso {i + 1}]({path})", ""]
        if sn["kind"] == "init":
            body.append("> Se ordenan las aristas de menor a mayor peso. Al comienzo cada vértice es "
                        "su propia componente.")
        else:
            e = sn["edge"]
            if sn["accepted"]:
                txt = (f"> ${_ekey(e)}$ (peso ${e[2]}$) une dos componentes distintas: **se agrega**.")
                if len(sn["T"]) == len(vertices) - 1:
                    tot = sum(x[2] for x in sn["T"])
                    txt += (f" Ya hay $n-1 = {len(vertices) - 1}$ aristas: terminó. Peso total: "
                            f"${tot}$.")
                body.append(txt)
            else:
                body.append(f"> ${_ekey(e)}$ (peso ${e[2]}$) tiene sus dos extremos en la misma "
                            f"componente: crearía un circuito. **Se descarta.**")
        if i in notes:
            body += ["", notes[i]]
        if i in questions:
            body += ["", f"> **{questions[i]}**"]
        out.append("\n".join(body))
    return out, snaps


# Floyd-Warshall
def floyd_steps(vertices, edges, directed=True, notes=None, questions=None, fig=None):
    """fig = (page, prefix, pos, label_pos): dibuja el grafo con el pivote resaltado."""
    snaps = floyd_trace(vertices, edges, directed)
    notes = _norm(notes, len(snaps))
    questions = _norm(questions, len(snaps))
    out = []
    for i, sn in enumerate(snaps):
        W = latex_matrix("W", vertices, vertices, sn["W"], sn["changed"], lfmt, sub=f"_{{{i}}}")
        P = latex_matrix("P", vertices, vertices, sn["P"], sn["changed"], str, sub=f"_{{{i}}}")
        body = []
        if fig:
            page, prefix, pos = fig
            ns = {sn["k"]: "hl"} if sn["k"] else {}
            svg = SVG()
            draw_graph(svg, pos, edges, directed, node_style=ns)
            body += [f"![Floyd-Warshall, paso {i + 1}]({page.img(f'{prefix}-{i:02d}', svg)})", ""]
        body += ["$$", W + r"\qquad " + P, "$$", ""]
        if sn["k"] is None:
            body.append("> $W_0$ tiene los pesos de las aristas ($\\infty$ si no hay arista, $0$ en "
                        "la diagonal). $P_0$ dice «ir directo»: para ir de $i$ a $j$ el siguiente "
                        "vértice es $j$.")
        else:
            k = sn["k"]
            if sn["changed"]:
                ch = ", ".join(f"$({mv(vertices[a])},{mv(vertices[b])})$" for a, b in sn["changed"])
                body.append(f"> Pivote ${mv(k)}$: se prueba pasar por ${mv(k)}$. Mejoran {ch}; en esas "
                            f"casillas $P_{{{i}}}$ guarda ${mv(k)}$.")
            else:
                body.append(f"> Pivote ${mv(k)}$: ningún recorrido mejora al pasar por ${mv(k)}$. "
                            f"$W_{{{i}}} = W_{{{i - 1}}}$.")
        if i in notes:
            body += ["", notes[i]]
        if i in questions:
            body += ["", f"> **{questions[i]}**"]
        out.append("\n".join(body))
    return out, snaps


def floyd_route_steps(vertices, snaps, a, b):
    last = snaps[-1]
    P, W = last["P"], last["W"]
    idx = {v: i for i, v in enumerate(vertices)}
    seq = floyd_route(vertices, P, a, b)
    out = []
    for k, route in enumerate(seq):
        txt = r" \to ".join(mv(x) for x in route)
        body = [f"$$ {txt} $$", ""]
        if k == 0:
            body.append(f"> Se busca $({mv(a)},{mv(b)})$ en $P$: el valor mínimo es "
                        f"$W[{mv(a)}][{mv(b)}] = {lfmt(W[idx[a]][idx[b]])}$.")
        else:
            prev = seq[k - 1]
            ins = [x for x in route if x not in prev]
            body.append(f"> Se inserta {_vlist(ins)} en el recorrido.")
        out.append("\n".join(body))
    pairs = [(x, y) for x, y in zip(seq[-1], seq[-1][1:])]
    out.append(f"$$ {' \\to '.join(mv(x) for x in seq[-1])} $$\n\n> Se buscan "
               + ", ".join(f"$({mv(x)},{mv(y)})$" for x, y in pairs)
               + " en $P$: todas dicen «ir directo». No se insertan nuevos vértices. Costo: "
               f"${lfmt(W[idx[a]][idx[b]])}$.")
    return out
