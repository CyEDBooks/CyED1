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
    p.put("fig-problema", f"![Red de sedes con costos]({static(p, 'problema', G.MST_POS, G.MST_E)})")
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
    st, sn2 = prim_steps(p, "ej2", MST2_V, MST2_POS, MST2_E, "a")
    p.put("ej2", steps("Prim desde a", st))
    p.put("ej2-peso", str(sum(e[2] for e in sn2[-1]["T"])))

    st, sn3 = prim_steps(p, "ej3", MST2_V, MST2_POS, MST2_E, "e")
    p.put("ej3", steps("Prim desde e", st))
    p.put("ej3-peso", str(sum(e[2] for e in sn3[-1]["T"])))
    p.put("ej2-aristas", edge_list(sn2[-1]["T"]))
    p.put("ej3-aristas", edge_list(sn3[-1]["T"]))
    p.assemble("index.md")

    p.put("fig-ex1", f"![Grafo a..h]({static(p, 'ex1', EX_POS, EX_E)})")
    t = prim_trace(EX_V, EX_E, "a")[-1]["T"]
    p.put("ex1-sol", edge_list(t))
    p.put("ex1-peso", str(sum(e[2] for e in t)))
    p.put("fig-ex1-sol", f"![Árbol recubridor mínimo]({tree_fig(p, 'ex1-sol', EX_POS, EX_E, t)})")
    t = prim_trace(EX_V, EX_E, "h")[-1]["T"]
    p.put("ex2-sol", edge_list(t))
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

    p.put("fig-ex1", f"![Grafo a..h]({static(p, 'ex1', EX_POS, EX_E)})")
    sk = kruskal_trace(EX_V, EX_E)
    p.put("ex1-sol", edge_list(sk[-1]["T"]))
    p.put("ex1-desc", ", ".join(f"$\\{{{x['edge'][0]},{x['edge'][1]}\\}}$" for x in sk[1:] if not x["accepted"]) or "ninguna")
    p.put("ex1-peso", str(sum(e[2] for e in sk[-1]["T"])))
    p.assemble("exercises.md")


def build():
    build_prim()
    build_kruskal()


if __name__ == "__main__":
    build()
