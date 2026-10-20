"""Trazas de los algoritmos de la Unidad 5.

Cada función devuelve la lista de estados del algoritmo, uno por paso. Las
páginas convierten cada estado en una figura y una tabla.
"""
import copy

INF = float("inf")


def adjacency(vertices, edges, directed=False):
    adj = {v: [] for v in vertices}
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) > 2 else 1
        adj[u].append((v, w))
        if not directed and u != v:
            adj[v].append((u, w))
    order = {v: i for i, v in enumerate(vertices)}
    for v in adj:
        adj[v].sort(key=lambda p: order[p[0]])
    return adj


# BFS
def bfs_trace(vertices, adj, s):
    color = {v: "white" for v in vertices}
    d = {v: INF for v in vertices}
    pi = {v: None for v in vertices}
    color[s], d[s] = "gray", 0
    Q = [s]
    snaps = [dict(kind="init", u=None, new=[s], color=dict(color), d=dict(d),
                  pi=dict(pi), Q=list(Q))]
    while Q:
        u = Q.pop(0)
        new = []
        for v, _ in adj[u]:
            if color[v] == "white":
                color[v] = "gray"
                d[v] = d[u] + 1
                pi[v] = u
                Q.append(v)
                new.append(v)
        color[u] = "black"
        snaps.append(dict(kind="deq", u=u, new=new, color=dict(color), d=dict(d),
                          pi=dict(pi), Q=list(Q)))
    return snaps


# DFS
def dfs_trace(vertices, adj, roots=None, directed=True):
    """Un estado por evento: descubrir o finalizar un vértice."""
    color = {v: "white" for v in vertices}
    d, f, pi = {}, {}, {v: None for v in vertices}
    cls = {}
    t = [0]
    snaps = []
    stack = []

    def snap(kind, u, edge=None):
        snaps.append(dict(kind=kind, u=u, edge=edge, color=dict(color), d=dict(d),
                          f=dict(f), pi=dict(pi), cls=dict(cls), stack=list(stack),
                          time=t[0]))

    def visit(u):
        t[0] += 1
        d[u] = t[0]
        color[u] = "gray"
        stack.append(u)
        snap("disc", u, (pi[u], u) if pi[u] is not None else None)
        for v, _ in adj[u]:
            if color[v] == "white":
                pi[v] = u
                cls[(u, v)] = "T"
                visit(v)
            else:
                if (u, v) in cls or (not directed and (v, u) in cls):
                    continue
                if color[v] == "gray":
                    cls[(u, v)] = "B"
                elif d[u] < d[v]:
                    cls[(u, v)] = "F"
                else:
                    cls[(u, v)] = "C"
        color[u] = "black"
        t[0] += 1
        f[u] = t[0]
        stack.pop()
        snap("fin", u)

    for u in (roots or vertices):
        if color[u] == "white":
            visit(u)
    return snaps


# Dijkstra
def dijkstra_trace(vertices, adj, s):
    """Versión de Bedoya: etiquetas [distancia, predecesor] y nodos permanentes.

    Empates: se escoge el primero en el orden de 'vertices'.
    """
    L = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    L[s] = 0
    S = []
    snaps = [dict(kind="init", u=None, L=dict(L), pred=dict(pred), S=list(S), changed=[s])]
    while len(S) < len(vertices):
        cand = [v for v in vertices if v not in S and L[v] < INF]
        if not cand:
            break
        u = min(cand, key=lambda v: (L[v], vertices.index(v)))
        S.append(u)
        changed = []
        for v, w in adj[u]:
            if v not in S and L[u] + w < L[v]:
                L[v] = L[u] + w
                pred[v] = u
                changed.append(v)
        snaps.append(dict(kind="perm", u=u, L=dict(L), pred=dict(pred), S=list(S),
                          changed=changed))
    return snaps


def path_to(pred, v):
    p = []
    while v is not None:
        p.append(v)
        v = pred[v]
    return p[::-1]


# Prim
def prim_trace(vertices, edges, start=None):
    """Prim: se crece un único árbol.

    start=None: como en las diapositivas de Bedoya, se empieza con la arista de
    menor peso de todo el grafo. Empates: la arista que aparece primero en 'edges'.
    """
    inT = [] if start is None else [start]
    T = []
    snaps = [dict(kind="init", inT=list(inT), T=list(T),
                  cand=_prim_cand(edges, inT) if inT else list(edges), chosen=None)]
    while len(inT) < len(vertices):
        cand = _prim_cand(edges, inT) if inT else list(edges)
        if not cand:
            break
        e = min(cand, key=lambda e: (e[2], edges.index(e)))
        T.append(e)
        if not inT:
            inT += [e[0], e[1]]
        else:
            inT.append(e[1] if e[0] in inT else e[0])
        snaps.append(dict(kind="add", inT=list(inT), T=list(T),
                          cand=_prim_cand(edges, inT), chosen=e, prev_cand=cand))
    return snaps


def _prim_cand(edges, inT):
    return [e for e in edges if (e[0] in inT) != (e[1] in inT)]


# Kruskal
def kruskal_trace(vertices, edges):
    """Kruskal con conjuntos disjuntos (componentes visibles en cada paso)."""
    order = sorted(edges, key=lambda e: (e[2], edges.index(e)))
    comp = {v: v for v in vertices}

    def find(v):
        while comp[v] != v:
            v = comp[v]
        return v

    T = []
    snaps = [dict(kind="init", order=order, i=-1, T=[], accepted=None, comps=_comps(vertices, find))]
    for i, e in enumerate(order):
        a, b = find(e[0]), find(e[1])
        if a != b:
            comp[b] = a
            T.append(e)
            acc = True
        else:
            acc = False
        snaps.append(dict(kind="edge", order=order, i=i, T=list(T), accepted=acc, edge=e,
                          comps=_comps(vertices, find)))
        if len(T) == len(vertices) - 1:
            break
    return snaps


def _comps(vertices, find):
    groups = {}
    for v in vertices:
        groups.setdefault(find(v), []).append(v)
    return [g for g in groups.values()]


# Floyd-Warshall
def floyd_trace(vertices, edges, directed=True):
    """W_k y P_k al estilo Bedoya: P[i][j] = vértice que se inserta en el
    recorrido de i a j (al inicio P0[i][j] = j: ir directo)."""
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    W = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    P = [[vertices[j] for j in range(n)] for i in range(n)]
    for e in edges:
        u, v, w = e
        W[idx[u]][idx[v]] = min(W[idx[u]][idx[v]], w)
        if not directed:
            W[idx[v]][idx[u]] = min(W[idx[v]][idx[u]], w)
    snaps = [dict(k=None, W=copy.deepcopy(W), P=copy.deepcopy(P), changed=[])]
    for k in range(n):
        changed = []
        for i in range(n):
            for j in range(n):
                if W[i][k] + W[k][j] < W[i][j]:
                    W[i][j] = W[i][k] + W[k][j]
                    P[i][j] = vertices[k]
                    changed.append((i, j))
        snaps.append(dict(k=vertices[k], W=copy.deepcopy(W), P=copy.deepcopy(P),
                          changed=changed))
    return snaps


def floyd_route(vertices, P, a, b):
    """Reconstruye el recorrido insertando pivotes (como en las diapositivas)."""
    idx = {v: i for i, v in enumerate(vertices)}
    steps = [[a, b]]
    route = [a, b]
    changed = True
    while changed:
        changed = False
        new = [route[0]]
        for x, y in zip(route, route[1:]):
            k = P[idx[x]][idx[y]]
            if k != y:
                new.append(k)
                changed = True
            new.append(y)
        if changed:
            route = new
            steps.append(list(route))
    return steps


# Warshall
def warshall_trace(vertices, M):
    n = len(vertices)
    W = [row[:] for row in M]
    snaps = [dict(k=None, W=[r[:] for r in W], changed=[])]
    for k in range(n):
        changed = []
        for i in range(n):
            if W[i][k]:
                for j in range(n):
                    if W[k][j] and not W[i][j]:
                        W[i][j] = 1
                        changed.append((i, j))
        snaps.append(dict(k=vertices[k], W=[r[:] for r in W], changed=changed))
    return snaps


def bool_product(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return [[int(any(A[i][t] and B[t][j] for t in range(k))) for j in range(m)] for i in range(n)]


def int_product(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


# búsqueda en espacio de estados
def tree_search(start, succ, is_goal, mode="bfs", avoid="path", max_nodes=500):
    """Búsqueda no informada al estilo de las diapositivas de Bedoya.

    Expandir un nodo = verificar si es meta y, si no lo es, crear sus hijos.
    mode: "bfs" (cola) o "dfs" (pila; los hijos se apilan para salir en orden).
    avoid: "none", "path" (no repetir estados de la rama: «evite devolverse»)
           o "global" (no crear estados ya creados).
    Devuelve nodos {id, state, parent, op, depth}, el orden de expansión, la
    meta encontrada y el estado de la frontera tras cada expansión.
    """
    nodes = [dict(id=0, state=start, parent=None, op=None, depth=0)]
    frontier = [0]
    expanded = []
    snaps = [dict(frontier=list(frontier), expanded=[], created=[0], current=None)]
    seen = {start}
    goal = None
    while frontier:
        cur = frontier.pop(0)
        expanded.append(cur)
        n = nodes[cur]
        if is_goal(n["state"]):
            goal = cur
            snaps.append(dict(frontier=list(frontier), expanded=list(expanded), created=[],
                              current=cur, goal=True))
            break
        path_states = set()
        p = cur
        while p is not None:
            path_states.add(nodes[p]["state"])
            p = nodes[p]["parent"]
        kids = []
        for op, st in succ(n["state"]):
            if avoid == "path" and st in path_states:
                continue
            if avoid == "global" and st in seen:
                continue
            seen.add(st)
            nid = len(nodes)
            nodes.append(dict(id=nid, state=st, parent=cur, op=op, depth=n["depth"] + 1))
            kids.append(nid)
        if mode == "bfs":
            frontier = frontier + kids
        else:
            frontier = kids + frontier
        snaps.append(dict(frontier=list(frontier), expanded=list(expanded), created=kids,
                          current=cur, goal=False))
        if len(nodes) > max_nodes:
            break
    return nodes, expanded, goal, snaps


def explicit_tree(t):
    """Convierte (etiqueta, [hijos]) en una función de sucesores."""
    ch = {}

    def rec(node):
        lab, kids = node
        ch[lab] = [k[0] for k in kids]
        for k in kids:
            rec(k)
    rec(t)
    return lambda s: [(None, k) for k in ch[s]]


def minimax(tree_nodes, children, value_leaf, root=0, maximizing_first=True):
    """Evalúa un árbol de juego en postorden. Devuelve valores y el orden de evaluación."""
    val = {}
    order = []

    def rec(v, maxi):
        ch = children.get(v, [])
        if not ch:
            val[v] = value_leaf(v, maxi)
        else:
            for c in ch:
                rec(c, not maxi)
            vals = [val[c] for c in ch]
            val[v] = max(vals) if maxi else min(vals)
        order.append(v)
    rec(root, maximizing_first)
    return val, order
