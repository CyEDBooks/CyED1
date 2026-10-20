---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 5: Algoritmo de Prim"
---

# Unidad 5: Algoritmo de Prim

Los ejemplos se desarrollan en desplegables con pestañas **Paso 1, Paso 2, …**: cada paso conserva lo anterior y muestra lo nuevo **en color**.

## 1. El problema

Una empresa tiene siete sedes. Cada arista es un enlace de comunicaciones que se puede mantener; su peso es el costo mensual de mantenerlo.

{{GEN:fig-problema}}

**¿Qué enlaces se deben mantener para que todas las sedes sigan comunicadas (directa o indirectamente) con el menor costo total?**

Pruebe con una selección propia antes de seguir.

:::{admonition} Algunas observaciones
:class: dropdown
- Si la selección tiene un **circuito**, se puede quitar cualquier arista del circuito y todo sigue comunicado, más barato. La solución no tiene circuitos.
- Si la selección no **conecta** todas las sedes, no sirve.
- Un subgrafo conexo, sin circuitos y con los $7$ vértices es un **árbol**: tiene exactamente $7 - 1 = 6$ aristas.
:::

Una primera idea es listar **todos** los árboles que contienen a los $7$ vértices y quedarse con el de menor peso. Pero son demasiados: un grafo completo de $n$ vértices tiene $n^{n-2}$ de esos árboles (fórmula de Cayley); con $n = 20$ son más de $10^{23}$.

## 2. Árbol recubridor

**Árbol recubridor.** Sea $G$ un grafo simple. Un árbol recubridor de $G$ es un subgrafo de $G$ que es un **árbol** y que contiene **todos** los vértices de $G$.

Ejemplo. El grafo $G$:

{{GEN:fig-sp-g}}

| Es árbol recubridor | Es árbol recubridor | No: tiene un circuito y no es conexo | No: no contiene a $e$ |
|---|---|---|---|
| {{GEN:fig-sp-t1}} | {{GEN:fig-sp-t2}} | {{GEN:fig-sp-no1}} | {{GEN:fig-sp-no2}} |

**Árbol recubridor mínimo.** En un grafo con pesos, el peso de un árbol recubridor es la suma de los pesos de sus aristas. Un árbol recubridor mínimo es uno cuyo peso es menor o igual que el de cualquier otro árbol recubridor.

El problema de las sedes pide un árbol recubridor mínimo.

### ¿Entendimos el problema?

| | |
|---|---|
| **Entradas** | Un grafo no dirigido, conexo y con pesos. |
| **Salidas** | Un conjunto de $n - 1$ aristas que forman un árbol recubridor de peso mínimo, y ese peso. |

> **¿Por qué el grafo tiene que ser conexo?** Si no lo es, ningún subgrafo con todos sus vértices puede ser conexo, y no existe árbol recubridor.

## 3. El método

**Algoritmo de Prim.** Se escoge la arista de menor peso y se agrega al árbol. Después, se agrega la arista de menor peso que sea **incidente** con el árbol (un extremo dentro, otro fuera) y que no cree un circuito. Se repite hasta que el árbol tenga $n - 1$ aristas.

### Ejemplo 1

El grafo de las sedes. En cada paso las aristas punteadas son las **candidatas**: tienen un extremo en el árbol y el otro fuera.

{{GEN:ej1}}

Árbol recubridor mínimo obtenido con el algoritmo de Prim: {{GEN:ej1-aristas}}. Peso: **{{GEN:ej1-peso}}**.

### Ejemplo 2

Se puede empezar desde un **vértice** en lugar de hacerlo desde la arista más barata: el árbol inicial tiene solo ese vértice y ninguna arista. En este grafo hay varias aristas de peso $5$ y de peso $6$.

{{GEN:fig-ej2}}

{{GEN:ej2}}

Aristas: {{GEN:ej2-aristas}}. Peso: **{{GEN:ej2-peso}}**.

### Ejemplo 3

El mismo grafo, empezando desde $e$.

{{GEN:ej3}}

Aristas: {{GEN:ej3-aristas}}. Peso: **{{GEN:ej3-peso}}**.

> **¿Cambió el resultado?** El **orden** en que entran las aristas cambió, pero el árbol y el peso son los mismos. Cuando hay empates, Prim puede producir árboles distintos según el vértice inicial o la arista que escoja en un empate; todos tienen el mismo peso mínimo.

## 4. El algoritmo

```text
procedure Prim(G: grafo conexo no dirigido con pesos y n vértices)
    T = una arista de peso mínimo
    for i = 1 to n − 2
        e = una arista de peso mínimo incidente con un vértice de T
            y que no forme un circuito simple en T si se agrega a T
        T = T con e agregada
    return T   {T es un árbol recubridor mínimo de G}
```

«Que no forme un circuito» equivale a «que tenga exactamente un extremo en $T$»: si los dos extremos ya están en $T$, la arista cierra un circuito.

### Complejidad

> **¿Qué operación se repite en cada paso?**

:::{admonition} Respuesta
:class: dropdown
Encontrar la candidata de menor peso. Si se revisan todas las aristas en cada uno de los $n - 1$ pasos, el costo es $O(V \cdot E)$. Si se guarda, para cada vértice fuera del árbol, el peso de la arista más barata que lo une al árbol, cada paso cuesta $O(V)$ y el total es $O(V^2)$.
:::

Con una **cola de prioridad** (un *heap*) que entrega la candidata de menor peso, el total es $O(E \log V)$.

## 5. Implementación en Java

**Análisis.**

| | |
|---|---|
| **Entradas** | Número de vértices, aristas no dirigidas con peso, vértice inicial. |
| **Salidas** | La lista de aristas del árbol, en el orden en que se agregan, y su peso total. |
| **Proceso** | `enArbol[v]` marca los vértices del árbol; una `PriorityQueue` guarda las candidatas. |

**Diseño.** Se empieza desde un vértice. Al sacar una arista de la cola se revisa si sus dos extremos ya están en el árbol; en ese caso dejó de ser candidata (crearía un circuito) y se descarta. Si no, se agrega y entran a la cola las aristas del vértice nuevo.

**Codificación.**

```java
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class Prim {

    record Arista(int u, int v, int peso) { }

    private final int n;
    private final List<List<Arista>> adj;

    public Prim(int n) {
        this.n = n;
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
    }

    public void agregarArista(int u, int v, int w) {
        Arista a = new Arista(u, v, w);
        adj.get(u).add(a);
        adj.get(v).add(a);
    }

    public List<Arista> prim(int inicio) {
        boolean[] enArbol = new boolean[n];
        List<Arista> arbol = new ArrayList<>();
        PriorityQueue<Arista> candidatas =
                new PriorityQueue<>((a, b) -> Integer.compare(a.peso(), b.peso()));
        enArbol[inicio] = true;
        candidatas.addAll(adj.get(inicio));
        while (arbol.size() < n - 1 && !candidatas.isEmpty()) {
            Arista a = candidatas.remove();
            if (enArbol[a.u()] && enArbol[a.v()]) {
                continue;   // ya no es candidata: crearía un circuito
            }
            int nuevo = enArbol[a.u()] ? a.v() : a.u();
            enArbol[nuevo] = true;
            arbol.add(a);
            for (Arista b : adj.get(nuevo)) {
                if (!enArbol[b.u()] || !enArbol[b.v()]) {
                    candidatas.add(b);
                }
            }
        }
        return arbol;
    }

    public static void main(String[] args) {
        String nombres = "abcdefg";
        Prim g = new Prim(7);
        String[] aristas = {"ab1", "bc2", "ad4", "bd6", "be4", "ce5", "cf6", "de3", "ef8", "dg4",
                            "eg7", "fg3"};
        for (String a : aristas) {
            g.agregarArista(nombres.indexOf(a.charAt(0)), nombres.indexOf(a.charAt(1)),
                    a.charAt(2) - '0');
        }
        int total = 0;
        for (Arista a : g.prim(0)) {
            System.out.println("{" + nombres.charAt(a.u()) + "," + nombres.charAt(a.v()) + "} "
                    + a.peso());
            total += a.peso();
        }
        System.out.println("peso total = " + total);
    }
}
```

**Prueba.** Con el grafo del Ejemplo 1, desde $a$:

```text
{a,b} 1
{b,c} 2
{b,e} 4
{d,e} 3
{d,g} 4
{f,g} 3
peso total = 17
```

El peso es $17$, como en el Ejemplo 1, pero el árbol no es el mismo: en el tercer paso hay un empate entre $\{a,d\}$ y $\{b,e\}$ (peso $4$), y la `PriorityQueue` de Java escogió $\{b,e\}$. Los dos árboles son mínimos.

## 6. Formalización

- **Propiedad del corte.** Sea $S$ un conjunto de vértices con $\emptyset \neq S \neq V$. Si $e$ es una arista de peso mínimo entre las que tienen un extremo en $S$ y el otro en $V - S$, entonces existe un árbol recubridor mínimo que contiene a $e$.
- Prim aplica la propiedad del corte en cada paso con $S$ = vértices del árbol: la arista que agrega es la de menor peso que cruza de $S$ a $V - S$. Por eso el resultado es un árbol recubridor mínimo.
- Es un algoritmo **voraz**: en cada paso toma la arista más barata posible y nunca la quita.
- Complejidad: $O(V^2)$ con arreglos; $O(E \log V)$ con un *heap* binario.

## Ejercicios

Practique con los [ejercicios de Prim](exercises.md).

## Fuentes

- Bedoya, O. *Árboles: árbol recubridor, algoritmos de Prim y Kruskal*. Diapositivas del curso, Universidad del Valle.
- Rosen, K. H. *Discrete Mathematics and Its Applications*, 7.ª ed. McGraw-Hill, 2011. Sección 11.5.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Capítulo 23.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
