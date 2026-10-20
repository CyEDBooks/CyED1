---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Isomorfismo, planaridad y coloración: Ejercicios"
---

# Isomorfismo, planaridad y coloración: Ejercicios

Use esta página después de leer el [material de estudio](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

¿Cuántos grafos simples **no isomorfos** de $3$ vértices hay? ¿Y de $4$ vértices con exactamente $3$ aristas? Dibújelos.

:::{admonition} Pistas
:class: dropdown
- Clasifique por número de aristas.
- Con $4$ vértices y $3$ aristas, piense en la secuencia de grados.
:::

:::{admonition} Solución general
:class: dropdown
Con $3$ vértices hay $4$: con $0$, $1$, $2$ y $3$ aristas (uno por cada número de aristas). Con $4$ vértices y $3$ aristas hay $3$: el triángulo más un vértice aislado (grados $2, 2, 2, 0$), el camino $P_4$ (grados $1, 2, 2, 1$) y la estrella $K_{1,3}$ (grados $3, 1, 1, 1$).
:::

### Ejercicio 2

Muestre que un grafo plano, simple y conexo tiene algún vértice de grado **menor o igual que 5**.

:::{admonition} Pistas
:class: dropdown
- Suponga que todos los vértices tienen grado al menos $6$ y use *handshaking*.
- Compare con $e \le 3v - 6$.
:::

:::{admonition} Solución general
:class: dropdown
Si todos los grados fueran $\ge 6$, por *handshaking* $2e \ge 6v$, es decir, $e \ge 3v$. Pero el corolario de la fórmula de Euler dice $e \le 3v - 6 < 3v$. Contradicción.
:::

### Ejercicio 3

Calcule el número cromático del siguiente grafo. Aplique la coloración voraz (orden: de mayor a menor grado; empates en orden alfabético) y compare.

{{GEN:fig-ex-color}}

:::{admonition} Pistas
:class: dropdown
- Busque un triángulo: da una cota inferior.
- El borde es un ciclo de longitud $7$ (impar).
:::

:::{admonition} Solución general
:class: dropdown
$\chi = {{GEN:ex-chi}}$. Una coloración: {{GEN:ex-chi-sol}}.

Coloración voraz ({{GEN:ex-greedy-n}} colores): {{GEN:ex-greedy}}.
:::

### Ejercicio 4

Encuentre un grafo y un orden de sus vértices para el cual la coloración voraz use **más** colores que $\chi(G)$.

:::{admonition} Pistas
:class: dropdown
- Basta con un grafo bipartito ($\chi = 2$).
- Haga que dos vértices no adyacentes reciban colores «equivocados» al principio.
:::

:::{admonition} Solución general
:class: dropdown
El camino $a - b - c - d$ con el orden $a, d, b, c$: $a$ y $d$ reciben el color 1; $b$ (vecino de $a$) recibe el 2; $c$ es vecino de $b$ (color 2) y de $d$ (color 1) y recibe el **3**. Pero $\chi = 2$.
:::

### Ejercicio 5

Determine si el grafo de Petersen es plano y calcule su número cromático. Justifique sus respuestas.

---

*Material adaptado del material original de los profesores Oscar Bedoya y Juan Marcos Caicedo Mejía.*
