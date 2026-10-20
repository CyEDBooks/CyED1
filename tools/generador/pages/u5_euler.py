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


def build():
    p = Page("Unidad5-Grafos/ConectividadEulerHamilton")

    # Caminos (grafos 2)
    V = list("abcdef")
    pos = scale({"a": (0, 0.6), "b": (1, 0), "c": (1, 1.2), "d": (2.2, 0), "e": (2.2, 1.2),
                 "f": (3.2, 0.6)}, 90)
    E = [("a", "b"), ("a", "c"), ("b", "c"), ("b", "d"), ("c", "d"), ("c", "e"), ("d", "e"),
         ("d", "f"), ("e", "f")]
    p.put("fig-caminos", gfig(p, "caminos", pos, E))
    tabs = []
    for name, seq, txt in (
        ("cam-1", "baceF", "Un camino **simple** de longitud $4$ que empieza en $b$: $b, a, c, e, f$. No repite aristas (ni vértices)."),
        ("cam-2", "fdcdef", "Un camino **cerrado** de longitud $5$ que empieza en $f$: $f, d, c, d, e, f$. Repite la arista $\\{c, d\\}$, así que no es un circuito simple."),
        ("cam-3", "dbcbcd", "Un camino de longitud $5$ de $d$ a $d$… y que repite aristas: $d, b, c, b, c, d$."),
        ("cam-4", "cbdec", "Un **circuito simple** de longitud $4$ que empieza en $c$: $c, b, d, e, c$."),
    ):
        seq = seq.lower()
        tabs.append(f"{path_fig(p, name, pos, E, list(seq))}\n\n> {txt}")
    p.put("caminos", steps("Caminos en el grafo", tabs))

    # Conexo / no conexo
    p1 = scale({"a": (0, 0), "b": (1, 0), "c": (1, 1), "d": (0, 1), "e": (2, 0.5)}, 80)
    p.put("fig-conexo", gfig_caption(p, "conexo", p1, [("a", "b"), ("b", "c"), ("c", "d"), ("b", "e")], "G₁"))
    p.put("fig-noconexo", gfig_caption(p, "no-conexo", p1, [("a", "b"), ("a", "d"), ("c", "e")], "G₂"))

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
    p.put("fig-kon", gfig(p, "konigsberg", pk, K, r=20))
    p.put("fig-kon-grados", gfig(p, "konigsberg-grados", pk, K, r=20, labels=lab,
                                 label_pos={"A": "left", "B": "above", "C": "below", "D": "right"},
                                 node_style={v: "bad" for v in "ABCD"}))

    # Euler: grafos A y B de las diapositivas
    pA = scale({"t": (0, 0), "z": (1, 0), "w": (2, 0), "x": (2, 1), "y": (1, 1)}, 85)
    EA = [("t", "z"), ("z", "w"), ("w", "x"), ("x", "y"), ("y", "z")]
    pB = scale({"a": (0, 0), "b": (1, 0), "e": (0.5, 0.9), "c": (0, 1.8), "d": (1, 1.8)}, 85)
    EB = [("a", "e"), ("e", "c"), ("c", "d"), ("d", "e"), ("e", "b"), ("b", "a")]
    p.put("fig-eA", gfig_caption(p, "euler-A", pA, EA, "A"))
    p.put("fig-eB", gfig_caption(p, "euler-B", pB, EB, "B"))
    p.put("fig-eA-sol", path_fig(p, "euler-A-sol", pA, EA, list("tzwxyz")))
    p.put("fig-eB-sol", path_fig(p, "euler-B-sol", pB, EB, list("aecdeba")))
    # ¿Tiene circuito o camino de Euler?
    k4 = circle_pos(list("abcd"), 50, -45)
    EK4 = [(x, y) for i, x in enumerate("abcd") for y in "abcd"[i + 1:]]
    c5 = circle_pos(list("abcde"), 50)
    EC5 = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "a")]
    casa = scale({"a": (0.5, 0), "b": (0, 0.7), "c": (1, 0.7), "d": (0, 1.6), "e": (1, 1.6)}, 80)
    ECasa = [("a", "b"), ("a", "c"), ("b", "c"), ("b", "d"), ("c", "e"), ("d", "e")]
    p.put("fig-e1", gfig_caption(p, "e1", k4, EK4, "a)"))
    p.put("fig-e2", gfig_caption(p, "e2", c5, EC5, "b)"))
    p.put("fig-e3", gfig_caption(p, "e3", casa, ECasa, "c)"))
    p.put("fig-e3-sol", path_fig(p, "e3-sol", casa, ECasa, euler_path(ECasa, "b")))
    p.put("e3-seq", ", ".join(euler_path(ECasa, "b")))

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
        for a, b in used:
            es[(a, b)] = "tree"
        for a, b in zip(sub, sub[1:]):
            es[(a, b)] = "new"
        svg = SVG()
        ns = {sub[0]: "hl"}
        draw_graph(svg, ph, EH, False, edge_style=es, node_style=ns)
        img = p.img(f"hierholzer-{k:02d}", svg)
        for a, b in zip(sub, sub[1:]):
            used.add((a, b))
        seq = ", ".join(circ)
        if k == 0:
            txt = (f"> Se parte de $a$ y se camina por aristas no usadas hasta que no se pueda seguir: "
                   f"$a, b, c, a$. Se quedó atascado en $a$ (todas sus aristas están usadas), pero "
                   f"$b$ y $c$ todavía tienen aristas sin usar.")
        else:
            txt = (f"> Desde ${sub[0]}$, que está en el circuito y tiene aristas sin usar, se recorre "
                   f"otro circuito: ${', '.join(sub)}$. Se **inserta** en el circuito en el lugar de "
                   f"${sub[0]}$.")
        if k == len(subs) - 1:
            txt += " Ya no quedan aristas sin usar."
        tabs.append(f"![Hierholzer, paso {k + 1}]({img})\n\n{txt}\n\n$$\n{c(seq)}\n$$")
    p.put("hierholzer", steps("Construir un circuito de Euler", tabs))
    p.put("fig-hier", gfig(p, "hierholzer-grafo", ph, EH))

    # Hamilton
    p.put("fig-hA", path_fig(p, "ham-A", pA, EA, list("tzyxw")))
    p.put("fig-hB", path_fig(p, "ham-B", pB, EB, list("abedc")))
    hep = circle_pos(list("abcdefg"), 70)
    EHep = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("f", "g"), ("g", "a"),
            ("a", "d"), ("b", "f"), ("c", "g")]
    p.put("fig-hC", gfig(p, "ham-C", hep, EHep))
    p.put("fig-hC-sol", path_fig(p, "ham-C-sol", hep, EHep, list("abcdefga")))
    p.assemble("index.md")

    # ejercicios
    pe = scale({"a": (0, 0), "b": (1, 0), "c": (2, 0), "d": (0, 1), "e": (1, 1.6), "f": (2, 1)}, 85)
    EE = [("a", "b"), ("b", "c"), ("a", "d"), ("b", "e"), ("c", "f"), ("d", "e"), ("e", "f"),
          ("b", "d"), ("b", "f")]
    p.put("fig-ex1", gfig(p, "ex1", pe, EE))
    deg = {v: 0 for v in "abcdef"}
    for a, b in EE:
        deg[a] += 1
        deg[b] += 1
    p.put("ex1-grados", ", ".join(f"$\\delta({v}) = {deg[v]}$" for v in "abcdef"))
    EE2 = EE + [("d", "f")]
    seq = euler_path(EE2, "b")
    assert len(seq) == len(EE2) + 1
    p.put("fig-ex1-sol", path_fig(p, "ex1-sol", pe, EE2, seq))
    p.put("ex1-seq", ", ".join(seq))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
