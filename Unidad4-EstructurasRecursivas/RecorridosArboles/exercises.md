---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Recorridos de árboles: Ejercicios"
---

# Recorridos de árboles: Ejercicios

Use esta página después de leer el [material de estudio de recorridos](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Muestre el recorrido en preorden, inorden y postorden del siguiente árbol.

![Árbol binario del ejercicio](images/ex1.svg)

:::{admonition} Pistas
:class: dropdown
- En preorden la primera es la raíz; en postorden, la última.
- Este árbol es un árbol de búsqueda: ¿qué propiedad tiene su inorden?
:::

:::{admonition} Solución general
:class: dropdown
- Preorden: 50 – 30 – 20 – 40 – 35 – 70 – 60 – 80 – 90
- Inorden: 20 – 30 – 35 – 40 – 50 – 60 – 70 – 80 – 90
- Postorden: 20 – 35 – 40 – 30 – 60 – 90 – 80 – 70 – 50

El inorden sale **ordenado**: es la propiedad de los árboles binarios de búsqueda.
:::

### Ejercicio 2

Represente en notación infija, prefija y posfija la expresión dada por el siguiente árbol, y calcule su valor.

![Árbol de expresión del ejercicio](images/ex2.svg)

:::{admonition} Pistas
:class: dropdown
- Infija: inorden con paréntesis en cada operador.
- Para el valor, evalúe la posfija con una pila.
:::

:::{admonition} Solución general
:class: dropdown
- Infija: $((8 - 6) ↑ 3) + (10 / (7 - 2))$
- Prefija: `+ ↑ − 8 6 3 / 10 − 7 2`
- Posfija: `8 6 − 3 ↑ 10 7 2 − / +`

Valor: $2^3 + 10/5 = 10$.
:::

### Ejercicio 3

Indique el valor de la expresión en notación prefija `/ − + + 4 3 13 5 − ↑ − 6 4 3 3`.

:::{admonition} Pistas
:class: dropdown
- Aplique la regla del operador más a la derecha seguido de dos números.
- El primer paso reduce `− 6 4`.
:::

:::{admonition} Solución general
:class: dropdown
- `/ − + + 4 3 13 5 − ↑ − 6 4 3 3`
- `/ − + + 4 3 13 5 − ↑ 2 3 3`
- `/ − + + 4 3 13 5 − 8 3`
- `/ − + + 4 3 13 5 5`
- `/ − + 7 13 5 5`
- `/ − 20 5 5`
- `/ 15 5`
- `3`
:::

### Ejercicio 4

Indique el valor de la expresión en notación posfija `7 2 3 * − 4 ↑ 9 3 / +`.

:::{admonition} Pistas
:class: dropdown
- El primer operador que aparece es `*`: opera sobre $2$ y $3$.
:::

:::{admonition} Solución general
:class: dropdown
Valor: **4**.

| Símbolo | Pila |
|---|---|
| `7` | 7 |
| `2` | 7 2 |
| `3` | 7 2 3 |
| `*` | 7 6 |
| `−` | 1 |
| `4` | 1 4 |
| `↑` | 1 |
| `9` | 1 9 |
| `3` | 1 9 3 |
| `/` | 1 3 |
| `+` | 4 |
:::

### Ejercicio 5

El preorden de un árbol binario es $A, B, D, E, C, F, G$ y su inorden es $D, B, E, A, F, C, G$. Reconstruya el árbol y dé su postorden.

:::{admonition} Pistas
:class: dropdown
- El primero del preorden es la raíz.
- En el inorden, lo que está a la izquierda de la raíz forma el subárbol izquierdo.
- Repita con cada subárbol.
:::

:::{admonition} Solución general
:class: dropdown
Raíz $A$; subárbol izquierdo con inorden $D, B, E$ y raíz $B$ (hijos $D$ y $E$); subárbol derecho con inorden $F, C, G$ y raíz $C$ (hijos $F$ y $G$). Es un árbol lleno de altura $3$. Postorden: $D, E, B, F, G, C, A$.
:::

### Ejercicio 6

¿El preorden y el **postorden** juntos determinan un único árbol binario? Justifique con un contraejemplo o una demostración.

---

*Material adaptado del material original de los profesores Oscar Bedoya y Andrés Aristizábal.*
