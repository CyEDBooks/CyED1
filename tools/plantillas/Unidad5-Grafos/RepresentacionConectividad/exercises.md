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

Escriba la matriz de adyacencia de cada grafo dirigido. Verifique que la suma de cada fila es el grado de salida del vértice.

{{GEN:fig-ex-adj}}

:::{admonition} Pistas
:class: dropdown
- La fila de $v_i$ tiene un $1$ en cada columna $v_j$ a la que llega una arista que sale de $v_i$.
- Un bucle en $v_i$ va en la diagonal, en la posición $(i, i)$.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:ex-adj-sol}}
:::

### Ejercicio 2

Muestre $M_R$, $M_R^{[2]}$ y $M_R^{[3]}$ para cada grafo.

{{GEN:fig-ex-pot}}

:::{admonition} Pistas
:class: dropdown
- $M_R^{[2]} = M_R \odot M_R$ y $M_R^{[3]} = M_R^{[2]} \odot M_R$.
- Para revisar una casilla $(i, j)$ de $M_R^{[2]}$, busque un vértice $t$ con una arista de $v_i$ a $t$ y otra de $t$ a $v_j$.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:ex-pot-sol}}
:::

### Ejercicio 3

Aplique el algoritmo de Warshall para obtener la matriz de conectividad de cada grafo.

{{GEN:ex-w-enunciado}}

:::{admonition} Pistas
:class: dropdown
- Para el pivote $k$, liste las filas con $1$ en la columna $k$ y las columnas con $1$ en la fila $k$; ponga un $1$ en cada cruce.
- Una fila de ceros (nadie sale de ese vértice) sigue en ceros hasta el final.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:ex-w-soluciones}}
:::

### Ejercicio 4

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

### Ejercicio 5

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

### Ejercicio 6

Para la matriz e) del Ejercicio 3, calcule $M_R \vee M_R^{[2]} \vee \cdots \vee M_R^{[5]}$ con productos booleanos y compare el resultado con el de Warshall. ¿Cuántas operaciones $\wedge$ hace cada método para un grafo de $n$ vértices?

---

*Material adaptado del material original del profesor Oscar Bedoya.*
