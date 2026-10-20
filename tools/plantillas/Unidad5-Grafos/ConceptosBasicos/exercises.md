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

Clasifique cada grafo como simple, multigrafo o pseudografo.

{{GEN:fig-cl}}

:::{admonition} Pistas
:class: dropdown
- Busque primero bucles; después, pares de vértices unidos por más de una arista.
:::

:::{admonition} Solución general
:class: dropdown
- a) Simple: ni bucles ni aristas paralelas.
- b) Pseudografo: tiene dos bucles.
- c) Multigrafo: hay dos aristas paralelas, y no tiene bucles.
- d) Pseudografo: tiene un bucle y un par de aristas paralelas.
:::

### Ejercicio 2

Indique el grado de cada vértice.

{{GEN:fig-g2}}

:::{admonition} Pistas
:class: dropdown
- Cada bucle suma $2$; cada arista paralela cuenta por separado.
- Verifique con *handshaking*: la suma tiene que ser par.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:g2-sol}}. La suma es ${{GEN:g2-suma}}$, así que el grafo tiene ${{GEN:g2-e}}$ aristas.
:::

### Ejercicio 3

Indique $e$ y el grado de cada vértice en cada grafo.

{{GEN:fig-hs23}}

:::{admonition} Pistas
:class: dropdown
- Cuente $e$ directamente y verifique que la suma de los grados es $2e$.
:::

:::{admonition} Solución general
:class: dropdown
- a) {{GEN:hs2-sol}}.
- b) {{GEN:hs3-sol}}.
:::

### Ejercicio 4

Dibuje un grafo no dirigido **simple** con $4$ vértices $u, v, w, x$ cuyos grados sean $\delta(u) = 3$, $\delta(v) = 2$, $\delta(w) = 3$, $\delta(x) = 2$. Luego, uno con $5$ vértices $u, v, w, x, y$ y grados $\delta(u) = 3$, $\delta(v) = 3$, $\delta(w) = 4$, $\delta(x) = 2$, $\delta(y) = 2$.

:::{admonition} Pistas
:class: dropdown
- Primero calcule con *handshaking* cuántas aristas debe tener.
- Un vértice de grado $n - 1$ es vecino de todos los demás: empiece por él.
:::

:::{admonition} Solución general
:class: dropdown
Con $4$ vértices hay $e = 10/2 = 5$ aristas; con $5$ vértices, $e = 14/2 = 7$. Una solución para cada uno:

{{GEN:fig-dib}}
:::

### Ejercicio 5

Indique la cantidad de aristas de un grafo si los grados de sus vértices son:

- $3, 3, 3, 3, 2$
- $1, 2, 3, 4, 4$
- $0, 1, 2, 2, 3$
- $4, 5, 5, 2, 2$
- $1, 3, 2, 2, 2, 2, 4$

:::{admonition} Pistas
:class: dropdown
- Por *handshaking*, $e$ es la mitad de la suma de los grados.
:::

:::{admonition} Solución general
:class: dropdown
$7$, $7$, $4$, $9$ y $8$ aristas.
:::

### Ejercicio 6

Indique $\delta^-(v)$ y $\delta^+(v)$ para cada vértice de cada grafo dirigido.

{{GEN:fig-dirs}}

:::{admonition} Pistas
:class: dropdown
- Un bucle suma $1$ al grado de entrada y $1$ al de salida.
- Verifique: la suma de los grados de entrada es igual a la suma de los de salida, y las dos son el número de aristas.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:dirs-sol}}
:::

### Ejercicio 7

Indique cuáles de los siguientes grafos son bipartitos. Muestre $V_1$ y $V_2$ para los que lo sean.

{{GEN:fig-bip}}

:::{admonition} Pistas
:class: dropdown
- Ponga un vértice en $V_1$, todos sus vecinos en $V_2$, los vecinos de esos en $V_1$, y así. Si dos vecinos quedan en el mismo conjunto, no es bipartito.
- Un triángulo nunca es bipartito.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:fig-bip-sol}}

- a) Sí: $V_1 = \{a, d\}$, $V_2 = \{b, c\}$.
- b) Sí: $V_1 = \{a, c\}$, $V_2 = \{b, d, e\}$.
- c) No: $a$, $b$ y $c$ forman un triángulo.
- d) Sí: $V_1 = \{a, b, d, e\}$, $V_2 = \{c\}$.
:::

### Ejercicio 8

Si el grafo simple $G$ tiene $v$ vértices y $e$ aristas, ¿cuántas aristas tiene $\bar{G}$? Úselo para calcular cuántas aristas tiene el complementario de $C_6$ y el de $K_{3,3}$.

:::{admonition} Pistas
:class: dropdown
- $G \cup \bar{G} = K_v$, y $G$ y $\bar{G}$ no comparten aristas.
:::

:::{admonition} Solución general
:class: dropdown
$\dfrac{v(v-1)}{2} - e$. $\bar{C_6}$ tiene $15 - 6 = 9$ aristas, y $\bar{K_{3,3}}$ tiene $15 - 9 = 6$ (son dos triángulos separados).
:::

### Ejercicio 9

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

### Ejercicio 10

Muestre que en todo grafo simple con al menos $2$ vértices hay **dos vértices con el mismo grado**.

:::{admonition} Pistas
:class: dropdown
- Con $n$ vértices, los grados posibles van de $0$ a $n - 1$: son $n$ valores.
- ¿Pueden aparecer a la vez un vértice de grado $0$ y uno de grado $n - 1$?
:::

:::{admonition} Solución general
:class: dropdown
Un vértice de grado $n - 1$ es vecino de todos, así que no puede haber uno de grado $0$. Entonces los $n$ grados caen en a lo sumo $n - 1$ valores y, por el principio del palomar, dos vértices comparten grado.
:::

### Ejercicio 11

Sea $G$ un grafo dirigido con $n$ vértices en el que, para cada par de vértices distintos $u, v$, existe **exactamente una** de las aristas $(u, v)$ o $(v, u)$ (un **torneo**). Muestre que $\sum_v \big(\delta^+(v)\big)^2 = \sum_v \big(\delta^-(v)\big)^2$.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
