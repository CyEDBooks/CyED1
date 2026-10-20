from common import *

T = ("a", [("b", [("e", [("h", []), ("i", []), ("j", [])]), ("f", [])]),
           ("c", [("g", [("l", []), ("m", [("n", []), ("o", [])])]), ("k", [])]),
           ("d", [("p", []), ("q", [])])])
T2 = ("a", [("b", [("e", []), ("f", [("k", []), ("m", [])])]), ("c", [("g", [])]),
            ("d", [("h", []), ("i", [("n", [])]), ("j", [])])])


def info(t):
    parent, children, depth = {}, {}, {}

    def rec(node, p, d):
        lab, ch = node
        parent[lab] = p
        children[lab] = [c[0] for c in ch]
        depth[lab] = d
        for c in ch:
            rec(c, lab, d + 1)
    rec(t, None, 0)
    return parent, children, depth


def tfig(p, name, t, dx=46, dy=60, **kw):
    pos, E = tree_pos(t, dx, dy)
    return gfig(p, name, pos, E, **kw)


def build():
    p = Page("Unidad4-EstructurasRecursivas/Arboles")

    # ¿Es árbol?
    g1 = scale({"a": (0, 0), "b": (1, 0), "c": (2, 0), "d": (1, 1), "e": (2, 1)}, 70)
    cases = [
        ("es-1", g1, [("a", "b"), ("b", "c"), ("b", "d"), ("d", "e")], "a)"),
        ("es-2", g1, [("a", "b"), ("b", "c"), ("b", "d"), ("d", "e"), ("c", "e")], "b)"),
        ("es-3", g1, [("a", "b"), ("d", "e"), ("c", "e")], "c)"),
        ("es-4", g1, [("a", "d"), ("b", "d"), ("c", "d"), ("d", "e")], "d)"),
    ]
    for name, pos, E, cap in cases:
        p.put("fig-" + name, gfig_caption(p, name, pos, E, cap))
    p.put("fig-es-2-sol", gfig(p, "es-2-sol", g1, cases[1][2],
                               edge_style={("b", "c"): "new", ("c", "e"): "new", ("d", "e"): "new",
                                           ("b", "d"): "new"}))

    # Raíz: el mismo árbol con raíces distintas
    Tu = [("a", "b"), ("b", "c"), ("b", "d"), ("d", "e"), ("d", "f"), ("c", "g")]
    def rooted(r):
        adj = {}
        for x, y in Tu:
            adj.setdefault(x, []).append(y)
            adj.setdefault(y, []).append(x)
        def rec(v, par):
            return (v, [rec(w, v) for w in sorted(adj[v]) if w != par])
        return rec(r, None)
    p.put("fig-raiz-g", gfig_caption(p, "raiz-grafo", scale({"a": (0, 0), "b": (1, 0.3), "c": (2, 0),
                                                           "d": (1.4, 1.1), "e": (0.7, 1.7),
                                                           "f": (2.1, 1.7), "g": (3, 0.3)}, 70),
                                     Tu, "Árbol"))
    for r in ("a", "d"):
        pos, E = tree_pos(rooted(r), 50, 60)
        p.put(f"fig-raiz-{r}", gfig_caption(p, f"raiz-{r}", pos, E, f"Con raíz en {r}",
                                            node_style={r: "hl"}))

    # Terminología
    for key, t in (("t1", T), ("t2", T2)):
        pos, E = tree_pos(t, 46, 60)
        p.put(f"fig-{key}", gfig(p, f"term-{key}", pos, E))
        par, ch, dep = info(t)
        leaves = [v for v in ch if not ch[v]]
        internal = [v for v in ch if ch[v] and par[v] is not None]
        alt = max(dep.values()) + 1
        p.put(f"{key}-hojas", ", ".join(leaves))
        p.put(f"{key}-internos", ", ".join(internal))
        p.put(f"{key}-alt", str(alt))
        for v in ch:
            p.put(f"{key}-padre-{v}", par[v] or "—")
            p.put(f"{key}-hijos-{v}", ", ".join(ch[v]) or "ninguno")
            p.put(f"{key}-prof-{v}", str(dep[v]))
            p.put(f"{key}-ar-{v}", str(len(ch[v])))
    # rama y subárbol resaltados
    pos, E = tree_pos(T, 46, 60)
    rama = ["a", "c", "g", "m", "o"]
    es = {(x, y): "new" for x, y in zip(rama, rama[1:])}
    p.put("fig-rama", gfig(p, "rama", pos, E, edge_style=es, node_style={v: "hl" for v in rama}))
    sub = ["c", "g", "k", "l", "m", "n", "o"]
    p.put("fig-sub", gfig(p, "subarbol", pos, E, node_style={v: "tree" for v in sub},
                          edge_style={(x, y): "tree" for x, y in E if x in sub}))

    # n-arios
    nar = [
        ("nar-1", ("a", [("b", [("d", []), ("e", [])]), ("c", [])]), "a)"),
        ("nar-2", ("a", [("b", []), ("c", [("e", []), ("f", []), ("g", [])]), ("d", [])]), "b)"),
        ("nar-3", ("a", [("b", [("d", []), ("e", [])]), ("c", [("f", []), ("g", [])])]), "c)"),
        ("nar-4", ("a", [("b", [("e", []), ("f", []), ("g", []), ("h", [])]), ("c", []), ("d", [("i", [])])]), "d)"),
    ]
    for name, t, cap in nar:
        pos, E = tree_pos(t, 40, 55)
        p.put("fig-" + name, gfig_caption(p, name, pos, E, cap, r=15))

    # Árbol de decisión para ordenar a, b, c
    dec = ("a<b?", [("b<c?", [("a,b,c", []), ("a<c? ", [("a,c,b", []), ("c,a,b", [])])]),
                    ("a<c?", [("b,a,c", []), ("b<c? ", [("b,c,a", []), ("c,b,a", [])])])])
    pos, E = tree_pos(dec, 70, 70)
    ns = {v: ("tree" if "," in v else "plain") for v in pos}
    svg = SVG()
    draw_graph(svg, pos, E, False, node_style=ns, node_text={v: v.strip() for v in pos}, r=26,
               font=13)
    for a, b in E:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        sí = x2 < x1
        svg.text((x1 + x2) / 2 + (-8 if sí else 8), (y1 + y2) / 2, "sí" if sí else "no", 11,
                 PAL["muted"], anchor="end" if sí else "start", bg=True)
    p.put("fig-decision", f"![Árbol de decisión para ordenar tres elementos]({p.img('decision', svg)})")

    p.assemble("index.md")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
