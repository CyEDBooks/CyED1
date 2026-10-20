---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Árboles: Ejercicios"
---

# Árboles: Ejercicios

Use esta página después de leer el [material de estudio de árboles](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Demuestre por inducción sobre $n$ que todo árbol con $n \ge 1$ vértices tiene $n - 1$ aristas.

:::{admonition} Pistas
:class: dropdown
- Caso base: $n = 1$.
- Todo árbol con al menos $2$ vértices tiene al menos una **hoja** (piense en el último vértice de un camino simple de longitud máxima).
- Quite una hoja y su arista: ¿lo que queda sigue siendo un árbol?
:::

:::{admonition} Solución general
:class: dropdown
Base: un árbol de $1$ vértice tiene $0$ aristas. Paso: sea $T$ un árbol con $n + 1$ vértices; tiene una hoja $v$. $T - v$ es conexo (ningún camino entre otros dos vértices pasa por una hoja) y sin circuitos, así que es un árbol con $n$ vértices y, por hipótesis, $n - 1$ aristas. $T$ tiene una arista más: $n$.
:::

### Ejercicio 2

¿Cuántas aristas tiene un **bosque** con $n$ vértices y $c$ componentes?

:::{admonition} Pistas
:class: dropdown
- Cada componente es un árbol. Aplique el resultado del Ejercicio 1 a cada uno.
:::

:::{admonition} Solución general
:class: dropdown
Si las componentes tienen $n_1, \dots, n_c$ vértices, las aristas son $\sum (n_i - 1) = n - c$.
:::

### Ejercicio 3

Un torneo de tenis por eliminación directa empieza con $64$ jugadores. Cada partido es un nodo interno de un árbol binario completo cuyas hojas son los jugadores. ¿Cuántos partidos se juegan? ¿Cuántas rondas?

:::{admonition} Pistas
:class: dropdown
- Use $n = m \cdot i + 1$ con $m = 2$.
- Cada ronda es un nivel del árbol.
:::

:::{admonition} Solución general
:class: dropdown
Hay $64$ hojas y $n = 2i + 1$ nodos, con $n = i + 64$: $i = 63$ partidos. Como $64 = 2^6$, hay $6$ rondas (el árbol tiene altura $7$ en nodos).
:::

### Ejercicio 4

Agregue a la clase `ArbolNArio<T>` los métodos `int darNivel(T e)` (la profundidad del elemento, o $-1$ si no está) y `List<T> darHojas()`. Indique cuál de los dos patrones (descenso recursivo o recorrido total) sigue cada uno.

:::{admonition} Pistas
:class: dropdown
- `darNivel` puede pasar el nivel actual como parámetro del método recursivo del nodo.
- `darHojas` acumula en una lista que se pasa como parámetro.
:::

:::{admonition} Solución general
:class: dropdown
`darNivel`: descenso recursivo. Se baja por los hijos con `nivel + 1` y se retorna apenas se encuentra el elemento. `darHojas`: recorrido total. Cada hoja se agrega a la lista y cada nodo interno delega en todos sus hijos. Con el árbol de la sección 3, `darNivel("n")` es $4$ y `darHojas()` devuelve las $10$ hojas.
:::

### Ejercicio 5

Muestre que un árbol binario con $\ell$ hojas tiene altura (en nodos) **al menos** $\lceil \log_2 \ell \rceil + 1$. Úselo para demostrar que **todo** algoritmo de ordenamiento por comparaciones hace $\Omega(n \log n)$ comparaciones en el peor caso.

---

*Material adaptado del material original de los profesores Oscar Bedoya y Andrés Aristizábal.*
