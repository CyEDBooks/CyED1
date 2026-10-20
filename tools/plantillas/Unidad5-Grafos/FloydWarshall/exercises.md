---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Floyd-Warshall: Ejercicios"
---

# Floyd-Warshall: Ejercicios

Use esta página después de leer el [material de estudio de Floyd-Warshall](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Aplique el algoritmo de Floyd-Warshall a cada grafo. Muestre las matrices $W$ y $P$ después de cada pivote y encuentre los valores mínimos y los recorridos que se piden.

{{GEN:fw-enunciados-1}}

:::{admonition} Pistas
:class: dropdown
- En $W_0$ hay $\infty$ donde no hay arco y $0$ en la diagonal; el grafo es dirigido: $W[a][b] \neq W[b][a]$.
- Con el pivote $k$ solo pueden mejorar las casillas $(i, j)$ con $W[i][k]$ y $W[k][j]$ finitos.
- Para el recorrido, inserte pivotes hasta que todos los tramos digan «ir directo».
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:fw-soluciones-1}}
:::

### Ejercicio 2

Aplique el algoritmo de Floyd-Warshall a cada grafo y encuentre los valores mínimos y los recorridos que se piden.

{{GEN:fw-enunciados-2}}

:::{admonition} Pistas
:class: dropdown
- Escriba primero $W_0$ y $P_0$ a partir del grafo.
- Cuando un vértice no tiene arcos de entrada, su columna se queda en $\infty$ (salvo la diagonal).
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:fw-soluciones-2}}
:::

### Ejercicio 3

En el Ejemplo 1, cambie el orden de los pivotes a $d, c, b, a$. ¿Cambia $W_4$? ¿Cambia $P_4$?

:::{admonition} Pistas
:class: dropdown
- $W_4$ guarda valores mínimos, y el valor mínimo entre dos vértices no depende de cómo se calcule.
- $P_4$ guarda **un** pivote por casilla. ¿Un mismo recorrido mínimo puede describirse con pivotes distintos?
:::

:::{admonition} Solución general
:class: dropdown
$W_4$ no cambia: sus casillas son los valores mínimos, que son únicos. $P_4$ puede cambiar: por ejemplo, el recorrido $b \to d \to a \to c$ se puede registrar en $P[b][c]$ con el pivote $d$ o con el pivote $a$, según cuál se pruebe primero. En ambos casos se reconstruye el mismo recorrido.
:::

### Ejercicio 4

Agregue al grafo del Ejemplo 1 el arco $c \to a$ con peso $-8$. Corra el algoritmo y muestre que aparece un valor negativo en la diagonal. ¿Qué circuito lo produce?

:::{admonition} Pistas
:class: dropdown
- Busque un circuito que use el arco nuevo.
- Sume los pesos de $a \to c \to a$.
:::

:::{admonition} Solución general
:class: dropdown
El circuito $a \to c \to a$ cuesta $4 + (-8) = -4 < 0$. Con el pivote $a$ ya se obtiene $W[c][c] = -8 + 4 = -4$, y con el pivote $c$, $W[a][a] = 4 + (-8) = -4$. Un valor negativo en la diagonal indica un circuito de costo negativo, y los demás valores de $W$ dejan de tener sentido como «valor mínimo».
:::

### Ejercicio 5

Escriba el algoritmo de **Warshall** (matriz de conectividad) como una modificación de Floyd-Warshall: ¿qué reemplaza a la suma? ¿Y al mínimo? Pruébelo con el grafo del Ejemplo 1 y verifique que la matriz de conectividad tiene solo unos.

:::{admonition} Pistas
:class: dropdown
- En Warshall cada casilla dice si **hay** camino, no cuánto cuesta.
:::

:::{admonition} Solución general
:class: dropdown
La suma $W[i][k] + W[k][j]$ se reemplaza por $W[i][k] \wedge W[k][j]$ y el mínimo por $\vee$. En el Ejemplo 1 todos los vértices están en el circuito $a \to b \to d \to a$ o llegan a él y salen de él ($a \to c \to d$), así que de cualquier vértice se llega a cualquier otro: la matriz de conectividad tiene solo unos.
:::

### Ejercicio 6

Aplicar el algoritmo de Floyd-Warshall. Mostrar las matrices $W_0, W_1, W_2, W_3, W_4, W_5$, $P_0, P_1, P_2, P_3, P_4, P_5$. Encuentre el valor mínimo y el recorrido entre $a$ y $e$, y entre $d$ y $b$.

{{GEN:fig-fw-open}}

---

*Material adaptado del material original del profesor Oscar Bedoya.*
