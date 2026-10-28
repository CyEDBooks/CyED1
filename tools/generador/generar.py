"""Regenera las páginas e imágenes de las Unidades 4 y 5 de CyED1.

Uso, desde la raíz del repositorio:

    python3 tools/generador/generar.py            # todas las páginas
    python3 tools/generador/generar.py u5_bfs     # solo una
"""
import importlib
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO

PAGES = {
    "u4_arboles": "Unidad4-EstructurasRecursivas/Arboles",
    "u4_binarios": "Unidad4-EstructurasRecursivas/ArbolesBinarios",
    "u4_recorridos": "Unidad4-EstructurasRecursivas/RecorridosArboles",
    "u4_abb": "Unidad4-EstructurasRecursivas/ArbolesBinariosBusqueda",
    "u4_avl": "Unidad4-EstructurasRecursivas/ArbolesAVL",
    "u4_monticulos": "Unidad4-EstructurasRecursivas/Monticulos",
    "u5_conceptos": "Unidad5-Grafos/ConceptosBasicos",
    "u5_repr": "Unidad5-Grafos/RepresentacionConectividad",
    "u5_euler": "Unidad5-Grafos/ConectividadEulerHamilton",
    "u5_iso": "Unidad5-Grafos/IsomorfismoPlanaridadColoreo",
    "u5_bfs": "Unidad5-Grafos/BFS",
    "u5_dfs": "Unidad5-Grafos/DFS",
    "u5_estados": "Unidad5-Grafos/BusquedaEspacioEstados",
    "u5_dijkstra": "Unidad5-Grafos/Dijkstra",
    "u5_mst": ("Unidad5-Grafos/Prim", "Unidad5-Grafos/Kruskal"),
    "u5_floyd": "Unidad5-Grafos/FloydWarshall",
}

if __name__ == "__main__":
    names = sys.argv[1:] or list(PAGES)
    for name in names:
        if name not in PAGES:
            sys.exit(f"página desconocida: {name}")
        dirs = PAGES[name] if isinstance(PAGES[name], tuple) else (PAGES[name],)
        # se borran las imágenes viejas para que no queden SVG huérfanos
        for d in dirs:
            shutil.rmtree(os.path.join(REPO, d, "images"), ignore_errors=True)
        importlib.import_module(f"pages.{name}").build()
        print("ok", name)
