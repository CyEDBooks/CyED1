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

Muestre el recorrido en preorden, inorden y postorden de cada árbol.

{{GEN:fig-ex1}}

:::{admonition} Pistas
:class: dropdown
- En preorden la primera es la raíz; en postorden, la última.
- Fíjese de qué lado cuelga cada hijo único: $j$ cuelga a la derecha de $h$; $n$ y $j$ cuelgan a la izquierda de $i$ y de $g$.
:::

:::{admonition} Solución general
:class: dropdown
a)
- Preorden: {{GEN:ex1a-pre}}
- Inorden: {{GEN:ex1a-in}}
- Postorden: {{GEN:ex1a-post}}

b)
- Preorden: {{GEN:ex1b-pre}}
- Inorden: {{GEN:ex1b-in}}
- Postorden: {{GEN:ex1b-post}}

c)
- Preorden: {{GEN:ex1c-pre}}
- Inorden: {{GEN:ex1c-in}}
- Postorden: {{GEN:ex1c-post}}
:::

### Ejercicio 2

Muestre el recorrido en preorden, inorden y postorden de cada árbol.

{{GEN:fig-ex2}}

:::{admonition} Pistas
:class: dropdown
- Con tres hijos, el inorden es: el primer subárbol, la raíz y luego los otros dos subárboles.
:::

:::{admonition} Solución general
:class: dropdown
a)
- Preorden: {{GEN:ex2a-pre}}
- Inorden: {{GEN:ex2a-in}}
- Postorden: {{GEN:ex2a-post}}

b)
- Preorden: {{GEN:ex2b-pre}}
- Inorden: {{GEN:ex2b-in}}
- Postorden: {{GEN:ex2b-post}}
:::

### Ejercicio 3

Muestre el recorrido en preorden, inorden, postorden y por niveles del siguiente árbol.

{{GEN:fig-ex3}}

:::{admonition} Pistas
:class: dropdown
- La raíz es $10$. ¿Qué subárbol se recorre completo antes que el otro?
- Por niveles: la raíz, luego los del nivel $1$ de izquierda a derecha, y así.
:::

:::{admonition} Solución general
:class: dropdown
- Preorden: {{GEN:ex3-pre}}
- Inorden: {{GEN:ex3-in}}
- Postorden: {{GEN:ex3-post}}
- Por niveles: {{GEN:ex3-niv}}
:::

### Ejercicio 4

Muestre un árbol binario que represente cada expresión matemática:

- a) $(x+5)/(x-3)$
- b) $(x+(y/z))*3$
- c) $x+(y/(x+3))$

:::{admonition} Pistas
:class: dropdown
- La raíz es el operador que se evalúa **último**, el que queda por fuera de todos los paréntesis.
- Luego se repite con cada operando.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:fig-ex4}}

En c) se lee en inorden $x+(y/(x+3))$: el árbol tiene a $+$ en dos lugares distintos.
:::

### Ejercicio 5

Escriba en notación prefija y postfija las tres expresiones del Ejercicio 4.

:::{admonition} Pistas
:class: dropdown
- Prefija = preorden del árbol; postfija = postorden.
:::

:::{admonition} Solución general
:class: dropdown
| Expresión | Prefija | Postfija |
|---|---|---|
{{GEN:ex5-rows}}
:::

### Ejercicio 6

Indique el valor de las siguientes expresiones, que están en notación prefija:

- a) `+ − * 2 3 5 / ↑ 2 3 4`
- b) `/ − + + 4 3 13 5 − ↑ − 6 4 3 3`

:::{admonition} Pistas
:class: dropdown
- Busque el operador más a la derecha que esté seguido de dos números.
- En a), el primer paso reduce `↑ 2 3`.
:::

:::{admonition} Solución general
:class: dropdown
a) Valor **{{GEN:ex6a-res}}**:

{{GEN:ex6a-lines}}

b) Valor **{{GEN:ex6b-res}}**:

{{GEN:ex6b-lines}}
:::

### Ejercicio 7

Indique el valor de las siguientes expresiones, que están en notación postfija:

- a) `7 2 3 * − 4 ↑ 9 3 / +`
- b) `2 3 ↑ 3 1 + / 4 ↑ 1 4 + 2 ↑ 5 / +`

:::{admonition} Pistas
:class: dropdown
- Busque el operador más a la izquierda que esté precedido de dos números.
- En a), el primer operador que aparece es `*`: opera sobre $2$ y $3$.
:::

:::{admonition} Solución general
:class: dropdown
a) Valor **{{GEN:ex7a-res}}**:

{{GEN:ex7a-lines}}

b) Valor **{{GEN:ex7b-res}}**:

{{GEN:ex7b-lines}}
:::

### Ejercicio 8

El preorden de un árbol binario es $A, B, D, E, C, F, G$ y su inorden es $D, B, E, A, F, C, G$. Reconstruya el árbol y dé su postorden.

:::{admonition} Pistas
:class: dropdown
- El primero del preorden es la raíz.
- En el inorden, lo que está a la izquierda de la raíz forma el subárbol izquierdo.
- Repita con cada subárbol.
:::

:::{admonition} Solución general
:class: dropdown
Raíz $A$; subárbol izquierdo con inorden $D, B, E$ y raíz $B$ (hijos $D$ y $E$); subárbol derecho con inorden $F, C, G$ y raíz $C$ (hijos $F$ y $G$). Postorden: $D, E, B, F, G, C, A$.
:::

### Ejercicio 9

Mostrar el recorrido en preorden, inorden y postorden para el siguiente árbol:

{{GEN:fig-ex9}}

---

*Material adaptado del material original de los profesores Oscar Bedoya, Andrés Aristizábal y Victor Manuel Vargas.*
