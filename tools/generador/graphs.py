"""Grafos de ejemplo usados en la Unidad 5 (tomados de las diapositivas fuente)."""
from common import scale, tree_pos

# Árbol de las diapositivas de Recorridos (BFS y DFS sobre un árbol)
TREE_AI = ("A", [("B", [("C", []), ("D", []), ("E", [("F", [])])]),
                 ("G", [("H", [("I", [])])])])

# CLRS fig. 22.3: grafo no dirigido r..y
CLRS_V = list("rstuvwxy")
CLRS_POS = scale({"r": (0, 0), "s": (1, 0), "t": (2, 0), "u": (3, 0),
                  "v": (0, 1), "w": (1, 1), "x": (2, 1), "y": (3, 1)}, 110)
CLRS_E = [("r", "s"), ("r", "v"), ("s", "w"), ("w", "t"), ("w", "x"), ("t", "x"),
          ("t", "u"), ("x", "u"), ("x", "y"), ("u", "y")]
CLRS_LP = {v: "above" for v in "rstu"} | {v: "below" for v in "vwxy"}

# Ejercicio de las diapositivas: grafo 1..5 con origen en 3
G5_V = ["1", "2", "3", "4", "5"]
G5_POS = scale({"1": (0, 0), "2": (1.3, 0), "3": (2.2, 0.75), "4": (1.3, 1.5), "5": (0, 1.5)}, 95)
G5_E = [("1", "2"), ("1", "5"), ("2", "5"), ("2", "3"), ("2", "4"), ("3", "4"), ("4", "5")]
G5_LP = {"1": "above", "2": "above", "3": "right", "4": "below", "5": "below"}

# CLRS fig. 22.2: grafo dirigido 1..6
D6_V = ["1", "2", "3", "4", "5", "6"]
D6_POS = scale({"1": (0, 0), "2": (1, 0), "3": (2, 0), "4": (0, 1), "5": (1, 1), "6": (2, 1)}, 115)
D6_E = [("1", "2"), ("1", "4"), ("2", "5"), ("3", "6"), ("3", "5"), ("4", "2"), ("5", "4"),
        ("6", "6")]
D6_LP = {v: "above" for v in "123"} | {v: "below" for v in "456"}

# CLRS fig. 22.4: grafo dirigido u..z (DFS)
DFS_V = list("uvwxyz")
DFS_POS = scale({"u": (0, 0), "v": (1, 0), "w": (2, 0), "x": (0, 1), "y": (1, 1), "z": (2, 1)}, 120)
DFS_E = [("u", "v"), ("u", "x"), ("x", "v"), ("v", "y"), ("y", "x"), ("w", "y"), ("w", "z"),
         ("z", "z")]
DFS_LP = {v: "above" for v in "uvw"} | {v: "below" for v in "xyz"}

# CLRS fig. 22.6: grafo dirigido q..z (ejercicio DFS desde q)
Q_V = list("qrstuvwxyz")
Q_POS = scale({"q": (1.2, 0), "r": (3.4, 0), "s": (0.2, 0.9), "t": (2.1, 0.9), "u": (3.4, 0.9),
               "v": (0, 2), "w": (1.0, 2), "x": (2.0, 2), "y": (2.9, 2), "z": (2.4, 2.9)}, 100)
Q_E = [("q", "s"), ("q", "w"), ("q", "t"), ("r", "u"), ("r", "y"), ("s", "v"), ("t", "x"),
       ("t", "y"), ("u", "y"), ("v", "w"), ("w", "s"), ("x", "z"), ("y", "q"), ("z", "x")]

# Mapa del sur de Alemania (BFS desde Frankfurt; Dijkstra con km)
DE_V = ["Frankfurt", "Mannheim", "Würzburg", "Kassel", "Karlsruhe", "Erfurt", "Nürnberg",
        "Augsburg", "Stuttgart", "München"]
DE_SHORT = {"Frankfurt": "Fra", "Mannheim": "Man", "Würzburg": "Wür", "Kassel": "Kas",
            "Karlsruhe": "Kar", "Erfurt": "Erf", "Nürnberg": "Nür", "Augsburg": "Aug",
            "Stuttgart": "Stu", "München": "Mün"}
DE_E = [("Frankfurt", "Mannheim", 85), ("Frankfurt", "Würzburg", 217), ("Frankfurt", "Kassel", 173),
        ("Mannheim", "Karlsruhe", 80), ("Würzburg", "Erfurt", 186), ("Würzburg", "Nürnberg", 103),
        ("Kassel", "München", 502), ("Karlsruhe", "Augsburg", 250), ("Nürnberg", "Stuttgart", 183),
        ("Nürnberg", "München", 167), ("Augsburg", "München", 84)]
DE_POS = scale({"Frankfurt": (1.6, 0.9), "Kassel": (4.8, 0.3), "Erfurt": (3.6, 1.4),
                "Würzburg": (2.6, 1.7), "Mannheim": (0.6, 1.8), "Nürnberg": (3.8, 2.6),
                "Karlsruhe": (0.2, 3.0), "Stuttgart": (2.2, 3.2), "Augsburg": (3.0, 4.2),
                "München": (4.8, 4.2)}, 85)

# Dijkstra de Bedoya (dirigido)
BED_V = list("abcdef")
BED_POS = scale({"a": (0, 1), "b": (1.2, 0), "c": (1.2, 2), "d": (2.6, 0), "e": (2.6, 2),
                 "f": (3.7, 1)}, 95)
BED_E = [("a", "b", 2), ("a", "c", 1), ("b", "d", 1), ("c", "d", 3), ("c", "e", 4),
         ("d", "f", 2), ("e", "f", 2)]
BED_LP = {"a": "left", "b": "above", "d": "above", "c": "below", "e": "below", "f": "right"}

# Bogotá a Buenos Aires (Rosen; diapositivas Grafos 3)
SA_V = ["Bogotá", "Lima", "Quito", "La Paz", "Asunción", "B. Aires"]
SA_SHORT = {"Bogotá": "Bog", "Lima": "Lim", "Quito": "Qui", "La Paz": "Paz",
            "Asunción": "Asu", "B. Aires": "BA"}
SA_E = [("Bogotá", "Lima", 4), ("Bogotá", "Quito", 2), ("Lima", "Quito", 1), ("Lima", "La Paz", 5),
        ("Lima", "Asunción", 7), ("Quito", "La Paz", 8), ("Quito", "Asunción", 10),
        ("La Paz", "Asunción", 2), ("La Paz", "B. Aires", 6), ("Asunción", "B. Aires", 3)]
SA_POS = scale({"Bogotá": (0, 1), "Lima": (1.3, 0), "Quito": (1.3, 2), "La Paz": (3.2, 0),
                "Asunción": (3.2, 2), "B. Aires": (4.5, 1)}, 100)
SA_LP = {"Bogotá": "left", "Lima": "above", "La Paz": "above", "Quito": "below",
         "Asunción": "below", "B. Aires": "right"}

# Prim/Kruskal de Bedoya
MST_V = list("abcdefg")
MST_POS = scale({"a": (0, 0), "b": (1.3, 0), "c": (2.6, 0), "d": (0, 1.1), "e": (1.3, 1.1),
                 "f": (2.6, 1.1), "g": (1.3, 2.4)}, 100)
MST_E = [("a", "b", 1), ("b", "c", 2), ("a", "d", 4), ("b", "d", 6), ("b", "e", 4), ("c", "e", 5),
         ("c", "f", 6), ("d", "e", 3), ("e", "f", 8), ("d", "g", 4), ("e", "g", 7), ("f", "g", 3)]

# Floyd-Warshall de Bedoya (dirigido)
FW_V = list("abcd")
FW_POS = scale({"a": (0, 1), "b": (1.5, 0), "c": (1.5, 2), "d": (3, 1)}, 80)
FW_E = [("a", "b", 3), ("a", "c", 4), ("b", "d", 5), ("c", "d", 3), ("d", "a", 8)]
DE_LP = {"Mün": "right", "Aug": "below", "Stu": "below", "Kar": "below", "Nür": "right",
         "Erf": "right", "Kas": "right"}

# Orden topológico (CLRS fig. 22.7, la ropa del profesor)
ROPA_V = ["calzoncillos", "pantalón", "cinturón", "camisa", "corbata", "chaqueta", "medias",
          "zapatos", "reloj"]
ROPA_E = [("calzoncillos", "pantalón"), ("calzoncillos", "zapatos"), ("pantalón", "cinturón"),
          ("pantalón", "zapatos"), ("cinturón", "chaqueta"), ("camisa", "cinturón"),
          ("camisa", "corbata"), ("corbata", "chaqueta"), ("medias", "zapatos")]
ROPA_POS = scale({"calzoncillos": (0, 0), "zapatos": (1.1, 0), "medias": (2.2, 0),
                  "pantalón": (0, 1), "camisa": (2.2, 1), "cinturón": (0, 2),
                  "corbata": (2.2, 2), "chaqueta": (1.1, 3), "reloj": (3.3, 0.5)}, 110)

Q_LP = {"q": "above", "r": "above", "s": "left", "t": "right", "u": "right", "v": "left",
        "w": "below", "x": "left", "y": "below", "z": "below"}
