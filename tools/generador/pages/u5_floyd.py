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

    # Ejercicios: los siete grafos de Bedoya, dados por su W0, con las respuestas de las diapositivas
    I = INF

    def from_w0(V, rows):
        return [(V[i], V[j], w) for i, r in enumerate(rows) for j, w in enumerate(r) if i != j and w != I]
    pos4 = scale({"a": (0, 0), "b": (1.4, 0), "c": (0, 1.2), "d": (1.4, 1.2)}, 85)
    pos5 = scale({"a": (0, 0.8), "b": (1.2, 0), "c": (1.2, 1.6), "d": (2.5, 0), "e": (2.5, 1.6)}, 80)
    pos6 = scale({"a": (0, 1), "b": (1.2, 0), "c": (1.2, 2), "d": (2.6, 0), "e": (2.6, 2), "f": (3.7, 1)}, 80)
    fw = [
        ("abcd", pos4, [[0, 5, I, I], [I, 0, I, 2], [3, I, 0, 4], [6, I, 1, 0]],
         [("b", "a", 6, "bdca"), ("a", "c", 8, "abdc")]),
        ("abcd", pos4, [[0, 4, 7, I], [I, 0, 1, 6], [I, I, 0, 2], [I, 3, I, 0]],
         [("a", "d", 7, "abcd"), ("d", "c", 4, "dbc")]),
        ("abcde", pos5, [[0, 5, 1, I, I], [I, 0, I, 3, I], [I, I, 0, I, 2], [6, I, I, 0, 4],
                         [I, I, I, I, 0]],
         [("b", "c", 10, "bdac"), ("a", "e", 3, "ace")]),
        ("abcde", pos5, [[0, 4, 2, I, I], [I, 0, I, 6, 1], [I, 1, 0, I, 4], [I, I, I, 0, I],
                         [I, I, 3, 2, 0]],
         [("a", "d", 6, "acbed"), ("c", "d", 4, "cbed")]),
        ("abcde", pos5, [[0, 3, 5, I, I], [I, 0, 1, 6, I], [I, I, 0, 2, 7], [I, 4, I, 0, 2],
                         [I, I, I, 3, 0]],
         [("a", "e", 8, "abcde"), ("e", "c", 8, "edbc")]),
        ("abcde", pos5, [[0, I, 2, I, I], [1, 0, I, 4, I], [I, I, 0, 1, 5], [3, I, I, 0, 1],
                         [I, 5, I, I, 0]],
         [("a", "e", 4, "acde"), ("e", "c", 8, "ebac")]),
        ("abcdef", pos6, [[0, 3, 5, I, I, I], [I, 0, 1, 6, I, I], [I, I, 0, 2, 2, I],
                          [I, I, I, 0, 2, 7], [I, I, I, I, 0, 3], [I, I, I, I, I, 0]],
         [("a", "d", 6, "abcd"), ("a", "f", 9, "abcef")]),
    ]
    enun = {1: [], 2: []}
    sols = {1: [], 2: []}
    for k, (Vs, pos, W0, asks) in enumerate(fw):
        V = list(Vs)
        E = from_w0(V, W0)
        t = floyd_trace(V, E)
        idx = {v: i for i, v in enumerate(V)}
        lines = []
        for x, y, want, route in asks:
            got = t[-1]["W"][idx[x]][idx[y]]
            r = floyd_route(V, t[-1]["P"], x, y)[-1]
            assert got == want and "".join(r) == route, (k, x, y, got, r)
            lines.append(f"entre ${x}$ y ${y}$: valor mínimo ${want}$, recorrido ${', '.join(r)}$")
        grp = 1 if k < 4 else 2
        cap = "abcd"[k if grp == 1 else k - 4] + ")"
        img = static(p, f"fw{k + 1}", pos, E)
        q = " y ".join(f"entre ${x}$ y ${y}$" for x, y, *_ in asks)
        enun[grp].append(f"{cap} Encuentre los valores mínimos y los recorridos {q}.\n\n![Grafo dirigido con pesos]({img})")
        Wm = latex_matrix("W", V, V, t[-1]["W"], (), lfmt, sub=f"_{{{len(V)}}}")
        Pm = latex_matrix("P", V, V, t[-1]["P"], (), str, sub=f"_{{{len(V)}}}")
        cambios = ", ".join(f"${x['k']}$: {len(x['changed'])}" for x in t[1:])
        sols[grp].append(f"{cap} Casillas que mejoran con cada pivote: {cambios}.\n\n$$\n{Wm} \\qquad {Pm}\n$$\n\n"
                         + "; ".join(lines) + ".")
    for g in (1, 2):
        p.put(f"fw-enunciados-{g}", "\n\n".join(enun[g]))
        p.put(f"fw-soluciones-{g}", "\n\n".join(sols[g]))
    posO = scale({"a": (0, 0), "b": (1.3, 0), "d": (2.6, 0), "c": (1.3, 1.3), "e": (2.6, 1.3)}, 80)
    EO = [("a", "b", 4), ("a", "c", 2), ("c", "b", 1), ("b", "d", 3), ("d", "e", 2), ("e", "c", 5),
          ("e", "a", 4, 40)]
    p.put("fig-fw-open", f"![Grafo dirigido con pesos]({static(p, 'fw-open', posO, EO)})")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
