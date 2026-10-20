---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 5: Algoritmo de Dijkstra"
---

# Unidad 5: Algoritmo de Dijkstra

## 1. El problema

En este grafo cada arista tiene un **peso** (un costo, una distancia, un tiempo).

{{GEN:fig-problema}}

**¿Cuál es el costo mínimo para ir desde $a$ hasta $f$?**

:::{admonition} Algunos caminos de $a$ a $f$
:class: dropdown
- $a \to b \to d \to f$: $2 + 1 + 2 = 5$
- $a \to c \to d \to f$: $1 + 3 + 2 = 6$
- $a \to c \to e \to f$: $1 + 4 + 2 = 7$

El mínimo es $5$. Con $6$ vértices se pueden listar todos los caminos; con miles de vértices, no.
:::

**Grafo con pesos.** Cada arista $(u, v)$ tiene un valor $w(u, v)$. La **longitud** (o costo) de un camino es la **suma** de los pesos de sus aristas, no el número de aristas.

### ¿Sirve BFS?

BFS encuentra el camino con **menos aristas**. Pruébelo en este grafo, desde $s$ hasta $t$:

{{GEN:fig-bfs-falla}}

:::{admonition} ¿Qué camino da BFS? ¿Es el más barato?
:class: dropdown
BFS descubre $t$ directamente desde $s$ (una arista) y devuelve $s \to t$, que cuesta $10$. Pero $s \to a \to t$ tiene dos aristas y cuesta $1 + 1 = 2$. **Menos aristas no significa menos costo.**
:::

### ¿Entendimos el problema?

| | |
|---|---|
| **Entradas** | Un grafo dirigido con pesos **no negativos** y un vértice origen $s$. |
| **Salidas** | Para cada vértice $v$: el costo mínimo de un camino de $s$ a $v$ y el vértice anterior a $v$ en ese camino. |

Traza a mano con el grafo de la sección 1: el costo mínimo de $a$ a $f$ es $5$ y el anterior a $f$ es $d$; el de $a$ a $d$ es $3$ y el anterior a $d$ es $b$.

## 2. El método

**Algoritmo de Dijkstra.** Cada vértice lleva una etiqueta $[\text{valor acumulado}, \text{predecesor}]$. En cada paso, el vértice **no permanente** con **menor valor acumulado** se vuelve **permanente**, y se reetiquetan sus vecinos cuando llegar a ellos a través de él cuesta menos.

### Ejemplo 1

El grafo de la sección 1, desde $a$. Los vértices en rojo son permanentes; las flechas en azul van del predecesor al vértice.

{{GEN:ej1}}

Ahora se leen los caminos. **Para encontrar el camino de costo mínimo** se parte del destino y se siguen los predecesores hasta llegar al origen.

{{GEN:ej1-camino-d}}

{{GEN:ej1-camino-f}}

Todos los resultados:

{{GEN:ej1-final}}

### Ejemplo 2

Aplique el algoritmo de Dijkstra para encontrar el camino más corto entre Bogotá y Buenos Aires. El grafo es dirigido: cada tramo se recorre solo en el sentido de la flecha. Las abreviaturas son Bog (Bogotá), Lim (Lima), Qui (Quito), Paz (La Paz), Asu (Asunción) y BA (Buenos Aires).

{{GEN:fig-sa}}

{{GEN:ej2}}

{{GEN:ej2-camino}}

El camino más corto es Bogotá $\to$ Quito $\to$ Lima $\to$ Asunción $\to$ Buenos Aires, con longitud $13$.

### Ejemplo 3

El mapa del sur de Alemania del ejercicio de BFS, ahora con las distancias en kilómetros. Origen: Frankfurt.

{{GEN:fig-de}}

{{GEN:ej3}}

{{GEN:ej3-final}}

> **¿Qué cambió respecto a BFS?** Con BFS, München quedaba como hijo de Kassel: es el camino con menos tramos (dos), pero cuesta $675$ km. Dijkstra encuentra Frankfurt $\to$ Würzburg $\to$ Nürnberg $\to$ München, con tres tramos y $487$ km.

## 3. El algoritmo

El pseudocódigo del curso (Rosen, sección 10.6), para un grafo $G$ conexo con pesos positivos, desde $a$ hasta $z$:

```text
Procedimiento Dijkstra(G: grafo ponderado conexo y todos los pesos positivos)
    para i = 1 hasta n
        L(v_i) = ∞
    L(a) = 0
    S = ∅
    mientras z ∉ S
        u = vértice con L(u) mínima entre los vértices que no están en S
        S = S ∪ {u}
        para todos los vértices v que no están en S
            si L(u) + w(u, v) < L(v)
                L(v) = L(u) + w(u, v)
                pred(v) = u
```

$L(v)$ es el valor acumulado de la etiqueta y $S$ es el conjunto de vértices permanentes. Si se quiere la distancia a **todos** los vértices, se cambia la condición del `mientras` por «mientras $S \neq V$».

### Complejidad

> **¿Cuántas veces se busca el mínimo, y cuánto cuesta cada búsqueda?**

:::{admonition} Respuesta
:class: dropdown
Se busca una vez por vértice ($|V|$ veces). Si las etiquetas están en un arreglo, cada búsqueda revisa hasta $|V|$ vértices: $O(V^2)$ en total. Revisar los vecinos suma $O(E)$ en todo el algoritmo. Total: $O(V^2 + E) = O(V^2)$.
:::

Con una **cola de prioridad** (un *heap*, Unidad 3), obtener el mínimo cuesta $O(\log V)$ y cada reetiquetado también. El total queda en $O((V + E) \log V)$, que es mejor cuando el grafo tiene pocas aristas.

### Cuando hay pesos negativos

La regla «una etiqueta permanente no cambia nunca» depende de que los pesos sean **no negativos**. Con un solo peso negativo puede fallar:

{{GEN:fig-neg}}

{{GEN:neg}}

Para grafos con pesos negativos (y sin circuitos de costo negativo) se usan otros algoritmos, como Floyd-Warshall o Bellman-Ford.

## 4. Formalización

- El algoritmo de Dijkstra (Edsger Dijkstra, 1959) determina la longitud del camino más corto desde un vértice a los demás en un grafo dirigido con pesos no negativos: los vecinos de $u$ son los vértices a los que sale una arista desde $u$. Rosen lo enuncia para grafos no dirigidos (sección 10.6, Teorema 1); un grafo no dirigido es el caso en que cada arista va en los dos sentidos.
- **Invariante.** Cuando un vértice $u$ entra a $S$, $L(u)$ es la longitud de un camino más corto de $s$ a $u$. Para todo $v \notin S$, $L(v)$ es la longitud del camino más corto de $s$ a $v$ cuyos vértices, salvo $v$, están todos en $S$.
- **Complejidad.** $O(V^2)$ con arreglos (Rosen, sección 10.6, Teorema 2); $O((V + E)\log V)$ con un *heap* binario.
- Es un algoritmo **voraz**: en cada paso toma la decisión que parece mejor (el vértice de menor etiqueta) y nunca la deshace.

## Ejercicios

Practique con los [ejercicios de Dijkstra](exercises.md).

## Fuentes

- Bedoya, O. *Grafos: grafos con pesos y algoritmo de Dijkstra* (ejemplo resuelto y ejercicios; ejemplo de Bogotá a Buenos Aires). Diapositivas del curso, Universidad del Valle.
- Aristizábal, A. y Gómez, M. *Grafos: recorridos* (mapa del sur de Alemania). Computación y Estructuras Discretas I, Universidad Icesi, 2025.
- Rosen, K. H. *Discrete Mathematics and Its Applications*, 7.ª ed. McGraw-Hill, 2011. Sección 10.6.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Sección 24.3.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
