---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "BFS: Ejercicios"
---

# BFS: Ejercicios

Use esta página después de leer el [material de estudio de BFS](index.md). Cada ejercicio trae una **solución general** (el resultado y el camino a grandes rasgos) y **pistas**. Intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Muestre los valores $d$ y $\pi$ que resultan de correr BFS sobre el grafo del Ejemplo 2 (estaciones) cuando el origen es el vértice $u$. Las listas de adyacencia están en orden alfabético.

:::{admonition} Pistas
:class: dropdown
- Inicialmente solo $u$ es gris y $Q = \langle u \rangle$.
- Los vecinos de $u$ en orden alfabético son $t$, $x$, $y$: los tres quedan con $d = 1$.
- Lleve la cola en cada paso; un vértice gris no se vuelve a descubrir.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:ex1-sol}}

El vértice más lejano es $v$, con $v.d = 5$. Siguiendo los predecesores desde $v$ se obtiene el camino $u \to t \to w \to s \to r \to v$. $w$ queda como hijo de $t$ (y no de $x$) porque $t$ sale de la cola antes que $x$.
:::

### Ejercicio 2

A partir del siguiente mapa del sur de Alemania, aplique BFS empezando en Frankfurt (Fra) y obtenga el árbol BF. Revise los vecinos en este orden: Fra, Man, Wür, Kas, Kar, Erf, Nür, Aug, Stu, Mün.

{{GEN:fig-de}}

:::{admonition} Pistas
:class: dropdown
- Ignore las distancias en kilómetros: BFS cuenta **aristas**, no kilómetros.
- Los tres vecinos de Frankfurt quedan en el nivel $1$.
- München se puede alcanzar desde Kassel, Nürnberg o Augsburg. ¿Cuál de ellos sale primero de la cola?
:::

:::{admonition} Solución general
:class: dropdown
Orden en que los vértices salen de la cola: {{GEN:ex2-orden}}.

{{GEN:fig-de-sol}}

München queda en el nivel $2$ como hijo de Kassel: es el primero de sus vecinos que sale de la cola. En kilómetros ese no es el camino más corto (Fra–Kas–Mün suma $675$ km); para eso hace falta el algoritmo de Dijkstra.
:::

### Ejercicio 3

Muestre los valores $d$ y $\pi$ que resultan de correr BFS sobre el grafo dirigido del Ejemplo 4, ahora con origen en el vértice $1$.

{{GEN:fig-ex3}}

:::{admonition} Pistas
:class: dropdown
- Desde $1$ salen aristas hacia $2$ y $4$.
- Un vértice al que no se puede llegar siguiendo el sentido de las flechas queda con $d = \infty$.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:ex3-sol}}

Los vértices $3$ y $6$ no son alcanzables desde $1$: ninguna arista entra a $3$, y a $6$ solo se llega desde $3$ (o desde sí mismo).
:::

### Ejercicio 4

En el grafo del Ejemplo 3, corra BFS desde $3$ con las listas de adyacencia en orden **decreciente**. Muestre que el árbol BF cambia, pero los valores de $d$ no.

{{GEN:fig-ex4}}

:::{admonition} Pistas
:class: dropdown
- Ahora los vecinos de $3$ se revisan como $4, 2$; los de $2$, como $5, 4, 3, 1$.
- Fíjese en quién descubre a $5$.
:::

:::{admonition} Solución general
:class: dropdown
Con orden decreciente, $4$ sale de la cola antes que $2$, así que $5$ se descubre desde $4$: $5.\pi = 4$ (antes era $2$). Las distancias no cambian: $d = (2, 1, 0, 1, 2)$ para $1, \dots, 5$. El árbol BF depende del orden de las listas; las distancias $\delta(s, v)$, no.
:::

### Ejercicio 5

Modifique BFS para que decida si un grafo no dirigido y conexo es **bipartito**. Justifique por qué su algoritmo es correcto y analice su complejidad.

---

*Material adaptado del material original de los profesores Andrés Aristizábal, Marlon Gómez y Oscar Bedoya.*
