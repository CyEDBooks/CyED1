from common import *
from figlib import text_width
from tviz import (from_tuple, draw, nodes, fb, height, avl_insert_trace, avl_delete_trace,
                  avl_insert, double_rotation_middle, copy_tree, find, rot_left, bst_build, N,
                  halo, ring, zoom, layout, parent_map, search_path)
from anim import anim_block
from pages.u4_avl_anim import (ops_anim, rotation_anim, check_frames, fib_tree, avl_frames, cadena_anim,
                                fb_anim, c_falla_anim)


def fbtxt(f):
    return {0: "0"}.get(f, f"{f:+d}".replace("-", "−"))


def fbl(root):
    labels, ls = {}, {}
    for n in nodes(root):
        f = fb(n)
        labels[n.key] = fbtxt(f)
        if abs(f) > 1:
            ls[n.key] = "bad"
    return labels, ls


def adraw(t, **kw):
    """Árbol AVL con el factor de balanceo junto a cada nodo."""
    labels, ls = fbl(t)
    return draw(t, labels=labels, label_style=ls, **kw)


def pre(n):
    return [] if n is None else [n.key] + pre(n.left) + pre(n.right)


# Pasos de inserción y eliminación (tabs)
def avl_tabs(p, prefix, ops, start=None, k_img=0):
    """ops: lista de ('i', k) o ('d', k). Devuelve las pestañas y el árbol final."""
    root = start
    out = []
    for op, k in ops:
        if op == "i":
            root_after, snaps = avl_insert_trace(root, k)
        else:
            root_after, snaps = avl_delete_trace(root, k)
        unb = None
        for s in snaps:
            t = s["tree"]
            if s["kind"] == "insert":
                ns = {x: "hl" for x in s["path"]}
                ns[k] = "new"
                es = {(a, b): "path" for a, b in zip(s["path"], s["path"][1:] + [k])}
                txt = f"> Se inserta ${k}$ como en un ABB" + (
                    f" (camino: {', '.join(map(str, s['path']))})." if s["path"] else ": es la raíz.")
                if len(snaps) == 1:
                    txt += (" Se revisan los factores de balanceo de abajo hacia arriba, por el "
                            "camino del nodo nuevo: todos están entre $-1$ y $1$. Sigue siendo AVL.")
                else:
                    txt += " Se revisan los factores de balanceo de abajo hacia arriba, por el camino del nodo nuevo."
                img = adraw(t, node_style=ns, edge_style=es)
            elif s["kind"] == "delete":
                if s["succ"] is not None:
                    txt = (f"> Se borra ${k}$ como en un ABB. Tiene dos hijos: su sucesor "
                           f"${s['succ']}$ sale del árbol y su llave reemplaza a ${k}$.")
                    ns = {s["succ"]: "new"}
                else:
                    txt = f"> Se borra ${k}$ como en un ABB."
                    ns = {}
                if s["start"] is not None:
                    ns[s["start"]] = ns.get(s["start"], "hl")
                    txt += (f" El primer nodo posiblemente desbalanceado es ${s['start']}$, el "
                            f"padre del nodo que salió; desde ahí se sube revisando hasta la raíz.")
                rots = [x for x in snaps if x["kind"] == "rotated"]
                if not rots:
                    txt += " Todos los factores están entre $-1$ y $1$: sigue siendo AVL."
                img = adraw(t, node_style=ns) if t is not None else draw(None)
            elif s["kind"] == "unbalanced":
                p_ = find(t, s["key"])
                q = p_.right if s["fb"] == 2 else p_.left
                ns = {s["key"]: "bad", q.key: "hl"}
                txt = (f"> El primer nodo desbalanceado (subiendo) es $p = {s['key']}$, con "
                       f"$fb(p) = {fbtxt(s['fb'])}$. Su hijo del lado más alto es $q = {q.key}$, "
                       f"con $fb(q) = {fbtxt(fb(q))}$.")
                img = adraw(t, node_style=ns)
                unb = s
            else:
                case = s["case"]
                if case in ("C", "F"):
                    mid = double_rotation_middle(unb["tree"], unb["key"], case)
                    r1 = s["rots"][0]
                    img_mid = adraw(mid, node_style={r1[1]: "hl"})
                    path = p.img(f"{prefix}-{k_img:02d}", img_mid)
                    k_img += 1
                    out.append(f"![AVL, paso {len(out) + 1}]({path})\n\n> **Caso {case}:** $fb(q)$ "
                               f"tiene signo contrario a $fb(p)$. Primero `"
                               f"{'RIGHT' if r1[0] == 'derecha' else 'LEFT'}-ROTATE({r1[1]})`: "
                               f"se rota $q = {r1[1]}$ hacia la **{r1[0]}** y el peso queda «en "
                               f"línea».")
                    r2 = s["rots"][1]
                    txt = (f"> Luego `{'RIGHT' if r2[0] == 'derecha' else 'LEFT'}-ROTATE({r2[1]})`: "
                           f"se rota $p = {r2[1]}$ hacia la **{r2[0]}**. La nueva raíz del "
                           f"subárbol es ${s['newroot']}$ y todos los factores quedan entre $-1$ y "
                           f"$1$.")
                else:
                    r1 = s["rots"][0]
                    txt = (f"> **Caso {case}:** se ejecuta `{'RIGHT' if r1[0] == 'derecha' else 'LEFT'}"
                           f"-ROTATE({r1[1]})`: se rota $p = {r1[1]}$ hacia la **{r1[0]}**. La nueva "
                           f"raíz del subárbol es ${s['newroot']}$ y todos los factores del "
                           f"subárbol quedan entre $-1$ y $1$.")
                img = adraw(t, node_style={s["newroot"]: "new"})
            path = p.img(f"{prefix}-{k_img:02d}", img)
            k_img += 1
            out.append(f"![AVL, paso {len(out) + 1}]({path})\n\n{txt}")
        root = root_after
    return out, root


# Cinco ejemplos, de muy fácil a difícil. Cada desbalanceo se trata igual: revisar los fb de
# abajo hacia arriba, mirar de cerca el subárbol de p (alturas de sus dos lados y fb(q)),
# decidir el caso, rotar y comprobar que el árbol volvió a ser AVL.


def _avl_from(keys):
    r = None
    for k in keys:
        r = avl_insert(r, k)
    return r


EJEMPLOS = [
    dict(start=None, ops=[("i", 10), ("i", 20), ("i", 30)]),
    dict(start=bst_build([50, 40, 60, 30]), ops=[("i", 20)]),
    dict(start=bst_build([20, 10, 40, 30, 50]), ops=[("i", 35)]),
    dict(start=None, ops=[("i", k) for k in (40, 90, 25, 60, 75, 50, 95, 55)]),
    dict(start=_avl_from([65, 75, 95, 15, 60, 80, 70, 85, 5, 90, 40, 50, 25]), ops=[("d", 75)]),
]
LG = 7          # separación entre el nodo y su fb, para que no choque con el anillo rojo
ROT = {"izquierda": "LEFT", "derecha": "RIGHT"}


def _rings(*keys):
    def over(svg, pos):
        for k in keys:
            if k in pos:
                ring(svg, *pos[k])
    return over


def _fb(k, t):
    return f"fb({k}) = {fbtxt(fb(find(t, k)))}"


def _ancestors(t, k, stop):
    """Llaves de k hacia arriba hasta stop (inclusive)."""
    par = parent_map(t)
    out, x = [], find(t, k)
    while x is not None:
        out.append(x.key)
        if x.key == stop:
            break
        x = par[x.key]
    return out


def _sides(pn, dx=40, dy=56):
    """Sombras de los dos subárboles de p con su altura. Un lado vacío se dibuja como un hueco
    punteado en el lugar del hijo que falta."""
    def under(svg, pos):
        halo(svg, pos, pn.left, "blue", f"h = {height(pn.left)}")
        halo(svg, pos, pn.right, "orange", f"h = {height(pn.right)}")

    def over(svg, pos):
        x, y = pos[pn.key]
        for child, sgn, col in ((pn.left, -1, PAL["teal"]), (pn.right, 1, "#b86a00")):
            if child is None:
                gx, gy = x + sgn * dx * 0.7, y + dy
                svg.line(x + sgn * 9, y + 12, gx - sgn * 7, gy - 10, col, 1.2, "3,3")
                svg.ellipse(gx, gy, 12, 12, PAL["white"], col, 1.4, "3,3")
                svg.text(gx, gy + 5, "∅", 13, col)
                svg.text(gx, gy + 30, "h = 0", 13, col, bold=True)
    return under, over


def _case_fig(t, pk):
    """Figura del desbalanceo en p: con zoom al subárbol si el árbol es grande y p no es la raíz."""
    pn = find(t, pk)
    f = fb(pn)
    q = pn.right if f == 2 else pn.left
    under, over_sides = _sides(pn)
    labels, ls = fbl(t)

    def over(svg, pos):
        over_sides(svg, pos)
        ring(svg, *pos[q.key])
    if t.key == pk or len(nodes(t)) < 7:
        return adraw(t, node_style={pk: "bad", q.key: "hl"}, under=under, over=over, label_gap=LG, label_side="away")
    big = adraw(t, node_style={pk: "bad"}, label_gap=LG, label_side="away")
    pos, _ = layout(t, 40, 56)
    ks = [n.key for n in nodes(pn)]
    xs, ys = [pos[k][0] for k in ks], [pos[k][1] for k in ks]
    box = (min(xs) - 24, min(ys) - 26, max(xs) + 50, max(ys) + 24)
    sub = copy_tree(pn)
    under2, over2 = _sides(sub, dx=46)

    def over_z(svg, pos):
        over2(svg, pos)
        ring(svg, *pos[q.key])
    small = adraw(sub, node_style={pk: "bad", q.key: "hl"}, under=under2, over=over_z, label_gap=LG, label_side="away",
                  dx=46)
    return zoom(big, small, box, title=f"Zoom: subárbol de {pk}")


def _case_txt(t, pk):
    pn = find(t, pk)
    f = fb(pn)
    q = pn.right if f == 2 else pn.left
    fq = fb(q)
    hi, lo = ("derecho", "izquierdo") if f == 2 else ("izquierdo", "derecho")
    hh = height(pn.right if f == 2 else pn.left)
    hl_ = height(pn.left if f == 2 else pn.right)
    out = (f"Zoom en $p = {pk}$: su lado **{hi}** mide ${hh}$ y el {lo} ${hl_}$, así que "
           f"$fb(p) = {fbtxt(f)}$. El hijo del lado alto es $q = {q.key}$ (en el anillo), con "
           f"$fb(q) = {fbtxt(fq)}$. ")
    case = {(2, 1): "A", (2, 0): "B", (2, -1): "C", (-2, -1): "D", (-2, 0): "E", (-2, 1): "F"}[(f, fq)]
    d1 = "LEFT" if f == 2 else "RIGHT"
    if case in ("C", "F"):
        d0 = "RIGHT" if f == 2 else "LEFT"
        out += (f"**Signo contrario**: caso **{case}**, rotación doble: primero "
                f"`{d0}-ROTATE({q.key})` y luego `{d1}-ROTATE({pk})`.")
    else:
        same = "es $0$" if fq == 0 else "tiene el **mismo signo**"
        out += f"$fb(q)$ {same}: caso **{case}**, una sola rotación: `{d1}-ROTATE({pk})`."
    return out


def ejemplo_avl(p, i, ex):
    pref = f"ejx{i}"     # «ej1-», «ej2-», «ej3-» ya son de los ejemplos de las secciones 5 y 6
    tabs = []

    def add(svg, txt):
        tabs.append(f"![Ejemplo {i + 3}, paso {len(tabs) + 1}]({p.img(f'{pref}-{len(tabs) + 1:02d}', svg)})"
                    f"\n\n> {txt}")

    n = i + 3            # los ejemplos 1 a 3 están en las secciones 5 y 6
    root = copy_tree(ex["start"])
    verbs = {"i": "inserte", "d": "elimine"}
    ks = [k for _, k in ex["ops"]]
    what = (f"{verbs[ex['ops'][0][0]]} ${ks[0]}$" if len(ks) == 1
            else f"{verbs[ex['ops'][0][0]]}, en este orden, {', '.join(f'${k}$' for k in ks)}")
    if root is not None:
        head = (f"**Ejemplo {n}.** En el árbol AVL $T$, {what}. Junto a cada "
                f"nodo está su factor de balanceo.\n\n"
                f"![Árbol T del ejemplo {n}]({p.img(f'{pref}-00', adraw(root, label_gap=LG, label_side='away'))})")
    else:
        head = f"**Ejemplo {n}.** En un árbol AVL vacío, {what}."

    def rebalance(snaps, start):
        """Pestañas de cada par (unbalanced, rotated); start: llave desde donde se revisa."""
        cur = start
        drop = None      # (altura antes, altura después) del subárbol que se acaba de rotar
        for a, b in zip(snaps[::2], snaps[1::2]):
            t, pk = a["tree"], a["key"]
            chain = _ancestors(t, cur, pk)
            ns = {k: "goal" for k in chain[:-1]}
            ns[pk] = "bad"
            checks = ", ".join(f"${_fb(k, t)}$ ✓" for k in chain[:-1])
            pre = (f"La rotación anterior bajó la altura de ese subárbol de ${drop[0]}$ a "
                   f"${drop[1]}$, así que los factores de más arriba pueden cambiar: se sigue "
                   f"subiendo. " if drop and drop[0] != drop[1] else "")
            add(adraw(t, node_style=ns, over=_rings(pk), label_gap=LG, label_side="away"),
                pre + f"Se revisan los factores de abajo hacia arriba desde ${chain[0]}$: "
                + (checks + ", " if checks else "")
                + f"${_fb(pk, t)}$ ✗. El primer nodo desbalanceado es $p = {pk}$.")
            add(_case_fig(t, pk), _case_txt(t, pk))
            case = b["case"]
            if case in ("C", "F"):
                mid = double_rotation_middle(t, pk, case)
                r1 = b["rots"][0]
                qn = find(t, pk).right if case == "C" else find(t, pk).left
                rn = qn.left if case == "C" else qn.right
                add(adraw(mid, node_style={pk: "bad", rn.key: "new", qn.key: "hl"},
                          over=_rings(rn.key), label_gap=LG, label_side="away"),
                    f"`{ROT[r1[0]]}-ROTATE({r1[1]})`: ${rn.key}$ sube al lugar de ${qn.key}$. Ahora "
                    f"$p = {pk}$, ${rn.key}$ y ${qn.key}$ están **en línea**: el peso quedó todo de un "
                    f"lado, como en el caso {'A' if case == 'C' else 'D'}.")
            r2 = b["rots"][-1]
            nr = b["newroot"]
            others = [k for k in (pk, qn.key if case in ("C", "F") else None) if k is not None]
            add(adraw(b["tree"], node_style={nr: "new", **{k: "hl" for k in others}},
                      over=_rings(nr), label_gap=LG, label_side="away"),
                f"`{ROT[r2[0]]}-ROTATE({r2[1]})`: ${nr}$ sube a la raíz "
                f"{'del árbol' if b['tree'].key == nr else 'del subárbol'} y ${pk}$ baja "
                f"a ser su hijo {'izquierdo' if r2[0] == 'izquierda' else 'derecho'}. Los factores de "
                f"ese subárbol vuelven a estar entre $-1$ y $1$.")
            drop = (height(find(t, pk)), height(find(b["tree"], nr)))
            cur = nr

    for op, k in ex["ops"]:
        if op == "i":
            after, snaps = avl_insert_trace(root, k)
            s0 = snaps[0]
            t, path = s0["tree"], s0["path"]
            ns = {x: "hl" for x in path}
            ns[k] = "new"
            es = {(a, b): "path" for a, b in zip(path, path[1:] + [k])}
            if not path:
                txt = f"Insertar ${k}$: el árbol está vacío, ${k}$ es la raíz, con $fb = 0$."
            else:
                cmp_ = "; ".join(f"${k} {'<' if k < x else '>'} {x}$" for x in path)
                txt = (f"Insertar ${k}$ como en un ABB ({cmp_}): queda como hijo "
                       f"{'izquierdo' if k < path[-1] else 'derecho'} de ${path[-1]}$.")
                if len(snaps) == 1:
                    chain = _ancestors(t, k, t.key)
                    txt += (" Revisión de abajo hacia arriba: "
                            + ", ".join(f"${_fb(x, t)}$ ✓" for x in chain)
                            + ". Sigue siendo AVL, no hay que rotar.")
                else:
                    txt += (" Los factores que cambiaron están en el camino del nodo nuevo; "
                            "uno quedó en $\\pm 2$ (en rojo).")
            add(adraw(t, node_style=ns, edge_style=es, over=_rings(k), label_gap=LG, label_side="away"), txt)
            rebalance(snaps[1:], k)
        else:
            z = find(root, k)
            if z.left is not None and z.right is not None:
                sk = z.right
                path = [k]
                while sk is not None:
                    path.append(sk.key)
                    sk = sk.left
                sk = path[-1]
                es = {(a, b): "path" for a, b in zip(path, path[1:])}
                add(adraw(root, node_style={k: "bad", sk: "goal"}, edge_style=es,
                          under=lambda svg, pos: halo(svg, pos, z.right, "orange",
                                                      f"subárbol derecho de {k}"),
                          over=_rings(k, sk), label_gap=LG, label_side="away"),
                    f"Borrar ${k}$ como en un ABB. Tiene dos hijos: lo reemplaza su **sucesor**, el "
                    f"mínimo del subárbol derecho ({' → '.join(f'${x}$' for x in path)}): ${sk}$.")
            else:
                add(adraw(root, node_style={k: "bad"}, over=_rings(k), label_gap=LG, label_side="away"),
                    f"Borrar ${k}$ como en un ABB.")
            after, snaps = avl_delete_trace(root, k)
            s0 = snaps[0]
            st = s0["start"]
            moved = s0["succ"]
            ns = {st: "hl"}
            if moved is not None:
                ns[moved] = "new"
            add(adraw(s0["tree"], node_style=ns, over=_rings(st), label_gap=LG, label_side="away"),
                (f"${moved}$ sale de su lugar y su llave reemplaza a ${k}$. " if moved is not None
                 else "")
                + f"El nodo que salió físicamente colgaba de ${st}$: desde ahí se revisan los "
                  f"factores hacia la raíz. Ahora hay factores en $\\pm 2$ (en rojo).")
            rebalance(snaps[1:], st)
        root = after

    def over(svg, pos):
        ys = max(y for _, y in pos.values()) + 50
        x0 = min(x for x, _ in pos.values()) - 10
        draw_panel(svg, x0, ys, "Inorden:", [str(n.key) for n in nodes(root)], cell=30, wrap=12)
    assert all(abs(fb(n)) <= 1 for n in nodes(root))
    add(adraw(root, node_style={n.key: "goal" for n in nodes(root)}, over=over, label_gap=LG, label_side="away"),
        "**¿Es AVL?** Sí: todos los factores de balanceo están en $\\{-1, 0, 1\\}$. Y sigue siendo "
        "ABB: el inorden sale ordenado.")
    anim = ops_anim(p, f"{pref}-anim", ex["start"], ex["ops"], f"Animación del ejemplo {n}")
    return f"{head}\n\n{anim}\n\n" + steps("Paso a paso", tabs)


# Animaciones de los casos A–F con árboles concretos: inserción y eliminación
def _m(ks):
    return [100 - k for k in ks]


_CASOS = {
    ("A", "i"): ([20, 10, 30, 25, 40], ("i", 50)),
    ("A", "d"): ([20, 10, 30, 5, 25, 40, 45], ("d", 5)),
    ("B", "d"): ([20, 10, 30, 5, 25, 40, 22, 45], ("d", 5)),
    ("C", "i"): ([40, 20, 80, 10, 30, 60, 90, 50, 70, 95], ("i", 55)),
    ("C", "d"): ([20, 10, 30, 5, 25, 40, 22, 27], ("d", 5)),
}
for (_c, _o), (_ks, (_op, _k)) in list(_CASOS.items()):
    _CASOS[({"A": "D", "B": "E", "C": "F"}[_c], _o)] = (_m(_ks), (_op, 100 - _k))


def casos_anim(p, c):
    out = []
    for op in ("i", "d"):
        if (c, op) not in _CASOS:
            continue
        ks, (o, k) = _CASOS[(c, op)]
        t0 = bst_build(ks)
        assert all(abs(fb(n)) <= 1 for n in nodes(t0))
        _, sn = (avl_insert_trace if o == "i" else avl_delete_trace)(t0, k)
        rots = [s["case"] for s in sn if s["kind"] == "rotated"]
        assert rots == [c], (c, op, rots)
        verbo = "Insertar" if o == "i" else "Eliminar"
        out.append(f"**{verbo} ${k}$** (`AVL-{'INSERT' if o == 'i' else 'DELETE'}(T, {k})`):\n\n"
                   + ops_anim(p, f"caso{c}-{op}-anim", t0, [(o, k)],
                              f"Animación del caso {c}: {verbo.lower()} {k}"))
    return "\n\n".join(out)


# ¿Es AVL? Siete ejemplos: dos fáciles, tres medios y dos difíciles
def _l(k):
    return (k, None, None)


ES_AVL = [
    ("fácil", (20, _l(10), (30, None, _l(40)))),
    ("fácil", (30, (20, _l(10), None), None)),
    ("medio", (50, (30, _l(20), _l(40)), (70, None, (80, None, _l(90))))),
    ("medio", (50, (30, (20, _l(10), None), _l(40)), (70, _l(60), None))),
    ("medio", (40, (20, (10, _l(5), None), (30, _l(25), None)), _l(50))),
    ("difícil", (50, (30, _l(20), _l(60)), (70, _l(65), _l(80)))),
    ("difícil", None),     # AVL mínimo de altura 5 (árbol de Fibonacci)
]
ES_AVL_NOTAS = [
    "Cada nodo tiene $|fb| \\le 1$; $30$ tiene un solo hijo y eso está permitido.",
    "Una cadena de tres nodos: la raíz tiene $fb(30) = 0 - 2 = -2$.",
    "La raíz está bien ($fb(50) = 3 - 2 = +1$), pero $70$ no: su lado derecho mide $2$ y el izquierdo $0$. "
    "No basta mirar la raíz.",
    "Se ve cargado a la izquierda, pero ningún nodo pasa de $1$: $fb(50) = 2 - 3 = -1$. Sí es AVL.",
    "Todos los nodos están bien **menos la raíz**: $fb(40) = 1 - 3 = -2$. Hay que revisar cada nodo.",
    "Los factores están perfectos, pero $60$ está en el subárbol **izquierdo** de $50$: no es ABB, y un "
    "AVL ante todo es un ABB.",
    "Es el AVL con **menos nodos** posibles para su altura ($5$ niveles con $12$ nodos): en cada nodo, el "
    "lado izquierdo es exactamente $1$ más alto que el derecho. Parece desbalanceado, pero todos los "
    "factores son $0$ o $-1$.",
]


def es_avl(p):
    out = []
    for i, ((nivel, tup), nota) in enumerate(zip(ES_AVL, ES_AVL_NOTAS), 1):
        t = from_tuple(tup) if tup is not None else fib_tree(5, iter(range(5, 61, 5)))
        frames, bst, bal, labels, ls, badk = check_frames(t)
        q = f"![Árbol del ejemplo {i}]({p.img(f'esavl{i}', draw(t))})"
        anim = anim_block(p, f"esavl{i}-anim", frames, f"Animación: ¿es AVL? (ejemplo {i})")
        verd = "**Sí es AVL.**" if bst and bal else "**No es AVL.**"
        out.append(f"**Ejemplo {i}.** ¿Es AVL?\n\n{q}\n\n:::{{admonition}} Respuesta\n"
                   f":class: dropdown\n{anim}\n\n{verd} {nota}\n:::")
    return "\n\n".join(out)


# Diagramas esquemáticos de los casos (nodos con su fb y subárboles como triángulos)
def N_(name, fbv, left, right, st="plain"):
    return ("n", name, fbv, left, right, st)


def T_(name, hlab, units=1.0, st="plain"):
    return ("t", name, hlab, units, st)


def _w(s):
    if s[0] == "t":
        return 44 + 12 * s[3]
    return _w(s[3]) + _w(s[4]) + 8


def _place(s, x0, y, out):
    if s[0] == "t":
        w = _w(s)
        out.append((s, x0 + w / 2, y))
        return x0 + w / 2
    xl = _place(s[3], x0, y + 50, out)
    xr = _place(s[4], x0 + _w(s[3]) + 8, y + 50, out)
    x = (xl + xr) / 2
    out.append((s, x, y))
    s_children = (xl, xr)
    out.append(("edge", (x, y), (xl, y + 50), s[3][0]))
    out.append(("edge", (x, y), (xr, y + 50), s[4][0]))
    return x


def schem(svg, spec, x0, y0=0):
    items = []
    _place(spec, x0, y0, items)
    for it in items:
        if it[0] == "edge":
            (x1, y1), (x2, y2), kind = it[1], it[2], it[3]
            r = 15
            x1s, y1s = x1 + (x2 - x1) * r / max(1, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5), \
                y1 + (y2 - y1) * r / max(1, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            if kind == "n":
                d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                x2s, y2s = x2 - (x2 - x1) * r / d, y2 - (y2 - y1) * r / d
            else:
                x2s, y2s = x2, y2
            svg.line(x1s, y1s, x2s, y2s, PAL["ink"], 1.2)
    for it in items:
        if it[0] == "edge":
            continue
        s, x, y = it
        if s[0] == "t":
            _, name, hlab, units, st = s
            hgt = 34 + 26 * units
            hw = 16 + 8 * units
            col = PAL["new"] if st == "new" else PAL["ink"]
            fill = "#ffe3e3" if st == "new" else PAL["white"]
            svg.polygon([(x, y), (x - hw, y + hgt), (x + hw, y + hgt)], fill, col, 1.2)
            svg.text(x, y + hgt - 9, name, 14, col)
            if hlab:
                svg.text(x + hw + 3, y + hgt, hlab, 13, PAL["teal"], anchor="start")
        else:
            _, name, fbv, _, _, st = s
            bad = fbv in ("+2", "−2", "2", "-2")
            fill = "#ffd9d9" if bad else ("#fff2b3" if st == "hl" else PAL["white"])
            stroke = PAL["new"] if (bad or st == "hl") else PAL["ink"]
            svg.circle(x, y, 15, fill, stroke, 2.0 if (bad or st == "hl") else 1.3)
            svg.text(x, y + 4.5, fbv, 12 if len(fbv) <= 2 else 10, PAL["new"] if bad else PAL["ink"],
                     bold=bad)
            svg.text(x + 19, y - 9, name, 15, PAL["ink"], anchor="start", italic=True)
    return x0 + _w(spec)


def schem_row(p, name, panels, ops, alt):
    """panels: especificaciones; ops: texto de la flecha entre panel i e i+1.
    Cada flecha va pegada al panel que sigue, así una fila nueva empieza con su flecha."""
    parts = []
    for i, spec in enumerate(panels):
        svg = SVG()
        x = 0
        if i > 0:
            ax1 = max(96, text_width(ops[i - 1], 13) + 16)
            svg.line(0, 40, ax1 - 4, 40, PAL["new"], 1.6, marker="arr-new")
            svg.text(ax1 / 2, 32, ops[i - 1], 13, PAL["new"])
            x = ax1 + 18
        schem(svg, spec, x)
        parts.append(svg)
    return f"![{alt}]({p.img(name, tile(parts, 14, max_w=720))})"


def build():
    p = Page("Unidad4-EstructurasRecursivas/ArbolesAVL")

    deg = bst_build([1, 2, 3, 4, 5, 6, 7])
    p.put("fig-cadena", f"![Cadena]({p.img('cadena', draw(deg, dx=34))})")
    p.put("anim-cadena", cadena_anim(p))
    full = bst_build([4, 2, 6, 1, 3, 5, 7])
    p.put("fig-lleno", f"![ABB de altura 3]({p.img('lleno', draw(full))})")

    # Factor de balanceo paso a paso (árbol AVL de Vargas), de abajo hacia arriba
    vv = from_tuple((20, (15, (5, None, None), (18, (16, None, None), (19, None, None))),
                     (30, (25, None, None), (35, None, None))))

    def post(n):
        return [] if n is None else post(n.left) + post(n.right) + [n]
    done = {}
    tabs = []
    for i, n in enumerate(post(vv)):
        hl_, hr = height(n.left), height(n.right)
        done[n.key] = f"h={height(n)}, fb={fbtxt(hr - hl_)}"
        ns = {k: "tree" for k in done}
        ns[n.key] = "hl"
        svg = draw(vv, node_style=ns, labels=dict(done),
                   label_style={k: ("new" if k == n.key else None) for k in done}, dx=58)
        if n.left is None and n.right is None:
            txt = (f"> ${n.key}$ es hoja: sus dos subárboles son vacíos (altura $0$). "
                   f"$h = 1$ y $fb = 0 - 0 = 0$.")
        else:
            txt = (f"> ${n.key}$: el subárbol derecho tiene altura ${hr}$ y el izquierdo ${hl_}$. "
                   f"$h = 1 + \\max({hl_}, {hr}) = {height(n)}$ y $fb = {hr} - {hl_} = "
                   f"{fbtxt(hr - hl_)}$.")
        tabs.append(f"![Factor de balanceo, paso {i + 1}]({p.img(f'fb-{i:02d}', svg)})\n\n{txt}")
    p.put("fb-steps", steps("Altura (h) y factor de balanceo (fb) de cada nodo", tabs))
    p.put("anim-fb", fb_anim(p, vv))

    # ¿Es AVL?
    cands = [
        (8, (4, (2, None, None), (6, None, None)), (10, None, (12, None, None))),
        (8, (4, (2, (1, None, None), None), (6, None, None)), (10, None, None)),
        (8, (4, (2, (1, None, None), (3, None, None)), (6, None, None)), (10, (9, None, None), None)),
        (8, (4, None, None), (12, (10, None, None), (14, None, (16, None, None)))),
    ]

    def row(name, trees, caps, f):
        return p.img(name, tile([f(t) for t in trees], 50, caps=caps))
    trees = [from_tuple(t) for t in cands]
    caps = ["a)", "b)", "c)", "d)"]
    p.put("fig-es", f"![Cuatro ABB]({row('es', trees, caps, lambda t: draw(t, dx=34))})")
    p.put("fig-es-sol", f"![Cuatro ABB con su fb]({row('es-sol', trees, caps, lambda t: adraw(t, dx=40))})")
    p.put("es-avl", es_avl(p))

    # Daño al balanceo: al insertar y al eliminar
    t_ins = bst_build([4, 6, 7])
    t_del = bst_build([6, 8, 9])
    p.put("fig-dano", f"![Desbalanceo]({row('dano', [t_ins, t_del], ['Insertar 7 en 4, 6', 'Eliminar 4 de 6, 4, 8, 9'], lambda t: adraw(t, node_style={t.key: 'bad'}))})")

    # Rotación simple
    ch = bst_build([4, 6, 7])
    rt = rot_left(copy_tree(ch))
    tabs = [f"![Cadena 4, 6, 7]({p.img('rs-0', adraw(ch, node_style={4: 'bad'}))})\n\n> $fb(4) = 2 - 0 = +2$: "
            f"el subárbol derecho de $4$ es mucho más alto. Hay que «subir» a $6$.",
            f"![Después de rotar]({p.img('rs-1', adraw(rt, node_style={6: 'new'}))})\n\n> `LEFT-ROTATE(4)`: "
            f"$6$ sube a la raíz y $4$ baja a ser su hijo izquierdo. Todos los factores son $0$, "
            f"y el inorden sigue siendo $4, 6, 7$."]
    p.put("rot-simple", steps("Rotar a la izquierda en 4", tabs, dropdown=False))

    # Rotaciones genéricas
    before = N_("x", "", T_("α", ""), N_("y", "", T_("β", "", st="new"), T_("γ", "")))
    after = N_("y", "", N_("x", "", T_("α", ""), T_("β", "", st="new")), T_("γ", ""))
    svg = SVG()
    x = schem(svg, before, 0)
    ax0, ax1 = x + 20, x + 170
    svg.line(ax0, 30, ax1 - 4, 30, PAL["new"], 1.6, marker="arr-new")
    svg.text((ax0 + ax1) / 2, 22, "LEFT-ROTATE(x)", 13, PAL["new"])
    svg.line(ax1, 62, ax0 + 4, 62, PAL["new"], 1.6, marker="arr-new")
    svg.text((ax0 + ax1) / 2, 82, "RIGHT-ROTATE(y)", 13, PAL["new"])
    schem(svg, after, ax1 + 20)
    p.put("fig-rot", f"![Rotaciones]({p.img('rot', svg)})")
    p.put("rot-anim", rotation_anim(p))

    # Casos A–F
    h, h1 = "h", "h + 1"
    A = [N_("p", "+2", T_("A", h), N_("q", "+1", T_("B", h), T_("C", h1, 1.6))),
         N_("q", "0", N_("p", "0", T_("A", h), T_("B", h)), T_("C", h1, 1.6))]
    B = [N_("p", "+2", T_("A", h), N_("q", "0", T_("B", h1, 1.6), T_("C", h1, 1.6))),
         N_("q", "−1", N_("p", "+1", T_("A", h), T_("B", h1, 1.6)), T_("C", h1, 1.6))]
    C = [N_("p", "+2", T_("A", h), N_("q", "−1", N_("r", "", T_("D", "", 0.4), T_("E", "", 0.4)), T_("C", h))),
         N_("p", "+2", T_("A", h), N_("r", "", T_("D", "", 0.4), N_("q", "", T_("E", "", 0.4), T_("C", h)))),
         N_("r", "0", N_("p", "−1/0", T_("A", h), T_("D", "", 0.4)), N_("q", "0/+1", T_("E", "", 0.4), T_("C", h)))]
    Cfail = [C[0], N_("q", "−2", N_("p", "+1", T_("A", h), N_("r", "", T_("D", "", 0.4), T_("E", "", 0.4))), T_("C", h))]
    D = [N_("p", "−2", N_("q", "−1", T_("C", h1, 1.6), T_("B", h)), T_("A", h)),
         N_("q", "0", T_("C", h1, 1.6), N_("p", "0", T_("B", h), T_("A", h)))]
    E = [N_("p", "−2", N_("q", "0", T_("C", h1, 1.6), T_("B", h1, 1.6)), T_("A", h)),
         N_("q", "+1", T_("C", h1, 1.6), N_("p", "−1", T_("B", h1, 1.6), T_("A", h)))]
    F = [N_("p", "−2", N_("q", "+1", T_("C", h), N_("r", "", T_("E", "", 0.4), T_("D", "", 0.4))), T_("A", h)),
         N_("p", "−2", N_("r", "", N_("q", "", T_("C", h), T_("E", "", 0.4)), T_("D", "", 0.4)), T_("A", h)),
         N_("r", "0", N_("q", "0/−1", T_("C", h), T_("E", "", 0.4)), N_("p", "+1/0", T_("D", "", 0.4), T_("A", h)))]
    p.put("caso-A", schem_row(p, "caso-A", A, ["LEFT-ROTATE(p)"], "Caso A"))
    p.put("caso-B", schem_row(p, "caso-B", B, ["LEFT-ROTATE(p)"], "Caso B"))
    p.put("caso-C", schem_row(p, "caso-C", C, ["RIGHT-ROTATE(q)", "LEFT-ROTATE(p)"], "Caso C"))
    p.put("anim-C-falla", c_falla_anim(p))
    p.put("caso-C-falla", schem_row(p, "caso-C-falla", Cfail, ["LEFT-ROTATE(p)"], "Caso C: una sola rotación no basta"))
    p.put("caso-D", schem_row(p, "caso-D", D, ["RIGHT-ROTATE(p)"], "Caso D"))
    p.put("caso-E", schem_row(p, "caso-E", E, ["RIGHT-ROTATE(p)"], "Caso E"))
    p.put("caso-F", schem_row(p, "caso-F", F, ["LEFT-ROTATE(q)", "RIGHT-ROTATE(p)"], "Caso F"))

    # Ejemplos mínimos de cada caso (diapositivas de Aristizábal)
    ejemplos = {
        "A": (bst_build([4, 6]), [("i", 7)]),
        "B": (bst_build([6, 4, 8, 7, 9]), [("d", 4)]),
        "C": (bst_build([4, 6]), [("i", 5)]),
        "D": (bst_build([6, 3]), [("i", 1)]),
        "E": (bst_build([6, 4, 8, 3, 5]), [("d", 8)]),
        "F": (bst_build([6, 3]), [("i", 4)]),
    }
    for c, (t0, ops) in ejemplos.items():
        tabs = [f"![T]({p.img(f'ej{c}-T', adraw(t0))})\n\n> El árbol $T$, con el factor de "
                f"balanceo junto a cada nodo."]
        st, _ = avl_tabs(p, f"ej{c}", ops, start=t0)
        op, k = ops[0]
        p.put(f"ej-{c}", steps(f"AVL-{'INSERT' if op == 'i' else 'DELETE'}(T, {k})", tabs + st))
    for c in "ABCDEF":
        p.put(f"anim-{c}", casos_anim(p, c))

    # Ejemplo 1: 1..7
    st, _ = avl_tabs(p, "ej1", [("i", k) for k in range(1, 8)])
    p.put("ej1", ops_anim(p, "ej1-anim", None, [("i", k) for k in range(1, 8)],
                          "Animación: insertar 1, 2, 3, 4, 5, 6, 7") + "\n\n"
          + steps("Insertar 1, 2, 3, 4, 5, 6, 7", st))

    # Ejemplo 2: insertar 25 (caso F)
    base = None
    for k in [50, 20, 70, 10, 30]:
        base = avl_insert(base, k)
    p.put("fig-ej2-base", f"![AVL inicial]({p.img('ej2-base', adraw(base))})")
    st, _ = avl_tabs(p, "ej2", [("i", 25)], start=base)
    p.put("ej2", ops_anim(p, "ej2-anim", base, [("i", 25)], "Animación: AVL-INSERT(T, 25)") + "\n\n"
          + steps("AVL-INSERT(T, 25)", st))

    # Ejemplo 3: eliminación con dos rebalanceos
    base3 = bst_build([5, 2, 1, 3, 4, 8, 7, 6, 11, 9, 10, 12])
    p.put("fig-ej3-base", f"![AVL inicial]({p.img('ej3-base', adraw(base3))})")
    st, after3 = avl_tabs(p, "ej3", [("d", 1)], start=base3)
    st[-1] += ("\n\n> El primer rebalanceo bajó la altura del subárbol de $2$ de $3$ a $2$, y eso "
               "desbalanceó a la raíz: por eso hizo falta un **segundo** rebalanceo.")
    p.put("ej3", ops_anim(p, "ej3-anim", base3, [("d", 1)], "Animación: AVL-DELETE(T, 1)") + "\n\n"
          + steps("AVL-DELETE(T, 1)", st))

    for i, ex in enumerate(EJEMPLOS, 1):
        p.put(f"ejx{i}", ejemplo_avl(p, i, ex))
    p.assemble("index.md")

    # Ejercicios
    # 1. Placas (Aristizábal): compras e insertar, ventas y eliminar
    placas = [("i", "JOK458"), ("i", "PZY526"), ("i", "NOB512"), ("i", "AZX323"), ("i", "BMO419"),
              ("d", "PZY526"), ("i", "ENN422"), ("d", "AZX323"), ("i", "GIC437"), ("d", "NOB512")]
    nombres = {"JOK458": "Ford Focus", "PZY526": "Honda Civic", "NOB512": "Mazda 3",
               "AZX323": "Renault Clio", "BMO419": "Toyota Prius", "ENN422": "Mitsubishi Montero",
               "GIC437": "Audi A4"}
    root = None
    tabs = []
    resumen = []
    for i, (op, k) in enumerate(placas, 1):
        if op == "i":
            root, sn = avl_insert_trace(root, k)
        else:
            root, sn = avl_delete_trace(root, k)
        rots = [s for s in sn if s["kind"] == "rotated"]
        cases = ", ".join(f"caso {s['case']} en {s['key']}" for s in rots) or "sin rotaciones"
        verbo = "Se compra" if op == "i" else "Se vende"
        svg = adraw(root, node_style={k: "new"} if op == "i" else {}, dx=64, r=30, font=11) if root else draw(None)
        tabs.append(f"![Paso {i}]({p.img(f'placas-{i:02d}', svg)})\n\n> {i}. {verbo} el "
                    f"{nombres[k]} ({k}): {cases}.")
        resumen.append(f"{i}. {cases}")
    p.put("placas", steps("Estado del árbol después de cada operación", tabs, dropdown=False))

    # 2. Las cuatro eliminaciones restantes de Aristizábal
    dels = [("a", bst_build([6, 4, 8, 9]), 4), ("b", bst_build([6, 4, 8, 7]), 4),
            ("c", bst_build([6, 4, 8, 3]), 8), ("d", bst_build([6, 4, 8, 5]), 8)]
    figs, sols = [], []
    for lab, t0, k in dels:
        figs.append(t0)
        after, sn = avl_delete_trace(t0, k)
        rots = [s for s in sn if s["kind"] == "rotated"]
        sols.append(f"- {lab}) Caso {rots[0]['case']}: preorden final ${', '.join(map(str, pre(after)))}$.")
    p.put("fig-ex2", f"![Cuatro árboles]({row('ex2', figs, ['a) borrar 4', 'b) borrar 4', 'c) borrar 8', 'd) borrar 8'], lambda t: adraw(t, dx=38))})")
    p.put("ex2-sol", "\n".join(sols))

    # 3 y 4. Secuencias de inserción
    for key, seq in (("ex3", [10, 20, 30, 40, 50, 25]), ("ex4", [15, 20, 24, 10, 13, 7, 30, 36, 25])):
        r = None
        cases = []
        for k in seq:
            r, sn = avl_insert_trace(r, k)
            for s in sn:
                if s["kind"] == "rotated":
                    cases.append(f"al insertar ${k}$, caso {s['case']} en ${s['key']}$")
        p.put(f"{key}-sol", f"![Resultado]({p.img(f'{key}-sol', adraw(r))})")
        p.put(f"{key}-casos", "; ".join(cases))

    # 5. Eliminación con sucesor y dos rebalanceos
    base5 = bst_build([8, 5, 2, 1, 3, 4, 7, 6, 10, 9, 12, 11])
    p.put("fig-ex5", f"![AVL]({p.img('ex5', adraw(base5))})")
    after5, sn = avl_delete_trace(base5, 8)
    rots = [s for s in sn if s["kind"] == "rotated"]
    assert [s["case"] for s in rots] == ["C", "D"]
    p.put("ex5-casos", ", luego ".join(f"caso {s['case']} en ${s['key']}$" for s in rots))
    p.put("ex5-sol", f"![Resultado]({p.img('ex5-sol', adraw(after5))})")

    # 6. ¿Es AVL? (Vargas)
    p.put("fig-ex6", f"![Árbol]({p.img('ex6', draw(vv))})")
    p.put("ex6-sol", f"![Con fb]({p.img('ex6-sol', adraw(vv))})")
    p.assemble("exercises.md")


if __name__ == "__main__":
    build()
