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

Encuentre un árbol recubridor mínimo usando el algoritmo de Prim, empezando por el vértice $a$. Liste las aristas en el orden en que las adiciona al árbol.

{{GEN:fig-ex1}}

:::{admonition} Pistas
:class: dropdown
- Desde $a$ las candidatas son $\{a,b\}$ ($4$) y $\{a,c\}$ ($3$).
- Lleve la lista de candidatas en cada paso y descarte las que tengan los dos extremos en el árbol.
- El árbol debe terminar con $8 - 1 = 7$ aristas.
:::

:::{admonition} Solución general
:class: dropdown
Orden de las aristas: {{GEN:ex1-sol}}.

{{GEN:fig-ex1-sol}}

Peso total: **{{GEN:ex1-peso}}**.
:::

### Ejercicio 2

Repita el Ejercicio 1 empezando por el vértice $h$. ¿Obtiene el mismo árbol? ¿El mismo peso?

:::{admonition} Pistas
:class: dropdown
- Las candidatas iniciales son $\{f,h\}$ ($3$) y $\{g,h\}$ ($4$).
- Compare los conjuntos de aristas, no el orden en que entran.
:::

:::{admonition} Solución general
:class: dropdown
Orden de las aristas: {{GEN:ex2-sol}}.

Es el mismo conjunto de aristas del Ejercicio 1, en otro orden, con el mismo peso.
:::

### Ejercicio 3

Muestre con un ejemplo que, si en Prim se elimina la condición «incidente con el árbol» (es decir, se toma siempre la arista de menor peso de todo el grafo que no cree circuito **dentro de $T$**), lo que se va construyendo deja de ser un árbol en los pasos intermedios.

:::{admonition} Pistas
:class: dropdown
- Busque dos aristas baratas que estén lejos una de la otra.
- En el grafo de las sedes, ¿cuáles son las cuatro aristas más baratas?
:::

:::{admonition} Solución general
:class: dropdown
En el grafo de las sedes, las aristas más baratas son $\{a,b\}$ ($1$), $\{b,c\}$ ($2$), $\{d,e\}$ ($3$) y $\{f,g\}$ ($3$). Después de tomarlas, $T$ tiene tres componentes: $\{a,b,c\}$, $\{d,e\}$ y $\{f,g\}$; es un **bosque**, no un árbol. Esa variante es el algoritmo de Kruskal, que también llega a un árbol recubridor mínimo, pero por otro camino.
:::

### Ejercicio 4

Demuestre que si todos los pesos de un grafo conexo son **distintos**, su árbol recubridor mínimo es **único**.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
