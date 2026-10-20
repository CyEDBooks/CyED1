from common import *
from gviz import dijkstra_steps, dijkstra_path_steps, mv
from algos import adjacency, dijkstra_trace, path_to, bfs_trace
import graphs as G


def static(page, name, pos, edges, directed=False, **kw):
    svg = SVG()
    draw_graph(svg, pos, edges, directed, **kw)
    return page.img(name, svg)


def short(vs, es, posd, lpd=None):
    sh = {v: v for v in vs}
    if vs == G.SA_V:
        sh = G.SA_SHORT
    elif vs == G.DE_V:
        sh = G.DE_SHORT
    V = [sh[v] for v in vs]
    E = [(sh[a], sh[b], w) for a, b, w in es]
    P = {sh[k]: v for k, v in posd.items()}
    LP = {sh[k]: v for k, v in (lpd or {}).items()}
    return V, E, P, LP


EX_V = list("abcdefgh")
EX_E = [("a", "b", 4), ("a", "c", 2), ("b", "c", 1), ("b", "d", 5), ("c", "d", 8), ("c", "e", 10),
        ("d", "e", 2), ("d", "f", 6), ("e", "f", 2), ("e", "g", 5), ("f", "h", 3), ("g", "h", 1)]
EX_POS = scale({"a": (0, 1), "b": (1.2, 0), "c": (1.2, 2), "d": (2.5, 0), "e": (2.5, 2),
                "f": (3.7, 1), "g": (3.7, 2.8), "h": (4.8, 1.8)}, 95)
EX_LP = {"a": "left", "b": "above", "d": "above", "c": "below", "e": "below", "f": "above",
         "g": "below", "h": "right"}

NEG_V = list("abc")
NEG_E = [("a", "b", 2), ("a", "c", 3), ("c", "b", -2)]
NEG_POS = scale({"a": (0, 1), "b": (1.6, 0), "c": (1.6, 2)}, 80)
NEG_LP = {"a": "left", "b": "right", "c": "right"}

BFS_V = ["s", "a", "t"]
BFS_E = [("s", "t", 10), ("s", "a", 1), ("a", "t", 1)]
BFS_POS = scale({"s": (0, 1), "a": (1.2, 0), "t": (2.4, 1)}, 80)


def table_final(V, snaps, s):
    last = snaps[-1]
    rows = []
    for v in V:
        rows.append([f"${mv(v)}$", fmt(last["L"][v]),
                     " → ".join(path_to(last["pred"], v)) if last["L"][v] < INF else "—"])
    return md_table(["Destino", "Costo mínimo", "Camino"], rows)


def build():
    p = Page("Unidad5-Grafos/Dijkstra")

    p.put("fig-problema", f"![Grafo dirigido con pesos]({static(p, 'problema', G.BED_POS, G.BED_E, True)})")
    # BFS falla con pesos
    ns = {"s": "black", "t": "hl"}
    p.put("fig-bfs-falla", f"![Contraejemplo para BFS]({static(p, 'bfs-falla', BFS_POS, BFS_E, False, edge_style={('s', 't'): 'new'})})")

    # Ejemplo 1: Bedoya
    st, sn1 = dijkstra_steps(p, "ej1", G.BED_V, G.BED_POS, G.BED_E, "a", directed=True,
                             label_pos=G.BED_LP,
                             questions={2: "c ya tiene etiqueta [1,a] y ahora es permanente. "
                                           "¿Puede aparecer después un camino más barato hasta c?"},
                             notes={3: "> No. Cualquier otro camino de $a$ a $c$ tendría que pasar antes por "
                                       "un vértice no permanente, y todos tienen etiqueta $\\geq 1$. "
                                       "Como los pesos no son negativos, ese camino no puede costar "
                                       "menos que $1$. Por eso una etiqueta permanente **no cambia "
                                       "nunca**."})
    p.put("ej1", steps("Dijkstra desde a", st))
    p.put("ej1-camino-d", steps("Camino mínimo de a a d", dijkstra_path_steps(
        p, "ej1-cam-d", G.BED_V, G.BED_POS, G.BED_E, sn1, "a", "d", True, G.BED_LP)))
    p.put("ej1-camino-f", steps("Camino mínimo de a a f", dijkstra_path_steps(
        p, "ej1-cam-f", G.BED_V, G.BED_POS, G.BED_E, sn1, "a", "f", True, G.BED_LP)))
    p.put("ej1-final", table_final(G.BED_V, sn1, "a"))

    # Ejemplo 2: Bogotá - Buenos Aires
    V, E, P, LP = short(G.SA_V, G.SA_E, G.SA_POS, G.SA_LP)
    p.put("fig-sa", f"![Ciudades de Suramérica]({static(p, 'sa', P, E, r=21)})")
    st, sn2 = dijkstra_steps(p, "ej2", V, P, E, "Bog", label_pos=LP,
                             questions={3: "Paz es el siguiente permanente. Por Paz, Asu costaría "
                                           "8 + 2 = 10, igual a su etiqueta actual [10,Lim]. "
                                           "¿Se cambia la etiqueta de Asu?"},
                             notes={4: "> No se cambia: Dijkstra reetiqueta solo si el nuevo valor es "
                                       "**estrictamente menor**. Los dos caminos cuestan $10$; se "
                                       "conserva el que se encontró primero."})
    p.put("ej2", steps("Dijkstra desde Bogotá", st))
    p.put("ej2-camino", steps("Camino mínimo de Bogotá a Buenos Aires", dijkstra_path_steps(
        p, "ej2-cam", V, P, E, sn2, "Bog", "BA", False, LP)))

    # Ejemplo 3: Alemania
    V, E, P, LP = short(G.DE_V, G.DE_E, G.DE_POS)
    LP = G.DE_LP
    p.put("fig-de", f"![Mapa del sur de Alemania con distancias]({static(p, 'de', P, E, r=22)})")
    st, sn3 = dijkstra_steps(p, "ej3", V, P, E, "Fra", label_pos=LP,
                             questions={5: "Mün tiene la etiqueta [675,Kas]. ¿Puede mejorar todavía?"},
                             notes={6: "> Sí: por Nür, Mün cuesta $320 + 167 = 487 < 675$. "
                                       "Se reetiqueta con $[487,\\text{Nür}]$. La etiqueta de un "
                                       "vértice que **no** es permanente todavía puede bajar."})
    p.put("ej3", steps("Dijkstra desde Frankfurt", st))
    p.put("ej3-final", table_final(V, sn3, "Fra"))

    # Contraejemplo con peso negativo (para la sección de limitaciones)
    p.put("fig-neg", f"![Grafo con un peso negativo]({static(p, 'neg', NEG_POS, NEG_E, True)})")
    st, _ = dijkstra_steps(p, "neg", NEG_V, NEG_POS, NEG_E, "a", directed=True, label_pos=NEG_LP,
                           notes={-1: "> Dijkstra termina con $b = [2,a]$, pero el camino "
                                      "$a \\to c \\to b$ cuesta $3 + (-2) = 1$. Cuando $b$ se volvió "
                                      "permanente se supuso que nada podía abaratarlo, y con un peso "
                                      "negativo eso es falso."})
    p.put("neg", steps("Dijkstra con un peso negativo", st))
    p.assemble("index.md")

    # ejercicios
    p.put("fig-ex1", f"![Grafo a..h]({static(p, 'ex1', EX_POS, EX_E)})")
    sx = dijkstra_trace(EX_V, adjacency(EX_V, EX_E), "a")
    p.put("ex1-sol", table_final(EX_V, sx, "a"))
    p.put("ex1-orden", ", ".join(f"${x['u']}$ ({fmt(x['L'][x['u']])})" for x in sx[1:]))
    V, E, P, LP = short(G.SA_V, G.SA_E, G.SA_POS, G.SA_LP)
    sba = dijkstra_trace(V, adjacency(V, E), "BA")
    p.put("ex2-sol", table_final(V, sba, "BA"))
    p.put("ex2-orden", ", ".join(f"{x['u']} ({fmt(x['L'][x['u']])})" for x in sba[1:]))
    p.put("fig-ex2", f"![Ciudades de Suramérica]({static(p, 'ex2', P, E, r=21)})")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
