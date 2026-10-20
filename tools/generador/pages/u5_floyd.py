from common import *
from gviz import floyd_steps, floyd_route_steps, mv
from algos import floyd_trace, floyd_route
import graphs as G

CL_V = list("abcde")
CL_E = [("a", "b", 3), ("a", "c", 8), ("a", "e", -4), ("b", "d", 1), ("b", "e", 7), ("c", "b", 4),
        ("d", "a", 2), ("d", "c", -5), ("e", "d", 6)]
CL_POS = scale({"a": (0, 1), "b": (1.4, 0), "c": (2.8, 0.6), "d": (2.1, 2), "e": (0.7, 2)}, 95)

EX_V = list("abcde")
EX_E = [("a", "b", 2), ("a", "c", 9), ("b", "c", 4), ("b", "d", 7), ("c", "e", 1), ("d", "a", 3),
        ("e", "d", 2), ("e", "b", 6)]
EX_POS = scale({"a": (0, 1), "b": (1.3, 0), "c": (2.6, 0.5), "d": (1.3, 2), "e": (2.6, 1.6)}, 95)


def static(page, name, pos, edges, directed=True, **kw):
    svg = SVG()
    draw_graph(svg, pos, edges, directed, **kw)
    return page.img(name, svg)


def final_mats(V, E):
    t = floyd_trace(V, E)
    n = len(V)
    W = latex_matrix("W", V, V, t[-1]["W"], (), lfmt, sub=f"_{{{n}}}")
    P = latex_matrix("P", V, V, t[-1]["P"], (), str, sub=f"_{{{n}}}")
    return f"$$\n{W} \\qquad {P}\n$$", t


def route_text(V, t, a, b):
    idx = {v: i for i, v in enumerate(V)}
    r = floyd_route(V, t[-1]["P"], a, b)[-1]
    return f"valor mínimo ${lfmt(t[-1]['W'][idx[a]][idx[b]])}$, recorrido ${' \\to '.join(r)}$"


def build():
    p = Page("Unidad5-Grafos/FloydWarshall")
    p.put("fig-ej1", f"![Grafo dirigido a..d]({static(p, 'ej1-grafo', G.FW_POS, G.FW_E)})")
    st, sn = floyd_steps(G.FW_V, G.FW_E, fig=(p, "ej1", G.FW_POS),
                         questions={1: "Para el pivote b: ¿qué filas y columnas pueden mejorar? "
                                       "Pista: solo sirven las casillas (i, j) con W[i][b] y W[b][j] "
                                       "finitos."},
                         notes={2: "> Solo $d$ y $a$ llegan a $b$ (columna $b$ finita) y desde $b$ "
                                   "solo se llega a $d$ (fila $b$). Por eso las únicas casillas que "
                                   "se revisan con esperanza son $(a,d)$ y $(d,d)$; mejora $(a,d)$ "
                                   "(de $\\infty$ a $8$)."})
    p.put("ej1", steps("Floyd-Warshall: matrices W y P", st))
    for a, b in [("a", "d"), ("b", "c"), ("c", "b")]:
        p.put(f"ruta-{a}{b}", steps(f"Recorrido mínimo de {a} a {b}",
                                    floyd_route_steps(G.FW_V, sn, a, b)))

    p.put("fig-ej2", f"![Grafo con pesos negativos]({static(p, 'ej2-grafo', CL_POS, CL_E)})")
    st, sn2 = floyd_steps(CL_V, CL_E, fig=(p, "ej2", CL_POS),
                          notes={-1: "> Hay valores negativos en $W_5$, como $W[a][c] = -3$, pero "
                                     "ningún valor de la diagonal es negativo: el grafo no tiene "
                                     "circuitos de costo negativo y los resultados son válidos."})
    p.put("ej2", steps("Floyd-Warshall con pesos negativos", st))
    p.put("ruta2", steps("Recorrido mínimo de c a e", floyd_route_steps(CL_V, sn2, "c", "e")))
    p.assemble("index.md")

    p.put("fig-ex1", f"![Grafo a..e]({static(p, 'ex1', EX_POS, EX_E)})")
    m, t = final_mats(EX_V, EX_E)
    p.put("ex1-sol", m)
    p.put("ex1-ae", route_text(EX_V, t, "a", "e"))
    p.put("ex1-db", route_text(EX_V, t, "d", "b"))
    tt = floyd_trace(EX_V, EX_E)
    p.put("ex1-cambios", ", ".join(
        f"$W_{{{i}}}$ (pivote ${x['k']}$): {len(x['changed'])}" for i, x in enumerate(tt[1:], 1)))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
