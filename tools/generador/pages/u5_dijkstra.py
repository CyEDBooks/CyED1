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
# Bogotá - Buenos Aires con cada tramo dirigido hacia el sur (de Bogotá hacia Buenos Aires)
SA_DIR = [("Bogotá", "Lima", 4), ("Bogotá", "Quito", 2), ("Quito", "Lima", 1), ("Lima", "La Paz", 5),
          ("Lima", "Asunción", 7), ("Quito", "La Paz", 8), ("Quito", "Asunción", 10),
          ("La Paz", "Asunción", 2), ("La Paz", "B. Aires", 6), ("Asunción", "B. Aires", 3)]
assert {frozenset(e[:2]) for e in SA_DIR} == {frozenset(e[:2]) for e in G.SA_E}

BFS_POS = scale({"s": (0, 1), "a": (1.2, 0), "t": (2.4, 1)}, 80)


def _svg(pos, E):
    svg = SVG()
    draw_graph(svg, pos, E, True)
    return svg


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
    p.put("fig-bfs-falla", f"![Contraejemplo para BFS]({static(p, 'bfs-falla', BFS_POS, BFS_E, True, edge_style={('s', 't'): 'new'})})")

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
    V, E, P, LP = short(G.SA_V, SA_DIR, G.SA_POS, G.SA_LP)
    p.put("fig-sa", f"![Ciudades de Suramérica]({static(p, 'sa', P, E, True)})")
    st, sn2 = dijkstra_steps(p, "ej2", V, P, E, "Bog", directed=True, label_pos=LP,
                             questions={3: "Paz es el siguiente permanente. Por Paz, Asu costaría "
                                           "8 + 2 = 10, igual a su etiqueta actual [10,Lim]. "
                                           "¿Se cambia la etiqueta de Asu?"},
                             notes={4: "> No se cambia: Dijkstra reetiqueta solo si el nuevo valor es "
                                       "**estrictamente menor**. Los dos caminos cuestan $10$; se "
                                       "conserva el que se encontró primero."})
    p.put("ej2", steps("Dijkstra desde Bogotá", st))
    p.put("ej2-camino", steps("Camino mínimo de Bogotá a Buenos Aires", dijkstra_path_steps(
        p, "ej2-cam", V, P, E, sn2, "Bog", "BA", True, LP)))
    assert sn2[-1]["L"]["BA"] == 13

    # Ejemplo 3: Alemania
    V, E, P, LP = short(G.DE_V, G.DE_E, G.DE_POS)
    LP = G.DE_LP
    p.put("fig-de", f"![Mapa del sur de Alemania con distancias]({static(p, 'de', P, E, True)})")
    st, sn3 = dijkstra_steps(p, "ej3", V, P, E, "Fra", directed=True, label_pos=LP,
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

    # Ejercicios: los grafos dirigidos de Bedoya, con las etiquetas finales de sus diapositivas
    G6 = scale({"a": (0, 1), "b": (1, 0), "c": (1, 2), "d": (2.6, 0), "e": (2.6, 2), "f": (3.6, 1)}, 80)
    G6b = scale({"a": (0, 1), "b": (1, 0), "e": (2.2, 0), "c": (1, 1), "f": (2.2, 1), "d": (1, 2)}, 85)
    G6c = scale({"a": (0, 0), "c": (1.2, 0), "e": (2.4, 0), "b": (0, 1.2), "d": (1.2, 1.2),
                 "f": (2.4, 1.2)}, 85)
    G8 = scale({"a": (0, 1), "b": (1.1, 0), "e": (2.3, 0), "c": (1.1, 1), "f": (2.3, 1), "h": (3.4, 1),
                "d": (1.1, 2), "g": (2.3, 2)}, 85)
    G10 = scale({"b": (0, 0), "d": (1.2, 0), "g": (2.4, 0), "a": (0, 1), "e": (1.2, 1), "h": (2.4, 1),
                 "j": (3.6, 1), "c": (0, 2), "f": (1.2, 2), "i": (2.4, 2)}, 85)
    bed = {
        "D1": (G6, [("a", "b", 3), ("a", "c", 5), ("b", "c", 1), ("b", "d", 6), ("c", "d", 2),
                    ("d", "e", 2), ("c", "e", 2), ("d", "f", 7), ("e", "f", 3)], "f",
               {"b": (3, "a"), "c": (4, "b"), "d": (6, "c"), "e": (6, "c"), "f": (9, "e")}),
        "D2": (G6b, [("a", "b", 6), ("a", "c", 4), ("a", "d", 2), ("d", "c", 1), ("c", "b", 2),
                     ("b", "e", 1), ("e", "f", 2), ("c", "f", 8), ("d", "f", 7)], "f",
               {"d": (2, "a"), "c": (3, "d"), "b": (5, "c"), "e": (6, "b"), "f": (8, "e")}),
        "D3": (G6c, [("a", "c", 7), ("a", "b", 5), ("b", "c", 1), ("c", "d", 1), ("b", "d", 4),
                     ("c", "e", 6), ("c", "f", 4), ("e", "f", 3), ("d", "f", 2)], "f",
               {"b": (5, "a"), "c": (6, "b"), "d": (7, "c"), "e": (12, "c"), "f": (9, "d")}),
        "D4": (G8, [("a", "b", 6), ("a", "c", 4), ("a", "d", 2), ("d", "c", 1), ("c", "b", 3),
                    ("b", "e", 6), ("c", "f", 3), ("f", "e", 2), ("e", "h", 1), ("f", "h", 5),
                    ("d", "g", 7), ("g", "f", 3), ("g", "h", 6)], "h",
               {"d": (2, "a"), "c": (3, "d"), "b": (6, "a"), "f": (6, "c"), "e": (8, "f"),
                "g": (9, "d"), "h": (9, "e")}),
        "D5": (G10, [("a", "b", 3), ("a", "e", 5), ("a", "c", 1), ("b", "d", 4), ("e", "d", 1),
                     ("d", "g", 3), ("f", "e", 1), ("c", "f", 2), ("e", "h", 9), ("g", "h", 4),
                     ("g", "j", 8), ("h", "j", 7), ("h", "i", 1), ("f", "i", 12), ("i", "j", 5)], "j",
               {"c": (1, "a"), "b": (3, "a"), "f": (3, "c"), "e": (4, "f"), "d": (5, "e"),
                "g": (8, "d"), "h": (12, "g"), "i": (13, "h"), "j": (16, "g")}),
        "D6": (G8, [("a", "b", 1), ("a", "c", 3), ("a", "d", 5, -30), ("b", "c", 1),
                    ("b", "e", 8), ("b", "f", 6), ("c", "f", 5), ("c", "d", 2), ("c", "g", 4),
                    ("d", "g", 1), ("g", "f", 1), ("f", "e", 2), ("e", "h", 1), ("f", "h", 5),
                    ("g", "h", 5)], "h",
               {"b": (1, "a"), "c": (2, "b"), "d": (4, "c"), "g": (5, "d"), "f": (6, "g"),
                "e": (8, "f"), "h": (9, "e")}),
    }

    def bed_solution(key, pos, E, t, want):
        V = sorted(pos)
        sn = dijkstra_trace(V, adjacency(V, E, True), "a")
        last = sn[-1]
        got = {v: (last["L"][v], last["pred"][v]) for v in V if v != "a"}
        assert got == want, (key, got)
        path = path_to(last["pred"], t)
        es = {(x, y): "new" for x, y in zip(path, path[1:])}
        lab = {v: f"[{fmt(last['L'][v])},{last['pred'][v] or '-'}]" for v in V}
        svg = SVG()
        draw_graph(svg, pos, E, True, node_style={v: "hl" for v in V}, edge_style=es, labels=lab)
        img = p.img(f"{key}-sol", svg)
        orden = ", ".join(f"${x['u']}$" for x in sn[1:])
        return (f"Orden en que los vértices se vuelven permanentes: {orden}.\n\n![Etiquetas finales]({img})"
                f"\n\nEl acumulado mínimo en ${t}$ es ${fmt(last['L'][t])}$. El camino mínimo es "
                f"${' \\to '.join(path)}$.")
    for key in bed:
        pos, E, t, want = bed[key]
        p.put(f"fig-{key}", f"![Grafo dirigido con pesos]({static(p, key, pos, E, True)})")
    p.put("fig-bd1", graph_row(p, "bd1", [(bed["D1"][0], bed["D1"][1], "a)", {"directed": True}),
                                          (bed["D3"][0], bed["D3"][1], "b)", {"directed": True})], gap=90))
    p.put("bd1-sol", "a) " + bed_solution("D1", *bed["D1"]) + "\n\nb) " + bed_solution("D3", *bed["D3"]))
    for out_key, key in (("bd2", "D2"), ("bd3", "D4"), ("bd4", "D5"), ("bd5", "D6")):
        p.put(f"fig-{out_key}", f"![Grafo dirigido con pesos]({p.img(out_key, _svg(bed[key][0], bed[key][1]))})")
        p.put(f"{out_key}-sol", bed_solution(key, *bed[key]))
    E7 = [("a", "b", 1), ("a", "c", 4), ("a", "d", 5, -30), ("b", "e", 4), ("b", "c", 2),
          ("c", "e", 2), ("c", "f", 6), ("f", "e", 4), ("e", "h", 7), ("f", "h", 3), ("c", "d", 1),
          ("d", "f", 5), ("d", "g", 1), ("g", "f", 2), ("g", "h", 6)]
    p.put("fig-bd7", f"![Grafo dirigido con pesos]({p.img('bd7', _svg(G8, E7))})")
    # Ejercicio: el mismo mapa con todos los tramos invertidos, desde Buenos Aires
    V, E, P, LP = short(G.SA_V, [(b, a, w) for a, b, w in SA_DIR], G.SA_POS, G.SA_LP)
    sba = dijkstra_trace(V, adjacency(V, E, True), "BA")
    assert sba[-1]["L"]["Bog"] == 13
    p.put("ex2-sol", table_final(V, sba, "BA"))
    p.put("ex2-orden", ", ".join(f"{x['u']} ({fmt(x['L'][x['u']])})" for x in sba[1:]))
    p.put("fig-ex2", f"![Ciudades de Suramérica, tramos invertidos]({static(p, 'ex2', P, E, True)})")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
