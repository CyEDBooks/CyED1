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

Crear un árbol de búsqueda binaria con las llaves $3, 7, 9, 12, 17, 23, 25$ que tenga la siguiente estructura:

{{GEN:fig-est1}}

:::{admonition} Pistas
:class: dropdown
- El inorden del árbol tiene que dar las llaves ordenadas.
- Recorra los círculos vacíos en inorden y ponga las llaves en ese orden.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:fig-est1-sol}}
:::

### Ejercicio 2

Crear un árbol de búsqueda binaria con las llaves $3, 7, 8, 10, 14, 17, 21, 25, 27, 29, 34, 38, 42$ que tenga la siguiente estructura:

{{GEN:fig-est2}}

:::{admonition} Pistas
:class: dropdown
- A la izquierda de $25$ quedan exactamente $7$ nodos: las $7$ llaves menores que $25$.
- $17$ ya está puesto: ¿qué llaves van en su subárbol?
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:fig-est2-sol}}
:::

### Ejercicio 3

Crear un árbol de búsqueda binaria **de altura mínima** con las siguientes llaves:

- apple tv
- ipad
- iphone
- ipod touch
- nintendo wii
- playstation
- smart tv

Luego, insertar la llave *kindle*.

:::{admonition} Pistas
:class: dropdown
- Las llaves se comparan en orden alfabético; la lista ya está ordenada.
- Para que la altura sea mínima, la raíz es la llave de la mitad, y así en cada subárbol.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:fig-ex3-sol}}

*kindle* va después de *ipod touch* y antes de *playstation* y de *nintendo wii*: queda como hijo izquierdo de *nintendo wii*.
:::

### Ejercicio 4

En el siguiente ABB, que tiene llaves repetidas, ¿cuál es el sucesor de $7$, de $9$, de $10$ (el hijo de $8$) y de $12$? Para cada uno, diga qué caso de `TREE-SUCCESSOR` se aplica.

{{GEN:fig-ex4}}

:::{admonition} Pistas
:class: dropdown
- Si el nodo tiene subárbol derecho, el sucesor es el mínimo de ese subárbol.
- Si no, suba hasta llegar a un padre desde su hijo **izquierdo**.
:::

:::{admonition} Solución general
:class: dropdown
- Sucesor de $7$: la raíz $8$. $7$ no tiene subárbol derecho y es hijo izquierdo de $8$.
- Sucesor de $9$: el $10$ hoja. Es el mínimo del subárbol derecho de $9$.
- Sucesor de $10$ (hijo de $8$): $12$, el mínimo de su subárbol derecho.
- Sucesor de $12$: no tiene (`nil`). Al subir siempre se llega desde un hijo derecho.

Con llaves repetidas, «la menor llave mayor que $k$» no basta para decir **qué nodo** es: `TREE-SUCCESSOR` devuelve el siguiente nodo en inorden.
:::

### Ejercicio 5

En el árbol de la sección 1 del material de estudio (raíz $24$), encuentre el mínimo, el máximo, el sucesor de $10$, de $29$ y de $42$, y el predecesor de $24$ y de $32$.

:::{admonition} Pistas
:class: dropdown
- El predecesor es el simétrico del sucesor: máximo del subárbol izquierdo, o subir hasta llegar a un padre desde su hijo **derecho**.
:::

:::{admonition} Solución general
:class: dropdown
Mínimo $1$, máximo $53$. Sucesor de $10$: {{GEN:ex5-s10}}; de $29$: {{GEN:ex5-s29}}; de $42$: {{GEN:ex5-s42}}. Predecesor de $24$: {{GEN:ex5-p24}}; de $32$: {{GEN:ex5-p32}}.
:::

### Ejercicio 6

Siga `TREE-INSERT` para insertar $6$ y luego $11$ en el árbol de la sección 4 del material de estudio (después de haber insertado $5$). Para cada uno, dé los valores que toman $y$ y $x$ en cada iteración del ciclo.

:::{admonition} Pistas
:class: dropdown
- $y$ siempre va un paso atrás de $x$; el ciclo termina cuando $x$ es `nil`.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:ex6-sol}}
:::

### Ejercicio 7

En el árbol de la sección 1 del material de estudio (raíz $24$), elimine, en este orden, $1$, $4$ y $24$. Diga qué caso es cada uno y dibuje el árbol final.

:::{admonition} Pistas
:class: dropdown
- Después de quitar $1$, ¿cuántos hijos le quedan a $4$?
- Para $24$: busque su sucesor, el mínimo del subárbol derecho.
:::

:::{admonition} Solución general
:class: dropdown
$1$ es hoja (caso 1). Luego $4$ tiene un solo hijo, $5$ (caso 2): $5$ sube a su lugar. $24$ tiene dos hijos (caso 3): su sucesor es $26$, que se separa del árbol, y su llave reemplaza a $24$.

{{GEN:ex7-sol}}
:::

### Ejercicio 8

Si se insertan $n$ llaves distintas en un ABB vacío, en orden **ascendente**, ¿cuál es la altura y cuántas comparaciones se hacen en total? ¿En qué orden habría que insertar $1, \dots, 7$ para obtener un árbol lleno?

:::{admonition} Pistas
:class: dropdown
- La $i$-ésima llave se compara con las $i - 1$ anteriores.
- Para el árbol lleno: la raíz debe ser la mediana.
:::

:::{admonition} Solución general
:class: dropdown
Cada llave nueva es la mayor y baja por la derecha pasando por todas las anteriores: $0 + 1 + \cdots + (n - 1) = n(n-1)/2$ comparaciones, y el árbol es una cadena de altura $n$. Para un árbol lleno con $1, \dots, 7$: $4, 2, 6, 1, 3, 5, 7$ (o cualquier orden que inserte $4$ primero y luego cada mediana antes que sus mitades).
:::

### Ejercicio 9

Escriba en pseudocódigo `SUCESOR(T, k)` y `PREDECESOR(T, k)` **sin** usar el apuntador al padre, y `CONTAR-EN-RANGO(x, a, b)` (cuántas llaves del subárbol con raíz $x$ están entre $a$ y $b$). `CONTAR-EN-RANGO` no debe recorrer subárboles que estén completamente fuera del rango.

:::{admonition} Pistas
:class: dropdown
- Sin apuntador al padre, el sucesor se encuentra bajando desde la raíz: cada vez que se baja a la izquierda, ese nodo es un candidato a sucesor.
- En `CONTAR-EN-RANGO`, si la llave del nodo es menor que $a$, el subárbol izquierdo no aporta nada.
:::

:::{admonition} Solución general
:class: dropdown
`SUCESOR` y `PREDECESOR` bajan por un solo camino: $O(h)$. `CONTAR-EN-RANGO` visita los nodos del rango más los caminos hacia sus bordes: $O(h + m)$, con $m$ el número de llaves que cuenta. En el árbol de la sección 1, `CONTAR-EN-RANGO` con $a = 10$ y $b = 30$ da $11$.
:::

### Ejercicio 10

Implemente un árbol binario de búsqueda genérico con buscar, mínimo, máximo, sucesor, predecesor, insertar y eliminar, siguiendo el pseudocódigo del material de estudio (con apuntador al padre). Pruébelo con los árboles de los Ejercicios 2 y 7.

---

*Material adaptado del material original de los profesores Oscar Bedoya y Andrés Aristizábal.*
