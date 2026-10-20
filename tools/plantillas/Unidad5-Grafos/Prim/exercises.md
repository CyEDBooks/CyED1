---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Prim: Ejercicios"
---

# Prim: Ejercicios

Use esta página después de leer el [material de estudio de Prim](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Encontrar un árbol recubridor mínimo usando el algoritmo de Prim. Liste las aristas en el orden en que las adiciona al árbol.

{{GEN:fig-bm3}}

:::{admonition} Pistas
:class: dropdown
- Hay tres aristas de peso $1$: la primera que se escoge es cualquiera de ellas.
- El árbol debe terminar con $12 - 1 = 11$ aristas.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:bm3-prim}}
:::

### Ejercicio 2

Encontrar un árbol recubridor mínimo usando el algoritmo de Prim, en cada grafo.

{{GEN:fig-bm45}}

:::{admonition} Pistas
:class: dropdown
- Lleve la lista de candidatas en cada paso y descarte las que tengan los dos extremos en el árbol.
- Cuando hay empate, escoja cualquiera: el peso final no cambia.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:bm45-prim}}
:::

### Ejercicio 3

Muestre con un ejemplo que, si en Prim se elimina la condición «incidente con el árbol» (es decir, se toma siempre la arista de menor peso de todo el grafo que no cree circuito **dentro de $T$**), lo que se va construyendo deja de ser un árbol en los pasos intermedios.

:::{admonition} Pistas
:class: dropdown
- Busque dos aristas baratas que estén lejos una de la otra.
- En el grafo del Ejemplo 2 del material de estudio, ¿cuáles son las cuatro aristas más baratas?
:::

:::{admonition} Solución general
:class: dropdown
En el grafo del Ejemplo 2, las aristas más baratas son $\{a,b\}$ ($1$), $\{b,c\}$ ($2$), $\{d,e\}$ ($3$) y $\{f,g\}$ ($3$). Después de tomarlas, $T$ tiene tres componentes: $\{a,b,c\}$, $\{d,e\}$ y $\{f,g\}$; es un **bosque**, no un árbol. Esa variante es el algoritmo de Kruskal, que también llega a un árbol recubridor mínimo, pero por otro camino.
:::

### Ejercicio 4

Demuestre que si todos los pesos de un grafo conexo son **distintos**, su árbol recubridor mínimo es **único**.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
