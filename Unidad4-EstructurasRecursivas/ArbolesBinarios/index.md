---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 4: Árboles binarios"
---

# Unidad 4: Árboles binarios

Algunos ejemplos se desarrollan en desplegables con pestañas **Paso 1, Paso 2, …**: cada paso conserva lo anterior y muestra lo nuevo **en color**.

## 1. El problema

¿Cómo se guarda en un programa una estructura en la que cada elemento se divide en **a lo sumo dos** partes, y **importa cuál es la izquierda y cuál la derecha**? Por ejemplo, la expresión $(x + 5) / (x - 3)$: el operador $/$ tiene un operando izquierdo, $(x + 5)$, y uno derecho, $(x - 3)$, y si se intercambian el resultado cambia. Cada operando, a su vez, se divide igual.

La respuesta es una estructura **recursiva**: un elemento y dos estructuras del mismo tipo.

## 2. Definición

**Árbol binario.** Un árbol binario es una estructura de datos recursiva que es:

- el **árbol vacío** (sin elementos ni subárboles), o
- un elemento, llamado **raíz**, con dos subárboles asociados, también binarios, llamados **hijo izquierdo** e **hijo derecho**.

A diferencia de un árbol $2$-ario cualquiera, en un árbol binario la posición **sí** importa. Estos dos árboles binarios son distintos:

| | |
|---|---|
| ![b como hijo izquierdo](images/izq.svg) | ![b como hijo derecho](images/der.svg) |
| $b$ es hijo **izquierdo** de $a$ | $b$ es hijo **derecho** de $a$ |

### Características

- **Hijo y padre.** $B$ es hijo de $A$ si $B$ es la raíz de alguno de los subárboles de $A$; $A$ es el padre de $B$.
- **Hermanos.** Dos elementos con el mismo padre.
- **Hoja.** Un elemento cuyos hijos izquierdo y derecho son vacíos.
- **Elemento no terminal.** Todo elemento que no es hoja.
- **Camino** entre $A$ y $B$. Una secuencia que empieza en $A$, termina en $B$ y en la que cada elemento es padre del siguiente. Su **longitud** es el número de elementos menos $1$.
- **Rama.** Un camino de la raíz a una hoja.
- **Peso.** El número de elementos del árbol.
- **Altura.** La longitud del camino más largo desde la raíz, más $1$ (el número de nodos de la rama más larga).
- **Nivel** de un elemento. La longitud del camino desde la raíz hasta el elemento.
- **Árbol binario completo.** Todo elemento no terminal tiene **exactamente dos** subárboles no vacíos.
- **Árbol binario lleno.** Es completo y además **todas sus hojas están en el mismo nivel**.

| | | |
|---|---|---|
| ![Completo](images/completo.svg) | ![Lleno](images/lleno.svg) | ![Ni completo ni lleno](images/ninguno.svg) |

Otros textos usan «completo» y «lleno» con otros significados (por ejemplo, para los montículos de la Unidad 3, «completo» quiere decir lleno en todos los niveles menos el último, que se llena de izquierda a derecha). Aquí se usan las definiciones de esta sección.

### Ejemplo

![Árbol binario de ejemplo](images/ejemplo.svg)

Responda sí o no:

1. ¿La raíz del árbol es $10$?
2. ¿La altura del árbol es $4$?
3. ¿El peso del árbol es $7$?
4. ¿Son hojas $7$, $6$ y $18$?
5. ¿Es un elemento no terminal $-6$?
6. ¿$15$ es hijo de $10$?
7. ¿$25$ es padre de $7$?
8. ¿Son hermanos $7$ y $6$?
9. ¿El camino entre $10$ y $7$ es $10, 15, 25, 7$?
10. ¿La longitud del camino entre $10$ y $7$ es $3$?
11. ¿$25$ está en el nivel $2$?
12. ¿El árbol es completo?
13. ¿El árbol está lleno?

:::{admonition} Respuesta
:class: dropdown
Del 1 al 11: **sí**. La rama más larga es $10, 15, 25, 7$ (o $10, 15, 25, 6$), con $4$ nodos.

12: **no**. $15$ es no terminal y tiene un solo subárbol no vacío (el izquierdo); lo mismo pasa con $-6$.

13: **no**. Para estar lleno tendría que ser completo.
:::

## 3. Altura y peso, recursivamente

La definición recursiva lleva directamente a fórmulas recursivas. Para un árbol con raíz $r$, subárbol izquierdo $I$ y subárbol derecho $D$:

$$
\text{peso}(\varnothing) = 0 \qquad \text{peso}(T) = 1 + \text{peso}(I) + \text{peso}(D)
$$

$$
\text{altura}(\varnothing) = 0 \qquad \text{altura}(T) = 1 + \max\big(\text{altura}(I), \text{altura}(D)\big)
$$

Así se ve el cálculo en el árbol del ejemplo. Cada nodo recibe su altura $h$ y su peso $p$ solo cuando ya se conocen los de sus dos subárboles:

:::::{admonition} Altura (h) y peso (p) de cada subárbol
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![Altura y peso, paso 1](images/altura-00.svg)

> $7$ es hoja: sus dos subárboles son vacíos (altura $0$, peso $0$). $h = 1 + \max(0, 0) = 1$, $p = 1 + 0 + 0 = 1$.

:::
:::{tab-item} Paso 2
![Altura y peso, paso 2](images/altura-01.svg)

> $6$ es hoja: sus dos subárboles son vacíos (altura $0$, peso $0$). $h = 1 + \max(0, 0) = 1$, $p = 1 + 0 + 0 = 1$.

> **¿Por qué se calcula primero $7$ y $6$, y no $10$?**

:::
:::{tab-item} Paso 3
![Altura y peso, paso 3](images/altura-02.svg)

> $25$: ya se conocen sus subárboles. $h = 1 + \max(1, 1) = 2$, $p = 1 + 1 + 1 = 3$.

> Porque la altura y el peso de un nodo **dependen** de los de sus hijos. Hay que resolver primero los subárboles: es la recursión regresando desde las hojas.

:::
:::{tab-item} Paso 4
![Altura y peso, paso 4](images/altura-03.svg)

> $15$: ya se conocen sus subárboles. $h = 1 + \max(2, 0) = 3$, $p = 1 + 3 + 0 = 4$.

:::
:::{tab-item} Paso 5
![Altura y peso, paso 5](images/altura-04.svg)

> $18$ es hoja: sus dos subárboles son vacíos (altura $0$, peso $0$). $h = 1 + \max(0, 0) = 1$, $p = 1 + 0 + 0 = 1$.

:::
:::{tab-item} Paso 6
![Altura y peso, paso 6](images/altura-05.svg)

> $-6$: ya se conocen sus subárboles. $h = 1 + \max(0, 1) = 2$, $p = 1 + 0 + 1 = 2$.

:::
:::{tab-item} Paso 7
![Altura y peso, paso 7](images/altura-06.svg)

> $10$: ya se conocen sus subárboles. $h = 1 + \max(3, 2) = 4$, $p = 1 + 4 + 2 = 7$.

:::
::::
:::::

## 4. ¿Cuántos nodos caben?

> **¿Cuántos nodos puede tener, como máximo, el nivel $i$ de un árbol binario? ¿Y un árbol binario de altura $h$?**

:::{admonition} Respuesta
:class: dropdown
El nivel $0$ tiene $1$ nodo (la raíz) y cada nodo tiene a lo sumo $2$ hijos, así que el nivel $i$ tiene a lo sumo $2^i$ nodos. Un árbol de altura $h$ tiene niveles $0, \dots, h - 1$:

$$
1 + 2 + 4 + \cdots + 2^{h-1} = 2^h - 1
$$

El máximo se alcanza en un árbol **lleno**. Por ejemplo, con altura $4$: $2^4 - 1 = 15$ nodos.

![Árbol binario lleno de altura 4](images/lleno4.svg)
:::

Al revés: un árbol binario con $n$ nodos tiene altura **al menos** $\lceil \log_2(n + 1) \rceil$. Esto importa para los árboles de búsqueda: si el árbol se mantiene «bajo», recorrer una rama cuesta $O(\log n)$.

## 5. Implementación en Java

**Análisis.**

| | |
|---|---|
| **Entradas** | Un árbol binario construido a mano. |
| **Salidas** | Peso, altura, número de hojas y si es completo. |
| **Proceso** | Clase `NodoBinario<T>` con `izq` y `der`; métodos recursivos en dos niveles (como en los árboles $n$-arios). |

**Diseño.** Las fórmulas de la sección 3. En el segundo nivel, un subárbol vacío es `null`, así que antes de llamar recursivamente se revisa si el hijo existe. `esCompleto` sigue el patrón de descenso: apenas un nodo no terminal tiene un solo hijo, la respuesta es `false`.

**Codificación.**

```java
public class ArbolBinario<T> {

    static class NodoBinario<T> {
        T elem;
        NodoBinario<T> izq;
        NodoBinario<T> der;

        NodoBinario(T elem, NodoBinario<T> izq, NodoBinario<T> der) {
            this.elem = elem;
            this.izq = izq;
            this.der = der;
        }

        boolean esHoja() {
            return izq == null && der == null;
        }

        int darPeso() {
            int peso = 1;
            if (izq != null) {
                peso += izq.darPeso();
            }
            if (der != null) {
                peso += der.darPeso();
            }
            return peso;
        }

        int darAltura() {
            int hi = izq == null ? 0 : izq.darAltura();
            int hd = der == null ? 0 : der.darAltura();
            return 1 + Math.max(hi, hd);
        }

        int contarHojas() {
            if (esHoja()) {
                return 1;
            }
            return (izq == null ? 0 : izq.contarHojas()) + (der == null ? 0 : der.contarHojas());
        }

        // Completo: todo elemento no terminal tiene exactamente dos hijos.
        boolean esCompleto() {
            if (esHoja()) {
                return true;
            }
            if (izq == null || der == null) {
                return false;
            }
            return izq.esCompleto() && der.esCompleto();
        }
    }

    private final NodoBinario<T> raiz;

    public ArbolBinario(NodoBinario<T> raiz) {
        this.raiz = raiz;
    }

    public int darPeso() {
        return raiz == null ? 0 : raiz.darPeso();
    }

    public int darAltura() {
        return raiz == null ? 0 : raiz.darAltura();
    }

    public int contarHojas() {
        return raiz == null ? 0 : raiz.contarHojas();
    }

    public boolean esCompleto() {
        return raiz == null || raiz.esCompleto();
    }

    static <T> NodoBinario<T> n(T e, NodoBinario<T> izq, NodoBinario<T> der) {
        return new NodoBinario<>(e, izq, der);
    }

    public static void main(String[] args) {
        ArbolBinario<Integer> t = new ArbolBinario<>(
                n(10, n(15, n(25, n(7, null, null), n(6, null, null)), null),
                      n(-6, null, n(18, null, null))));
        System.out.println("peso = " + t.darPeso());
        System.out.println("altura = " + t.darAltura());
        System.out.println("hojas = " + t.contarHojas());
        System.out.println("completo = " + t.esCompleto());
    }
}
```

**Prueba.** Con el árbol del ejemplo:

```text
peso = 7
altura = 4
hojas = 3
completo = false
```

Coincide con las respuestas de la sección 2 y con la última pestaña de la sección 3.

## Ejercicios

Practique con los [ejercicios de árboles binarios](exercises.md).

## Fuentes

- Aristizábal, A. *Árboles $n$-arios y árboles de búsqueda binaria*. Computación y Estructuras Discretas I, Universidad Icesi, 2026.
- Bedoya, O. *Árboles*. Diapositivas del curso, Universidad del Valle.

---

*Material adaptado del material original de los profesores Andrés Aristizábal y Oscar Bedoya.*
