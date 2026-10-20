from common import *
from figlib import NODE_STYLES

COLORS = ["#8ecae6", "#ffb703", "#90d18f", "#f4a3b4", "#c3b1e1"]
CNAMES = ["azul", "amarillo", "verde", "rosado", "lila"]


def colored(p, name, pos, E, col, new=None, r=18):
    svg = SVG()
    draw_graph(svg, pos, E, False, r=r, node_style={v: ("hl" if v == new else "plain") for v in pos})
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
    # ejercicio de regiones
    pr = scale({"a": (0, 0), "b": (1, 0), "c": (2, 0), "d": (0, 1), "e": (1, 1), "f": (2, 1)}, 85)
    ER = [("a", "b"), ("b", "c"), ("a", "d"), ("b", "e"), ("c", "f"), ("d", "e"), ("e", "f")]
    p.put("fig-reg", gfig(p, "regiones", pr, ER))

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
    p.put("fig-dual", gfig(p, "dual", pm, EM, r=20))
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
    p.put("fig-examenes", gfig(p, "examenes", px, EX, r=24))
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
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
