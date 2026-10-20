---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 5: Algoritmo de Kruskal"
---

# Unidad 5: Algoritmo de Kruskal

Los ejemplos se desarrollan en desplegables con pestañas **Paso 1, Paso 2, …**: cada paso conserva lo anterior y muestra lo nuevo **en color**.

## 1. El problema

Es el mismo problema de la [página de Prim](../Prim/index.md): encontrar un **árbol recubridor mínimo** de un grafo conexo con pesos.

{{GEN:fig-problema}}

Prim hace crecer **un solo árbol** desde un punto. ¿Y si se toman directamente las aristas más baratas de todo el grafo?

### Un primer intento

Tome las $6$ aristas más baratas ($n - 1 = 6$): {{GEN:ingenuo-aristas}}.

{{GEN:fig-ingenuo}}

> **¿Es un árbol recubridor?**

:::{admonition} Respuesta
:class: dropdown
No. $\{a,b\}$, $\{b,e\}$, $\{d,e\}$ y $\{a,d\}$ forman el circuito $a - b - e - d - a$. Además $\{f,g\}$ queda separado del resto: el subgrafo no es conexo. Con $n - 1$ aristas, un circuito obliga a que falte conexión. Tomar las más baratas **sin revisar circuitos** no sirve.
:::

La corrección es pequeña: se recorren las aristas de la más barata a la más cara y se **descarta** la que cierre un circuito.

## 2. El método

**Algoritmo de Kruskal.** Se ordenan las aristas de menor a mayor peso. Se recorren en ese orden y se agrega al árbol cada arista que **no cree un circuito** con las ya escogidas. Se termina cuando el árbol tiene $n - 1$ aristas.

A diferencia de Prim, en Kruskal la arista escogida **no tiene que ser incidente** con lo que ya se ha construido: en los pasos intermedios se tiene un **bosque** (varios árboles), que al final queda unido en un solo árbol.

¿Cómo saber si una arista crea un circuito? Se lleva la **componente** (el árbol del bosque) de cada vértice. Una arista $\{u, v\}$ crea un circuito si y solo si $u$ y $v$ ya están en la misma componente.

### Ejemplo 1

El grafo de las sedes. Debajo del grafo están las aristas ordenadas: la del paso actual en color, las ya procesadas en gris.

{{GEN:ej1}}

Árbol recubridor mínimo obtenido con el algoritmo de Kruskal: {{GEN:ej1-aristas}}. Peso: **{{GEN:ej1-peso}}**.

Comparado con el de Prim:

| Prim | Kruskal |
|---|---|
| {{GEN:fig-cmp-prim}} | {{GEN:fig-cmp-kruskal}} |

En este grafo los dos algoritmos llegan al **mismo** árbol, agregando las aristas en distinto orden.

### Ejemplo 2

El grafo con empates del Ejemplo 2 de Prim.

{{GEN:fig-ej2}}

{{GEN:ej2}}

Peso: **{{GEN:ej2-peso}}**, el mismo que se obtuvo con Prim.

## 3. El algoritmo

```text
procedure Kruskal(G: grafo conexo no dirigido con pesos y n vértices)
    T = grafo vacío
    for i = 1 to n − 1
        e = cualquier arista de G de peso mínimo que no forme
            un circuito simple cuando se agrega a T
        T = T con e agregada
    return T   {T es un árbol recubridor mínimo de G}
```

Para la implementación, la forma de llevar las componentes es una estructura de **conjuntos disjuntos** con dos operaciones:

- `encontrar(v)`: devuelve el representante de la componente de $v$.
- `unir(u, v)`: junta las componentes de $u$ y de $v$.

Cada componente se guarda como un árbol de vértices en el que cada uno apunta a su `padre`; el representante es la raíz.

### Complejidad

- Ordenar las aristas: $O(E \log E)$.
- Recorrerlas haciendo `encontrar` y `unir`: con las mejoras usuales (unión por rango y compresión de caminos), casi $O(E)$.

$$
T_{Kruskal}(V, E) = O(E \log E) = O(E \log V)
$$

(Se cumple $\log E = O(\log V)$ porque $E \le V^2$.)

## 4. Implementación en Java

**Análisis.**

| | |
|---|---|
| **Entradas** | Número de vértices y lista de aristas con peso. |
| **Salidas** | La lista de aristas del árbol, en el orden en que se agregan, y su peso total. |
| **Proceso** | Ordenar las aristas; conjuntos disjuntos con un arreglo `padre[]`. |

**Diseño.** El pseudocódigo de la sección 3. `encontrar` sube por `padre[]` hasta la raíz; para unir, la raíz de una componente pasa a apuntar a la raíz de la otra.

**Codificación.**

```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Kruskal {

    record Arista(int u, int v, int peso) { }

    private final int n;
    private final List<Arista> aristas = new ArrayList<>();
    private int[] padre;

    public Kruskal(int n) {
        this.n = n;
    }

    public void agregarArista(int u, int v, int w) {
        aristas.add(new Arista(u, v, w));
    }

    // Representante de la componente de v: se sube por 'padre' hasta la raíz.
    private int encontrar(int v) {
        while (padre[v] != v) {
            v = padre[v];
        }
        return v;
    }

    public List<Arista> kruskal() {
        padre = new int[n];
        for (int v = 0; v < n; v++) {
            padre[v] = v;   // cada vértice empieza en su propia componente
        }
        List<Arista> ordenadas = new ArrayList<>(aristas);
        ordenadas.sort(Comparator.comparingInt(Arista::peso));
        List<Arista> arbol = new ArrayList<>();
        for (Arista a : ordenadas) {
            int ru = encontrar(a.u());
            int rv = encontrar(a.v());
            if (ru != rv) {
                padre[rv] = ru;   // unir las dos componentes
                arbol.add(a);
                if (arbol.size() == n - 1) {
                    break;
                }
            }
        }
        return arbol;
    }

    public static void main(String[] args) {
        String nombres = "abcdefg";
        Kruskal g = new Kruskal(7);
        String[] aristas = {"ab1", "bc2", "ad4", "bd6", "be4", "ce5", "cf6", "de3", "ef8", "dg4",
                            "eg7", "fg3"};
        for (String a : aristas) {
            g.agregarArista(nombres.indexOf(a.charAt(0)), nombres.indexOf(a.charAt(1)),
                    a.charAt(2) - '0');
        }
        int total = 0;
        for (Arista a : g.kruskal()) {
            System.out.println("{" + nombres.charAt(a.u()) + "," + nombres.charAt(a.v()) + "} "
                    + a.peso());
            total += a.peso();
        }
        System.out.println("peso total = " + total);
    }
}
```

**Prueba.** Con el grafo del Ejemplo 1 (`sort` es estable, así que los empates conservan el orden en que se agregaron las aristas):

```text
{a,b} 1
{b,c} 2
{d,e} 3
{f,g} 3
{a,d} 4
{d,g} 4
peso total = 17
```

Es la misma secuencia del Ejemplo 1.

## 5. Prim y Kruskal

| | Prim | Kruskal |
|---|---|---|
| Qué se construye en los pasos intermedios | un solo árbol que crece | un bosque que se va uniendo |
| Qué arista se escoge | la más barata **incidente** con el árbol | la más barata del grafo que **no cree circuito** |
| Cómo se evita el circuito | la arista debe tener un solo extremo en el árbol | los extremos deben estar en componentes distintas |
| Estructura auxiliar | cola de prioridad de candidatas | aristas ordenadas + conjuntos disjuntos |
| Complejidad | $O(E \log V)$ con *heap* | $O(E \log V)$ |

Los dos son **voraces** y los dos son correctos por la **propiedad del corte**: si $e$ es una arista de peso mínimo entre las que cruzan de un conjunto de vértices $S$ a $V - S$, existe un árbol recubridor mínimo que contiene a $e$. En Kruskal, $S$ es la componente de uno de los extremos de la arista que se agrega.

## Ejercicios

Practique con los [ejercicios de Kruskal](exercises.md).

## Fuentes

- Bedoya, O. *Árboles: árbol recubridor, algoritmos de Prim y Kruskal*. Diapositivas del curso, Universidad del Valle.
- Rosen, K. H. *Discrete Mathematics and Its Applications*, 7.ª ed. McGraw-Hill, 2011. Sección 11.5.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Capítulo 23 y sección 21.3.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
