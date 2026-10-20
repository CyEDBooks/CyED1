from common import *
from figlib import NODE_STYLES

COLORS = ["#8ecae6", "#ffb703", "#90d18f", "#f4a3b4", "#c3b1e1"]
CNAMES = ["azul", "amarillo", "verde", "rosado", "lila"]


def colored(p, name, pos, E, col, new=None, r=18):
    svg = SVG()
    draw_graph(svg, pos, E, False, r=r, node_style={v: ("hl" if v == new else "plain") for v in pos},
               dots=False)
    # pintar encima el relleno de color
    for v, k in col.items():
        x, y = pos[v]
        stroke = PAL["new"] if v == new else PAL["ink"]
        svg.circle(x, y, r, COLORS[k], stroke, 3.0 if v == new else 1.6)
        svg.text(x, y + 5, v, 14, PAL["ink"], bold=(v == new))
    return f"![{name}]({p.img(name, svg)})"


def greedy(V, E, order):
    adj = {v: set() for v in V}
    for a, b in E:
        adj[a].add(b)
        adj[b].add(a)
    col = {}
    snaps = []
    for v in order:
        used = {col[u] for u in adj[v] if u in col}
        k = 0
        while k in used:
            k += 1
        col[v] = k
        snaps.append((v, dict(col), sorted(used)))
    return snaps, adj


def isomorphisms(VG, EG, VH, EH, directed=False):
    """Todas las biyecciones que preservan la adyacencia (fuerza bruta; grafos pequeños)."""
    import itertools
    def key(a, b):
        return (a, b) if directed else tuple(sorted((a, b)))
    from collections import Counter
    cG = Counter(key(e[0], e[1]) for e in EG)
    cH = Counter(key(e[0], e[1]) for e in EH)
    out = []
    for perm in itertools.permutations(VH):
        f = dict(zip(VG, perm))
        if Counter(key(f[a], f[b]) for a, b in cG.elements()) == cH:
            out.append(f)
    return out


def build():
    p = Page("Unidad5-Grafos/IsomorfismoPlanaridadColoreo")

    # isomorfismo: G (cuadrado) y H (corbatín)
    pG = scale({"v1": (0, 0), "v2": (1, 0), "v3": (0, 1), "v4": (1, 1)}, 90)
    EG = [("v1", "v2"), ("v1", "v3"), ("v2", "v4"), ("v3", "v4")]
    pH = scale({"w1": (0, 0), "w2": (1, 0), "w3": (1, 1), "w4": (0, 1)}, 90)
    EH = [("w1", "w4"), ("w1", "w3"), ("w4", "w2"), ("w3", "w2")]
    f = {"v1": "w1", "v2": "w4", "v3": "w3", "v4": "w2"}
    p.put("fig-G", gfig_caption(p, "iso-G", pG, EG, "G", r=20))
    p.put("fig-H", gfig_caption(p, "iso-H", pH, EH, "H", r=20))
    tabs = []
    done = []
    for k, (a, b) in enumerate(EG):
        svg = SVG()
        es = {e: "tree" for e in done}
        es[(a, b)] = "new"
        draw_graph(svg, pG, EG, False, edge_style=es, node_style={a: "hl", b: "hl"}, r=20)
        off = {v: (x + 260, y) for v, (x, y) in pH.items()}
        fe = (f[a], f[b])
        esH = {(f[x], f[y]): "tree" for x, y in done}
        esH[fe] = "new"
        draw_graph(svg, off, EH, False, edge_style=esH, node_style={f[a]: "hl", f[b]: "hl"}, r=20)
        svg.text(45, 135, "G", 14, PAL["ink"], bold=True)
        svg.text(305, 135, "H", 14, PAL["ink"], bold=True)
        done.append((a, b))
        tabs.append(f"![Isomorfismo, paso {k + 1}]({p.img(f'iso-{k:02d}', svg)})\n\n"
                    f"> $\\{{{a.replace('v', 'v_')}, {b.replace('v', 'v_')}\\}}$ es arista de $G$ "
                    f"y $\\{{f({a.replace('v', 'v_')}), f({b.replace('v', 'v_')})\\}} = "
                    f"\\{{{f[a].replace('w', 'w_')}, {f[b].replace('w', 'w_')}\\}}$ es arista de $H$.")
    tabs.append(tabs[-1].split("\n\n")[0] + "\n\n> Las $4$ aristas de $G$ van a aristas de $H$, y $H$ "
                "tiene exactamente $4$ aristas: $f$ también lleva no-aristas a no-aristas. "
                "**$f$ es un isomorfismo.**")
    p.put("iso-steps", steps("Verificar que f preserva la adyacencia", tabs))

    # Con matrices de adyacencia (Grafos 3)
    VG6 = ["u1", "u2", "u3", "u4", "u5", "u6"]
    pG6 = scale({"u1": (0, 0), "u2": (1.6, 0), "u3": (1.6, 1), "u4": (0, 1), "u5": (0.5, 0.5),
                 "u6": (1.2, 0.5)}, 80)
    EG6 = [("u1", "u2"), ("u1", "u4"), ("u2", "u3"), ("u2", "u6"), ("u3", "u4"), ("u4", "u5"),
           ("u5", "u6")]
    VH6 = ["v1", "v2", "v3", "v4", "v5", "v6"]
    pH6 = scale({"v1": (0, 0), "v3": (1.6, 0), "v4": (1.6, 1), "v5": (0, 1), "v2": (0.6, 0.5),
                 "v6": (1.2, 0.6)}, 80)
    EH6 = [("v1", "v2"), ("v1", "v5"), ("v2", "v3"), ("v3", "v4"), ("v3", "v6"), ("v4", "v5"),
           ("v5", "v6")]
    fG6 = {"u1": "v6", "u2": "v3", "u3": "v4", "u4": "v5", "u5": "v1", "u6": "v2"}
    assert fG6 in isomorphisms(VG6, EG6, VH6, EH6)
    sub = lambda v: v[0] + "_" + v[1:]
    nt = {v: sub(v).replace("_", "") for v in VG6 + VH6}
    sl = lambda pos: {v: v[0] + "".join("₀₁₂₃₄₅₆₇₈₉"[int(ch)] for ch in v[1:]) for v in pos}
    p.put("fig-GH6", graph_row(p, "GH6", [(pG6, EG6, "G", {"node_text": sl(pG6)}),
                                          (pH6, EH6, "H", {"node_text": sl(pH6)})], gap=110))

    def amat(V, E, order):
        idx = {v: i for i, v in enumerate(order)}
        M = [[0] * len(order) for _ in order]
        for a, b in E:
            M[idx[a]][idx[b]] = M[idx[b]][idx[a]] = 1
        return M
    hord = [fG6[u] for u in VG6]
    MG = amat(VG6, EG6, VG6)
    MH = amat(VH6, EH6, hord)
    assert MG == MH
    p.put("mat-GH6", "$$\n" + latex_matrix("A_G", [sub(v) for v in VG6], [sub(v) for v in VG6], MG, (), str)
          + " \\qquad " + latex_matrix("A_H", [sub(v) for v in hord], [sub(v) for v in hord], MH, (), str)
          + "\n$$")
    # Pares isomorfos (Grafos 3)
    pX = scale({"a": (0, 0), "b": (1.4, 0), "e": (0.7, 0.55), "c": (0, 1.1), "d": (1.4, 1.1)}, 70)
    EX_ = [("a", "e"), ("b", "e"), ("c", "e"), ("d", "e")]
    pS = scale({"x": (0, 0.55), "y": (1.1, 0), "z": (1.2, 0.4), "w": (1.2, 0.75), "r": (1.1, 1.1)}, 70)
    ES = [("x", "y"), ("x", "z"), ("x", "w"), ("x", "r")]
    pK = scale({"a": (0, 0.5), "b": (0.5, 0), "c": (1.4, 0), "d": (1.9, 0.6), "e": (0.6, 1.1)}, 70)
    EK = [("a", "b"), ("b", "c"), ("a", "d"), ("c", "e"), ("a", "e"), ("c", "d")]
    pK2 = scale({"o": (0, 0.3), "p": (0, 1.1), "q": (1.2, 0), "r": (1.2, 0.7), "s": (1.2, 1.4)}, 70)
    EK2 = [("o", "q"), ("o", "r"), ("o", "s"), ("p", "q"), ("p", "r"), ("p", "s")]
    assert {"a": "o", "c": "p", "b": "q", "d": "r", "e": "s"} in isomorphisms("abcde", EK, "opqrs", EK2)
    p.put("fig-pares", graph_row(p, "pares1", [(pX, EX_, ""), (pS, ES, "")], gap=90) + "\n\n"
          + graph_row(p, "pares2", [(pK, EK, ""), (pK2, EK2, "")], gap=90))
    # Cubos (Grafos 3): misma secuencia de grados, no isomorfos
    pc = scale({"a": (0, 0), "b": (2, 0), "c": (2, 1.4), "d": (0, 1.4), "e": (0.6, 0.45),
                "f": (1.4, 0.45), "g": (1.4, 0.95), "h": (0.6, 0.95)}, 70)
    ECG = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("e", "f"), ("f", "g"), ("g", "h"),
           ("h", "e"), ("b", "f"), ("d", "h")]
    pc2 = {k2: pc[k1] for k1, k2 in zip("abcdefgh", "stuvwxyz")}
    ECH = [("s", "t"), ("t", "u"), ("u", "v"), ("v", "s"), ("w", "x"), ("x", "y"), ("y", "z"),
           ("z", "w"), ("s", "w"), ("v", "z")]
    assert not isomorphisms("abcdefgh", ECG, "stuvwxyz", ECH)
    p.put("fig-cubos", graph_row(p, "cubos", [(pc, ECG, "G"), (pc2, ECH, "H")], gap=100))

    # no isomorfos por grado
    p5 = circle_pos(list("abcde"), 55)
    G2 = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "a"), ("a", "c")]
    pH2 = scale({"p": (0, 0), "q": (1, 0), "r": (1, 1), "s": (0, 1), "t": (-0.9, 1.5)}, 70)
    H2 = [("p", "q"), ("q", "r"), ("r", "s"), ("s", "p"), ("p", "r"), ("s", "t")]
    p.put("fig-G2", gfig_caption(p, "noiso-G", p5, G2, "G"))
    p.put("fig-H2", gfig_caption(p, "noiso-H", pH2, H2, "H"))
    # misma secuencia de grados, no isomorfos
    p6 = circle_pos(list("abcdef"), 55)
    C6 = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("f", "a")]
    p33 = {**circle_pos(list("pqr"), 40, cx=0), **circle_pos(list("stu"), 40, cx=110)}
    T2 = [("p", "q"), ("q", "r"), ("r", "p"), ("s", "t"), ("t", "u"), ("u", "s")]
    p.put("fig-C6", gfig_caption(p, "c6", p6, C6, "G"))
    p.put("fig-2C3", gfig_caption(p, "dos-c3", p33, T2, "H"))

    # planaridad
    k4 = circle_pos(list("abcd"), 55, -45)
    EK4 = [(x, y) for i, x in enumerate("abcd") for y in "abcd"[i + 1:]]
    p.put("fig-k4-cruce", gfig_caption(p, "k4-cruce", k4, EK4, "K4 con un cruce"))
    k4p = scale({"a": (0, 1.2), "b": (1, -0.4), "c": (2, 1.2), "d": (1, 0.5)}, 80)
    p.put("fig-k4-plano", gfig_caption(p, "k4-plano", k4p, EK4, "K4 sin cruces",
                                       edge_style={("b", "d"): "new", ("a", "c"): "plain"}))
    svg = SVG()
    draw_graph(svg, k4p, EK4, False)
    for txt, x, y in (("R1", 50, 40), ("R2", 112, 40), ("R3", 82, 80), ("R4", 175, 0)):
        svg.text(x, y, txt, 13, PAL["new"], bold=True)
    p.put("fig-k4-regiones", f"![Regiones de K4]({p.img('k4-regiones', svg)})")
    k5 = circle_pos(list("abcde"), 60)
    EK5 = [(x, y) for i, x in enumerate("abcde") for y in "abcde"[i + 1:]]
    p.put("fig-k5", gfig_caption(p, "k5", k5, EK5, "K5"))
    A = ["a1", "a2", "a3"]
    B = ["b1", "b2", "b3"]
    pk33 = {a: (i * 70, 0) for i, a in enumerate(A)} | {b: (i * 70, 100) for i, b in enumerate(B)}
    p.put("fig-k33", gfig_caption(p, "k33", pk33, [(a, b) for a in A for b in B], "K3,3",
                                  node_text={v: v.replace("a", "v").replace("b", "w") for v in A + B}))
    # Bedoya: un grafo dibujado con cruces que sí es plano, y sus regiones
    VR = list("pabcde")
    cruce = scale({"p": (1, 1), "a": (1.6, 0), "b": (2, 1.3), "c": (0, 1), "d": (0, 2), "e": (1.6, 2)}, 75)
    ER = [("p", "a"), ("p", "b"), ("a", "b"), ("p", "c"), ("p", "d"), ("c", "d"), ("p", "e")]
    plano = scale({"p": (1, 1), "a": (0.2, 0.2), "b": (0, 1.3), "c": (1, 2), "d": (2, 1),
                   "e": (2, 0)}, 75)
    ER2 = [("p", "a"), ("p", "b"), ("a", "b"), ("p", "c"), ("p", "d"), ("c", "d"), ("p", "e")]
    t1 = SVG()
    draw_graph(t1, scale({"p": (1, 1), "a": (0.2, 0), "b": (2.1, 0.8), "c": (0, 1.6), "d": (1.1, 2.1),
                          "e": (2.2, 0)}, 75), [("p", "a"), ("p", "b"), ("a", "b"), ("p", "c"), ("p", "d"),
                                                ("c", "e"), ("p", "e")] if False else ER2)
    tabs = []
    svg = SVG()
    cross = scale({"p": (1, 1), "a": (0, 0.2), "b": (2.2, 1.2), "c": (0, 1.8), "d": (1.4, 2.2),
                   "e": (2.1, 0)}, 75)
    Ecross = [("p", "a"), ("p", "b"), ("p", "c"), ("p", "d"), ("p", "e"), ("a", "d"), ("c", "b")]
    draw_graph(svg, cross, Ecross, node_text={v: "" for v in cross})
    tabs.append(f"![Dibujo con cruces]({p.img('plano-0', svg)})\n\n> En este dibujo hay aristas "
                f"que se cruzan.")
    svg = SVG()
    re_ = {"a": (0.2, 0.2), "d": (0, 1.3), "c": (1, 2), "b": (2, 1), "e": (2, 0), "p": (1, 1)}
    draw_graph(svg, scale(re_, 75), Ecross, node_text={v: "" for v in cross},
               edge_style={("a", "d"): "new", ("c", "b"): "new"})
    tabs.append(f"![Dibujo sin cruces]({p.img('plano-1', svg)})\n\n> Moviendo los vértices, el "
                f"mismo grafo se dibuja **sin cruces**: dos triángulos que comparten un vértice y "
                f"una arista que cuelga. **El grafo es plano.**")
    p.put("plano-steps", steps("¿Es plano?", tabs))
    pr = scale(re_, 80)
    p.put("fig-reg", gfig(p, "regiones", pr, Ecross, node_text={v: "" for v in pr}))
    svg = SVG()
    draw_graph(svg, pr, Ecross, node_text={v: "" for v in pr})
    for txt, (x, y) in (("R1", (34, 72)), ("R2", (108, 112)), ("R3", (175, 150))):
        svg.text(x, y, txt, 14, PAL["new"], bold=True)
    p.put("fig-reg-sol", f"![Tres regiones]({p.img('regiones-sol', svg)})")

    # coloración: mapa y grafo dual
    svg = SVG()
    cells = [("A", 0, 0, 300, 60), ("B", 0, 60, 100, 80), ("C", 100, 60, 100, 80),
             ("D", 200, 60, 100, 80), ("E", 0, 140, 300, 60)]
    for nm, x, y, w, h in cells:
        svg.rect(x, y, w, h, PAL["soft"], PAL["ink"], 1.6, rx=0)
        svg.text(x + w / 2, y + h / 2 + 6, nm, 18, PAL["ink"], bold=True)
    p.put("fig-mapa", f"![Mapa con cinco regiones]({p.img('mapa', svg)})")
    pm = scale({"A": (1, 0), "B": (0, 1), "C": (1, 1), "D": (2, 1), "E": (1, 2)}, 85)
    EM = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("C", "D"), ("E", "B"), ("E", "C"),
          ("E", "D")]
    p.put("fig-dual", gfig(p, "dual", pm, EM, r=20, dots=False))
    snaps, adj = greedy(list("ABCDE"), EM, ["C", "A", "E", "B", "D"])
    tabs = []
    for k, (v, col, used) in enumerate(snaps):
        img = colored(p, f"color-{k:02d}", pm, EM, col, new=v, r=20)
        usedn = ", ".join(CNAMES[u] for u in used) or "ninguno"
        tabs.append(f"{img}\n\n> ${v}$ (grado ${len(adj[v])}$): sus vecinos ya coloreados usan "
                    f"{usedn}. Se le asigna el primer color libre: **{CNAMES[col[v]]}**.")
    tabs[-1] += f"\n\n> Se usaron **{max(snaps[-1][1].values()) + 1}** colores."
    p.put("color-steps", steps("Coloración voraz del mapa", tabs))

    # Aplicación: exámenes
    VX = ["Cál", "Fís", "Prog", "Disc", "Quím", "Ingl"]
    EX = [("Cál", "Fís"), ("Cál", "Prog"), ("Cál", "Disc"), ("Fís", "Quím"), ("Prog", "Disc"),
          ("Prog", "Ingl"), ("Disc", "Quím"), ("Quím", "Ingl")]
    px = circle_pos(VX, 85)
    deg = {v: sum(1 for e in EX if v in e) for v in VX}
    order = sorted(VX, key=lambda v: (-deg[v], VX.index(v)))
    snaps, adj = greedy(VX, EX, order)
    tabs = []
    for k, (v, col, used) in enumerate(snaps):
        img = colored(p, f"examen-{k:02d}", px, EX, col, new=v, r=24)
        usedn = ", ".join(CNAMES[u] for u in used) or "ninguno"
        tabs.append(f"{img}\n\n> {v} (grado {deg[v]}): sus vecinos coloreados usan {usedn}. "
                    f"Color: **{CNAMES[col[v]]}**.")
    ncol = max(snaps[-1][1].values()) + 1
    groups = {}
    for v, k in snaps[-1][1].items():
        groups.setdefault(k, []).append(v)
    tabs[-1] += (f"\n\n> {ncol} colores = {ncol} franjas de examen: " +
                 "; ".join(f"franja {k + 1} ({CNAMES[k]}): {', '.join(groups[k])}" for k in sorted(groups)) + ".")
    p.put("fig-examenes", gfig(p, "examenes", px, EX, r=24, dots=False))
    p.put("examen-orden", ", ".join(f"{v} ({deg[v]})" for v in order))
    p.put("examen-steps", steps("Coloración voraz de los exámenes", tabs))
    p.assemble("index.md")

    # ejercicios
    pe = circle_pos(list("abcdefg"), 70)
    EE = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("f", "g"), ("g", "a"),
          ("a", "c"), ("a", "e"), ("c", "e")]
    p.put("fig-ex-color", gfig(p, "ex-color", pe, EE))
    import itertools
    Vs = list("abcdefg")
    for k in range(1, 5):
        sol = None
        for combo in itertools.product(range(k), repeat=len(Vs)):
            cmap = dict(zip(Vs, combo))
            if all(cmap[a] != cmap[b] for a, b in EE):
                sol = cmap
                break
        if sol:
            break
    p.put("ex-chi", str(k))
    p.put("ex-chi-sol", ", ".join(f"${v}$: {CNAMES[sol[v]]}" for v in Vs))
    deg = {v: sum(1 for e in EE if v in e) for v in Vs}
    order = sorted(Vs, key=lambda v: (-deg[v], Vs.index(v)))
    sn, _ = greedy(Vs, EE, order)
    p.put("ex-greedy", ", ".join(f"${v}$: {CNAMES[sn[-1][1][v]]}" for v in order))
    p.put("ex-greedy-n", str(max(sn[-1][1].values()) + 1))

    # Pares dirigidos (Grafos 3)
    sq = scale({"1": (0, 0), "2": (1.2, 0), "3": (0, 1.2), "4": (1.2, 1.2)}, 70)
    pu = {"u" + k: v for k, v in sq.items()}
    pv = {"v" + k: v for k, v in sq.items()}
    EU = [("u2", "u1"), ("u2", "u2"), ("u2", "u4"), ("u3", "u4"), ("u1", "u3", None, 16),
          ("u3", "u1", None, 16), ("u3", "u2")]
    fdir = {"u1": "v3", "u2": "v4", "u3": "v2", "u4": "v1"}
    EV = [(fdir[a], fdir[b], *rest) for a, b, *rest in EU]
    assert fdir in isomorphisms(list(pu), EU, list(pv), EV, directed=True)
    tri = scale({"1": (0.7, 0), "2": (0, 1.2), "3": (1.4, 1.2), "4": (0.7, 0.75)}, 70)
    pt1 = {"u" + k: v for k, v in tri.items()}
    pt2 = {"v" + k: v for k, v in tri.items()}
    ET1 = [("u1", "u2"), ("u1", "u3"), ("u2", "u3"), ("u1", "u4"), ("u4", "u2"), ("u3", "u4")]
    ET2 = [("v2", "v1"), ("v1", "v3"), ("v3", "v2"), ("v4", "v1"), ("v2", "v4"), ("v4", "v3")]
    assert not isomorphisms(list(pt1), ET1, list(pt2), ET2, directed=True)
    lab = lambda pos: {v: v[0] + "".join("₀₁₂₃₄₅₆₇₈₉"[int(ch)] for ch in v[1:]) for v in pos}
    p.put("fig-ex-dir", graph_row(p, "ex-dir1", [(pu, EU, "", {"directed": True, "node_text": lab(pu)}),
                                                 (pv, EV, "", {"directed": True, "node_text": lab(pv)})],
                                  gap=100) + "\n\n" +
          graph_row(p, "ex-dir2", [(pt1, ET1, "", {"directed": True, "node_text": lab(pt1)}),
                                   (pt2, ET2, "", {"directed": True, "node_text": lab(pt2)})], gap=100))
    outs1 = sorted(sum(1 for e in ET1 if e[0] == v) for v in pt1)
    outs2 = sorted(sum(1 for e in ET2 if e[0] == v) for v in pt2)
    p.put("ex-dir-no", f"Los grados de salida son ${', '.join(map(str, outs1[::-1]))}$ en el primero "
                       f"y ${', '.join(map(str, outs2[::-1]))}$ en el segundo: en el primero $u_1$ tiene "
                       f"grado de salida $3$ y en el segundo ningún vértice lo tiene. Además, el "
                       f"triángulo de afuera es un circuito dirigido en el segundo y no en el primero.")
    # Número cromático (Grafos 3)
    VV = ["Cali", "Jamundí", "Yumbo", "Palmira", "Buga", "Tuluá"]
    pVV = scale({"Jamundí": (0, 0), "Cali": (1.6, 0), "Yumbo": (0, 0.9), "Palmira": (1.6, 1.2),
                 "Buga": (2.6, 0.6), "Tuluá": (3.8, 0.6)}, 80)
    EVV = [("Jamundí", "Cali"), ("Cali", "Yumbo"), ("Cali", "Palmira"), ("Cali", "Buga"),
           ("Cali", "Tuluá"), ("Yumbo", "Palmira"), ("Palmira", "Buga"), ("Buga", "Tuluá")]
    p.put("fig-valle", gfig(p, "valle", pVV, EVV,
                            name_pos={"Jamundí": "above", "Cali": "above", "Yumbo": "below",
                                      "Palmira": "below", "Buga": "above", "Tuluá": "below"}))
    import itertools
    sol = None
    for k_ in range(1, 5):
        for combo in itertools.product(range(k_), repeat=len(VV)):
            cm = dict(zip(VV, combo))
            if all(cm[a] != cm[b] for a, b in EVV):
                sol = cm
                break
        if sol:
            break
    assert k_ == 3
    p.put("valle-sol", ", ".join(f"{v}: {CNAMES[sol[v]]}" for v in VV))
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
