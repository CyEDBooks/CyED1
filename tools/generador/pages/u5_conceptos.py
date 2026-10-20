from common import *


def degrees(V, E):
    d = {v: 0 for v in V}
    for e in E:
        d[e[0]] += 1
        d[e[1]] += 1
    return d


def inout(V, E):
    di = {v: 0 for v in V}
    do = {v: 0 for v in V}
    for e in E:
        do[e[0]] += 1
        di[e[1]] += 1
    return di, do


def dlist(V, d):
    return ", ".join(f"$\\delta({v}) = {d[v]}$" for v in V)


NONAME = None


def build():
    p = Page("Unidad5-Grafos/ConceptosBasicos")

    # Definición: dirigido y no dirigido
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
    p.put("fig-tipos", graph_row(p, "tipos", [(posS, simple, "Grafo simple"),
                                              (posS, multi, "Multigrafo"),
                                              (posS, pseudo, "Pseudografo")]))

    # Grado: ejemplo y ejercicio de Bedoya
    P0 = scale({"v": (1, 0), "u": (0, 0.7), "r": (2, 0.7), "s": (1, 1.4)}, 80)
    E0 = [("u", "v"), ("u", "s"), ("v", "r"), ("v", "s"), ("r", "s")]
    assert degrees(list("uvrs"), E0) == {"u": 2, "v": 3, "r": 2, "s": 3}
    p.put("fig-grado0", gfig(p, "grado0", P0, E0))
    G1V = list("abcdef")
    G1P = scale({"b": (0.8, 0), "c": (2.3, 0), "d": (3.0, 0.3), "a": (0, 1.1), "e": (2.7, 1.1),
                 "f": (1.4, 1.8)}, 85)
    G1E = [("a", "b"), ("b", "c"), ("a", "c"), ("a", "e"), ("a", "f"), ("b", "f"), ("c", "e"),
           ("e", "f"), ("c", "c"), ("f", "f")]
    d = degrees(G1V, G1E)
    assert d == {"a": 4, "b": 3, "c": 5, "d": 0, "e": 3, "f": 5}
    p.put("fig-grado", gfig(p, "grado", G1P, G1E))
    p.put("grado-sol", dlist(G1V, d))

    # Handshaking: revelado incremental
    hs = []
    cfgs = [
        ({"u": (0, 0), "v": (90, 0)}, [("u", "v")]),
        ({"u": (0, 0), "v": (90, 0), "w": (45, 70)}, [("u", "v"), ("u", "w")]),
        ({"u": (0, 0), "v": (90, 0), "w": (45, 70)}, [("u", "v"), ("u", "w"), ("v", "w")]),
        ({"u": (0, 0), "v": (90, 0), "w": (45, 70)}, [("u", "v"), ("u", "w"), ("v", "w"), ("w", "w")]),
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

    def hs_fig(name, V, pos, E, want, cap=None):
        dd = degrees(V, E)
        assert dd == want, (name, dd)
        return dd

    HS1V = list("abcdefg")
    HS1P = scale({"b": (1, 0), "c": (2.3, 0), "d": (3.2, 0), "a": (0, 1), "e": (1, 1), "f": (2.3, 1),
                  "g": (3.2, 1)}, 80)
    HS1E = [("a", "b"), ("a", "e"), ("b", "c"), ("b", "e"), ("b", "f"), ("c", "e"), ("c", "f"),
            ("c", "d"), ("e", "f")]
    dd = hs_fig("hs1", HS1V, HS1P, HS1E, dict(a=2, b=4, c=4, d=1, e=4, f=3, g=0))
    p.put("fig-hs1", gfig(p, "hs1", HS1P, HS1E))
    p.put("hs1-sol", f"$e = {len(HS1E)}$; " + dlist(HS1V, dd))
    p.put("hs1-suma", " + ".join(str(dd[v]) for v in HS1V) + f" = {sum(dd.values())}")
    p.put("hs1-e", str(len(HS1E)))

    # Vértices de grado impar: intentos de dejar uno solo
    IP = scale({"v": (1, 0), "y": (2.1, 0), "u": (0, 1), "w": (2.1, 1), "x": (1, 2)}, 75)
    IE = [("u", "v"), ("u", "w"), ("u", "x"), ("v", "y"), ("v", "w"), ("w", "y"), ("w", "x")]
    attempts = [
        ("base", None, None),
        ("Se agrega un vértice $z$ unido a $v$.", "z", [("v", "z")]),
        ("Se agrega la arista $\\{v, y\\}$.", None, [("v", "y", None, -16)]),
        ("Se agrega otra arista entre $u$ y $v$.", None, [("u", "v", None, -18)]),
        ("Se agrega la arista $\\{x, y\\}$.", None, [("x", "y")]),
    ]
    tabs = []
    for k, (txt, newv, newE) in enumerate(attempts):
        pos = dict(IP)
        E = list(IE)
        if newv:
            pos[newv] = (0, -40)
        if newE:
            E += newE
        V = list(pos)
        dd = degrees(V, E)
        odd = [v for v in V if dd[v] % 2]
        ns = {v: "hl" for v in odd}
        es = {(e[0], e[1]): "new" for e in (newE or [])}
        lab = {v: f"δ={dd[v]}" for v in V}
        svg = SVG()
        draw_graph(svg, pos, E, node_style=ns, edge_style=es, labels=lab,
                   label_style={v: ("new" if v in odd else "dim") for v in V})
        img = p.img(f"impar-{k}", svg)
        oddtxt = ", ".join(f"${v}$" for v in odd) if odd else "ninguno"
        if k == 0:
            body = (f"> Los vértices de grado impar (en rojo) son {oddtxt}: hay **{len(odd)}**. "
                    f"**¿Se puede modificar este grafo para que tenga solo un nodo de grado impar?**")
        else:
            body = f"> {txt} Ahora los de grado impar son {oddtxt}: hay **{len(odd)}**."
            if k == len(attempts) - 1:
                body += (" Cada arista nueva cambia la paridad de **sus dos** extremos a la vez: "
                         "la cantidad de vértices impares sube o baja de a $2$, o se queda igual.")
        tabs.append(f"![Intento {k}]({img})\n\n{body}")
    p.put("impar-steps", steps("¿Un solo vértice de grado impar?", tabs))

    # Dirigido: ejemplo de Bedoya (u, v, w)
    PD0 = scale({"u": (0, 0), "v": (1.7, 0), "w": (0, 1.2)}, 85)
    ED0 = [("u", "u"), ("v", "v"), ("u", "v"), ("u", "w"), ("w", "u"), ("w", "v"), ("v", "w")]
    di, do = inout(list("uvw"), ED0)
    assert (di, do) == ({"u": 2, "v": 3, "w": 2}, {"u": 3, "v": 2, "w": 2})
    p.put("fig-dir0", gfig(p, "dir0", PD0, ED0, directed=True))

    # Familias
    def kn(n):
        names = [f"v{i}" for i in range(1, n + 1)]
        return names, [(names[i], names[j]) for i in range(n) for j in range(i + 1, n)]

    items = []
    for n in range(2, 7):
        names, E = kn(n)
        items.append((circle_pos(names, 50 if n > 2 else 36), E, f"K{n}",
                      {"node_text": {v: "" for v in names}}))
    p.put("fam-k", graph_row(p, "Kn", items, gap=50))
    items = []
    for n in range(3, 7):
        names = [f"v{i}" for i in range(1, n + 1)]
        E = [(names[i], names[(i + 1) % n]) for i in range(n)]
        items.append((circle_pos(names, 50), E, f"C{n}"))
    p.put("fam-c", graph_row(p, "Cn", items, gap=60))
    items = []
    for n in range(3, 7):
        names = [f"v{i}" for i in range(1, n + 1)]
        E = [(names[i], names[(i + 1) % n]) for i in range(n)] + [("h", v) for v in names]
        pos = circle_pos(names, 52)
        pos["h"] = (0, 0)
        items.append((pos, E, f"W{n}", {"node_text": {v: "" for v in names + ["h"]}}))
    p.put("fam-w", graph_row(p, "Wn", items, gap=50))
    items = []
    for m, n in ((2, 3), (3, 3), (3, 5)):
        A = [f"a{i}" for i in range(m)]
        B = [f"b{i}" for i in range(n)]
        pos = {a: ((i - (m - 1) / 2) * 55, 0) for i, a in enumerate(A)}
        pos |= {b: ((i - (n - 1) / 2) * 55, 90) for i, b in enumerate(B)}
        E = [(a, b) for a in A for b in B]
        items.append((pos, E, f"K{m},{n}", {"node_text": {v: "" for v in A + B},
                                             "node_style": {v: "v1" for v in A} | {v: "v2" for v in B}}))
    p.put("fam-kmn", graph_row(p, "Kmn", items, gap=60))

    # Bipartitos: ejemplos de Bedoya
    b1 = (scale({"a": (0, 0), "b": (1.4, 0), "c": (0.7, 1.2)}, 70), [("a", "c"), ("b", "c")],
          {"a": "v1", "b": "v1", "c": "v2"}, "V1={a,b}, V2={c}")
    b2 = (scale({"a": (0, 0), "b": (1.5, 0), "c": (3, 0), "d": (0.7, 1.3), "e": (2.2, 1.3)}, 65),
          [("a", "d"), ("a", "e"), ("b", "d"), ("b", "e"), ("c", "d"), ("c", "e")],
          {"a": "v1", "b": "v1", "c": "v1", "d": "v2", "e": "v2"}, "V1={a,b,c}, V2={d,e}")
    b3P = scale({"a": (0, 0), "c": (0, 1), "e": (0, 2), "g": (0, 3), "b": (1.2, 0.6), "d": (1.2, 1.4),
                 "f": (1.2, 2.2)}, 55)
    b3E = [("a", "b"), ("a", "d"), ("c", "b"), ("c", "d"), ("c", "f"), ("e", "d"), ("g", "d"),
           ("g", "f")]
    st3 = {v: ("v1" if v in "aceg" else "v2") for v in b3P}
    b4P = dict(b3P) | {"h": (0, 4 * 55)}
    b4E = b3E + [("h", "b"), ("h", "d"), ("h", "f")]
    st4 = {v: ("v1" if v in "acegh" else "v2") for v in b4P}
    items = [(b1[0], b1[1], b1[3], {"node_style": b1[2]}),
             (b2[0], b2[1], b2[3], {"node_style": b2[2]}),
             (b3P, b3E, "V1={a,c,e,g}, V2={b,d,f}", {"node_style": st3}),
             (b4P, b4E, "V1={a,c,e,g,h}, V2={b,d,f}", {"node_style": st4})]
    p.put("fig-bip-ej", graph_row(p, "bip-ej", items, gap=70))

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

    # Ejercicio 1: clasificar (Bedoya)
    noname = lambda pos: {"node_text": {v: "" for v in pos}}
    ca = scale({"t": (1, 0), "l": (0, 1.6), "r": (2, 1.6), "m": (1, 1.0)}, 55)
    cbP = scale({"tl": (0, 0), "tr": (2, 0), "bl": (0, 1.6), "br": (2, 1.6), "m": (1, 0.8)}, 55)
    ccP = scale({"p1": (0.8, 0), "p2": (2, 0), "lf": (0, 1.3), "p3": (2.8, 1.3), "p4": (1.5, 1.9)}, 55)
    cdP = circle_pos(["n1", "n2", "n3", "n4", "n5"], 60)
    items = [
        (ca, [(x, y) for i, x in enumerate(ca) for y in list(ca)[i + 1:]], "a)", noname(ca)),
        (cbP, [("tl", "tr"), ("tr", "br"), ("br", "bl"), ("bl", "tl"), ("m", "tl"), ("m", "tr"),
               ("m", "bl"), ("m", "br"), ("tl", "tl"), ("tr", "tr")], "b)", noname(cbP)),
        (ccP, [("p1", "p2"), ("p1", "lf"), ("p1", "p3"), ("p2", "p3"), ("p2", "p3", None, 22),
               ("p1", "p4"), ("p4", "p3")], "c)", noname(ccP)),
        (cdP, [(x, y) for i, x in enumerate(cdP) for y in list(cdP)[i + 1:]]
         + [("n4", "n4"), ("n2", "n3", None, 20)], "d)", noname(cdP)),
    ]
    p.put("fig-cl", graph_row(p, "cl", items, gap=70))

    # Ejercicio 2: grados (Bedoya, u..y)
    G2V = list("uvwxy")
    G2P = scale({"v": (0.6, 0), "w": (1.9, 0), "u": (0, 1.2), "x": (2.6, 1.1), "y": (1.3, 2.0)}, 80)
    G2E = [("v", "w"), ("v", "x"), ("v", "y"), ("v", "y", None, 20), ("w", "x"),
           ("w", "x", None, 20), ("u", "y"), ("x", "y"), ("v", "v"), ("w", "w")]
    d2 = degrees(G2V, G2E)
    assert d2 == dict(u=1, v=6, w=5, x=4, y=4)
    p.put("fig-g2", gfig(p, "g2", G2P, G2E))
    p.put("g2-sol", dlist(G2V, d2))
    p.put("g2-suma", " + ".join(str(d2[v]) for v in G2V) + f" = {sum(d2.values())}")
    p.put("g2-e", str(len(G2E)))

    # Ejercicio 3: handshaking (Bedoya)
    HP = scale({"u": (0, 0), "v": (1.2, 0), "w": (2.4, 0), "x": (1.2, 1.0)}, 75)
    H2E = [("u", "u"), ("v", "v"), ("w", "w"), ("u", "v"), ("v", "w"), ("v", "x"), ("w", "x")]
    H3E = [("u", "v"), ("u", "v", None, 18), ("v", "v"), ("v", "w"), ("v", "x"), ("w", "x"),
           ("w", "x", None, 16), ("w", "x", None, -16)]
    dd2 = hs_fig("hs2", list("uvwx"), HP, H2E, dict(u=3, v=5, w=4, x=2))
    dd3 = hs_fig("hs3", list("uvwx"), HP, H3E, dict(u=2, v=6, w=4, x=4))
    p.put("fig-hs23", graph_row(p, "hs23", [(HP, H2E, "a)"), (HP, H3E, "b)")], gap=90))
    p.put("hs2-sol", f"$e = {len(H2E)}$; " + dlist("uvwx", dd2))
    p.put("hs3-sol", f"$e = {len(H3E)}$; " + dlist("uvwx", dd3))

    # Ejercicio 4: dibujar con grados dados
    D4P = scale({"v": (1, 0), "u": (0, 1), "w": (2, 1), "x": (1, 2)}, 70)
    D4E = [("u", "v"), ("v", "w"), ("w", "x"), ("x", "u"), ("u", "w")]
    D5P = dict(IP)
    D5E = list(IE)
    assert degrees(list("uvwx"), D4E) == dict(u=3, v=2, w=3, x=2)
    assert degrees(list("uvwxy"), D5E) == dict(u=3, v=3, w=4, x=2, y=2)
    p.put("fig-dib", graph_row(p, "dibujar", [(D4P, D4E, "δ(u)=3, δ(v)=2, δ(w)=3, δ(x)=2"),
                                              (D5P, D5E, "δ(u)=3, δ(v)=3, δ(w)=4, δ(x)=2, δ(y)=2")],
                               gap=90))

    # Ejercicio 6: grados en grafos dirigidos (Bedoya)
    dirs = [
        (scale({"a": (0, 0), "b": (1.1, 0), "c": (2.3, 0), "e": (0, 1.1), "d": (1.1, 1.1),
                "f": (2.4, 1.1)}, 80),
         [("a", "a"), ("a", "b"), ("a", "c", None, -22), ("a", "e"), ("e", "a"), ("c", "c"),
          ("c", "b"), ("b", "d"), ("d", "c"), ("e", "e"), ("e", "d"), ("d", "e")],
         dict(a=(2, 4), b=(2, 1), c=(3, 2), d=(2, 2), e=(3, 3), f=(0, 0))),
        (scale({"v": (0, 0), "w": (1.2, 0), "u": (-0.8, 0.9), "x": (1.6, 0.9), "y": (0.5, 1.7)}, 80),
         [("w", "w"), ("x", "x"), ("v", "w"), ("v", "x"), ("v", "y"), ("v", "u"), ("x", "w"),
          ("x", "y"), ("u", "w"), ("y", "u")],
         dict(u=(2, 1), v=(0, 4), w=(4, 1), x=(2, 3), y=(2, 1))),
        (scale({"a": (0, 0), "b": (1.2, 0), "c": (0, 1.1), "d": (1.2, 1.1)}, 85),
         [("a", "a"), ("b", "b"), ("b", "a"), ("c", "a"), ("c", "b"), ("c", "d"), ("b", "d"),
          ("d", "b")],
         dict(a=(3, 1), b=(3, 3), c=(0, 3), d=(2, 1))),
        (scale({"a": (0, 0), "b": (1.4, 0), "c": (0, 1.1), "d": (1.4, 1.1)}, 85),
         [("c", "c"), ("b", "b"), ("b", "a", None, 24), ("b", "a", None, -24), ("a", "b", None, 0),
          ("b", "d", None, 16), ("b", "d", None, -16), ("d", "a")],
         dict(a=(3, 1), b=(2, 5), c=(1, 1), d=(2, 1))),
    ]
    items, sols = [], []
    for i, (pos, E, want) in enumerate(dirs):
        V = sorted(pos)
        di, do = inout(V, E)
        assert {v: (di[v], do[v]) for v in V} == want, (i, di, do)
        cap = "abcd"[i] + ")"
        items.append((pos, E, cap, {"directed": True}))
        sols.append(f"- {cap} " + "; ".join(f"$\\delta^-({v}) = {di[v]}$, $\\delta^+({v}) = {do[v]}$"
                                            for v in V) + f". Total: ${len(E)}$ aristas.")
    p.put("fig-dirs", graph_row(p, "dirs", items, gap=80))
    p.put("dirs-sol", "\n".join(sols))

    # Ejercicio 7: bipartitos (Bedoya)
    sq = scale({"a": (0, 0), "b": (1.3, 0), "c": (0, 1.2), "d": (1.3, 1.2)}, 65)
    dm = scale({"a": (0, 1), "b": (1.2, 0), "d": (1.2, 1), "e": (1.2, 2), "c": (2.4, 1)}, 55)
    st = scale({"a": (0, 0), "b": (2.4, 0), "c": (1.2, 0.5), "d": (0, 1), "e": (2.4, 1)}, 60)
    bips = [
        (sq, [("a", "b"), ("b", "d"), ("d", "c"), ("c", "a")], {"a": "v1", "d": "v1", "b": "v2", "c": "v2"}),
        (dm, [("a", "b"), ("a", "d"), ("a", "e"), ("b", "c"), ("d", "c"), ("e", "c")],
         {"a": "v1", "c": "v1", "b": "v2", "d": "v2", "e": "v2"}),
        (sq, [("a", "b"), ("b", "d"), ("d", "c"), ("c", "a"), ("b", "c")], {}),
        (st, [("a", "c"), ("b", "c"), ("d", "c"), ("e", "c")],
         {"a": "v1", "b": "v1", "d": "v1", "e": "v1", "c": "v2"}),
    ]
    p.put("fig-bip", graph_row(p, "bip", [(pos, E, "abcd"[i] + ")") for i, (pos, E, _) in enumerate(bips)]))
    sol_items = []
    for i, (pos, E, colors) in enumerate(bips):
        es = {}
        if not colors:
            es = {("a", "b"): "new", ("b", "c"): "new", ("c", "a"): "new"}
        sol_items.append((pos, E, "abcd"[i] + ")", {"node_style": colors, "edge_style": es}))
        if colors:
            assert all(colors[x] != colors[y] for x, y in E)
    p.put("fig-bip-sol", graph_row(p, "bip-sol", sol_items))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
