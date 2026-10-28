"""Montículos (heaps): qué es uno, cómo reconocerlo y las operaciones de cola de prioridad.

No incluye HEAPIFY, BUILD-HEAP ni HEAPSORT (están en la Unidad 3): solo el concepto y
HEAP-MAXIMUM, MAX-HEAP-INSERT, HEAP-INCREASE-KEY y HEAP-EXTRACT-MAX.
"""
from common import *
from anim import Frame, still, anim_block

DX, DY, CW, CH = 44, 58, 36, 30


class G:
    """Geometría fija de una animación: alto del árbol y largo del arreglo dibujado debajo."""

    def __init__(self, maxidx, L=0, dx=DX, dy=DY):
        self.H = max(1, maxidx.bit_length())
        self.dx, self.dy, self.L = dx, dy, L
        self.tw = 2 ** (self.H - 1) * dx
        self.ax = self.tw / 2 - L * CW / 2
        self.ay = (self.H - 1) * dy + 52

    def xy(self, i):
        d = i.bit_length() - 1
        span = self.tw / 2 ** d
        return (i - 2 ** d + 0.5) * span, d * self.dy

    def cell(self, i):
        return self.ax + (i - 1) * CW, self.ay

    def cell_c(self, i):
        x, y = self.cell(i)
        return x + CW / 2, y + CH / 2

    def static(self):
        if not self.L:
            return []
        out = [(self.ax - 16, self.ay + CH / 2 + 5, "A", 15, PAL["ink"], "middle", True)]
        for i in range(1, self.L + 1):
            x, _ = self.cell_c(i)
            out.append((x, self.ay + CH + 15, str(i), 11, PAL["muted"], "middle", False))
        return out


def hframe(g, cap, tree, vals, arr=None, size=None, ns=None, es=None, cs=None, idx=False,
           rings=(), ghosts=(), fly_t=None, fly_a=None, aside=None, hold=None):
    """Un cuadro: tree = {posición: id}, arr = ids de A[1..L] (None = casilla vacía).
    fly_t / fly_a: {id: (x, y)} para dibujar ese nodo / esa casilla oculta en otro lugar, de
    donde sale volando en el cuadro siguiente. aside: {id: (x, y, rótulo)}, nodos fuera del
    montículo (el máximo extraído)."""
    fr = Frame(cap, hold)
    ns, es, cs, fly_t, fly_a = ns or {}, es or {}, cs or {}, fly_t or {}, fly_a or {}
    def side(i):
        # las hojas llevan el índice debajo, donde no llega ninguna arista
        if all(c not in tree and c not in ghosts for c in (2 * i, 2 * i + 1)):
            return "below"
        return "left" if i % 2 == 0 else "right"
    for i, e in tree.items():
        x, y = fly_t.get(e, g.xy(i))
        fr.node(f"t{e}", x, y, vals[e], ns.get(e, "plain"), label=str(i) if idx else "",
                lstyle="idx", lside=side(i), ring=e in rings, hidden=e in fly_t)
        if i > 1 and i // 2 in tree:
            fr.edge(f"t{e}", f"t{tree[i // 2]}", es.get(e, "plain"))
    for i in ghosts:
        x, y = g.xy(i)
        fr.node(f"g{i}", x, y, "?", shape="ghost", label=str(i), lstyle="bad", lside="below")
        if i // 2 in tree:
            fr.edge(f"g{i}", f"t{tree[i // 2]}", "bad")
    for e, (x, y, lab) in (aside or {}).items():
        fr.node(f"t{e}", x, y, vals[e], "goal", label=lab, lstyle="goal", lside="above")
    if arr is not None:
        size = len([a for a in arr if a is not None]) if size is None else size
        for i in range(1, g.L + 1):
            x, y = g.cell(i)
            fr.cell(f"s{i}", x, y, CW, CH, "", "slot" if i <= size else "slot-out")
        for i, e in enumerate(arr, 1):
            if e is None:
                continue
            if e in fly_a:
                x, y = fly_a[e]
                x, y = x - CW / 2, y - CH / 2
            else:
                x, y = g.cell(i)
            fr.cell(f"a{e}", x + 3, y + 3, CW - 6, CH - 6, vals[e],
                    cs.get(e, "plain" if i <= size else "dim"), hidden=e in fly_a)
    return fr


def angle(vs):
    return "⟨" + ", ".join(str(v) for v in vs) + "⟩"


def lang(vs):
    return r"\langle " + ", ".join(str(v) for v in vs) + r" \rangle"


# Montículo con elementos identificados, para que cada valor se deslice al intercambiarse
class Heap:
    def __init__(self, values, L=None):
        self.vals, self.A = {}, [None]
        self.next = 0
        for v in values:
            self.A.append(self.new(v))
        self.size = len(values)
        self.L = L or len(values)

    def new(self, v):
        self.next += 1
        self.vals[self.next] = v
        return self.next

    def v(self, i):
        return self.vals[self.A[i]]

    def values(self):
        return [self.v(i) for i in range(1, self.size + 1)]

    def tree(self):
        return {i: self.A[i] for i in range(1, self.size + 1)}

    def arr(self):
        a = self.A[1:] + [None] * (self.L - (len(self.A) - 1))
        return a[:self.L]

    def fr(self, g, cap, **kw):
        return hframe(g, cap, self.tree(), self.vals, self.arr(), self.size, **kw)


def is_max_heap(vals):
    """vals: {posición: llave}. Devuelve (forma, orden, huecos, fallas de orden)."""
    n = max(vals)
    holes = [i for i in range(1, n) if i not in vals]
    bad = [(i // 2, i) for i in sorted(vals) if i > 1 and i // 2 in vals and vals[i // 2] < vals[i]]
    return not holes, not bad, holes, bad


# Operaciones (cada una agrega sus cuadros a 'frames')
def _sift_up(h, g, i, e, frames, kw):
    key = h.vals[e]
    pre = ""
    while True:
        if i == 1:
            frames.append(h.fr(g, pre + f"i = 1: {key} llegó a la raíz. Termina.",
                               ns={e: "new"}, cs={e: "new"}, **kw))
            return
        p = i // 2
        pv = h.v(p)
        if pv < key:
            frames.append(h.fr(g, pre + f"i = {i}: A[PARENT({i})] = A[{p}] = {pv} < {key}: se "
                               f"intercambian A[{i}] y A[{p}].",
                               ns={e: "new", h.A[p]: "hl"}, cs={e: "new", h.A[p]: "hl"},
                               es={e: "bad"}, **kw))
            h.A[i], h.A[p] = h.A[p], h.A[i]
            i = p
            pre = f"{key} subió a A[{p}]. "
        else:
            frames.append(h.fr(g, pre + f"i = {i}: A[PARENT({i})] = A[{p}] = {pv} ≥ {key}: el "
                               f"orden se cumple. Termina.",
                               ns={e: "new", h.A[p]: "goal"}, cs={e: "new"}, es={e: "good"}, **kw))
            return


def op_insert(h, g, key, frames, kw=None):
    kw = kw or {}
    n = h.size
    e = h.new(key)
    if len(h.A) <= n + 1:
        h.A.append(e)
    else:
        h.A[n + 1] = e
    h.size += 1
    where = ("es la raíz" if n == 0 else
             f"queda como hijo {'izquierdo' if (n + 1) % 2 == 0 else 'derecho'} de A[{(n + 1) // 2}] = "
             f"{h.v((n + 1) // 2)}")
    frames.append(h.fr(g, f"MAX-HEAP-INSERT(A, {key}): heap-size[A] pasa de {n} a {n + 1} y {key} "
                       f"entra en A[{n + 1}], la siguiente posición libre: {where}.",
                       ns={e: "new"}, cs={e: "new"}, rings={e}, **kw))
    _sift_up(h, g, n + 1, e, frames, kw)
    return e


def op_increase(h, g, i, key, frames, kw=None):
    kw = kw or {}
    old_e = h.A[i]
    old = h.vals[old_e]
    frames.append(h.fr(g, f"HEAP-INCREASE-KEY(A, {i}, {key}): A[{i}] = {old}.",
                       ns={old_e: "hl"}, cs={old_e: "hl"}, rings={old_e}, **kw))
    e = h.new(key)
    h.A[i] = e
    frames.append(h.fr(g, f"{key} ≥ {old}, no hay error: A[{i}] ← {key}. Ahora A[{i}] puede ser "
                       f"mayor que su padre: se sube mientras lo sea.",
                       ns={e: "new"}, cs={e: "new"}, rings={e}, **kw))
    _sift_up(h, g, i, e, frames, kw)
    return e


def op_extract(h, g, frames, kw=None):
    kw = dict(kw or {})
    n = h.size
    emax = h.A[1]
    mx = h.vals[emax]
    side = (g.tw + 30, 0, "max")
    frames.append(h.fr(g, f"HEAP-EXTRACT-MAX(A): max ← A[1] = {mx}, el mayor de todo el montículo.",
                       ns={emax: "goal"}, cs={emax: "goal"}, rings={emax}, **kw))
    aside = {emax: side}
    h.A[1] = None
    tree = {i: h.A[i] for i in range(2, n + 1)}
    arr = h.arr()
    frames.append(hframe(g, f"El máximo {mx} sale del montículo; la raíz queda vacía.", tree, h.vals,
                         arr, n, aside=aside, **kw))
    last = h.A[n]
    lv = h.vals[last]
    h.A[1], h.A[n] = last, None
    h.size = n - 1
    kw["aside"] = aside
    if h.size == 0:
        frames.append(h.fr(g, f"El montículo quedó vacío. return {mx}.", **kw))
        return mx
    frames.append(h.fr(g, f"A[1] ← A[{n}] = {lv}: el último elemento sube a la raíz y heap-size[A] "
                       f"pasa a {n - 1}. La forma se conserva, pero en la raíz el orden puede fallar.",
                       ns={last: "new"}, cs={last: "new"}, rings={last}, **kw))
    i = 1
    pre = ""
    while True:
        kids = [c for c in (2 * i, 2 * i + 1) if c <= h.size]
        v = h.v(i)
        if not kids:
            frames.append(h.fr(g, pre + f"A[{i}] = {v} no tiene hijos dentro del montículo. Termina.",
                               ns={last: "new"}, cs={last: "new"}, **kw))
            break
        m = max([i] + kids, key=lambda j: h.v(j))
        cmp_ = ", ".join(f"A[{j}] = {h.v(j)}" for j in [i] + kids)
        if m == i:
            frames.append(h.fr(g, pre + f"i = {i}: el mayor entre {cmp_} es A[{i}] mismo: {v} ≥ sus "
                               f"hijos. Termina.", ns={last: "new", **{h.A[c]: "goal" for c in kids}},
                               cs={last: "new"}, es={h.A[c]: "good" for c in kids}, **kw))
            break
        frames.append(h.fr(g, pre + f"i = {i}: el mayor entre {cmp_} es A[{m}] = {h.v(m)}: se "
                           f"intercambian A[{i}] y A[{m}].",
                           ns={last: "new", h.A[m]: "hl"}, cs={last: "new", h.A[m]: "hl"},
                           es={h.A[m]: "bad"}, **kw))
        h.A[i], h.A[m] = h.A[m], h.A[i]
        i = m
        pre = f"{v} bajó a A[{m}]. "
    return mx


def final_frame(h, g, cap, kw=None):
    return h.fr(g, cap, ns={e: "goal" for e in h.tree().values()}, **(kw or {}))


def tabs_of(p, name, frames, g, alt):
    """Pestañas «Paso 1, 2, ...» con los mismos cuadros de la animación, quietos."""
    tabs = []
    for i, f in enumerate(frames):
        path = p.img(f"{name}-{i + 1:02d}", still(f, g.static()))
        tabs.append(f"![{alt}, paso {i + 1}]({path})\n\n> {f.caption}")
    return tabs


def anim_and_tabs(p, name, frames, g, title, alt):
    a = anim_block(p, f"{name}-anim", frames, f"Animación: {alt}", g.static())
    return a + "\n\n" + steps(title, tabs_of(p, name, frames, g, alt))


# ¿Es un montículo?
def check_frames(tree_vals=None, array=None, size=None, length=None):
    """Cuadros de la revisión de forma y orden. Con array, primero se arma el árbol desde el
    arreglo; con tree_vals y si resulta montículo, al final se pasa al arreglo."""
    frames = []
    if array is not None:
        L = length or len(array)
        size = size or len(array)
        vals = {i: v for i, v in enumerate(array, 1)}
        g = G(size, L)
        arr = list(range(1, len(array) + 1))
        out = (f" Solo A[1..{size}] forman el montículo; A[{size + 1}..{len(array)}] "
               f"({', '.join(str(v) for v in array[size:])}) quedan por fuera."
               if size < len(array) else "")
        lv = 0
        while 2 ** lv <= size:
            lv += 1
        # cuadro 0: solo el arreglo; la raíz espera, oculta, sobre A[1]
        frames.append(hframe(g, f"A = {angle(array)}, heap-size[A] = {size}, length[A] = {L}." + out,
                             {1: 1}, vals, arr, size, fly_t={1: g.cell_c(1)}))
        for d in range(lv):
            lo, hi = 2 ** d, min(2 ** (d + 1) - 1, size)
            shown = {i: i for i in range(1, hi + 1)}
            nxt = {i: g.cell_c(i) for i in range(hi + 1, min(2 * hi + 1, size) + 1)}
            shown.update({i: i for i in nxt})
            now = {i: "hl" for i in range(lo, hi + 1)}
            if d == 0:
                cap = f"A[1] = {vals[1]} es la raíz."
            else:
                cap = (f"Nivel {d}: A[{lo}..{hi}] son los hijos de A[{lo // 2}..{hi // 2}]: los hijos de "
                       f"A[i] están en A[2i] y A[2i + 1].")
            frames.append(hframe(g, cap, shown, vals, arr, size, ns=now, cs=now, fly_t=nxt))
        tree = {i: i for i in range(1, size + 1)}
        kw = dict(arr=arr, size=size)
    else:
        vals = dict(tree_vals)
        tree = {i: i for i in vals}
        forma, orden, _, _ = is_max_heap(vals)
        L = len(vals) if (forma and orden) else 0
        g = G(max(vals), L)
        frames.append(hframe(g, "¿Es un max-heap? Se revisan las dos propiedades: primero la forma y "
                             "luego el orden.", tree, vals))
        kw = {}
    tv = {i: vals[i] for i in tree}
    forma, orden, holes, bad = is_max_heap(tv)
    n = len(tree)
    ghosts = [h for h in holes if h // 2 in tree]
    if forma:
        cap = (f"Forma ✓: numerando por niveles, de izquierda a derecha, los {n} nodos ocupan las "
               f"posiciones 1 a {n}, sin huecos.")
    else:
        mayores = sorted(i for i in tree if i > holes[0])
        cap = (f"Forma ✗: la posición {holes[0]} está vacía, pero hay nodos en posiciones mayores "
               f"({', '.join(map(str, mayores))}). Los nodos no ocupan las posiciones 1 a {n} sin huecos.")
    frames.append(hframe(g, cap, tree, vals, idx=True, ghosts=ghosts, **kw))
    ns, es = {}, {}
    for i in sorted(tree):
        kids = [c for c in (2 * i, 2 * i + 1) if c in tree]
        if not kids:
            continue
        cur = dict(ns)
        cur[i] = "hl"
        for c in kids:
            es[c] = "good" if vals[i] >= vals[c] else "bad"
            if vals[i] < vals[c]:
                cur[c] = "bad"
        cmp_ = " y ".join(f"{vals[i]} {'≥' if vals[i] >= vals[c] else '<'} {vals[c]}" for c in kids)
        ok = all(vals[i] >= vals[c] for c in kids)
        quien = "sus hijos" if len(kids) == 2 else "su hijo"
        cap = (f"Orden, A[{i}] = {vals[i]} contra {quien}: {cmp_} " + ("✓" if ok else
               "✗: la raíz de este subárbol no es la mayor."))
        frames.append(hframe(g, cap, tree, vals, idx=True, ghosts=ghosts, ns=cur, es=dict(es), **kw))
        ns[i] = "goal" if ok else "bad"
        for c in kids:
            if vals[i] < vals[c]:
                ns[c] = "bad"
    if forma and orden:
        verdict = "Sí es un max-heap: cumple la propiedad de forma y la de orden."
        fin = {i: "goal" for i in tree}
    else:
        falla = " y ".join(x for x, okx in (("la forma", forma), ("el orden", orden)) if not okx)
        verdict = f"No es un montículo: falla {falla}."
        fin = {i: ns.get(i, "plain") for i in tree}
        fin = {i: ("bad" if s == "bad" else "plain") for i, s in fin.items()}
    if array is None and forma and orden:
        fa = {i: g.xy(i) for i in tree}
        frames.append(hframe(g, verdict, tree, vals, list(range(1, n + 1)), n, ns=fin, es=es,
                             fly_a=fa))
        frames.append(hframe(g, f"Como arreglo, por niveles y de izquierda a derecha: A = "
                             f"{angle([vals[i] for i in range(1, n + 1)])}.", tree, vals,
                             list(range(1, n + 1)), n, ns=fin, es=es))
    else:
        frames.append(hframe(g, verdict, tree, vals, ns=fin, es=es, ghosts=ghosts, **kw))
    return frames, g, (forma, orden, holes, bad)


def question_fig(p, name, tree_vals=None, array=None, size=None, length=None):
    if array is not None:
        L = length or len(array)
        g = G(1, L)
        g.ax, g.ay = 0, 0
        fr = hframe(g, "", {}, {i: v for i, v in enumerate(array, 1)},
                    list(range(1, len(array) + 1)), size or len(array))
        return f"![Arreglo A]({p.img(name, still(fr, g.static()))})"
    g = G(max(tree_vals))
    fr = hframe(g, "", {i: i for i in tree_vals}, dict(tree_vals))
    return f"![Árbol]({p.img(name, still(fr))})"


def tup_to_idx(t, i=1, out=None):
    """(llave, izq, der) -> {posición por niveles: llave}."""
    out = {} if out is None else out
    if t is None:
        return out
    k, l, r = t
    out[i] = k
    tup_to_idx(l, 2 * i, out)
    tup_to_idx(r, 2 * i + 1, out)
    return out


def L_(k):
    return (k, None, None)


# Los siete ejemplos de «¿es un montículo?»: dos fáciles, tres medios y dos difíciles
EJEMPLOS = [
    ("Fácil", dict(tree_vals=tup_to_idx((8, (5, L_(4), L_(3)), (7, L_(1), L_(2)))))),
    ("Fácil", dict(tree_vals=tup_to_idx((8, (5, L_(4), L_(3)), L_(9))))),
    ("Medio", dict(tree_vals=tup_to_idx((8, L_(5), (7, L_(1), L_(2)))))),
    ("Medio", dict(array=[20, 10, 5, 4, 3, 1], size=6, length=10)),
    ("Medio", dict(tree_vals=tup_to_idx((8, (5, L_(4), (3, L_(1), None)), (7, L_(1), L_(2)))))),
    ("Difícil", dict(array=[8, 4, 2, 1, 7, 9], size=4, length=10)),
    ("Difícil", dict(tree_vals=tup_to_idx((8, (5, (2, L_(4), L_(1)), L_(3)), (7, L_(1), L_(2)))))),
]
ESPERADO = [(True, True), (True, False), (False, True), (True, True), (False, True), (True, True),
            (True, False)]


def build():
    p = Page("Unidad4-EstructurasRecursivas/Monticulos")

    # 1. El problema: tres representaciones de la misma cola de prioridad
    # 2. Definición: el montículo de Bedoya, árbol y arreglo
    base = Heap([8, 5, 7, 4, 3, 1, 2], L=10)
    g = G(7, 10)
    p.put("fig-def", f"![Montículo y su arreglo]({p.img('def', still(base.fr(g, '', idx=True), g.static()))})")

    # Llenado por niveles (propiedad de forma)
    gf = G(12)
    frames = []
    for k in range(1, 13):
        t = {i: i for i in range(1, k + 1)}
        frames.append(hframe(gf, f"Posición {k}" + (": la raíz." if k == 1 else
                             f": hijo {'izquierdo' if k % 2 == 0 else 'derecho'} de la posición {k // 2}."),
                             t, {i: i for i in range(1, 13)}, ns={k: "new"}, hold=1.1))
    frames.append(hframe(gf, "Así crece un montículo: nivel por nivel, y cada nivel de izquierda a "
                         "derecha. Nunca hay un hueco antes del último nodo.",
                         {i: i for i in range(1, 13)}, {i: i for i in range(1, 13)}))
    p.put("anim-llenado", anim_block(p, "llenado-anim", frames, "Animación: orden en que se llenan las "
                                     "posiciones de un montículo"))

    # Representación en arreglo: los nodos bajan al arreglo nivel por nivel
    h = Heap([8, 5, 7, 4, 3, 1, 2], L=10)
    tree, vals = h.tree(), h.vals
    arr = h.arr()
    frames = []
    shown = []
    levels = [[1], [2, 3], [4, 5, 6, 7]]
    for d, lev in enumerate([[]] + levels):
        shown += lev
        nxt = levels[d] if d < len(levels) else []
        a = [e if (e in shown or e in nxt) else None for e in arr]
        fa = {e: g.xy(e) for e in nxt}
        if d == 0:
            cap = "El montículo como árbol. Se recorre por niveles, de izquierda a derecha."
        else:
            cap = (f"Nivel 0: la raíz {vals[1]} va a A[1]." if d == 1 else
                   f"Nivel {d - 1}: {', '.join(str(vals[e]) for e in lev)} van a A[{lev[0]}..{lev[-1]}].")
        frames.append(hframe(g, cap, tree, vals, a, 7, idx=True, ns={e: "hl" for e in lev},
                             cs={e: "hl" for e in lev}, fly_a=fa))
    frames.append(hframe(g, "A[1..heap-size[A]] es el montículo: heap-size[A] = 7 y length[A] = 10. "
                         "Las casillas grises no son parte del montículo.", tree, vals, arr, 7, idx=True))
    for i, js, txt in ((2, [1], "PARENT(2) = ⌊2/2⌋ = 1 y PARENT(3) = ⌊3/2⌋ = 1"),
                       (4, [2], "PARENT(4) = ⌊4/2⌋ = 2 y PARENT(5) = ⌊5/2⌋ = 2"),
                       (6, [3], "PARENT(6) = ⌊6/2⌋ = 3 y PARENT(7) = ⌊7/2⌋ = 3")):
        st = {i: "hl", i + 1: "hl", js[0]: "goal"}
        frames.append(hframe(g, txt + ".", tree, vals, arr, 7, idx=True, ns=st, cs=st,
                             es={i: "good", i + 1: "good"}))
    st = {2: "goal", 4: "hl", 5: "hl"}
    frames.append(hframe(g, "Al revés: LEFT(2) = 2·2 = 4 y RIGHT(2) = 2·2 + 1 = 5.", tree, vals, arr, 7,
                         idx=True, ns=st, cs=st, es={4: "good", 5: "good"}))
    p.put("anim-arreglo", anim_block(p, "arreglo-anim", frames, "Animación: del árbol al arreglo",
                                     g.static()))

    # 3. ¿Es un montículo? Siete ejemplos
    out = []
    for k, ((nivel, spec), esp) in enumerate(zip(EJEMPLOS, ESPERADO), 1):
        frames, gk, (forma, orden, holes, bad) = check_frames(**spec)
        assert (forma, orden) == esp, (k, forma, orden)
        q = question_fig(p, f"es{k}", **spec)
        if "array" in spec:
            enun = (f"$A = {lang(spec['array'])}$, con $heap\\text{{-}}size[A] = {spec['size']}$ y "
                    f"$length[A] = {spec['length']}$.")
        else:
            enun = "Dado el árbol:"
        si = "✓" if forma else "✗"
        so = "✓" if orden else "✗"
        resp = []
        if forma and orden:
            resp.append("**Sí es un max-heap.**")
        else:
            resp.append("**No es un montículo.**")
        resp.append(f"- Forma {si}" + ("." if forma else
                    f": la posición ${holes[0]}$ está vacía y hay nodos más a la derecha o más abajo."))
        resp.append(f"- Orden {so}" + ("." if orden else ": " + ", ".join(
            f"$A[{a}] = {spec_val(spec, a)} < A[{b}] = {spec_val(spec, b)}$" for a, b in bad) + "."))
        nota = NOTAS[k - 1]
        anim = anim_block(p, f"es{k}-anim", frames, f"Animación: ¿es un montículo? (ejemplo {k})",
                          gk.static())
        out.append(f"### Ejemplo {k}\n\n{enun}\n\n{q}\n\n¿Cumple la propiedad de "
                   f"forma? ¿Y la de orden? ¿Es un max-heap?\n\n:::{{admonition}} Respuesta\n:class: "
                   f"dropdown\n{anim}\n\n" + "\n".join(resp) + f"\n\n{nota}\n:::")
    p.put("ejemplos-es", "\n\n".join(out))

    # 4. Operaciones
    # HEAP-MAXIMUM
    h = Heap([16, 14, 10, 8, 7, 9, 3, 2, 4, 1])
    g10 = G(10, 10)
    p.put("fig-maximum", f"![HEAP-MAXIMUM]({p.img('maximum', still(h.fr(g10, '', ns={h.A[1]: 'goal'}, cs={h.A[1]: 'goal'}, rings={h.A[1]}), g10.static()))})")

    # MAX-HEAP-INSERT: el más simple, el que no sube y uno de CLRS
    for name, vals0, key, alt in (("ins1", [9, 8, 6, 2, 5], 7, "MAX-HEAP-INSERT(A, 7)"),
                                  ("ins2", [9, 8, 6, 2, 5], 4, "MAX-HEAP-INSERT(A, 4)"),
                                  ("ins3", [16, 14, 10, 8, 7, 9, 3, 2, 4, 1], 15, "MAX-HEAP-INSERT(A, 15)")):
        h = Heap(vals0, L=len(vals0) + 1)
        gg = G(len(vals0) + 1, len(vals0) + 1)
        frames = [h.fr(gg, f"A = {angle(vals0)}, heap-size[A] = {len(vals0)}. Es un max-heap.")]
        op_insert(h, gg, key, frames)
        frames.append(final_frame(h, gg, f"Resultado: A = {angle(h.values())}. Sigue siendo un max-heap."))
        p.put(name, anim_and_tabs(p, name, frames, gg, alt, alt))
        p.put(name + "-res", f"$A = {lang(h.values())}$")

    # Insertar uno a uno en un montículo vacío
    seq = [5, 12, 8, 20, 3, 15]
    h = Heap([], L=len(seq))
    gg = G(len(seq), len(seq))
    frames = [h.fr(gg, f"Montículo vacío: heap-size[A] = 0. Se insertan {', '.join(map(str, seq))}, en ese orden.")]
    for k in seq:
        op_insert(h, gg, k, frames)
    frames.append(final_frame(h, gg, f"Resultado: A = {angle(h.values())}."))
    p.put("ins-seq", anim_and_tabs(p, "insseq", frames, gg, "Insertar " + ", ".join(map(str, seq)),
                                   "insertar " + ", ".join(map(str, seq))))
    p.put("ins-seq-res", f"$A = {lang(h.values())}$")

    # HEAP-INCREASE-KEY (CLRS, figura 6.5)
    h = Heap([16, 14, 10, 8, 7, 9, 3, 2, 4, 1])
    frames = [h.fr(g10, f"A = {angle(h.values())}, heap-size[A] = 10. Es un max-heap.")]
    op_increase(h, g10, 9, 15, frames)
    frames.append(final_frame(h, g10, f"Resultado: A = {angle(h.values())}. Sigue siendo un max-heap."))
    p.put("inc1", anim_and_tabs(p, "inc1", frames, g10, "HEAP-INCREASE-KEY(A, 9, 15)",
                                "HEAP-INCREASE-KEY(A, 9, 15)"))
    p.put("inc1-res", f"$A = {lang(h.values())}$")

    # HEAP-EXTRACT-MAX: el más simple y el de CLRS
    for name, vals0 in (("ext1", [9, 8, 6, 2, 5]), ("ext2", [16, 14, 10, 8, 7, 9, 3, 2, 4, 1])):
        h = Heap(vals0)
        gg = G(len(vals0), len(vals0))
        frames = [h.fr(gg, f"A = {angle(vals0)}, heap-size[A] = {len(vals0)}. Es un max-heap.")]
        mx = op_extract(h, gg, frames)
        aside = {e: (gg.tw + 30, 0, "max") for e in h.vals if h.vals[e] == mx and e not in h.A}
        frames.append(final_frame(h, gg, f"return {mx}. Quedan A[1..{h.size}] = {angle(h.values())}: "
                                  f"otra vez un max-heap, con un elemento menos.", dict(aside=aside)))
        p.put(name, anim_and_tabs(p, name, frames, gg, "HEAP-EXTRACT-MAX(A)", "HEAP-EXTRACT-MAX(A)"))
        p.put(name + "-res", f"$A[1..{h.size}] = {lang(h.values())}$")

    # Hundir con el hijo equivocado (error productivo) y luego con el correcto
    vals0 = [1, 14, 10, 8, 7, 9, 3, 2, 4]
    h = Heap(vals0)
    gg = G(9, 9)
    r, l_, r_ = h.A[1], h.A[2], h.A[3]
    frames = [h.fr(gg, "Después de las líneas 3 a 5 de HEAP-EXTRACT-MAX (ejemplo 7): 1 está en la raíz y sus "
                   "hijos son 14 y 10. Ambos son mayores que 1.", ns={r: "new", l_: "hl", r_: "hl"},
                   cs={r: "new"}, rings={r})]
    h.A[1], h.A[3] = h.A[3], h.A[1]
    frames.append(h.fr(gg, "Intento equivocado: intercambiar 1 con 10, el hijo derecho.",
                       ns={r_: "hl", r: "new"}, cs={r_: "hl", r: "new"}))
    frames.append(h.fr(gg, "Ahora 10 es la raíz y su hijo izquierdo es 14: 10 < 14 ✗. El orden falla otra vez "
                       "en la raíz.", ns={r_: "bad", l_: "bad", r: "new"}, cs={r_: "bad", l_: "bad"},
                       es={l_: "bad"}))
    h.A[1], h.A[3] = h.A[3], h.A[1]
    frames.append(h.fr(gg, "Se deshace el intento: 1 vuelve a la raíz.", ns={r: "new", l_: "hl", r_: "hl"},
                       cs={r: "new"}, rings={r}))
    h.A[1], h.A[2] = h.A[2], h.A[1]
    frames.append(h.fr(gg, "Correcto: intercambiar 1 con 14, el MAYOR de los hijos. 14 ≥ 10 y 14 ≥ 1: en la raíz "
                       "el orden se cumple, y 1 sigue bajando por la izquierda.",
                       ns={l_: "goal", r_: "goal", r: "new"}, cs={l_: "goal", r: "new"},
                       es={r_: "good", r: "good"}))
    p.put("anim-hijo", anim_block(p, "hijo-anim", frames, "Animación: hundir con el hijo equivocado y con "
                                  "el correcto", gg.static()))

    # Cola de urgencias: inserciones y extracciones mezcladas
    ops = [("i", 5), ("i", 12), ("i", 8), ("x", None), ("i", 20), ("i", 3), ("x", None), ("i", 15)]
    h = Heap([], L=4)
    gg = G(4, 4)
    frames = [h.fr(gg, "Sala de urgencias vacía. Llegan pacientes (INSERT) y se atiende al de mayor prioridad "
                   "(EXTRACT-MAX), en el orden en que ocurren.")]
    atendidos = []
    for o, k in ops:
        if o == "i":
            op_insert(h, gg, k, frames)
        else:
            atendidos.append(op_extract(h, gg, frames))
    frames.append(final_frame(h, gg, f"Se atendió a {' y luego a '.join(map(str, atendidos))}. En espera: "
                              f"A = {angle(h.values())}, con {h.v(1)} como el próximo."))
    p.put("anim-urgencias", anim_block(p, "urgencias-anim", frames, "Animación: cola de urgencias",
                                       gg.static()))
    p.put("urgencias-res", f"se atiende a ${atendidos[0]}$ y luego a ${atendidos[1]}$, y quedan en espera "
          f"$A = {lang(h.values())}$")
    p.assemble("index.md")

    # Ejercicios
    ex1 = [("a", dict(array=[23, 17, 14, 6, 13, 10, 1, 5, 7, 12])),
           ("b", dict(array=[10, 9, 8, 7, 6, 5, 4])),
           ("c", dict(array=[8, 5, 7, 4, 3, 1, 2, 1, 2, 1])),
           ("d", dict(array=[8, 4, 2, 1, 7, 9], size=6))]
    sols = []
    for lab, spec in ex1:
        a = spec["array"]
        size = spec.get("size", len(a))
        vals = {i: v for i, v in enumerate(a[:size], 1)}
        forma, orden, holes, bad = is_max_heap(vals)
        txt = "sí es un max-heap" if orden else "no: " + ", ".join(
            f"$A[{x}] = {vals[x]} < A[{y}] = {vals[y]}$" for x, y in bad)
        sols.append(f"- {lab}) $A = {lang(a)}$: {txt}.")
    p.put("ex1-sol", "\n".join(sols))
    frames, gk, _ = check_frames(array=[23, 17, 14, 6, 13, 10, 1, 5, 7, 12])
    p.put("ex1-anim", anim_block(p, "ex1-anim", frames, "Animación: ejercicio 1 a)", gk.static()))

    h = Heap([8, 5, 7, 4, 3, 1, 2], L=8)
    gg = G(8, 8)
    frames = [h.fr(gg, f"A = {angle(h.values())}.")]
    op_insert(h, gg, 12, frames)
    p.put("ex3-sol", f"$A = {lang(h.values())}$; ${sum(1 for f in frames if 'se intercambian' in f.caption)}$ "
          f"intercambios.")
    p.put("ex3-anim", anim_block(p, "ex3-anim", frames, "Animación: ejercicio 3", gg.static()))

    h = Heap([10, 8, 9, 4, 7, 1, 6, 2, 3])
    gg = G(9, 9)
    frames = [h.fr(gg, f"A = {angle(h.values())}.")]
    op_increase(h, gg, 8, 11, frames)
    p.put("ex4-sol", f"$A = {lang(h.values())}$")
    p.put("ex4-anim", anim_block(p, "ex4-anim", frames, "Animación: ejercicio 4", gg.static()))

    h = Heap([10, 8, 9, 4, 7, 1, 6, 2, 3])
    gg = G(9, 9)
    frames = [h.fr(gg, f"A = {angle(h.values())}.")]
    m1 = op_extract(h, gg, frames)
    r1 = h.values()
    frames2 = []
    m2 = op_extract(h, gg, frames2)
    p.put("ex5-sol", f"La primera extracción devuelve ${m1}$ y deja $A[1..{len(r1)}] = {lang(r1)}$; la "
          f"segunda devuelve ${m2}$ y deja $A[1..{h.size}] = {lang(h.values())}$.")

    h = Heap([], L=8)
    seq = [5, 12, 8, 20, 3, 15, 10, 25]
    gg = G(8, 8)
    frames = []
    for k in seq:
        op_insert(h, gg, k, frames)
    nswap = sum(1 for f in frames if "se intercambian" in f.caption)
    p.put("ex6-sol", f"$A = {lang(h.values())}$, con ${nswap}$ intercambios en total.")
    p.assemble("exercises.md")


def spec_val(spec, i):
    if "array" in spec:
        return spec["array"][i - 1]
    return spec["tree_vals"][i]


NOTAS = [
    "El ejemplo de las diapositivas de Bedoya: un árbol lleno donde cada padre es mayor que sus hijos.",
    "Basta **un** padre menor que un hijo para que falle el orden: aquí $8 < 9$ en la raíz.",
    "El orden se cumple, pero los dos hijos de $5$ faltan mientras $7$ tiene los suyos: hay ramas de "
    "longitud $2$ a la izquierda de ramas de longitud $3$.",
    "Del arreglo se arma el árbol por niveles: $A[1]$ es la raíz, $A[2]$ y $A[3]$ sus hijos, y así. "
    "Las casillas $7$ a $10$ están en el arreglo pero no en el montículo.",
    "Parece casi un árbol lleno, pero $1$ cuelga de $3$ (posición $10$) mientras $4$ no tiene hijos "
    "(posiciones $8$ y $9$ vacías): el último nivel no se llenó de izquierda a derecha.",
    "Aunque $7$ y $9$ son mayores que $4$ y $2$, **no** están en el montículo: $heap\\text{-}size[A] = 4$ "
    "deja solo $8, 4, 2, 1$. Con $heap\\text{-}size[A] = 6$ no sería montículo.",
    "La raíz es mayor que todos y el segundo nivel también está bien: la falla está abajo, en el "
    "subárbol $2$–$4$–$1$, donde la raíz $2$ no es mayor que $4$. Hay que revisar **todos** los padres.",
]


if __name__ == "__main__":
    build()
