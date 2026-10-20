---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Grafos, conceptos básicos: Ejercicios"
---

# Grafos, conceptos básicos: Ejercicios

Use esta página después de leer el [material de estudio](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Dibuje un grafo no dirigido **simple** con $4$ vértices $u, v, w, x$ cuyos grados sean $\delta(u) = 3$, $\delta(v) = 2$, $\delta(w) = 3$, $\delta(x) = 2$. Luego, uno con $5$ vértices y grados $3, 3, 4, 2, 2$.

:::{admonition} Pistas
:class: dropdown
- Primero verifique con *handshaking* cuántas aristas debe tener.
- Un vértice de grado $n - 1$ es vecino de todos los demás: empiece por él.
:::

:::{admonition} Solución general
:class: dropdown
- $4$ vértices: $e = 10/2 = 5$. Por ejemplo $u-v$, $u-w$, $u-x$, $v-w$, $w-x$ ($K_4$ sin la arista $\{v, x\}$).
- $5$ vértices: $e = 14/2 = 7$. El de grado $4$ es vecino de todos; con eso los demás quedan con grados pendientes $2, 2, 1, 1$, que se completan con un camino de $3$ aristas entre ellos, por ejemplo $\{u, v\}$, $\{u, x\}$ y $\{v, y\}$, si los de grado $3$ son $u$ y $v$.
:::

### Ejercicio 2

En el grafo de $5$ vértices del Ejercicio 1, ¿cuántos vértices son de grado impar? ¿Se puede modificar el grafo (agregando o quitando aristas) para que tenga **solo un** vértice de grado impar?

:::{admonition} Pistas
:class: dropdown
- Agregar o quitar una arista cambia la paridad del grado de **sus dos** extremos.
- Use el corolario del teorema de *handshaking*.
:::

:::{admonition} Solución general
:class: dropdown
Hay dos vértices de grado impar (los de grado $3$). **No** se puede dejar uno solo: todo grafo no dirigido tiene un número par de vértices de grado impar. Cada arista que se agrega o se quita cambia la paridad de dos vértices a la vez, así que la cantidad de vértices impares cambia en $-2$, $0$ o $+2$.
:::

### Ejercicio 3

¿Cuántas aristas tiene $\bar{G}$ si el grafo simple $G$ tiene $v$ vértices y $e$ aristas?

:::{admonition} Pistas
:class: dropdown
- $G \cup \bar{G} = K_v$, y $G$ y $\bar{G}$ no comparten aristas.
:::

:::{admonition} Solución general
:class: dropdown
$\dfrac{v(v-1)}{2} - e$.
:::

### Ejercicio 4

¿Cuántos vértices y cuántas aristas tienen $K_n$, $C_n$, $W_n$ y $K_{m,n}$? ¿Cuáles de ellos son bipartitos?

:::{admonition} Pistas
:class: dropdown
- Use *handshaking* con el grado de cada vértice.
- Busque ciclos de longitud impar.
:::

:::{admonition} Solución general
:class: dropdown
| Grafo | Vértices | Aristas | ¿Bipartito? |
|---|---|---|---|
| $K_n$ | $n$ | $n(n-1)/2$ | solo si $n \le 2$ |
| $C_n$ | $n$ | $n$ | sí si $n$ es par |
| $W_n$ | $n + 1$ | $2n$ | nunca (el centro y dos vecinos del ciclo forman un triángulo) |
| $K_{m,n}$ | $m + n$ | $mn$ | siempre |
:::

### Ejercicio 5

Muestre que en todo grafo simple con al menos $2$ vértices hay **dos vértices con el mismo grado**.

:::{admonition} Pistas
:class: dropdown
- Con $n$ vértices, los grados posibles van de $0$ a $n - 1$: son $n$ valores.
- ¿Pueden aparecer a la vez un vértice de grado $0$ y uno de grado $n - 1$?
- Principio del palomar.
:::

:::{admonition} Solución general
:class: dropdown
Un vértice de grado $n - 1$ es vecino de todos, así que no puede haber uno de grado $0$. Entonces los $n$ grados caen en a lo sumo $n - 1$ valores ($\{0, \dots, n-2\}$ o $\{1, \dots, n-1\}$) y, por el principio del palomar, dos vértices comparten grado.
:::

### Ejercicio 6

Sea $G$ un grafo dirigido con $n$ vértices en el que, para cada par de vértices distintos $u, v$, existe **exactamente una** de las aristas $(u, v)$ o $(v, u)$ (un **torneo**). Muestre que $\sum_v \big(\delta^+(v)\big)^2 = \sum_v \big(\delta^-(v)\big)^2$.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
