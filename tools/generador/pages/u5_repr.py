from common import *
from algos import warshall_trace, bool_product, int_product


def mat(name, V, M, changed=(), cols=None, sub=None):
    return latex_matrix(name, V, cols or V, M, changed, str, sub=sub)


def adj_matrix(V, E, directed=False):
    idx = {v: i for i, v in enumerate(V)}
    M = [[0] * len(V) for _ in V]
    for e in E:
        a, b = idx[e[0]], idx[e[1]]
        M[a][b] += 1
        if not directed and a != b:
            M[b][a] += 1
    return M


def or_m(A, B):
    return [[int(a or b) for a, b in zip(r, s)] for r, s in zip(A, B)]


def build():
    p = Page("Unidad5-Grafos/RepresentacionConectividad")

    # Grafo simple de entrada
    V = list("abcd")
    pos = scale({"a": (0, 0), "b": (1, 0), "c": (0, 1), "d": (1, 1)}, 100)
    E = [("a", "b"), ("a", "c"), ("b", "c"), ("b", "d")]
    p.put("fig-r1", gfig(p, "r1", pos, E))
    M = adj_matrix(V, E)
    p.put("r1-mat", f"$$\n{mat('A', V, M)}\n$$")
    adjl = {v: [] for v in V}
    for a, b in E:
        adjl[a].append(b)
        adjl[b].append(a)
    p.put("r1-lista", "\n".join(f"- ${v}$: " + (", ".join(f"${x}$" for x in sorted(adjl[v])) or "∅")
                                for v in V))
    # revelado fila a fila de la matriz
    st = []
    for k in range(len(V)):
        Mk = [row[:] if i <= k else ["?"] * len(V) for i, row in enumerate(M)]
        ch = {(k, j) for j in range(len(V))}
        nb = ", ".join(f"${x}$" for x in sorted(adjl[V[k]]))
        st.append(f"$$\n{mat('A', V, Mk, ch)}\n$$\n\n> Fila ${V[k]}$: es adyacente a {nb}; en "
                  f"esas columnas va un $1$.")
    p.put("r1-steps", steps("Construir la matriz de adyacencia", st))

    # Pseudografo (grafos 2)
    posP = scale({"a": (0, 0), "b": (1.3, 0), "c": (0, 1.2), "d": (1.3, 1.2)}, 95)
    EP = [("a", "b", None, 14), ("a", "b", None, -14), ("a", "c"), ("a", "d"), ("b", "b"), ("b", "d")]
    p.put("fig-pseudo", gfig(p, "pseudo", posP, EP))
    MP = adj_matrix(V, EP)
    p.put("pseudo-mat", f"$$\n{mat('A', V, MP)}\n$$")
    MP2 = int_product(MP, MP)
    p.put("pseudo-mat2", f"$$\n{mat('A', V, MP)} \\qquad {latex_matrix('A^2', V, V, MP2, {(0, 0)}, str)}\n$$")
    p.put("pseudo-aa", str(MP2[0][0]))

    # Dirigido (grafos 2)
    V5 = list("abcde")
    pos5 = circle_pos(V5, 75)
    E5 = [("a", "b"), ("b", "c"), ("b", "d"), ("c", "d"), ("d", "e"), ("e", "a")]
    p.put("fig-dir", gfig(p, "dir", pos5, E5, True))
    M5 = adj_matrix(V5, E5, True)
    p.put("dir-mat", f"$$\n{mat('M_R', V5, M5)}\n$$")

    # Incidencia
    Einc = [("a", "b"), ("a", "c"), ("b", "c"), ("b", "d")]
    names = ["e_1", "e_2", "e_3", "e_4"]
    svg = SVG()
    draw_graph(svg, pos, Einc)
    for (a, b), nm in zip(Einc, names):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        svg.text((x1 + x2) / 2 + 10, (y1 + y2) / 2 - 6, nm.replace("_", ""), 13, PAL["teal"],
                 anchor="start", bg=True)
    p.put("fig-inc", f"![Grafo con aristas numeradas]({p.img('incidencia', svg)})")
    MI = [[1 if v in e else 0 for e in Einc] for v in V]
    p.put("inc-mat", f"$$\n{latex_matrix('M', V, names, MI, (), str)}\n$$")

    # Producto booleano (Bedoya)
    A = [[1, 0], [0, 1], [1, 1]]
    B = [[1, 1, 0], [0, 1, 1]]
    C = bool_product(A, B)
    st = []
    for i in range(3):
        rows = []
        for r in range(3):
            if r < i:
                rows.append(" & ".join(str(x) for x in C[r]))
            elif r == i:
                cells = []
                for j in range(3):
                    terms = " \\vee ".join(f"({A[r][t]} \\wedge {B[t][j]})" for t in range(2))
                    cells.append(c(f"{terms} = {C[r][j]}"))
                rows.append(" & ".join(cells))
            else:
                rows.append(" & ".join("?" for _ in range(3)))
        body = r"\\ ".join(rows)
        st.append(f"$$\nA \\odot B = \\begin{{bmatrix}} {body} \\end{{bmatrix}}\n$$\n\n> Fila {i + 1}: "
                  f"se combina la fila {i + 1} de $A$ con cada columna de $B$.")
    final = r"\\ ".join(" & ".join(str(x) for x in row) for row in C)
    st.append(f"$$\nA \\odot B = \\begin{{bmatrix}} {final} \\end{{bmatrix}}\n$$\n\n> Resultado "
              f"($3 \\times 2$ por $2 \\times 3$ da $3 \\times 3$).")
    p.put("prod-steps", steps("Producto booleano paso a paso", st))

    # Potencias de M_R (caminos de longitud k)
    pw = [M5]
    for _ in range(4):
        pw.append(bool_product(pw[-1], M5))
    st = []
    for k in range(1, 5):
        prev = pw[k - 1]
        cur = pw[k]
        ch = {(i, j) for i in range(5) for j in range(5) if cur[i][j]}
        st.append(f"$$\n{latex_matrix('M_R^{[' + str(k + 1) + ']}', V5, V5, cur, ch, str)}\n$$\n\n"
                  f"> $M_R^{{[{k + 1}]}} = M_R^{{[{k}]}} \\odot M_R$: un $1$ en $(i, j)$ significa "
                  f"que hay un camino de **longitud exactamente {k + 1}** de $i$ a $j$.")
    p.put("pot-steps", steps("Potencias booleanas de $M_R$", st))
    p.put("dir-m2", f"$$\n{latex_matrix('M_R^{[2]}', V5, V5, pw[1], {(0, 2)}, str)}\n$$")

    # Matriz de conectividad (grafos 2, ej. 32)
    V4 = list("abcd")
    E4 = [("a", "b"), ("b", "a"), ("b", "c"), ("c", "d")]
    pos4 = scale({"a": (0, 0), "b": (1.2, 0), "c": (1.2, 1.1), "d": (0, 1.1)}, 95)
    p.put("fig-con", gfig(p, "conectividad", pos4, E4, True))
    M4 = adj_matrix(V4, E4, True)
    acc = M4
    pws = [M4]
    for _ in range(3):
        pws.append(bool_product(pws[-1], M4))
    st = []
    acc = [r[:] for r in M4]
    st.append(f"$$\n{latex_matrix('M_R', V4, V4, M4, (), str)}\n$$\n\n> Caminos de longitud $1$.")
    for k in range(1, 4):
        new = or_m(acc, pws[k])
        ch = {(i, j) for i in range(4) for j in range(4) if new[i][j] and not acc[i][j]}
        acc = new
        st.append(f"$$\n{latex_matrix('M_R^{[' + str(k + 1) + ']}', V4, V4, pws[k], (), str)} "
                  f"\\qquad {latex_matrix('M_R \\vee \\cdots \\vee M_R^{[' + str(k + 1) + ']}', V4, V4, acc, ch, str)}\n$$\n\n"
                  f"> Se agregan los caminos de longitud ${k + 1}$." +
                  (" Aparecen unos nuevos." if ch else " No aparece ningún uno nuevo."))
    p.put("con-steps", steps("Matriz de conectividad", st))

    # Warshall (Bedoya)
    for key, M0, pos_, E_ in (
        ("w1", [[1, 0, 0, 1], [0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 0]], None, None),
        ("w2", M4, pos4, E4),
    ):
        tr = warshall_trace(V4, M0)
        st = []
        for i, sn in enumerate(tr):
            Wm = latex_matrix("W", V4, V4, sn["W"], sn["changed"], str, sub=f"_{{{i}}}")
            body = f"$$\n{Wm}\n$$\n\n"
            if sn["k"] is None:
                body += "> $W_0$ es la matriz de adyacencia."
            else:
                k = sn["k"]
                ki = V4.index(k)
                rows = [V4[r] for r in range(4) if tr[i - 1]["W"][r][ki]]
                cols = [V4[cc] for cc in range(4) if tr[i - 1]["W"][ki][cc]]
                body += (f"> Pivote ${k}$. En la **columna** ${k}$ de $W_{{{i - 1}}}$ hay unos en las "
                         f"filas {', '.join(f'${x}$' for x in rows) or 'ninguna'}; en la **fila** ${k}$ "
                         f"hay unos en las columnas {', '.join(f'${x}$' for x in cols) or 'ninguna'}. "
                         f"Se pone un $1$ en cada casilla (fila, columna) de esas listas.")
                if not sn["changed"]:
                    body += " No se adicionan unos nuevos."
            st.append(body)
        p.put(key, steps("Algoritmo de Warshall", st))
        p.put(key + "-final", f"$$\n{latex_matrix('W', V4, V4, tr[-1]['W'], (), str, sub='_4')}\n$$")
    p.put("w1-mat", f"$$\n{latex_matrix('M_R', V4, V4, [[1, 0, 0, 1], [0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 0]], (), str)}\n$$")
    p.put("fig-w1", gfig(p, "w1", scale({"a": (0, 0), "b": (1.2, 0), "c": (0, 1.1), "d": (1.2, 1.1)}, 95),
                         [("a", "a"), ("a", "d"), ("b", "d"), ("c", "a"), ("c", "d"), ("d", "b")], True))
    p.assemble("index.md")

    # ejercicios
    VE = list("abcde")
    ME = [[0, 1, 0, 0, 1], [1, 1, 1, 0, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1], [0, 1, 1, 0, 0]]
    p.put("ex-w-mat", f"$$\n{latex_matrix('M_R', VE, VE, ME, (), str)}\n$$")
    tr = warshall_trace(VE, ME)
    p.put("ex-w-sol", f"$$\n{latex_matrix('W', VE, VE, tr[-1]['W'], (), str, sub='_5')}\n$$")
    p.put("ex-w-cambios", ", ".join(f"$W_{{{i}}}$: {len(x['changed'])}" for i, x in enumerate(tr[1:], 1)))
    EE = []
    for i, a in enumerate(VE):
        for j, b in enumerate(VE):
            if ME[i][j]:
                EE.append((a, b))
    p.put("fig-ex-w", gfig(p, "ex-w", circle_pos(VE, 75), EE, True))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
