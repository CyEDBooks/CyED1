from common import *
from gviz import dfs_steps, mv
from algos import adjacency, dfs_trace
import graphs as G


def static(page, name, pos, edges, directed=False, **kw):
    svg = SVG()
    draw_graph(svg, pos, edges, directed, **kw)
    return page.img(name, svg)


def df_table(vertices, snaps):
    last = snaps[-1]
    header = ["", *[f"${mv(v)}$" for v in vertices]]
    rd = ["$d$", *[str(last["d"][v]) for v in vertices]]
    rf = ["$f$", *[str(last["f"][v]) for v in vertices]]
    rp = ["$\\pi$", *[(last["pi"][v] or "NIL") for v in vertices]]
    return md_table(header, [rd, rf, rp])


def parens(snaps):
    out = []
    for sn in snaps:
        out.append(f"({sn['u']}" if sn["kind"] == "disc" else f"{sn['u']})")
    return " ".join(out)


def cls_table(snaps, edges):
    last = snaps[-1]["cls"]
    names = {"T": "de árbol (T)", "B": "de retorno (B)", "F": "de avance (F)", "C": "de cruce (C)"}
    rows = []
    for e in edges:
        k = last.get((e[0], e[1]))
        rows.append([f"$({mv(e[0])}, {mv(e[1])})$", names[k]])
    return md_table(["Arista", "Tipo"], rows)


def build():
    p = Page("Unidad5-Grafos/DFS")

    # Ejemplo 1: árbol
    tpos, tedges = tree_pos(G.TREE_AI, 80, 72)
    tv = list("ABCDEFGHI")
    lp = {v: "right" for v in tv}
    st, sn1 = dfs_steps(p, "ej1", tv, tpos, tedges, directed=False, label_pos=lp, roots=["A"],
                        classify=False,
                        questions={2: "C no tiene hijos. ¿Qué hace la búsqueda ahora?"},
                        notes={3: "> Termina $C$ y **regresa** a $B$, que todavía tiene hijos sin "
                                  "visitar. Es el *backtracking*: se retrocede solo lo necesario."})
    p.put("ej1", steps("Recorrido DFS desde A", st))
    p.put("ej1-orden", ", ".join(sn["u"] for sn in sn1 if sn["kind"] == "disc"))

    # Ejemplo 2: CLRS 22.4
    p.put("fig-ej2", f"![Grafo dirigido u..z]({static(p, 'ej2-grafo', G.DFS_POS, G.DFS_E, True)})")
    st, sn2 = dfs_steps(p, "ej2", G.DFS_V, G.DFS_POS, G.DFS_E, directed=True,
                        label_pos=G.DFS_LP,
                        questions={3: "Desde x se llega a v, que es gris. ¿Se visita?"},
                        notes={4: "> No: $v$ ya está gris, es decir, está en la pila de llamadas "
                                  "(es un **antecesor** de $x$). La arista $(x, v)$ cierra un "
                                  "circuito $v \\to y \\to x \\to v$; se marca **B** (de retorno)."})
    p.put("ej2", steps("Recorrido DFS (grafo dirigido)", st))
    p.put("ej2-final", df_table(G.DFS_V, sn2))
    p.put("ej2-parens", parens(sn2))
    p.put("ej2-cls", cls_table(sn2, G.DFS_E))

    # Ejemplo 3: no dirigido G5 desde 1
    p.put("fig-ej3", f"![Grafo de 5 vértices]({static(p, 'ej3-grafo', G.G5_POS, G.G5_E)})")
    st, sn3 = dfs_steps(p, "ej3", G.G5_V, G.G5_POS, G.G5_E, directed=False,
                        label_pos=G.G5_LP)
    p.put("ej3", steps("Recorrido DFS desde 1 (no dirigido)", st))
    p.put("ej3-final", df_table(G.G5_V, sn3))

    # Orden topológico
    adj = adjacency(G.ROPA_V, G.ROPA_E, True)
    snr = dfs_trace(G.ROPA_V, adj, None, True)
    last = snr[-1]
    lab = {v: f"{last['d'][v]}/{last['f'][v]}" for v in G.ROPA_V}
    lpr = {v: "below" for v in G.ROPA_V}
    p.put("fig-ropa", f"![Prendas con dependencias]({static(p, 'ropa', G.ROPA_POS, G.ROPA_E, True, r=34, font=12)})")
    p.put("fig-ropa-df", f"![Prendas con tiempos d/f]({static(p, 'ropa-df', G.ROPA_POS, G.ROPA_E, True, r=34, font=12, labels=lab, label_pos=lpr)})")
    order = sorted(G.ROPA_V, key=lambda v: -last["f"][v])
    p.put("ropa-orden", " → ".join(f"{v} ({last['f'][v]})" for v in order))
    p.assemble("index.md")

    # Ejercicios
    p.put("fig-q", f"![Grafo dirigido q..z]({static(p, 'q-grafo', G.Q_POS, G.Q_E, True)})")
    snq = dfs_trace(G.Q_V, adjacency(G.Q_V, G.Q_E, True), None, True)
    p.put("q-sol", df_table(G.Q_V, snq))
    p.put("q-cls", cls_table(snq, G.Q_E))
    p.put("q-parens", parens(snq))
    lastq = snq[-1]
    lab = {v: f"{lastq['d'][v]}/{lastq['f'][v]}" for v in G.Q_V}
    es = {}
    for (a, b), k in lastq["cls"].items():
        es[(a, b)] = "tree" if k == "T" else "back"
    p.put("fig-q-sol", f"![Bosque DF desde q]({static(p, 'q-sol', G.Q_POS, G.Q_E, True, labels=lab, edge_style=es, label_pos=G.Q_LP)})")
    sn5 = dfs_trace(G.G5_V, adjacency(G.G5_V, G.G5_E), ["3", "1", "2", "4", "5"], False)
    p.put("ex2-sol", df_table(G.G5_V, sn5))
    p.put("ex2-parens", parens(sn5))
    p.put("fig-ex2", f"![Grafo 1..5]({static(p, 'ex2-grafo', G.G5_POS, G.G5_E)})")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
