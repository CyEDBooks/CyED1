"""Figuras para árboles de búsqueda (espacio de estados) y árboles de juego."""
from common import *
from figlib import text_width, NODE_STYLES, _shorten


def layout(nodes, dx=60, dy=70):
    children = {}
    for n in nodes:
        if n["parent"] is not None:
            children.setdefault(n["parent"], []).append(n["id"])
    pos = {}
    counter = [0]

    def rec(v, depth):
        ch = children.get(v, [])
        for c in ch:
            rec(c, depth + 1)
        if ch:
            xs = [pos[c][0] for c in ch]
            pos[v] = ((min(xs) + max(xs)) / 2, depth * dy)
        else:
            pos[v] = (counter[0] * dx, depth * dy)
            counter[0] += 1
    rec(0, 0)
    return pos, children


def draw_board(svg, x, y, board, style="plain", cell=17):
    fill, stroke, tc, width = NODE_STYLES[style]
    w = 3 * cell
    x0, y0 = x - w / 2, y - w / 2
    svg.rect(x0 - 3, y0 - 3, w + 6, w + 6, fill, stroke, width, rx=5)
    for i in range(3):
        for j in range(3):
            v = board[i][j]
            cx, cy = x0 + j * cell, y0 + i * cell
            if v == 0:
                svg.rect(cx + 1, cy + 1, cell - 2, cell - 2, "#d9e2e6", "#d9e2e6", 0.5, rx=2)
            else:
                svg.rect(cx + 1, cy + 1, cell - 2, cell - 2, PAL["white"], PAL["border"], 0.8, rx=2)
                svg.text(cx + cell / 2, cy + cell / 2 + 4.5, v, 12, PAL["ink"])


def search_step_svg(nodes, pos, children, snap, upto, label, kind="circle", r=20,
                    frontier_title="Cola:", show_ops=False, font=13):
    """Dibuja los nodos creados hasta 'upto' con los estilos de ese paso."""
    svg = SVG()
    visible = {n["id"] for n in nodes if n["id"] <= upto}
    expanded = set(snap["expanded"])
    frontier = set(snap["frontier"])
    created = set(snap["created"])
    cur = snap["current"]
    for n in nodes:
        if n["id"] in visible and n["parent"] is not None:
            (x1, y1), (x2, y2) = pos[n["parent"]], pos[n["id"]]
            off = r + 3 if kind == "circle" else 32
            st = "new" if n["id"] in created else "plain"
            color, width, _ = EDGE_STYLES_[st]
            if kind == "circle":
                sx1, sy1, sx2, sy2 = _shorten(x1, y1, x2, y2, off, off)
            else:
                sx1, sy1, sx2, sy2 = x1, y1 + off, x2, y2 - off
            svg.line(sx1, sy1, sx2, sy2, color, width)
            if show_ops and n["op"]:
                svg.text((x1 + x2) / 2 + (8 if x2 >= x1 else -8), (y1 + y2) / 2 + 4, n["op"], 11,
                         PAL["muted"], anchor="start" if x2 >= x1 else "end", bg=True)
    for n in nodes:
        i = n["id"]
        if i not in visible:
            continue
        if snap.get("goal") and i == cur:
            st = "goal"
        elif i == cur:
            st = "hl"
        elif i in created:
            st = "new"
        elif i in expanded:
            st = "green"
        elif i in frontier:
            st = "plain"
        else:
            st = "plain"
        x, y = pos[i]
        if kind == "board":
            draw_board(svg, x, y, n["state"], st)
        else:
            fill, stroke, tc, width = NODE_STYLES[st]
            svg.circle(x, y, r, fill, stroke, width)
            t = label(n)
            size = font if len(t) <= 3 else max(9, font - (len(t) - 3))
            svg.text(x, y + size * 0.35, t, size, tc, bold=(st in ("new", "hl", "goal")))
    ys = max(y for _, y in pos.values()) + (50 if kind == "circle" else 62)
    x0 = min(x for x, _ in pos.values()) - 20
    if kind != "board":
        fr = [label(nodes[i]) for i in snap["frontier"]]
        newi = [k for k, i in enumerate(snap["frontier"]) if i in created]
        draw_panel(svg, x0, ys, frontier_title, fr, new=newi, wrap=10)
    return svg


EDGE_STYLES_ = {"plain": (PAL["muted"], 1.5, None), "new": (PAL["new"], 3.0, None)}
