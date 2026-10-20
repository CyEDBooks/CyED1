---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Árboles binarios: Ejercicios"
---

# Árboles binarios: Ejercicios

Use esta página después de leer el [material de estudio de árboles binarios](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Dado el siguiente árbol binario, indique:

{{GEN:fig-vv}}

- La raíz del árbol
- El padre de $E$
- Los hijos de $C$
- Las hojas del árbol
- Los elementos no terminales
- El nivel de $I$
- La altura y el peso del árbol
- ¿Es completo? ¿Está lleno?

:::{admonition} Pistas
:class: dropdown
- El nivel es la longitud del camino desde la raíz: la raíz está en el nivel $0$.
- Completo: todo no terminal tiene sus **dos** subárboles no vacíos.
:::

:::{admonition} Solución general
:class: dropdown
Raíz $A$; padre de $E$: {{GEN:vv-padre-E}}; hijos de $C$: {{GEN:vv-hijos-C}}; hojas: {{GEN:vv-hojas}}; no terminales: {{GEN:vv-internos}}; nivel de $I$: {{GEN:vv-nivel-I}}; altura {{GEN:vv-alt}} y peso {{GEN:vv-peso}}. No es completo ({{GEN:vv-un-hijo}} tienen un solo hijo), así que tampoco está lleno.
:::

### Ejercicio 2

Dado el siguiente árbol binario, indique: la raíz, el padre de $9$, los hijos de $19$, las hojas, el nivel de $13$, la altura y el peso. ¿Es completo? ¿Está lleno?

{{GEN:fig-bed}}

:::{admonition} Pistas
:class: dropdown
- Para decidir si está lleno, compare los niveles de las hojas $21$ y $1$.
:::

:::{admonition} Solución general
:class: dropdown
Raíz $24$; padre de $9$: {{GEN:bed-padre-9}}; hijos de $19$: {{GEN:bed-hijos-19}}; hojas: {{GEN:bed-hojas}}; nivel de $13$: {{GEN:bed-nivel-13}}; altura {{GEN:bed-alt}} y peso {{GEN:bed-peso}}. **Es completo**: todos sus no terminales tienen dos hijos. **No está lleno**: la hoja $21$ está en el nivel $3$ y la hoja $1$, en el nivel $4$.
:::

### Ejercicio 3

Para el siguiente árbol binario indique: peso, altura, hojas, elementos no terminales, el nivel de $R$, el camino de $M$ a $G$ y su longitud. ¿Es completo? ¿Está lleno?

{{GEN:fig-ex1}}

:::{admonition} Pistas
:class: dropdown
- La altura cuenta **nodos** de la rama más larga.
- Revise cada elemento no terminal: ¿tiene los dos subárboles no vacíos?
:::

:::{admonition} Solución general
:class: dropdown
Peso {{GEN:ex1-peso}}, altura {{GEN:ex1-alt}}, hojas {{GEN:ex1-hojas}}. $R$ está en el nivel $3$. El camino de $M$ a $G$ es $M, F, H, G$, de longitud $3$. No es completo ($H$ y $P$ tienen un solo hijo) y por lo tanto no está lleno.
:::

### Ejercicio 4

Dibuje **todos** los árboles binarios distintos con $3$ nodos (sin importar los valores). ¿Cuántos son? ¿Cuántos tienen altura $3$?

:::{admonition} Pistas
:class: dropdown
- La raíz puede tener: $2$ nodos a la izquierda y $0$ a la derecha, $1$ y $1$, o $0$ y $2$.
- Con $2$ nodos hay $2$ árboles distintos.
:::

:::{admonition} Solución general
:class: dropdown
Son $5$: $2 \cdot 1 + 1 \cdot 1 + 1 \cdot 2$. Cuatro tienen altura $3$ (son «cadenas»); solo el que tiene un hijo a cada lado tiene altura $2$. En general, el número de árboles binarios con $n$ nodos es el número de Catalan $\frac{1}{n+1}\binom{2n}{n}$.
:::

### Ejercicio 5

Demuestre que en un árbol binario **completo** (todo no terminal tiene exactamente dos hijos) con $\ell$ hojas hay exactamente $\ell - 1$ elementos no terminales.

:::{admonition} Pistas
:class: dropdown
- Es el resultado $n = m \cdot i + 1$ de árboles $m$-arios completos con $m = 2$.
- O por inducción estructural: un árbol completo es una hoja, o una raíz con dos subárboles completos.
:::

:::{admonition} Solución general
:class: dropdown
Con $i$ no terminales, $n = 2i + 1$ y también $n = i + \ell$. Igualando: $\ell = i + 1$.
:::

### Ejercicio 6

Escriba en pseudocódigo los algoritmos recursivos `ESTA-LLENO(x)`, `CONTAR-EN-NIVEL(x, k)` (cuántos elementos hay en el nivel $k$ del subárbol con raíz $x$) y `SON-IGUALES(x, y)` (misma forma y mismos elementos). Aplíquelos al árbol del Ejercicio 3.

:::{admonition} Pistas
:class: dropdown
- `ESTA-LLENO`: completo y con todas las hojas a la misma profundidad. Otra forma: el peso es $2^{\text{altura}} - 1$.
- `CONTAR-EN-NIVEL(x, k)`: si $x$ es vacío es $0$; si $k = 0$ es $1$; si no, sume `CONTAR-EN-NIVEL` con $k - 1$ en cada hijo.
:::

:::{admonition} Solución general
:class: dropdown
Para el árbol del Ejercicio 3: `ESTA-LLENO` da falso; `CONTAR-EN-NIVEL` con $k = 0, 1, 2, 3$ da $1, 2, 4, 2$; `SON-IGUALES` con una copia del mismo árbol da verdadero, y con el árbol del ejemplo de la sección 2 da falso.
:::

### Ejercicio 7

Escriba un algoritmo que reciba un árbol binario y devuelva su **espejo** (el mismo árbol con los subárboles izquierdo y derecho intercambiados en todos los niveles). Demuestre por inducción estructural que el espejo del espejo es el árbol original.

---

*Material adaptado del material original de los profesores Oscar Bedoya, Andrés Aristizábal y Victor Manuel Vargas.*
