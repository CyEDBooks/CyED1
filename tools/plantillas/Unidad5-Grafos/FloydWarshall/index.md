---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 5: Algoritmo de Floyd-Warshall"
---

# Unidad 5: Algoritmo de Floyd-Warshall

## 1. El problema

{{GEN:fig-ej1}}

**¿Cuál es el valor mínimo para ir de cada vértice a cada uno de los demás, y por qué recorrido?** No se pide desde un solo origen: se pide la **tabla completa**, como la tabla de distancias entre ciudades de un atlas de carreteras.

Pruebe con dos pares antes de seguir.

:::{admonition} ¿Valor mínimo de $a$ a $d$? ¿Y de $b$ a $c$?
:class: dropdown
- De $a$ a $d$: por $b$ cuesta $3 + 5 = 8$; por $c$ cuesta $4 + 3 = 7$. El mínimo es $7$, con el recorrido $a \to c \to d$.
- De $b$ a $c$ no hay arista. Hay que ir $b \to d \to a \to c$: $5 + 8 + 4 = 17$.
:::

Una idea: correr **Dijkstra desde cada vértice**. Funciona si todos los pesos son no negativos, pero ya se vio que Dijkstra puede fallar con un solo peso negativo. Se necesita un método que calcule todos los pares a la vez y que acepte pesos negativos (siempre que no haya circuitos de costo negativo).

### ¿Entendimos el problema?

| | |
|---|---|
| **Entradas** | Un grafo dirigido con pesos (pueden ser negativos), sin circuitos de costo negativo. |
| **Salidas** | Una matriz $W$ con $W[i][j]$ = valor mínimo de $i$ a $j$, y una matriz $P$ para reconstruir cada recorrido. |

## 2. El método

**Pivote.** Para ir de $i$ a $j$, se prueba si **pasar por un vértice $k$** (el pivote) es más barato que lo que se conoce:

$$
W[i][j] \;\leftarrow\; \min\big(W[i][j],\; W[i][k] + W[k][j]\big)
$$

**Algoritmo de Floyd-Warshall.** Se toma cada vértice como pivote, uno por uno. Con cada pivote se revisan todas las casillas de la matriz. Si pasar por el pivote mejora una casilla $(i, j)$, se actualiza $W[i][j]$ y se guarda el pivote en $P[i][j]$.

- $W_0$: los pesos de las aristas; $0$ en la diagonal y $\infty$ donde no hay arista.
- $P_0$: en cada casilla $(i, j)$, el vértice $j$, que significa «ir directo de $i$ a $j$».
- $W_k$, $P_k$: las matrices después de usar el pivote número $k$.

### Ejemplo 1

El grafo de la sección 1. Orden de los pivotes: $a, b, c, d$. En el grafo se resalta el pivote de cada paso.

{{GEN:ej1}}

### Leer el recorrido en $P$

$W_4$ da los valores mínimos. Para el recorrido se usa $P_4$: si $P[i][j] = j$, se va directo; si $P[i][j] = k \neq j$, el recorrido pasa por $k$, y se repite el proceso con $(i, k)$ y con $(k, j)$.

¿Cuál es el valor mínimo entre $a$ y $d$? ¿Cuál es el recorrido con el que se obtiene ese valor mínimo?

{{GEN:ruta-ad}}

¿Cuál es el valor mínimo entre $b$ y $c$?

{{GEN:ruta-bc}}

¿Cuál es el valor mínimo entre $c$ y $b$?

{{GEN:ruta-cb}}

> **¿Es lo mismo ir de $b$ a $c$ que de $c$ a $b$?** No: el grafo es dirigido. De $b$ a $c$ cuesta $17$ y de $c$ a $b$ cuesta $14$.

### Ejemplo 2

Floyd-Warshall acepta pesos **negativos**, siempre que no haya un circuito de costo negativo.

{{GEN:fig-ej2}}

{{GEN:ej2}}

{{GEN:ruta2}}

## 3. El algoritmo

```text
FLOYD-WARSHALL(W)            // W: matriz n × n de pesos
1  n = número de filas de W
2  P = matriz n × n con P[i][j] = j
3  for k = 1 to n            // pivote
4      for i = 1 to n
5          for j = 1 to n
6              if W[i][k] + W[k][j] < W[i][j]
7                  W[i][j] = W[i][k] + W[k][j]
8                  P[i][j] = k
9  return W, P
```

### Complejidad

> **¿Cuántas veces se ejecuta la línea 6?**

:::{admonition} Respuesta
:class: dropdown
Una vez por cada combinación de $k$, $i$ y $j$: $n \cdot n \cdot n = n^3$ veces.
:::

$$
T(n) = \Theta(n^3)
$$

El espacio es $\Theta(n^2)$: las matrices se pueden actualizar en el mismo lugar, sin guardar $W_0, W_1, \dots$ por separado.

> **¿Por qué se puede sobrescribir $W$ sin dañar el cálculo?** Durante el pivote $k$, la fila $k$ y la columna $k$ no cambian: $W[k][k] = 0$, así que $W[i][k] + W[k][k] = W[i][k]$ nunca mejora a $W[i][k]$.

Comparación con correr Dijkstra $n$ veces: con arreglos cuesta $n \cdot O(n^2) = O(n^3)$, lo mismo, pero solo sirve con pesos no negativos.

### Circuitos de costo negativo

Si después de correr el algoritmo algún valor de la diagonal queda **negativo**, $W[i][i] < 0$, hay un circuito de costo negativo que pasa por $i$: dando vueltas en él, el costo baja sin límite y «el camino más barato» no existe.

## 4. Formalización

- Numere los vértices $v_1, \dots, v_n$. Sea $d_{ij}^{(k)}$ el valor mínimo de un camino de $v_i$ a $v_j$ cuyos vértices **intermedios** están todos en $\{v_1, \dots, v_k\}$. Entonces

$$
d_{ij}^{(0)} = w_{ij}
\qquad
d_{ij}^{(k)} = \min\big(d_{ij}^{(k-1)},\; d_{ik}^{(k-1)} + d_{kj}^{(k-1)}\big) \quad (k \ge 1)
$$

- La razón: un camino mínimo con intermedios en $\{v_1, \dots, v_k\}$ o **no** usa $v_k$ (y su valor es $d_{ij}^{(k-1)}$), o lo usa **una sola vez** (si no hay circuitos negativos) y se parte en dos caminos mínimos con intermedios en $\{v_1, \dots, v_{k-1}\}$.
- $W_k$ es la matriz $\big(d_{ij}^{(k)}\big)$ y $W_n$ contiene los valores mínimos entre todos los pares.
- Es un algoritmo de **programación dinámica**: construye la solución de cada subproblema ($k$) a partir de la del anterior ($k-1$).
- Con valores booleanos (hay camino / no hay camino) en lugar de pesos, la misma recurrencia es el **algoritmo de Warshall** para la matriz de conectividad (ver [Representación y conectividad](../RepresentacionConectividad/index.md)).

## Ejercicios

Practique con los [ejercicios de Floyd-Warshall](exercises.md).

## Fuentes

- Bedoya, O. *Grafos: algoritmo de Floyd-Warshall*. Diapositivas del curso, Universidad del Valle.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Sección 25.2.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
