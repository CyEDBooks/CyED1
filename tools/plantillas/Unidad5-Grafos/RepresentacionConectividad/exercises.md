---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Representación y conectividad: Ejercicios"
---

# Representación y conectividad: Ejercicios

Use esta página después de leer el [material de estudio](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Aplique el algoritmo de Warshall a la siguiente matriz de adyacencia. Muestre $W_1, \dots, W_5$.

{{GEN:ex-w-mat}}

{{GEN:fig-ex-w}}

:::{admonition} Pistas
:class: dropdown
- Para el pivote $k$, liste las filas con $1$ en la columna $k$ y las columnas con $1$ en la fila $k$.
- La fila $c$ es toda cero: desde $c$ no sale ninguna arista. ¿Puede cambiar en algún paso?
:::

:::{admonition} Solución general
:class: dropdown
Unos nuevos en cada paso: {{GEN:ex-w-cambios}}.

{{GEN:ex-w-sol}}

La fila $c$ sigue en ceros (desde $c$ no se llega a ninguna parte) y la columna $d$ también (a $d$ no llega ninguna arista).
:::

### Ejercicio 2

Sea $A$ la matriz de adyacencia de un grafo simple no dirigido. ¿Qué representan los elementos de la **diagonal** de $A^2$ (producto usual)?

:::{admonition} Pistas
:class: dropdown
- La posición $(i, i)$ de $A^2$ cuenta caminos de longitud $2$ de $v_i$ a $v_i$.
- En un grafo simple, un camino de longitud $2$ que empieza y termina en $v_i$ es «ir a un vecino y volver».
:::

:::{admonition} Solución general
:class: dropdown
$(A^2)_{ii} = \delta(v_i)$: hay un camino $v_i, v_t, v_i$ por cada vecino $v_t$. Por *handshaking*, la **traza** de $A^2$ es $2e$.
:::

### Ejercicio 3

¿Qué se puede decir de un grafo dirigido cuya matriz de conectividad $M_R^\infty$ tiene **solo unos**? ¿Y de uno no dirigido?

:::{admonition} Pistas
:class: dropdown
- La posición $(i, j)$ de $M_R^\infty$ es $1$ si hay un camino de $v_i$ a $v_j$.
- ¿Qué pasa con la diagonal en un grafo no dirigido con al menos una arista en cada vértice?
:::

:::{admonition} Solución general
:class: dropdown
En un grafo dirigido, que todas las posiciones fuera de la diagonal sean $1$ significa que hay camino en ambos sentidos entre cualquier par de vértices: el grafo es **fuertemente conexo**. En uno no dirigido, que sea **conexo** (y, para que la diagonal también sea $1$, que cada vértice tenga al menos una arista: se va al vecino y se vuelve).
:::

### Ejercicio 4

Escriba en Java un método `boolean[][] warshall(boolean[][] m)` y pruébelo con la matriz del Ejercicio 1. Compare su resultado con el de calcular $M_R \vee M_R^{[2]} \vee \cdots \vee M_R^{[5]}$ usando un método `boolean[][] productoBooleano(boolean[][] a, boolean[][] b)`.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
