from common import *


def euler_path(E, start):
    """Hierholzer: devuelve la secuencia de vértices de un camino/circuito de Euler."""
    adj = {}
    for i, (a, b, *_) in enumerate(E):
        adj.setdefault(a, []).append((b, i))
        adj.setdefault(b, []).append((a, i))
    for v in adj:
        adj[v].sort()
    used = set()
    stack, out = [start], []
    while stack:
        v = stack[-1]
        while adj[v] and adj[v][0][1] in used:
            adj[v].pop(0)
        if adj[v]:
            w, i = adj[v].pop(0)
            used.add(i)
            stack.append(w)
        else:
            out.append(stack.pop())
    return out[::-1]


def path_fig(p, name, pos, E, seq, directed=False, closed_note=None):
    used = list(zip(seq, seq[1:]))
    es = {}
    for a, b in used:
        es[(a, b)] = "new"
    ns = {seq[0]: "hl"}
    if seq[-1] != seq[0]:
        ns[seq[-1]] = "hl"
    svg = SVG()
    draw_graph(svg, pos, E, directed, edge_style=es, node_style=ns)
    # numerar el orden en que se recorren las aristas
    for k, (a, b) in enumerate(used, 1):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        d = (dx * dx + dy * dy) ** 0.5
        # desplazamiento distinto si la arista se repite
        rep = used[:k - 1].count((a, b)) + used[:k - 1].count((b, a))
        off = 12 + 14 * rep
        svg.text(mx - dy / d * off, my + dx / d * off + 4, str(k), 11, PAL["new"], bold=True, bg=True)
    return f"![{name}]({p.img(name, svg)})"


def check_euler(E, seq, closed):
    """Verifica que seq recorre cada arista de E exactamente una vez."""
    pool = [tuple(sorted((e[0], e[1]))) for e in E]
    for a, b in zip(seq, seq[1:]):
        k = tuple(sorted((a, b)))
        assert k in pool, (k, seq)
        pool.remove(k)
    assert not pool, pool
    assert (seq[0] == seq[-1]) == closed


def check_ham(E, V, seq, closed):
    es = {tuple(sorted((e[0], e[1]))) for e in E}
    body = seq[:-1] if closed else seq
    assert sorted(body) == sorted(V), seq
    for a, b in zip(seq, seq[1:]):
        assert tuple(sorted((a, b))) in es, (a, b)


def degs(V, E):
    d = {v: 0 for v in V}
    for e in E:
        d[e[0]] += 1
        d[e[1]] += 1
    return d


def build():
    p = Page("Unidad5-Grafos/ConectividadEulerHamilton")

    # Caminos (Bedoya)
    pos = scale({"a": (1, 0), "b": (0, 0.6), "c": (1.6, 0.5), "d": (0, 1.6), "e": (1.6, 1.5),
                 "f": (0.9, 2.0)}, 75)
    E = [("a", "b"), ("a", "c"), ("b", "c"), ("b", "d"), ("b", "e"), ("c", "d"), ("c", "e"),
         ("d", "e"), ("d", "f"), ("e", "f")]
    p.put("fig-caminos", gfig(p, "caminos", pos, E))
    tabs = []
    for name, seq, txt in (
        ("cam-0", "abdecbdf", "Un **camino**: $a, b, d, e, c, b, d, f$. Repite la arista $\\{b, d\\}$ y los vértices $b$ y $d$: está permitido."),
        ("cam-1", "fdcedb", "Un **camino simple**: $f, d, c, e, d, b$. Repite el vértice $d$, pero no repite aristas."),
        ("cam-2", "bacef", "Un camino simple de longitud $4$ que empieza en $b$: $b, a, c, e, f$."),
        ("cam-3", "fdcdef", "Un **circuito** de longitud $5$ que empieza en $f$: $f, d, c, d, e, f$. Repite la arista $\\{c, d\\}$, así que no es un circuito simple."),
        ("cam-4", "cbdec", "Un **circuito simple** de longitud $4$ que empieza en $c$: $c, b, d, e, c$."),
    ):
        tabs.append(f"{path_fig(p, name, pos, E, list(seq))}\n\n> {txt}")
    p.put("caminos", steps("Caminos en el grafo", tabs))

    # Conexo / no conexo (Bedoya)
    pc = scale({"a": (0, 0), "b": (1, 0), "c": (0, 1), "d": (1, 1), "e": (0, 1.7), "f": (1, 1.7)}, 70)
    pn = scale({"a": (0, 0), "b": (1, 0), "c": (0, 0.7), "d": (1, 0.8), "e": (0, 1.5), "f": (1, 1.5)}, 70)
    p.put("fig-conexo", graph_row(p, "conexo", [
        (pc, [("a", "b"), ("a", "d"), ("b", "c"), ("c", "d"), ("c", "e"), ("d", "f")], "Grafo conexo"),
        (pn, [("a", "b"), ("a", "c"), ("d", "e"), ("e", "f"), ("d", "f")], "Grafo no conexo")], gap=110))

    # Dirigidos: fuerte y débil
    pd = scale({"a": (0, 0.5), "b": (1, 0), "c": (2, 0), "d": (1.5, 1), "e": (2.7, 1)}, 85)
    H = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "b"), ("d", "e")]
    p.put("fig-H", gfig_caption(p, "H", pd, H, "H", True))
    Gs = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("c", "e"), ("e", "d")]
    p.put("fig-Gs", gfig_caption(p, "Gfuerte", pd, Gs, "G", True))
    p.put("fig-H-scc", gfig(p, "H-scc", pd, H, True,
                            node_style={"a": "goal", "e": "bad", "b": "tree", "c": "tree", "d": "tree"}))
    pdag = scale({"a": (0, 0), "b": (1, 0), "c": (2, 0), "d": (0.5, 1), "e": (1.5, 1)}, 85)
    p.put("fig-dag", gfig(p, "dag", pdag, [("a", "b"), ("b", "c"), ("a", "d"), ("d", "e"),
                                           ("b", "e"), ("e", "c")], True))

    # Königsberg
    pk = scale({"A": (1, 1), "B": (1, 0), "C": (1, 2), "D": (2.4, 1)}, 90)
    K = [("A", "B", None, 16), ("A", "B", None, -16), ("A", "C", None, 16), ("A", "C", None, -16),
         ("A", "D"), ("B", "D"), ("C", "D")]
    lab = {"A": "δ=5", "B": "δ=3", "C": "δ=3", "D": "δ=3"}
    p.put("fig-kon", gfig(p, "konigsberg", pk, K))
    p.put("fig-kon-grados", gfig(p, "konigsberg-grados", pk, K, labels=lab,
                                 label_pos={"A": "left", "B": "above", "C": "below", "D": "right"},
                                 node_style={v: "bad" for v in "ABCD"}))

    # Euler: ejemplos de Bedoya
    pE1 = scale({"b": (0.7, 0), "a": (0, 0.6), "c": (1.4, 0.6), "d": (0.7, 1.2), "e": (0.7, 1.9)}, 75)
    EE1 = [("b", "a"), ("b", "c"), ("a", "d"), ("c", "d"), ("d", "e")]
    pE2 = scale({"a": (0, 0), "b": (1.3, 0), "c": (0.65, 0.75), "d": (0, 1.5), "e": (1.3, 1.5)}, 70)
    EE2 = [("a", "b"), ("a", "c"), ("b", "c"), ("c", "d"), ("c", "e"), ("d", "e")]
    s1, s2 = list("edabcd"), list("acedcba")
    check_euler(EE1, s1, False)
    check_euler(EE2, s2, True)
    svg1 = path_fig(p, "euler-1", pE1, EE1, s1)
    svg2 = path_fig(p, "euler-2", pE2, EE2, s2)
    p.put("euler-ej", f"| | |\n|---|---|\n| {svg1} | {svg2} |\n| Camino de Euler: $e, d, a, b, c, d$ | "
                      f"Circuito de Euler: $a, c, e, d, c, b, a$ |")
    # ¿camino o circuito? (Bedoya)
    casa = scale({"a": (0.7, 0), "b": (0, 0.7), "c": (1.4, 0.7), "d": (0, 1.6), "e": (1.4, 1.6)}, 75)
    ECasa = [("a", "b"), ("a", "c"), ("b", "c"), ("b", "d"), ("b", "e"), ("c", "d"), ("c", "e"),
             ("d", "e")]
    sc = list("edcabcebd")
    check_euler(ECasa, sc, False)
    d = degs("abcde", ECasa)
    p.put("fig-e1", gfig(p, "e1", casa, ECasa))
    p.put("e1-grados", ", ".join(f"$\\delta({v}) = {d[v]}$" for v in "abcde"))
    p.put("fig-e1-sol", path_fig(p, "e1-sol", casa, ECasa, sc))
    p.put("e1-seq", "$" + ", ".join(sc) + "$")

    # Hierholzer
    ph = scale({"a": (0, 1), "b": (1, 0.3), "c": (1, 1.7), "f": (1.8, -0.4), "g": (0.3, -0.4),
                "d": (2, 2.2), "e": (0.2, 2.5)}, 90)
    EH = [("a", "b"), ("b", "c"), ("c", "a"), ("b", "f"), ("f", "g"), ("g", "b"), ("c", "d"),
          ("d", "e"), ("e", "c")]
    subs = [list("abca"), list("bfgb"), list("cdec")]
    circuits = [list("abca"), list("abfgbca"), list("abfgbcdeca")]
    tabs = []
    used = set()
    for k, (sub, circ) in enumerate(zip(subs, circuits)):
        es = {}
        for a_, b_ in used:
            es[(a_, b_)] = "tree"
        for a_, b_ in zip(sub, sub[1:]):
            es[(a_, b_)] = "new"
        svg = SVG()
        draw_graph(svg, ph, EH, False, edge_style=es, node_style={sub[0]: "hl"})
        img = p.img(f"hierholzer-{k:02d}", svg)
        for a_, b_ in zip(sub, sub[1:]):
            used.add((a_, b_))
        seq = ", ".join(circ)
        if k == 0:
            txt = ("> Se parte de $a$ y se camina por aristas no usadas hasta que no se pueda "
                   "seguir: $a, b, c, a$. Se quedó atascado en $a$ (todas sus aristas están usadas), "
                   "pero $b$ y $c$ todavía tienen aristas sin usar.")
        else:
            txt = (f"> Desde ${sub[0]}$, que está en el circuito y tiene aristas sin usar, se recorre "
                   f"otro circuito: ${', '.join(sub)}$. Se **inserta** en el circuito en el lugar de "
                   f"${sub[0]}$.")
        if k == len(subs) - 1:
            txt += " Ya no quedan aristas sin usar."
        tabs.append(f"![Hierholzer, paso {k + 1}]({img})\n\n{txt}\n\n$$\n{c(seq)}\n$$")
    p.put("hierholzer", steps("Construir un circuito de Euler", tabs))
    p.put("fig-hier", gfig(p, "hierholzer-grafo", ph, EH))

    # Hamilton (Bedoya)
    h1, h2 = list("edabc"), list("abcde")
    check_ham(EE1, "abcde", h1, False)
    check_ham(EE2, "abcde", h2, False)
    p.put("ham-ej", f"| | |\n|---|---|\n| {path_fig(p, 'ham-1', pE1, EE1, h1)} | "
                    f"{path_fig(p, 'ham-2', pE2, EE2, h2)} |\n| Camino de Hamilton: $e, d, a, b, c$ | "
                    f"Camino de Hamilton: $a, b, c, d, e$ |")

    def kn(n):
        names = [f"v{i}" for i in range(1, n + 1)]
        return names, [(names[i], names[j]) for i in range(n) for j in range(i + 1, n)]
    items = []
    for n in (4, 5, 6):
        names, Ek = kn(n)
        items.append((circle_pos(names, 50), Ek, f"K{n}", {"node_text": {v: "" for v in names}}))
    p.put("fig-kn", graph_row(p, "kn", items, gap=60))
    pH = scale({"a": (0, 0), "b": (2, 0), "c": (1, 0.8), "d": (2, 0.8), "e": (3, 0.8), "f": (0, 1.6),
                "g": (2, 1.6)}, 70)
    EHm = [("a", "b"), ("a", "c"), ("a", "f"), ("b", "c"), ("b", "d"), ("b", "e"), ("c", "d"),
           ("c", "f"), ("c", "g"), ("d", "e"), ("d", "g"), ("e", "g"), ("f", "g")]
    hc = list("abcdegfa")
    check_ham(EHm, "abcdefg", hc, True)
    p.put("fig-hC", gfig(p, "ham-C", pH, EHm))
    p.put("fig-hC-sol", path_fig(p, "ham-C-sol", pH, EHm, hc))
    p.assemble("index.md")

    # Ejercicio 1: Euler (Bedoya)
    pF = dict(pos)
    EF = list(E)
    sF = list("acdfebcedba")
    check_euler(EF, sF, True)
    pM = scale({"b": (1, 0), "a": (0, 0.5), "c": (2, 0.5), "f": (0, 1.4), "d": (2, 1.4), "e": (1, 1.9)}, 70)
    EM = [("a", "b"), ("b", "c"), ("b", "e"), ("a", "f", None, 0), ("a", "f", None, 16),
          ("a", "f", None, -16), ("f", "e"), ("c", "d", None, 0), ("c", "d", None, 16),
          ("c", "d", None, -16), ("d", "e")]
    sM = list("bafafebcdcde")
    check_euler(EM, sM, False)
    pN = scale({"a": (0, 0), "b": (1.4, 0), "c": (0.7, 0.75), "d": (0, 1.5), "e": (1.4, 1.5)}, 75)
    EN = [("a", "b"), ("b", "e", None, 0), ("b", "e", None, -26), ("b", "c"), ("c", "e"), ("d", "e"),
          ("c", "d"), ("a", "c"), ("a", "d", None, 0), ("a", "d", None, 26)]
    sN = list("abebcedcada")
    check_euler(EN, sN, True)
    pO = scale({"a": (0, 0.4), "b": (0, 1.1), "c": (0.5, 0.6), "d": (1.5, -0.2), "e": (1.5, 0.4),
                "h": (2.8, 0.6), "f": (1, 1.2), "g": (2.2, 1.2)}, 70)
    EO = [("a", "b"), ("a", "c"), ("b", "c"), ("c", "d"), ("c", "e"), ("c", "h"), ("c", "f"),
          ("d", "h"), ("e", "h"), ("f", "g"), ("g", "h")]
    sO = list("abcdhechgfca")
    check_euler(EO, sO, True)
    items = [(pF, EF, "a)"), (pM, EM, "b)"), (pN, EN, "c)"), (pO, EO, "d)")]
    p.put("fig-ex-euler", graph_row(p, "ex-euler", items, gap=70))
    sols = []
    for (P_, E_, cap), seq_ in zip(items, [sF, sM, sN, sO]):
        dd = degs(sorted(P_), E_)
        odd = [v for v in sorted(P_) if dd[v] % 2]
        kind = "circuito" if seq_[0] == seq_[-1] else "camino"
        why = ("todos los grados son pares" if not odd else
               f"los vértices de grado impar son ${odd[0]}$ y ${odd[1]}$")
        sols.append(f"- {cap} Grados: " + ", ".join(f"$\\delta({v}) = {dd[v]}$" for v in sorted(P_))
                    + f". Como {why}, tiene **{kind}** de Euler: ${', '.join(seq_)}$.")
    p.put("ex-euler-sol", "\n".join(sols))

    # Ejercicio 2: A y B (Grafos 2)
    pA = scale({"t": (0, 0), "z": (1, 0), "w": (2, 0), "x": (2, 1), "y": (1, 1)}, 85)
    EA = [("t", "z"), ("z", "w"), ("w", "x"), ("x", "y"), ("y", "z")]
    pB = scale({"a": (0, 0), "b": (1, 0), "e": (0.5, 0.9), "c": (0, 1.8), "d": (1, 1.8)}, 85)
    EB = [("a", "e"), ("e", "c"), ("c", "d"), ("d", "e"), ("e", "b"), ("b", "a")]
    check_euler(EA, list("tzwxyz"), False)
    check_euler(EB, list("aecdeba"), True)
    check_ham(EA, "twxyz", list("tzyxw"), False)
    check_ham(EB, "abcde", list("abedc"), False)
    p.put("fig-AB", graph_row(p, "AB", [(pA, EA, "A"), (pB, EB, "B")], gap=110))

    # Ejercicio 3: circuitos grandes (Grafos 2)
    seq1 = "z y t y x z t x t w u y z".split()
    seq2 = "a b c b f g c d h g r o h o y z r j x z x p i j f e i e a".split()

    def from_seq(seq_):
        out, cnt = [], {}
        for a_, b_ in zip(seq_, seq_[1:]):
            k = tuple(sorted((a_, b_)))
            cnt[k] = cnt.get(k, 0) + 1
            bend = {1: None, 2: 18, 3: -18}[cnt[k]]
            out.append((a_, b_, None, bend) if bend else (a_, b_))
        return out
    pG1 = scale({"u": (0, 0), "w": (1, 0), "t": (1.5, 1), "y": (0, 1), "x": (1, 2), "z": (0, 2)}, 80)
    E1 = from_seq(seq1)
    grid = "a b c d / e f g h / i j r o / p x z y".split(" / ")
    pG2 = {}
    for r_, row in enumerate(grid):
        for c_, v in enumerate(row.split()):
            pG2[v] = (c_ * 75, r_ * 75)
    E2 = from_seq(seq2)
    check_euler(E1, seq1, True)
    check_euler(E2, seq2, True)
    p.put("fig-ex-grandes", graph_row(p, "ex-grandes", [(pG1, E1, "a)"), (pG2, E2, "b)")], gap=100))
    p.put("ex-grandes-sol", graph_row(p, "ex-grandes-sol", [
        (pG1, E1, "a)", {"edge_style": {(a_, b_): "new" for a_, b_, *_ in E1}}),
        (pG2, E2, "b)", {"edge_style": {(a_, b_): "new" for a_, b_, *_ in E2}})], gap=100)
        + "\n\nTodos los vértices tienen grado par en los dos grafos.")

    # Ejercicio 4: Hamilton (Bedoya y heptágono)
    pP = scale({"a": (0, 0.6), "b": (0.6, 0.6), "c": (1.1, 0), "d": (2, 0), "e": (1.1, 1.2),
                "f": (1.6, 0.6), "g": (2, 1.1), "h": (2.5, 0.5)}, 70)
    EP = [("a", "b"), ("b", "c"), ("b", "e"), ("c", "e"), ("c", "d"), ("c", "f"), ("d", "f"),
          ("d", "h"), ("e", "f"), ("f", "g")]
    pQ = {k: v for k, v in pP.items() if k not in "gh"}
    EQ = [e for e in EP if "g" not in e and "h" not in e]
    check_ham(EQ, "abcdef", list("abcdfe"), False)
    hep = circle_pos(list("abcdefg"), 70)
    EHep = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("f", "g"), ("g", "a"),
            ("a", "d"), ("b", "f"), ("c", "g")]
    check_ham(EHep, "abcdefg", list("abcdefga"), True)
    p.put("fig-ex-ham", graph_row(p, "ex-ham", [(pP, EP, "a)"), (pQ, EQ, "b)"), (hep, EHep, "c)")]))

    # Ejercicio 5: agregar una arista
    pe = scale({"a": (0, 0), "b": (1, 0), "c": (2, 0), "d": (0, 1), "e": (1, 1.6), "f": (2, 1)}, 85)
    EE = [("a", "b"), ("b", "c"), ("a", "d"), ("b", "e"), ("c", "f"), ("d", "e"), ("e", "f"),
          ("b", "d"), ("b", "f")]
    p.put("fig-ex1", gfig(p, "ex1", pe, EE))
    deg = degs("abcdef", EE)
    p.put("ex1-grados", ", ".join(f"$\\delta({v}) = {deg[v]}$" for v in "abcdef"))
    EE2 = EE + [("d", "f")]
    seq = euler_path(EE2, "b")
    check_euler(EE2, seq, False)
    p.put("fig-ex1-sol", path_fig(p, "ex1-sol", pe, EE2, seq))
    p.put("ex1-seq", "$" + ", ".join(seq) + "$")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
