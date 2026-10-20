from common import *


def degrees(V, E):
    d = {v: 0 for v in V}
    for e in E:
        d[e[0]] += 1
        d[e[1]] += 1
    return d


def build():
    p = Page("Unidad5-Grafos/ConceptosBasicos")

    # Definición: dirigido y no dirigido (Bedoya)
    pos3 = scale({"a": (0, 1), "b": (1, 0), "c": (1.6, 1.3)}, 90)
    Ed = [("a", "a"), ("a", "b"), ("a", "c"), ("b", "b"), ("b", "c"), ("c", "a"), ("c", "b")]
    p.put("fig-dir", gfig_caption(p, "dirigido", pos3, Ed, "Grafo dirigido", True))
    pos4 = scale({"a": (0, 0), "b": (1, 0), "c": (0, 1), "d": (1, 1)}, 100)
    Eu = [("a", "b"), ("a", "c"), ("a", "d"), ("b", "c"), ("b", "d"), ("c", "d")]
    p.put("fig-nodir", gfig_caption(p, "no-dirigido", pos4, Eu, "Grafo no dirigido"))

    # Simple / multigrafo / pseudografo
    posS = scale({"u": (0, 0), "v": (1, 0), "w": (1, 1), "x": (0, 1)}, 90)
    simple = [("u", "v"), ("v", "w"), ("w", "x"), ("x", "u"), ("u", "w")]
    multi = [("u", "v", None, 14), ("u", "v", None, -14), ("v", "w"), ("w", "x", None, 14),
             ("w", "x", None, -14), ("x", "u")]
    pseudo = [("u", "u"), ("u", "v"), ("v", "w", None, 14), ("v", "w", None, -14), ("w", "x"),
              ("x", "x")]
    p.put("fig-simple", gfig_caption(p, "simple", posS, simple, "Simple"))
    p.put("fig-multi", gfig_caption(p, "multigrafo", posS, multi, "Multigrafo"))
    p.put("fig-pseudo", gfig_caption(p, "pseudografo", posS, pseudo, "Pseudografo"))
    # Clasificar
    cl = [
        ("cl-a", [("u", "v"), ("v", "w"), ("w", "u"), ("w", "x")], "a)"),
        ("cl-b", [("u", "v", None, 14), ("u", "v", None, -14), ("v", "w"), ("w", "x")], "b)"),
        ("cl-c", [("u", "v"), ("v", "w"), ("w", "w"), ("x", "u")], "c)"),
        ("cl-d", [("u", "v"), ("v", "w", None, 14), ("v", "w", None, -14), ("x", "x"), ("x", "w")], "d)"),
    ]
    for name, E, cap in cl:
        p.put("fig-" + name, gfig_caption(p, name, posS, E, cap))

    # Grados
    G1V = list("abcdef")
    G1P = scale({"a": (0, 0.5), "b": (1, 0), "c": (1.1, 1.2), "d": (2.6, 1.5), "e": (0.2, 1.8),
                 "f": (2.2, 0.3)}, 90)
    G1E = [("a", "b"), ("a", "c"), ("a", "e"), ("b", "c"), ("c", "e"), ("c", "f"), ("b", "f"),
           ("e", "c", None, 22)]
    p.put("fig-grado", gfig(p, "grado", G1P, G1E))
    d = degrees(G1V, G1E)
    p.put("grado-sol", ", ".join(f"$\\delta({v}) = {d[v]}$" for v in G1V))
    p.put("grado-suma", f"{' + '.join(str(d[v]) for v in G1V)} = {sum(d.values())}")
    p.put("grado-e", str(len(G1E)))

    # Handshaking: revelado incremental
    hs = []
    cfgs = [
        ({"u": (0, 0), "v": (90, 0)}, [("u", "v")]),
        ({"u": (0, 0), "v": (90, 0), "w": (45, 70)}, [("u", "v"), ("v", "w")]),
        ({"u": (0, 0), "v": (90, 0), "w": (45, 70)}, [("u", "v"), ("v", "w"), ("w", "u")]),
        ({"u": (0, 0), "v": (90, 0), "w": (45, 70)}, [("u", "v"), ("v", "w"), ("w", "u"), ("w", "w")]),
    ]
    rows = []
    for k, (pos, E) in enumerate(cfgs):
        V = list(pos)
        dd = degrees(V, E)
        es = {(E[-1][0], E[-1][1]): "new"}
        lab = {v: f"δ={dd[v]}" for v in V}
        img = gfig(p, f"hs-{k:02d}", pos, E, edge_style=es, labels=lab,
                   label_pos={"u": "left", "v": "right", "w": "right"})
        rows.append([str(len(E)), " + ".join(str(dd[v]) for v in V), str(sum(dd.values()))])
        rr = [r[:] for r in rows]
        rr[-1] = [hl(x) for x in rr[-1]]
        extra = ""
        if k == 3:
            extra = ("\n\n> El bucle en $w$ suma **2** al grado de $w$: la arista toca a $w$ por sus "
                     "dos extremos.")
        hs.append(f"{img}\n\n{md_table(['$e$', 'grados', 'suma'], rr)}{extra}")
    hs[-1] += "\n\n> **¿Qué relación hay entre la suma de los grados y $e$?**"
    p.put("handshaking", steps("Sumar los grados", hs))

    # Familias
    def kn(n):
        names = [f"v{i}" for i in range(1, n + 1)]
        return names, [(names[i], names[j]) for i in range(n) for j in range(i + 1, n)]

    figs = []
    for n in range(2, 7):
        names, E = kn(n)
        pos = circle_pos(names, 52 if n > 2 else 40)
        figs.append(gfig_caption(p, f"K{n}", pos, E, f"K{n}", node_text={v: "" for v in names}, r=8))
    p.put("fam-k", " ".join(figs))
    figs = []
    for n in range(3, 7):
        names = [f"v{i}" for i in range(1, n + 1)]
        E = [(names[i], names[(i + 1) % n]) for i in range(n)]
        figs.append(gfig_caption(p, f"C{n}", circle_pos(names, 50), E, f"C{n}",
                                 node_text={v: "" for v in names}, r=8))
    p.put("fam-c", " ".join(figs))
    figs = []
    for n in range(3, 7):
        names = [f"v{i}" for i in range(1, n + 1)]
        E = [(names[i], names[(i + 1) % n]) for i in range(n)] + [("h", v) for v in names]
        pos = circle_pos(names, 52)
        pos["h"] = (0, 0)
        figs.append(gfig_caption(p, f"W{n}", pos, E, f"W{n}",
                                 node_text={v: "" for v in names + ["h"]}, r=8))
    p.put("fam-w", " ".join(figs))
    figs = []
    for m, n in ((2, 3), (3, 3), (3, 5)):
        A = [f"a{i}" for i in range(m)]
        B = [f"b{i}" for i in range(n)]
        pos = {a: ((i - (m - 1) / 2) * 55, 0) for i, a in enumerate(A)}
        pos |= {b: ((i - (n - 1) / 2) * 55, 90) for i, b in enumerate(B)}
        E = [(a, b) for a in A for b in B]
        figs.append(gfig_caption(p, f"K{m}{n}", pos, E, f"K{m},{n}",
                                 node_text={v: "" for v in A + B}, r=8,
                                 node_style={v: "tree" for v in A}))
    p.put("fam-kmn", " ".join(figs))

    # Bipartitos
    bips = [
        ("bip-1", scale({"a": (0, 0), "b": (1, 0), "c": (1, 1), "d": (0, 1)}, 80),
         [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")], "a)"),
        ("bip-2", scale({"a": (0, 0), "b": (1, 0), "c": (0.5, 0.85)}, 85),
         [("a", "b"), ("b", "c"), ("c", "a")], "b)"),
        ("bip-3", circle_pos(list("abcdef"), 55),
         [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("f", "a"), ("a", "d")], "c)"),
        ("bip-4", circle_pos(list("abcde"), 55),
         [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "a")], "d)"),
    ]
    for name, pos, E, cap in bips:
        p.put("fig-" + name, gfig_caption(p, name, pos, E, cap))
    pos = circle_pos(list("abcdef"), 55)
    E = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("f", "a"), ("a", "d")]
    p.put("fig-bip-3-sol", gfig(p, "bip-3-sol", pos, E,
                                node_style={v: "tree" for v in "ace"}))

    # Complementario
    pos = circle_pos(list("abcde"), 60)
    E = [("a", "b"), ("b", "c"), ("c", "d"), ("a", "c")]
    allE = [(x, y) for i, x in enumerate("abcde") for y in "abcde"[i + 1:]]
    comp = [e for e in allE if e not in E and (e[1], e[0]) not in E]
    p.put("fig-g", gfig_caption(p, "comp-g", pos, E, "G"))
    p.put("fig-gc", gfig_caption(p, "comp-gc", pos, comp, "Ḡ"))
    union = [(a, b) for a, b in E] + comp
    es = {e: "new" for e in comp}
    p.put("fig-gug", gfig_caption(p, "comp-union", pos, union, "G ∪ Ḡ = K5", edge_style=es))
    d1 = degrees(list("abcde"), E)
    d2 = degrees(list("abcde"), comp)
    p.put("comp-grados", md_table(["", *[f"${v}$" for v in "abcde"]],
                                  [["$\\delta_G$", *[str(d1[v]) for v in "abcde"]],
                                   ["$\\delta_{\\bar G}$", *[str(d2[v]) for v in "abcde"]]]))
    p.assemble("index.md")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
