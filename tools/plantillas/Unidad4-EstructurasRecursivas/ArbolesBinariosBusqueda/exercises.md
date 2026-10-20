---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Árboles binarios de búsqueda: Ejercicios"
---

# Árboles binarios de búsqueda: Ejercicios

Use esta página después de leer el [material de estudio](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Cree un árbol binario de búsqueda insertando, en este orden, las llaves: mango, fresa, uva, banano, kiwi, pera, cereza, lima (orden alfabético). Dé su inorden y su altura.

:::{admonition} Pistas
:class: dropdown
- La primera llave es la raíz.
- Compare alfabéticamente: «fresa» < «mango» porque «f» va antes que «m».
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:ex1-fig}}

Inorden: {{GEN:ex1-inorden}} (orden alfabético). Altura: {{GEN:ex1-alt}}.
:::

### Ejercicio 2

En el árbol de la sección 2, ¿cuál es el sucesor de $4$, $7$, $13$ y $17$? ¿Cuál es el predecesor de $6$ y de $17$? Para cada uno, diga qué caso de `TREE-SUCCESSOR` (o de su simétrico) se aplica.

{{GEN:fig-ex2}}

:::{admonition} Pistas
:class: dropdown
- Si tiene subárbol derecho, el sucesor es el mínimo de ese subárbol.
- Si no, suba hasta que llegue desde un hijo **izquierdo**.
- El predecesor es el simétrico: máximo del subárbol izquierdo, o subir hasta llegar desde un hijo **derecho**.
:::

:::{admonition} Solución general
:class: dropdown
- Sucesor de $4$: $6$ (sube: $4$ es hijo derecho de $3$, que es hijo izquierdo de $6$).
- Sucesor de $7$: $9$ (mínimo del subárbol derecho, que empieza en $13$).
- Sucesor de $13$: $15$ (sube hasta la raíz).
- Sucesor de $17$: $18$ ($17$ es hijo izquierdo de $18$).
- Predecesor de $6$: $4$ (máximo del subárbol izquierdo).
- Predecesor de $17$: $15$ (sube: $17$ es hijo izquierdo de $18$, que es hijo derecho de $15$).
:::

### Ejercicio 3

En el árbol de la sección 2, elimine $6$ (dos hijos). Dibuje el resultado. ¿Qué pasa con el hijo derecho del sucesor?

:::{admonition} Pistas
:class: dropdown
- El sucesor de $6$ es $7$.
- $7$ no tiene hijo izquierdo pero sí derecho ($13$): quitar $7$ es el caso 2.
:::

:::{admonition} Solución general
:class: dropdown
Se separa $7$; su hijo $13$ (con $9$) sube a ocupar su lugar como hijo derecho del antiguo nodo de $6$, y la llave $7$ reemplaza a $6$. El nodo que antes tenía $6$ queda con $7$, hijo izquierdo $3$ (con $2$ y $4$) e hijo derecho $13$ (con $9$).
:::

### Ejercicio 4

Muestre que si se insertan $n$ llaves distintas en un ABB vacío, en orden **ascendente**, la altura es $n$ y el número total de comparaciones es $\frac{n(n-1)}{2}$. ¿En qué orden habría que insertar $1, \dots, 7$ para obtener un árbol lleno?

:::{admonition} Pistas
:class: dropdown
- La $i$-ésima llave se compara con las $i - 1$ anteriores.
- Para el árbol lleno: la raíz debe ser la mediana.
:::

:::{admonition} Solución general
:class: dropdown
Cada llave nueva es la mayor y baja por la derecha pasando por todas las anteriores: $0 + 1 + \cdots + (n - 1) = n(n-1)/2$ comparaciones, y el árbol es una cadena de altura $n$. Para un árbol lleno con $1, \dots, 7$: $4, 2, 6, 1, 3, 5, 7$ (o cualquier orden que inserte $4$ primero y luego cada mediana antes que sus mitades).
:::

### Ejercicio 5

Agregue a la clase `ABB<T>` los métodos `T sucesor(T k)`, `T predecesor(T k)` y `int contarEnRango(T a, T b)` (cuántas llaves hay entre $a$ y $b$). `contarEnRango` no debe recorrer subárboles que estén completamente fuera del rango. Analice su complejidad.

---

*Material adaptado del material original de los profesores Andrés Aristizábal y Oscar Bedoya.*
