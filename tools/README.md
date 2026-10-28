---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: Generador de las Unidades 4 y 5
---

# Generador de las Unidades 4 y 5

Las páginas de `Unidad4-EstructurasRecursivas/` y `Unidad5-Grafos/` salen de este generador. El texto vive en `plantillas/`. Las figuras SVG y las tablas de cada paso las calcula `generador/` corriendo los algoritmos, así que una traza de BFS o una rotación AVL coincide con lo que haría el código.

No edite los `.md` de las unidades a mano: la próxima regeneración los sobrescribe. Edite la plantilla o el script de la página.

## Regenerar

Necesita Python 3.10 o superior, sin paquetes extra. Desde la raíz del repositorio:

```bash
python3 tools/generador/generar.py            # todas las páginas
python3 tools/generador/generar.py u5_bfs     # una sola
```

El script borra la carpeta `images/` de cada página antes de dibujarla, para no dejar figuras viejas.

## Contenido

| Carpeta | Qué tiene |
|---|---|
| `plantillas/` | Un `index.md` y un `exercises.md` por tema, con marcas `{{GEN:nombre}}` donde va lo calculado. |
| `generador/pages/` | Un script por tema (`u4_avl.py`, `u5_dijkstra.py`, ...). Cada uno llena las marcas de sus plantillas. |
| `generador/algos.py`, `tviz.py` | Los algoritmos con su traza: BFS, DFS, Dijkstra, Prim, Kruskal, Floyd-Warshall, Warshall, búsqueda en espacio de estados, minimax, ABB y AVL. |
| `generador/figlib.py`, `gviz.py`, `sviz.py` | El dibujo de grafos, árboles y tableros, y el paso de cada traza a pestañas. |
| `generador/anim.py` | Las animaciones: una lista de cuadros (dónde está cada nodo, su estilo, su padre) se vuelve un SVG con SMIL que desliza los nodos de un cuadro al siguiente y se repite solo. Funciona dentro de un `<img>`, sin JavaScript. Los mismos cuadros, quietos, dan las pestañas «Paso 1, Paso 2, ...». |
| `generador/graphs.py` | Los grafos de ejemplo, tomados de las diapositivas del curso y de CLRS. |
| `generador/mdlib.py`, `common.py` | El bloque de pestañas «Paso 1, Paso 2, ...», las tablas y el armado de cada página. |

## Cambiar una página

1. Edite el texto en `plantillas/<Unidad>/<Tema>/index.md` o `exercises.md`.
2. Si cambia un ejemplo (otro grafo, otra secuencia de llaves), edite `generador/pages/<tema>.py` o `generador/graphs.py`.
3. Regenere esa página y compile el libro con `npx mystmd build --html` para revisar.

Las marcas `{{GEN:...}}` que una plantilla pide y el script no llena hacen fallar la generación con el nombre de la marca que falta.
