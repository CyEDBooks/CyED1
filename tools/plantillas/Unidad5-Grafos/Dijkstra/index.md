---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 5: Algoritmo de Dijkstra"
---

# Unidad 5: Algoritmo de Dijkstra

Los ejemplos se desarrollan en desplegables con pestañas **Paso 1, Paso 2, …**: cada paso conserva lo anterior y muestra lo nuevo **en color**.

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
| **Entradas** | Un grafo (dirigido o no) con pesos **no negativos** y un vértice origen $s$. |
| **Salidas** | Para cada vértice $v$: el costo mínimo de un camino de $s$ a $v$ y el vértice anterior a $v$ en ese camino. |

Traza a mano con el grafo de la sección 1: el costo mínimo de $a$ a $f$ es $5$ y el anterior a $f$ es $d$; el de $a$ a $d$ es $3$ y el anterior a $d$ es $b$.

## 2. El método

**Algoritmo de Dijkstra.** Cada vértice lleva una etiqueta $[\text{valor acumulado}, \text{predecesor}]$. En cada paso, el vértice **no permanente** con **menor valor acumulado** se vuelve **permanente**, y se reetiquetan sus vecinos cuando llegar a ellos a través de él cuesta menos.

### Ejemplo 1

El grafo de la sección 1, desde $a$. Los vértices negros son permanentes; las flechas en azul van del predecesor al vértice.

{{GEN:ej1}}

Ahora se leen los caminos. **Para encontrar el camino de costo mínimo** se parte del destino y se siguen los predecesores hasta llegar al origen.

{{GEN:ej1-camino-d}}

{{GEN:ej1-camino-f}}

Todos los resultados:

{{GEN:ej1-final}}

### Ejemplo 2

Aplique el algoritmo de Dijkstra para encontrar el camino más corto entre Bogotá y Buenos Aires. El grafo es no dirigido; las abreviaturas son Bog (Bogotá), Lim (Lima), Qui (Quito), Paz (La Paz), Asu (Asunción) y BA (Buenos Aires).

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

## 4. Implementación en Java

**Análisis.**

| | |
|---|---|
| **Entradas** | Número de vértices, aristas no dirigidas con peso entero no negativo, origen $s$. |
| **Salidas** | Arreglos `dist[]` (valor acumulado) y `pred[]` (predecesor); el camino a cualquier destino. |
| **Proceso** | Etiquetas en arreglos; el siguiente permanente se obtiene de una `PriorityQueue`. |

**Diseño.** Se sigue el pseudocódigo de la sección 3 con una decisión: `PriorityQueue` de Java no permite bajar la prioridad de un elemento. Cada vez que se reetiqueta $v$ se agrega **otra** entrada $\{dist[v], v\}$, y al sacar una entrada de un vértice que ya es permanente, se ignora.

**Codificación.**

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

public class Dijkstra {

    record Arista(int destino, int peso) { }

    static final int INF = Integer.MAX_VALUE;

    private final List<List<Arista>> adj;
    private final int[] dist;
    private final int[] pred;

    public Dijkstra(int n) {
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        dist = new int[n];
        pred = new int[n];
    }

    public void agregarArista(int u, int v, int w) {
        adj.get(u).add(new Arista(v, w));
        adj.get(v).add(new Arista(u, w));
    }

    public void dijkstra(int s) {
        int n = adj.size();
        boolean[] permanente = new boolean[n];
        Arrays.fill(dist, INF);
        Arrays.fill(pred, -1);
        dist[s] = 0;
        // Cada entrada es {distancia, vértice}; la cola entrega primero la menor distancia.
        PriorityQueue<int[]> cola = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        cola.add(new int[] {0, s});
        while (!cola.isEmpty()) {
            int u = cola.remove()[1];
            if (permanente[u]) {
                continue;   // entrada vieja: u ya tiene su distancia definitiva
            }
            permanente[u] = true;
            for (Arista a : adj.get(u)) {
                int v = a.destino();
                if (!permanente[v] && dist[u] + a.peso() < dist[v]) {
                    dist[v] = dist[u] + a.peso();
                    pred[v] = u;
                    cola.add(new int[] {dist[v], v});
                }
            }
        }
    }

    public String camino(String[] nombres, int v) {
        if (pred[v] == -1) {
            return nombres[v];
        }
        return camino(nombres, pred[v]) + " -> " + nombres[v];
    }

    public static void main(String[] args) {
        String[] nombres = {"Bogota", "Lima", "Quito", "La Paz", "Asuncion", "B. Aires"};
        Dijkstra g = new Dijkstra(6);
        int[][] aristas = {{0, 1, 4}, {0, 2, 2}, {1, 2, 1}, {1, 3, 5}, {1, 4, 7},
                           {2, 3, 8}, {2, 4, 10}, {3, 4, 2}, {3, 5, 6}, {4, 5, 3}};
        for (int[] a : aristas) {
            g.agregarArista(a[0], a[1], a[2]);
        }
        g.dijkstra(0);
        for (int v = 0; v < nombres.length; v++) {
            System.out.println(nombres[v] + ": " + g.dist[v] + "  (" + g.camino(nombres, v) + ")");
        }
    }
}
```

**Prueba.** Con el grafo del Ejemplo 2:

```text
Bogota: 0  (Bogota)
Lima: 3  (Bogota -> Quito -> Lima)
Quito: 2  (Bogota -> Quito)
La Paz: 8  (Bogota -> Quito -> Lima -> La Paz)
Asuncion: 10  (Bogota -> Quito -> Lima -> Asuncion)
B. Aires: 13  (Bogota -> Quito -> Lima -> Asuncion -> B. Aires)
```

Son las etiquetas finales de la tabla del Ejemplo 2.

## 5. Formalización

- El algoritmo de Dijkstra (Edsger Dijkstra, 1959) determina la longitud del camino más corto entre dos vértices de un grafo ponderado simple, conexo y no dirigido, con pesos positivos (Rosen, sección 10.6, Teorema 1). La misma idea funciona en grafos dirigidos: los vecinos de $u$ son los vértices a los que sale una arista desde $u$.
- **Invariante.** Cuando un vértice $u$ entra a $S$, $L(u)$ es la longitud de un camino más corto de $s$ a $u$. Para todo $v \notin S$, $L(v)$ es la longitud del camino más corto de $s$ a $v$ cuyos vértices, salvo $v$, están todos en $S$.
- **Complejidad.** $O(V^2)$ con arreglos (Rosen, sección 10.6, Teorema 2); $O((V + E)\log V)$ con un *heap* binario.
- Es un algoritmo **voraz**: en cada paso toma la decisión que parece mejor (el vértice de menor etiqueta) y nunca la deshace.

## Ejercicios

Practique con los [ejercicios de Dijkstra](exercises.md).

## Fuentes

- Caicedo Mejía, J. M. *Unidad 5: Grafos* (Grafos 3: algoritmo de Dijkstra). Computación y Estructuras Discretas I, Universidad Icesi, 2026.
- Bedoya, O. *Grafos: grafos con pesos y algoritmo de Dijkstra*. Diapositivas del curso, Universidad del Valle.
- Rosen, K. H. *Discrete Mathematics and Its Applications*, 7.ª ed. McGraw-Hill, 2011. Sección 10.6.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Sección 24.3.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
