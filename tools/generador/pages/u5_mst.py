from common import *
from gviz import prim_steps, kruskal_steps, mv
from algos import prim_trace, kruskal_trace
import graphs as G

MST2_V = list("abcdef")
MST2_E = [("a", "b", 6), ("a", "c", 1), ("a", "d", 5), ("b", "c", 5), ("c", "d", 5), ("b", "e", 3),
          ("c", "e", 6), ("c", "f", 4), ("d", "f", 2), ("e", "f", 6)]
MST2_POS = scale({"a": (1.2, 0), "b": (0, 1), "c": (1.2, 1.1), "d": (2.4, 1), "e": (0.4, 2.3),
                  "f": (2.0, 2.3)}, 100)

EX_V = list("abcdefgh")
EX_E = [("a", "b", 4), ("a", "c", 3), ("b", "c", 2), ("b", "d", 5), ("c", "d", 6), ("c", "e", 4),
        ("d", "e", 1), ("d", "f", 7), ("e", "g", 5), ("f", "g", 2), ("f", "h", 3), ("g", "h", 4)]
EX_POS = scale({"a": (0, 1), "b": (1.2, 0), "c": (1.2, 2), "d": (2.5, 0.4), "e": (2.5, 1.9),
                "f": (3.8, 0.4), "g": (3.8, 1.9), "h": (5.0, 1.1)}, 95)

# Para mostrar qué es (y qué no es) un árbol recubridor
SP_V = list("abcde")
SP_E = [("a", "b"), ("a", "c"), ("b", "c"), ("b", "d"), ("c", "e"), ("d", "e")]
SP_POS = scale({"a": (1, 0), "b": (0, 1), "c": (2, 1), "d": (0.3, 2.1), "e": (1.7, 2.1)}, 80)


# Grafos de las diapositivas de Bedoya (cuadrícula a b c d / e f g h / i j k l)
GRID12 = {v: ((i % 4) * 95, (i // 4) * 85) for i, v in enumerate("abcdefghijkl")}
B3_E = [("a", "b", 2), ("b", "c", 3), ("c", "d", 1), ("a", "e", 3), ("b", "f", 1), ("c", "g", 2),
        ("d", "h", 5), ("e", "f", 4), ("f", "g", 3), ("g", "h", 3), ("e", "i", 4), ("f", "j", 2),
        ("g", "k", 4), ("h", "l", 3), ("i", "j", 3), ("j", "k", 3), ("k", "l", 1)]
B4_POS = scale({"a": (0, 0), "b": (1.2, 0), "c": (2.4, 0), "d": (3.1, 0.55), "e": (0, 1.1),
                "f": (1.2, 1.1), "g": (2.4, 1.1), "h": (1.2, 2.3)}, 85)
B4_E = [("a", "b", 1), ("b", "c", 2), ("a", "e", 4), ("b", "e", 3), ("b", "f", 4), ("b", "g", 1),
        ("c", "g", 6), ("c", "d", 4), ("d", "g", 2), ("e", "f", 1), ("f", "g", 8), ("e", "h", 5),
        ("f", "h", 2), ("g", "h", 7)]
B5_E = [("a", "b", 5), ("b", "c", 3), ("c", "d", 2), ("a", "e", 3), ("a", "f", 1), ("b", "f", 2),
        ("c", "f", 5), ("c", "g", 3), ("d", "h", 5), ("e", "f", 4), ("f", "g", 6), ("g", "h", 4),
        ("e", "i", 1), ("f", "i", 1), ("f", "j", 2), ("f", "k", 1), ("g", "k", 4), ("h", "l", 2),
        ("i", "j", 3), ("j", "k", 1), ("k", "l", 6)]
OPEN_E = [("a", "b", 2), ("b", "c", 3), ("c", "d", 1), ("a", "e", 3), ("b", "e", 3), ("b", "f", 6),
          ("b", "g", 1), ("c", "g", 4), ("d", "g", 7), ("d", "h", 5), ("e", "f", 4), ("f", "g", 9),
          ("g", "h", 2), ("e", "i", 1), ("f", "i", 3), ("f", "j", 5), ("f", "k", 1), ("g", "k", 4),
          ("h", "k", 5), ("h", "l", 3), ("i", "j", 3), ("j", "k", 3), ("k", "l", 8)]
CIT_POS = scale({"San Francisco": (0, 0.6), "Denver": (1.4, 0.95), "Chicago": (3.0, 0.3),
                 "New York": (4.4, 0), "Atlanta": (3.7, 1.9)}, 95)
CIT_E = [("San Francisco", "Chicago", 1200), ("San Francisco", "New York", 2000, -75),
         ("San Francisco", "Denver", 900), ("San Francisco", "Atlanta", 2200, 80),
         ("Denver", "Chicago", 1300), ("Denver", "New York", 1600), ("Denver", "Atlanta", 1400),
         ("Chicago", "New York", 1000), ("Chicago", "Atlanta", 700), ("New York", "Atlanta", 800)]
CIT_NAMES = {"San Francisco": "left", "Denver": "below", "Chicago": "above", "New York": "right",
             "Atlanta": "right"}


def static(page, name, pos, edges, directed=False, **kw):
    svg = SVG()
    draw_graph(svg, pos, edges, directed, **kw)
    return page.img(name, svg)


def tree_fig(page, name, pos, edges, T, **kw):
    es = {(a, b): "dim" for a, b, *_ in edges}
    ws = {(a, b): "dim" for a, b, *_ in edges}
    for e in T:
        es[(e[0], e[1])] = "tree"
        ws[(e[0], e[1])] = "tree"
    return static(page, name, pos, edges, edge_style=es, weight_style=ws, **kw)


def edge_list(T):
    return ", ".join(f"$\\{{{a},{b}\\}}$ ({w})" for a, b, w in T)


def build_prim():
    p = Page("Unidad5-Grafos/Prim")
    p.put("fig-problema", f"![Red de comunicaciones con costos]({static(p, 'problema', CIT_POS, CIT_E, name_pos=CIT_NAMES)})")
    t3600 = [("San Francisco", "Chicago"), ("San Francisco", "Denver"), ("Chicago", "Atlanta"),
             ("New York", "Atlanta")]
    t4700 = [("San Francisco", "Chicago"), ("Denver", "Chicago"), ("Denver", "Atlanta"),
             ("New York", "Atlanta")]
    w = {(a, b): x for a, b, x, *_ in CIT_E}
    assert sum(w[e] for e in t3600) == 3600 and sum(w[e] for e in t4700) == 4700
    mst = prim_trace(list(CIT_POS), [e[:3] for e in CIT_E], None)[-1]["T"]
    assert sum(e[2] for e in mst) == 3600
    items = []
    for T, cap in ((t3600, "costo 3600"), (t4700, "costo 4700")):
        es = {e: "new" for e in T}
        items.append((CIT_POS, CIT_E, cap, {"edge_style": es, "weight_style": es, "name_pos": CIT_NAMES}))
    p.put("fig-ciudades", graph_row(p, "ciudades", items, gap=120))
    # qué es un árbol recubridor
    p.put("fig-sp-g", f"![Grafo G]({static(p, 'sp-g', SP_POS, SP_E)})")
    p.put("fig-sp-t1", f"![Árbol recubridor de G]({tree_fig(p, 'sp-t1', SP_POS, SP_E, [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'e')])})")
    p.put("fig-sp-t2", f"![Otro árbol recubridor de G]({tree_fig(p, 'sp-t2', SP_POS, SP_E, [('a', 'b'), ('b', 'c'), ('b', 'd'), ('d', 'e')])})")
    p.put("fig-sp-no1", f"![Subgrafo con circuito]({tree_fig(p, 'sp-no1', SP_POS, SP_E, [('a', 'b'), ('a', 'c'), ('b', 'c'), ('d', 'e')])})")
    p.put("fig-sp-no2", f"![Subgrafo que no toca a e]({tree_fig(p, 'sp-no2', SP_POS, SP_E, [('a', 'b'), ('a', 'c'), ('b', 'd')])})")

    st, sn = prim_steps(p, "ej1", G.MST_V, G.MST_POS, G.MST_E, None,
                        questions={2: "La arista {b,d} pesa 6 y tiene un extremo en el árbol. "
                                      "¿Se puede escoger ahora?"},
                        notes={3: "> No se escogió: no era la de **menor** peso entre las candidatas "
                                  "($\\{a,d\\}$ y $\\{b,e\\}$ pesan $4$). Y ahora que $d$ entró al "
                                  "árbol, $\\{b,d\\}$ ya no es candidata: sus dos extremos están en "
                                  "el árbol y agregarla crearía un circuito."})
    p.put("ej1", steps("Prim, empezando por la arista de menor peso", st))
    p.put("ej1-aristas", edge_list(sn[-1]["T"]))
    p.put("ej1-peso", str(sum(e[2] for e in sn[-1]["T"])))

    p.put("fig-ej2", f"![Grafo con empates]({static(p, 'ej2-grafo', MST2_POS, MST2_E)})")
    st, sn2 = prim_steps(p, "ej2", MST2_V, MST2_POS, MST2_E, None)
    p.put("ej2", steps("Prim, empezando por la arista de menor peso", st))
    p.put("ej2-peso", str(sum(e[2] for e in sn2[-1]["T"])))

    st, sn3 = prim_steps(p, "ej3", MST2_V, MST2_POS, MST2_E, "e")
    p.put("ej3", steps("Prim desde e", st))
    p.put("ej3-peso", str(sum(e[2] for e in sn3[-1]["T"])))
    p.put("ej2-aristas", edge_list(sn2[-1]["T"]))
    p.put("ej3-aristas", edge_list(sn3[-1]["T"]))
    p.put("fig-ej1", f"![Grafo con pesos]({static(p, 'ej1-grafo', G.MST_POS, G.MST_E)})")
    same = {frozenset(e[:2]) for e in sn2[-1]["T"]} == {frozenset(e[:2]) for e in sn3[-1]["T"]}
    p.put("ej3-cmp", ("El **orden** en que entran las aristas cambió, pero el árbol y el peso son los "
                      "mismos." if same else
                      "El árbol es **otro**: cambian algunas aristas. Pero el peso es el mismo: los "
                      "dos son árboles recubridores mínimos.") +
          " Cuando hay empates, Prim puede producir árboles distintos según el punto de partida o la "
          "arista que escoja en un empate; todos tienen el mismo peso mínimo.")
    p.assemble("index.md")

    # Ejercicios (Bedoya)
    p.put("fig-bm3", f"![Cuadrícula con pesos]({static(p, 'bm3', GRID12, B3_E)})")
    t3 = prim_trace(list(GRID12), B3_E, None)[-1]["T"]
    assert sum(e[2] for e in t3) == 24        # costo que dan las diapositivas
    p.put("bm3-prim", f"Orden de las aristas: {edge_list(t3)}.\n\n"
                      f"![Árbol recubridor mínimo]({tree_fig(p, 'bm3-sol', GRID12, B3_E, t3)})\n\n"
                      f"Costo **{sum(e[2] for e in t3)}**.")
    p.put("fig-bm45", graph_row(p, "bm45", [(B4_POS, B4_E, "a)"), (GRID12, B5_E, "b)")], gap=90))
    sols = []
    for cap, pos, E, nm in (("a)", B4_POS, B4_E, "bm4"), ("b)", GRID12, B5_E, "bm5")):
        t = prim_trace(sorted(pos), E, None)[-1]["T"]
        sols.append(f"{cap} Orden: {edge_list(t)}. Costo **{sum(e[2] for e in t)}**.\n\n"
                    f"![Árbol recubridor mínimo]({tree_fig(p, nm + '-sol', pos, E, t)})")
    p.put("bm45-prim", "\n\n".join(sols))
    p.assemble("exercises.md")


def build_kruskal():
    p = Page("Unidad5-Grafos/Kruskal")
    p.put("fig-problema", f"![Red de sedes con costos]({static(p, 'problema', G.MST_POS, G.MST_E)})")
    st, sn = kruskal_steps(p, "ej1", G.MST_V, G.MST_POS, G.MST_E,
                           questions={5: "La siguiente arista es {b,e}, de peso 4. ¿Se agrega?"})
    p.put("ej1", steps("Kruskal", st))
    p.put("ej1-aristas", edge_list(sn[-1]["T"]))
    p.put("ej1-peso", str(sum(e[2] for e in sn[-1]["T"])))
    prim_t = prim_trace(G.MST_V, G.MST_E, None)[-1]["T"]
    p.put("fig-cmp-prim", f"![Árbol de Prim]({tree_fig(p, 'cmp-prim', G.MST_POS, G.MST_E, prim_t)})")
    p.put("fig-cmp-kruskal", f"![Árbol de Kruskal]({tree_fig(p, 'cmp-kruskal', G.MST_POS, G.MST_E, sn[-1]['T'])})")

    p.put("fig-ej2", f"![Grafo con empates]({static(p, 'ej2-grafo', MST2_POS, MST2_E)})")
    st, sn2 = kruskal_steps(p, "ej2", MST2_V, MST2_POS, MST2_E)
    p.put("ej2", steps("Kruskal", st))
    p.put("ej2-peso", str(sum(e[2] for e in sn2[-1]["T"])))

    # Tomar las aristas más baratas sin revisar circuitos
    order = sorted(G.MST_E, key=lambda e: (e[2], G.MST_E.index(e)))[:6]
    es = {(a, b): "dim" for a, b, _ in G.MST_E}
    ws = {(a, b): "dim" for a, b, _ in G.MST_E}
    for e in order:
        es[(e[0], e[1])] = "new"
        ws[(e[0], e[1])] = "new"
    p.put("fig-ingenuo", f"![Las seis aristas más baratas]({static(p, 'ingenuo', G.MST_POS, G.MST_E, edge_style=es, weight_style=ws)})")
    p.put("ingenuo-aristas", edge_list(order))
    p.assemble("index.md")

    items, sols = [], []
    for cap, pos, E, nm in (("a)", GRID12, B3_E, "k3"), ("b)", B4_POS, B4_E, "k4"), ("c)", GRID12, B5_E, "k5")):
        items.append((pos, E, cap))
        sk = kruskal_trace(sorted(pos), E)
        tk = sk[-1]["T"]
        tp = prim_trace(sorted(pos), E, None)[-1]["T"]
        assert sum(e[2] for e in tk) == sum(e[2] for e in tp)
        same = {frozenset(e[:2]) for e in tk} == {frozenset(e[:2]) for e in tp}
        desc = ", ".join(f"$\\{{{x['edge'][0]},{x['edge'][1]}\\}}$" for x in sk[1:]
                         if x["kind"] == "edge" and not x["accepted"]) or "ninguna"
        sols.append(f"{cap} Orden: {edge_list(tk)}. Descartadas: {desc}. Costo **{sum(e[2] for e in tk)}**, "
                    f"igual que con Prim; " + ("es el **mismo** árbol." if same else
                    "el árbol es **distinto** al de Prim (hay empates), con el mismo costo.") +
                    f"\n\n![Árbol de Kruskal]({tree_fig(p, nm + '-sol', pos, E, tk)})")
    p.put("fig-bmk", graph_row(p, "bmk", items, gap=80))
    p.put("bmk-sol", "\n\n".join(sols))
    p.put("fig-open", f"![Cuadrícula con pesos]({static(p, 'open', GRID12, OPEN_E)})")
    p.assemble("exercises.md")


def build():
    build_prim()
    build_kruskal()


if __name__ == "__main__":
    build()
