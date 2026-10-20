---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 4: Árboles AVL"
---

# Unidad 4: Árboles AVL

Los ejemplos se desarrollan en desplegables con pestañas **Paso 1, Paso 2, …**: cada paso conserva lo anterior y muestra lo nuevo **en color**. Junto a cada nodo aparece su **factor de balanceo**; en rojo, si el nodo está desbalanceado.

## 1. El problema

Inserte $1, 2, 3, 4, 5, 6, 7$, en ese orden, en un árbol binario de búsqueda:

{{GEN:fig-cadena}}

Es una cadena: buscar $7$ cuesta $7$ comparaciones. Con las mismas llaves, un árbol lleno tendría altura $3$. **¿Cómo mantener el árbol «bajo» sin importar el orden en que lleguen las llaves?** Hace falta (1) medir qué tan desbalanceado está cada nodo y (2) una operación que corrija el desbalance sin romper el orden del ABB.

## 2. Factor de balanceo y árbol AVL

**Factor de balanceo.** Para un nodo $v$ de un árbol binario:

$$
fb(v) = \text{altura del subárbol derecho de } v - \text{altura del subárbol izquierdo de } v
$$

**Árbol AVL.** Un árbol binario de búsqueda **balanceado en altura**: para cada nodo $v$, $|fb(v)| \le 1$. Es decir, en cada nodo las alturas de los dos subárboles difieren a lo sumo en $1$, y cada subárbol es también AVL.

Su nombre viene de sus creadores, Adelson-Velskii y Landis (1962). Fue el primer ABB balanceado publicado.

Indique cuáles de estos ABB son AVL:

| | | | |
|---|---|---|---|
| {{GEN:fig-es-1}} | {{GEN:fig-es-2}} | {{GEN:fig-es-3}} | {{GEN:fig-es-4}} |

:::{admonition} Respuesta
:class: dropdown
| | | | |
|---|---|---|---|
| {{GEN:fig-es-1-sol}} | {{GEN:fig-es-2-sol}} | {{GEN:fig-es-3-sol}} | {{GEN:fig-es-4-sol}} |

a) Sí. b) No: $fb(8) = 1 - 3 = -2$. c) Sí. d) No: $fb(8) = 3 - 1 = +2$.

Fíjese en b): todos los nodos **menos la raíz** están bien. Hay que revisar **cada** nodo.
:::

## 3. Rotaciones

**Rotación a la izquierda** de $x$ (`LEFT-ROTATE(x)`): $x$ debe tener hijo derecho $y$. Se baja $x$, se sube $y$ como raíz del subárbol, y el subárbol izquierdo de $y$ ($\beta$) pasa a ser el subárbol derecho de $x$.

| | |
|---|---|
| {{GEN:fig-rot-antes}} | {{GEN:fig-rot-despues}} |

**Rotación a la derecha** de $y$ (`RIGHT-ROTATE(y)`): la operación inversa. $y$ debe tener hijo izquierdo $x$; sube $x$, baja $y$, y el subárbol derecho de $x$ pasa a ser el izquierdo de $y$.

> **¿El resultado sigue siendo un ABB?**

:::{admonition} Respuesta
:class: dropdown
Sí. En ambos dibujos el inorden es $\alpha, x, \beta, y, \gamma$: todo lo de $\alpha$ es menor que $x$, todo lo de $\beta$ está entre $x$ y $y$, y todo lo de $\gamma$ es mayor que $y$. Las rotaciones se pueden aplicar en **cualquier** ABB; no dependen del balanceo.
:::

`LEFT-ROTATE` traslada **altura** del lado derecho al izquierdo, y `RIGHT-ROTATE`, del izquierdo al derecho.

## 4. Casos de desbalanceo

Sea $p$ un nodo con $fb(p) = \pm 2$ tal que todos los nodos debajo de $p$ están balanceados, y sea $q$ el hijo de $p$ del lado **más alto**. Hay seis casos:

| Caso | $fb(p)$ | $fb(q)$ | Solución |
|---|---|---|---|
| A | $+2$ | $+1$ | `LEFT-ROTATE(p)` |
| B | $+2$ | $0$ | `LEFT-ROTATE(p)` (solo al eliminar) |
| C | $+2$ | $-1$ | `RIGHT-ROTATE(q)` y luego `LEFT-ROTATE(p)` |
| D | $-2$ | $-1$ | `RIGHT-ROTATE(p)` |
| E | $-2$ | $0$ | `RIGHT-ROTATE(p)` (solo al eliminar) |
| F | $-2$ | $+1$ | `LEFT-ROTATE(q)` y luego `RIGHT-ROTATE(p)` |

Regla para recordarla: si $fb(q)$ tiene el **mismo signo** que $fb(p)$ (o es $0$), basta **una** rotación de $p$ hacia el lado contrario. Si tiene **signo contrario**, primero se rota $q$ para dejar el desbalance «en línea» y después se rota $p$ (**rotación doble**).

> **¿Por qué en el caso C no basta con rotar $p$ a la izquierda?**

:::{admonition} Respuesta
:class: dropdown
Porque el peso está en el subárbol **izquierdo** de $q$ (en el medio). Al rotar $p$ a la izquierda, ese subárbol del medio pasa a ser hijo derecho de $p$ y el desbalance aparece del otro lado ($fb = -2$ en la nueva raíz). Pruébelo en el Ejemplo 4 con las llaves $10, 30, 20$.
:::

## 5. Inserción

```text
AVL-INSERT(T, k)
1  insertar k en T como en un ABB; sea x el nodo agregado
2  AVL-REBALANCE(T, x)

AVL-REBALANCE(T, x)
1  for cada nodo p en el camino de x a la raíz (de abajo hacia arriba)
2      if |fb(p)| > 1
3          rebalancear el subárbol con raíz en p según el caso (A–F)
```

El nodo nuevo es una hoja, así que solo pueden cambiar los factores de balanceo de los nodos en el camino de la raíz al nodo nuevo. El primer nodo desbalanceado que se encuentra subiendo tiene $fb = \pm 2$ y cae en alguno de los casos. En la inserción, después de rebalancear ese nodo el subárbol recupera la altura que tenía antes, así que **basta un rebalanceo**.

### Ejemplo 1

{{GEN:ej1}}

### Ejemplo 2

Las mismas llaves de la sección 1:

{{GEN:ej2}}

Resultado: un árbol **lleno** de altura $3$, contra la cadena de altura $7$ del ABB.

### Ejemplo 3

Dado el árbol $T$:

{{GEN:fig-ej3-base}}

{{GEN:ej3}}

### Ejemplo 4

{{GEN:ej4}}

## 6. Eliminación

Se elimina como en un ABB y luego se rebalancean los nodos entre el padre del nodo que salió del árbol y la raíz (si el nodo tenía dos hijos, el que sale es su sucesor). Aquí sí pueden aparecer los casos B y E, y puede hacer falta **más de un** rebalanceo.

{{GEN:eliminar}}

## 7. Implementación en Java

**Análisis.**

| | |
|---|---|
| **Entradas** | Llaves comparables, insertadas una a una. |
| **Salidas** | El árbol en preorden y su altura. |
| **Proceso** | Cada nodo guarda la altura de su subárbol; inserción recursiva que rebalancea al regresar de la recursión. |

**Diseño.** La inserción recursiva del ABB devuelve la nueva raíz de cada subárbol. Al **regresar** de la recursión se recorre el camino del nodo nuevo hacia la raíz, de abajo hacia arriba: ahí se actualiza la altura y se aplica `rebalancear`, que implementa la tabla de casos de la sección 4.

**Codificación.**

```java
import java.util.ArrayList;
import java.util.List;

public class AVL<T extends Comparable<T>> {

    private static class Nodo<T> {
        T llave;
        Nodo<T> izq;
        Nodo<T> der;
        int altura = 1;                 // altura en nodos del subárbol

        Nodo(T llave) {
            this.llave = llave;
        }
    }

    private Nodo<T> raiz;

    private int altura(Nodo<T> n) {
        return n == null ? 0 : n.altura;
    }

    private void actualizar(Nodo<T> n) {
        n.altura = 1 + Math.max(altura(n.izq), altura(n.der));
    }

    // fb(v) = altura del subárbol derecho - altura del subárbol izquierdo
    private int fb(Nodo<T> n) {
        return altura(n.der) - altura(n.izq);
    }

    private Nodo<T> rotarIzquierda(Nodo<T> x) {
        Nodo<T> y = x.der;
        x.der = y.izq;
        y.izq = x;
        actualizar(x);
        actualizar(y);
        return y;
    }

    private Nodo<T> rotarDerecha(Nodo<T> y) {
        Nodo<T> x = y.izq;
        y.izq = x.der;
        x.der = y;
        actualizar(y);
        actualizar(x);
        return x;
    }

    private Nodo<T> rebalancear(Nodo<T> p) {
        actualizar(p);
        if (fb(p) == 2) {
            if (fb(p.der) < 0) {
                p.der = rotarDerecha(p.der);    // caso C: rotación doble
            }
            return rotarIzquierda(p);           // casos A y B
        }
        if (fb(p) == -2) {
            if (fb(p.izq) > 0) {
                p.izq = rotarIzquierda(p.izq);  // caso F: rotación doble
            }
            return rotarDerecha(p);             // casos D y E
        }
        return p;
    }

    public void insertar(T k) {
        raiz = insertar(raiz, k);
    }

    private Nodo<T> insertar(Nodo<T> x, T k) {
        if (x == null) {
            return new Nodo<>(k);
        }
        if (k.compareTo(x.llave) < 0) {
            x.izq = insertar(x.izq, k);
        } else {
            x.der = insertar(x.der, k);
        }
        return rebalancear(x);        // de abajo hacia arriba, por el camino de la inserción
    }

    public List<T> preorden() {
        List<T> res = new ArrayList<>();
        preorden(raiz, res);
        return res;
    }

    private void preorden(Nodo<T> x, List<T> res) {
        if (x != null) {
            res.add(x.llave);
            preorden(x.izq, res);
            preorden(x.der, res);
        }
    }

    public int altura() {
        return altura(raiz);
    }

    public static void main(String[] args) {
        AVL<Integer> t = new AVL<>();
        for (int k = 1; k <= 7; k++) {
            t.insertar(k);
        }
        System.out.println("1..7 -> preorden " + t.preorden() + ", altura " + t.altura());
        AVL<Integer> u = new AVL<>();
        for (int k : new int[] {50, 20, 70, 10, 30, 25}) {
            u.insertar(k);
        }
        System.out.println("50 20 70 10 30 25 -> preorden " + u.preorden() + ", altura " + u.altura());
    }
}
```

**Prueba.**

```text
1..7 -> preorden [4, 2, 1, 3, 6, 5, 7], altura 3
50 20 70 10 30 25 -> preorden [30, 20, 10, 25, 50, 70], altura 3
```

Son los árboles finales de los Ejemplos 2 y 3. El preorden basta para reconstruir un ABB: la primera llave es la raíz, las menores van a la izquierda y las mayores a la derecha.

## 8. Formalización

- Un árbol AVL con $n$ nodos tiene altura $O(\log n)$. Si $N(h)$ es el **mínimo** número de nodos de un AVL de altura $h$, entonces $N(h) = 1 + N(h-1) + N(h-2)$, que crece como los números de Fibonacci; de ahí, $h < 1{,}45 \log_2(n + 2)$.
- Por lo tanto, buscar, insertar y eliminar en un AVL cuestan $O(\log n)$.
- Las rotaciones cuestan $O(1)$ y preservan el invariante del ABB.
- En la inserción se hace a lo sumo un rebalanceo (una rotación simple o una doble); en la eliminación pueden hacer falta $O(\log n)$.

## Ejercicios

Practique con los [ejercicios de árboles AVL](exercises.md).

## Fuentes

- Aristizábal, A. *Árboles AVL* (factor de balanceo, rotaciones, casos de desbalanceo A–F, inserción y eliminación). Computación y Estructuras Discretas I, Universidad Icesi, 2026.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Problema 13-3 (árboles AVL) y sección 13.2 (rotaciones).

---

*Material adaptado del material original del profesor Andrés Aristizábal.*
