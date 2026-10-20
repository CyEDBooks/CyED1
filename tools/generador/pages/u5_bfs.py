from common import *
from gviz import bfs_steps, mv
from algos import adjacency, bfs_trace
import graphs as G


def static(page, name, pos, edges, directed=False, **kw):
    svg = SVG()
    draw_graph(svg, pos, edges, directed, **kw)
    return page.img(name, svg)


def table_final(vertices, snaps):
    last = snaps[-1]
    header = ["", *[f"${mv(v)}$" for v in vertices]]
    rd = ["$d$", *[fmt(last["d"][v]) for v in vertices]]
    rp = ["$\\pi$", *[(last["pi"][v] or "NIL") for v in vertices]]
    return md_table(header, [rd, rp])


def build():
    p = Page("Unidad5-Grafos/BFS")

    # Problema: el grafo de CLRS sin marcar
    p.put("fig-problema", f"![Red de estaciones]({static(p, 'problema', G.CLRS_POS, G.CLRS_E)})")

    # Ejemplo 1: árbol
    tpos, tedges = tree_pos(G.TREE_AI, 70, 70)
    tv = list("ABCDEFGHI")
    lp = {v: "right" for v in tv}
    st, _ = bfs_steps(p, "ej1", tv, tpos, tedges, "A", label_pos=lp, table=False,
                      questions={3: "¿Quién sale de la cola ahora: C o H? ¿Por qué?"},
                      notes={4: "> Sale $C$ (no $H$): $C$ entró a la cola antes. La cola respeta el "
                                "orden de llegada, y eso hace que se terminen los vértices a "
                                "distancia $2$ antes de pasar a los de distancia $3$."})
    p.put("ej1", steps("Recorrido BFS desde A", st))

    # Ejemplo 2: CLRS desde s
    st, snaps = bfs_steps(p, "ej2", G.CLRS_V, G.CLRS_POS, G.CLRS_E, "s", label_pos=G.CLRS_LP,
                          questions={4: "Al extraer t, su vecino x ya es gris. ¿Se cambia x.d?"},
                          notes={5: "> No. $x$ ya fue descubierto (desde $w$) con $d = 2$. Un vértice "
                                    "se descubre **una sola vez**: el primer camino que lo alcanza "
                                    "es el más corto, porque la cola procesa por niveles."})
    p.put("ej2", steps("Recorrido BFS desde s", st))
    p.put("ej2-final", table_final(G.CLRS_V, snaps))

    # Ejemplo 3: grafo 1..5 desde 3
    st, snaps3 = bfs_steps(p, "ej3", G.G5_V, G.G5_POS, G.G5_E, "3", label_pos=G.G5_LP)
    p.put("fig-ej3", f"![Grafo de 5 vértices]({static(p, 'ej3-grafo', G.G5_POS, G.G5_E)})")
    p.put("ej3", steps("Recorrido BFS desde 3", st))

    # Ejemplo 4: dirigido desde 3
    st, snaps4 = bfs_steps(p, "ej4", G.D6_V, G.D6_POS, G.D6_E, "3", directed=True,
                           label_pos=G.D6_LP,
                           questions={0: "¿Llegará el recorrido a todos los vértices?"},
                           notes={-1: "> La cola quedó vacía y el vértice $1$ sigue "
                                  "blanco con $d = \\infty$: **no es alcanzable** desde $3$. Ninguna "
                                  "arista entra a $1$."})
    p.put("fig-ej4", f"![Grafo dirigido de 6 vértices]({static(p, 'ej4-grafo', G.D6_POS, G.D6_E, True)})")
    p.put("ej4", steps("Recorrido BFS desde 3 (grafo dirigido)", st))

    # Árbol BF y camino (CLRS)
    last = snaps[-1]
    es = {(last["pi"][v], v): "tree" for v in G.CLRS_V if last["pi"][v]}
    lab = {v: str(last["d"][v]) for v in G.CLRS_V}
    p.put("fig-arbolbf", f"![Árbol BF desde s]({static(p, 'arbolbf', G.CLRS_POS, G.CLRS_E, edge_style={**{(a, b): 'dim' for a, b in G.CLRS_E}, **es}, labels=lab, label_pos=G.CLRS_LP)})")
    chain = ["y"]
    while last["pi"][chain[-1]]:
        chain.append(last["pi"][chain[-1]])
    cam = []
    for k in range(1, len(chain) + 1):
        part = chain[:k]
        ns = {v: "hl" for v in part}
        e2 = {**{(a, b): "dim" for a, b in G.CLRS_E}, **es}
        for a, b in zip(part[1:], part):
            e2[(a, b)] = "new"
        img = static(p, f"camino-{k:02d}", G.CLRS_POS, G.CLRS_E, node_style=ns, edge_style=e2,
                     labels=lab, label_pos=G.CLRS_LP)
        v = part[-1]
        if last["pi"][v]:
            txt = (f"> `PRINT-PATH(G, s, {v})`: como ${v} \\neq s$, primero se imprime el camino hasta "
                   f"${v}.\\pi = {last['pi'][v]}$.")
        else:
            txt = (f"> `PRINT-PATH(G, s, s)`: caso base, se imprime $s$. Al regresar de las llamadas "
                   f"se imprime el resto: ${' \\to '.join(chain[::-1])}$.")
        cam.append(f"![Camino, paso {k}]({img})\n\n{txt}")
    p.put("camino", steps("Camino más corto de s a y", cam))

    p.assemble("index.md")

    # ejercicios
    pe = p
    # Ej 1: CLRS desde u
    s1 = bfs_trace(G.CLRS_V, adjacency(G.CLRS_V, G.CLRS_E), "u")
    pe.put("ex1-sol", table_final(G.CLRS_V, s1))
    # Ej 2: Alemania desde Frankfurt
    sh = G.DE_SHORT
    V = [sh[v] for v in G.DE_V]
    E = [(sh[a], sh[b]) for a, b, _ in G.DE_E]
    POS = {sh[k]: v for k, v in G.DE_POS.items()}
    pe.put("fig-de", f"![Mapa del sur de Alemania]({static(pe, 'alemania', POS, E, r=22)})")
    s2 = bfs_trace(V, adjacency(V, E), "Fra")
    last = s2[-1]
    es = {**{(a, b): "dim" for a, b in E}, **{(last["pi"][v], v): "tree" for v in V if last["pi"][v]}}
    lab = {v: str(last["d"][v]) for v in V}
    pe.put("fig-de-sol", f"![Árbol BF desde Frankfurt]({static(pe, "alemania-bf", POS, E, edge_style=es, labels=lab, r=22, label_pos=G.DE_LP)})")
    pe.put("ex2-orden", ", ".join(f"{v}" for v in [x["u"] for x in s2[1:]]))
    # Ej 3: dirigido desde 1
    s3 = bfs_trace(G.D6_V, adjacency(G.D6_V, G.D6_E, True), "1")
    pe.put("fig-ex3", f"![Grafo dirigido]({static(pe, 'ex3-grafo', G.D6_POS, G.D6_E, True)})")
    pe.put("ex3-sol", table_final(G.D6_V, s3))
    # Ej 4: el orden de las listas de adyacencia
    pe.put("fig-ex4", f"![Grafo 1..5]({static(pe, 'ex4-grafo', G.G5_POS, G.G5_E)})")
    pe.assemble("exercises.md")


if __name__ == "__main__":
    build()
