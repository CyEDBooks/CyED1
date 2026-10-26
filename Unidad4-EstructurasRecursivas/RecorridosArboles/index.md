---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 4: Recorridos en preorden, inorden y postorden"
---

# Unidad 4: Recorridos en preorden, inorden y postorden

## 1. El problema

Hay que imprimir **todos** los elementos de un árbol, cada uno **exactamente una vez**. En una lista basta con ir de izquierda a derecha, pero un árbol no tiene un «siguiente» natural. **¿En qué orden se visitan los nodos?**

![Árbol de tres nodos](images/mini.svg)

> **¿De cuántas formas razonables se pueden listar $a$, $b$ y $c$ si los hijos siempre van de izquierda a derecha?**

:::{admonition} Respuesta
:class: dropdown
Lo único que cambia es **cuándo** se visita la raíz respecto a sus subárboles:

- antes de los dos: $a, b, c$ (**preorden**);
- entre los dos: $b, a, c$ (**inorden**);
- después de los dos: $b, c, a$ (**postorden**).
:::

Como el árbol es una estructura recursiva, cada subárbol se recorre **con la misma regla**.

## 2. Definiciones

Sea $T$ un árbol con raíz $r$ y subárboles $T_1, T_2, \dots, T_n$, de izquierda a derecha.

- **Preorden:** se visita $r$, luego se recorre $T_1$ en preorden, luego $T_2$ en preorden, así hasta $T_n$ en preorden.
- **Inorden:** se recorre $T_1$ en inorden, luego se visita $r$, luego se recorre $T_2$ en inorden, así hasta $T_n$ en inorden.
- **Postorden:** se recorre $T_1$ en postorden, $T_2$ en postorden, hasta $T_n$ en postorden, y luego se visita $r$.

En un árbol **binario** los subárboles son el izquierdo y el derecho:

```text
PREORDEN(x)              INORDEN(x)               POSTORDEN(x)
  if x ≠ NIL               if x ≠ NIL               if x ≠ NIL
      visitar(x)               INORDEN(x.izq)           POSTORDEN(x.izq)
      PREORDEN(x.izq)          visitar(x)               POSTORDEN(x.der)
      PREORDEN(x.der)          INORDEN(x.der)           visitar(x)
```

Los tres recorridos se diferencian en una sola cosa: la línea donde está `visitar(x)`.

### Recorrido en preorden

:::::{admonition} Recorrido en preorden
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![Recorrido en preorden: la regla](images/pre-regla.svg)

> La raíz es $e$, con subárboles $T_1$ (raíz $f$) y $T_2$ (raíz $b$). En preorden se recorre la raíz, luego $T_1$ completo en preorden y luego $T_2$ en preorden. Dentro de cada subárbol se aplica la **misma** regla.

:::
:::{tab-item} Paso 2
![preorden, paso 1](images/pre-00.svg)

:::
:::{tab-item} Paso 3
![preorden, paso 2](images/pre-01.svg)

> Después de $e$ se recorre **todo** $T_1$ en preorden: su raíz $f$ primero.

:::
:::{tab-item} Paso 4
![preorden, paso 3](images/pre-02.svg)

:::
:::{tab-item} Paso 5
![preorden, paso 4](images/pre-03.svg)

:::
:::{tab-item} Paso 6
![preorden, paso 5](images/pre-04.svg)

:::
:::{tab-item} Paso 7
![preorden, paso 6](images/pre-05.svg)

> Terminó $T_1$. Ahora se recorre $T_2$, que empieza en su raíz $b$.

:::
:::{tab-item} Paso 8
![preorden, paso 7](images/pre-06.svg)

:::
:::{tab-item} Paso 9
![preorden, paso 8](images/pre-07.svg)

:::
:::{tab-item} Paso 10
![preorden, paso 9](images/pre-08.svg)

:::
::::
:::::

### Recorrido en inorden

:::::{admonition} Recorrido en inorden
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![Recorrido en inorden: la regla](images/in-regla.svg)

> La raíz es $e$, con subárboles $T_1$ (raíz $f$) y $T_2$ (raíz $b$). En inorden se recorre $T_1$ completo en inorden, luego la raíz y luego $T_2$ en inorden. Dentro de cada subárbol se aplica la **misma** regla.

:::
:::{tab-item} Paso 2
![inorden, paso 1](images/in-00.svg)

> $a$ es el primero: se baja por el primer subárbol hasta donde se pueda antes de visitar cualquier raíz.

:::
:::{tab-item} Paso 3
![inorden, paso 2](images/in-01.svg)

:::
:::{tab-item} Paso 4
![inorden, paso 3](images/in-02.svg)

:::
:::{tab-item} Paso 5
![inorden, paso 4](images/in-03.svg)

:::
:::{tab-item} Paso 6
![inorden, paso 5](images/in-04.svg)

:::
:::{tab-item} Paso 7
![inorden, paso 6](images/in-05.svg)

> Se visita $e$ solo cuando ya se recorrió todo $T_1$.

:::
:::{tab-item} Paso 8
![inorden, paso 7](images/in-06.svg)

:::
:::{tab-item} Paso 9
![inorden, paso 8](images/in-07.svg)

:::
:::{tab-item} Paso 10
![inorden, paso 9](images/in-08.svg)

:::
::::
:::::

### Recorrido en postorden

:::::{admonition} Recorrido en postorden
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![Recorrido en postorden: la regla](images/post-regla.svg)

> La raíz es $e$, con subárboles $T_1$ (raíz $f$) y $T_2$ (raíz $b$). En postorden se recorre $T_1$ completo en postorden, luego $T_2$ en postorden y al final la raíz. Dentro de cada subárbol se aplica la **misma** regla.

:::
:::{tab-item} Paso 2
![postorden, paso 1](images/post-00.svg)

:::
:::{tab-item} Paso 3
![postorden, paso 2](images/post-01.svg)

:::
:::{tab-item} Paso 4
![postorden, paso 3](images/post-02.svg)

:::
:::{tab-item} Paso 5
![postorden, paso 4](images/post-03.svg)

:::
:::{tab-item} Paso 6
![postorden, paso 5](images/post-04.svg)

> $f$ va después de todo su subárbol: $a$, y luego $c, g, d$.

:::
:::{tab-item} Paso 7
![postorden, paso 6](images/post-05.svg)

:::
:::{tab-item} Paso 8
![postorden, paso 7](images/post-06.svg)

:::
:::{tab-item} Paso 9
![postorden, paso 8](images/post-07.svg)

:::
:::{tab-item} Paso 10
![postorden, paso 9](images/post-08.svg)

> La raíz $e$ es siempre la **última** en postorden.

:::
::::
:::::

| Recorrido | Resultado |
|---|---|
| Preorden | e – f – a – d – c – g – b – h – i |
| Inorden | a – f – c – d – g – e – h – b – i |
| Postorden | a – c – g – d – f – h – i – b – e |

> **¿Qué tienen en común los tres resultados?**

:::{admonition} Respuesta
:class: dropdown
La raíz $e$ es la **primera** en preorden y la **última** en postorden. En inorden separa los nodos del subárbol $T_1$ ($a, f, c, d, g$) de los del subárbol $T_2$ ($h, b, i$). Y en los tres, cada subárbol aparece **seguido**, sin mezclarse con otros nodos.
:::

### Un hijo solo: ¿izquierdo o derecho?

En un árbol binario importa de qué lado cuelga un hijo único. En este árbol, $h$ tiene un solo hijo, $j$, **a la derecha**:

![h con un solo hijo a la derecha](images/solo.svg)

> **¿Va $j$ antes o después de $h$ en inorden?**

:::{admonition} Respuesta
:class: dropdown
Después: el subárbol izquierdo de $h$ está vacío, así que se visita $h$ y luego su subárbol derecho, $j$. El inorden es a – b – c – d – h – j. Si $j$ colgara a la izquierda, iría antes: $\dots, j, h, \dots$.
:::

### Árboles $n$-arios

En un árbol $n$-ario, el preorden incluye primero la raíz y luego recorre en preorden todos sus subárboles. El orden que resulta no cumple ninguna propiedad particular, pero se garantiza que cada elemento del árbol aparece **exactamente una vez**.

![nario](images/nario.svg)

> **Muestre el recorrido en preorden, inorden y postorden para el árbol.**

:::{admonition} Respuesta
:class: dropdown
- Preorden: a – b – c – e – f – d – g – j – k – l – m – h – i
- Inorden: b – a – e – c – f – j – g – k – l – m – d – h – i
- Postorden: b – e – f – c – j – k – l – m – g – h – i – d – a

En inorden, la raíz va después del **primer** subárbol: $b$, luego $a$, luego los subárboles de $c$ y de $d$. Dentro de $g$, que tiene cuatro hijos, va $j$, luego $g$, luego $k, l, m$.
:::

### Recorrido por niveles

También se puede recorrer **nivel por nivel**, de izquierda a derecha: primero la raíz, luego los elementos del nivel $1$, y así sucesivamente. Para el árbol de las pestañas: e – f – b – a – d – h – i – c – g. Es el recorrido BFS de la Unidad 5, que usa una **cola**; los otros tres bajan por un subárbol hasta el fondo antes de pasar al siguiente, como el DFS.

## 3. Ejemplos

Cinco ejemplos por recorrido, de muy fácil a difícil. En las figuras, el **anillo rojo** señala el nodo del que habla cada paso; las **sombras** marcan subárboles (azul, el izquierdo; naranja, el derecho). El número junto a cada nodo es su turno en el recorrido: en rojo, el que se acaba de visitar. En preorden la sombra roja es el subárbol al que se acaba de entrar; en inorden y postorden, la sombra marca lo que **ya** se recorrió y por eso permite visitar el nodo.

### Preorden

**Ejemplo 1 (muy fácil).** Recorra el árbol en preorden (raíz, subárbol izquierdo, subárbol derecho).

![Árbol del ejemplo](images/ejpre1-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![preorden, paso 1](images/ejpre1-01.svg)

> Se empieza por la raíz $k$: en preorden la raíz va **primero**.

:::
:::{tab-item} Paso 2
![preorden, paso 2](images/ejpre1-02.svg)

> $m$ es la raíz del subárbol **izquierdo** de $k$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 3
![preorden, paso 3](images/ejpre1-03.svg)

> Como se terminó el subárbol izquierdo de $k$, sigue el **derecho**, que empieza por su raíz $d$.

> **Preorden:** k – m – d.

:::
::::
:::::

**Ejemplo 2 (fácil).** Recorra el árbol en preorden (raíz, subárbol izquierdo, subárbol derecho).

![Árbol del ejemplo](images/ejpre2-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![preorden, paso 1](images/ejpre2-01.svg)

> Se empieza por la raíz $f$: en preorden la raíz va **primero**.

:::
:::{tab-item} Paso 2
![preorden, paso 2](images/ejpre2-02.svg)

> $c$ es la raíz del subárbol **izquierdo** de $f$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 3
![preorden, paso 3](images/ejpre2-03.svg)

> $a$ es la raíz del subárbol **izquierdo** de $c$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 4
![preorden, paso 4](images/ejpre2-04.svg)

> Como se terminó el subárbol izquierdo de $c$, sigue el **derecho**, que empieza por su raíz $g$.

:::
:::{tab-item} Paso 5
![preorden, paso 5](images/ejpre2-05.svg)

> Como se terminó el subárbol izquierdo de $f$, sigue el **derecho**, que empieza por su raíz $e$.

> **Preorden:** f – c – a – g – e.

:::
::::
:::::

**Ejemplo 3 (medio).** Recorra el árbol en preorden (raíz, subárbol izquierdo, subárbol derecho).

![Árbol del ejemplo](images/ejpre3-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![preorden, paso 1](images/ejpre3-01.svg)

> Se empieza por la raíz $d$: en preorden la raíz va **primero**.

:::
:::{tab-item} Paso 2
![preorden, paso 2](images/ejpre3-02.svg)

> $h$ es la raíz del subárbol **izquierdo** de $d$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 3
![preorden, paso 3](images/ejpre3-03.svg)

> $b$ es la raíz del subárbol **izquierdo** de $h$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 4
![preorden, paso 4](images/ejpre3-04.svg)

> Como se terminó el subárbol izquierdo de $d$, sigue el **derecho**, que empieza por su raíz $k$.

:::
:::{tab-item} Paso 5
![preorden, paso 5](images/ejpre3-05.svg)

> $e$ es la raíz del subárbol **izquierdo** de $k$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 6
![preorden, paso 6](images/ejpre3-06.svg)

> Como se terminó el subárbol izquierdo de $k$, sigue el **derecho**, que empieza por su raíz $a$.

:::
:::{tab-item} Paso 7
![preorden, paso 7](images/ejpre3-07.svg)

> $m$ es la raíz del subárbol **izquierdo** de $a$: se visita apenas se entra a ese subárbol, antes que sus hijos.

> **Preorden:** d – h – b – k – e – a – m.

:::
::::
:::::

**Ejemplo 4 (medio).** Recorra el árbol en preorden (raíz, subárbol izquierdo, subárbol derecho).

![Árbol del ejemplo](images/ejpre4-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![preorden, paso 1](images/ejpre4-01.svg)

> Se empieza por la raíz $g$: en preorden la raíz va **primero**.

:::
:::{tab-item} Paso 2
![preorden, paso 2](images/ejpre4-02.svg)

> $c$ es la raíz del subárbol **izquierdo** de $g$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 3
![preorden, paso 3](images/ejpre4-03.svg)

> $f$ es la raíz del subárbol **izquierdo** de $c$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 4
![preorden, paso 4](images/ejpre4-04.svg)

> Como $f$ no tiene subárbol izquierdo, sigue el **derecho**, que empieza por su raíz $j$.

:::
:::{tab-item} Paso 5
![preorden, paso 5](images/ejpre4-05.svg)

> Como se terminó el subárbol izquierdo de $c$, sigue el **derecho**, que empieza por su raíz $b$.

:::
:::{tab-item} Paso 6
![preorden, paso 6](images/ejpre4-06.svg)

> Como se terminó el subárbol izquierdo de $g$, sigue el **derecho**, que empieza por su raíz $m$.

:::
:::{tab-item} Paso 7
![preorden, paso 7](images/ejpre4-07.svg)

> $h$ es la raíz del subárbol **izquierdo** de $m$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 8
![preorden, paso 8](images/ejpre4-08.svg)

> $l$ es la raíz del subárbol **izquierdo** de $h$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 9
![preorden, paso 9](images/ejpre4-09.svg)

> Como se terminó el subárbol izquierdo de $h$, sigue el **derecho**, que empieza por su raíz $n$.

> **Preorden:** g – c – f – j – b – m – h – l – n.

:::
::::
:::::

**Ejemplo 5 (difícil).** Recorra el árbol en preorden (raíz, subárbol izquierdo, subárbol derecho).

![Árbol del ejemplo](images/ejpre5-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![preorden, paso 1](images/ejpre5-01.svg)

> Se empieza por la raíz $p$: en preorden la raíz va **primero**.

:::
:::{tab-item} Paso 2
![preorden, paso 2](images/ejpre5-02.svg)

> $e$ es la raíz del subárbol **izquierdo** de $p$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 3
![preorden, paso 3](images/ejpre5-03.svg)

> $k$ es la raíz del subárbol **izquierdo** de $e$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 4
![preorden, paso 4](images/ejpre5-04.svg)

> $a$ es la raíz del subárbol **izquierdo** de $k$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 5
![preorden, paso 5](images/ejpre5-05.svg)

> Como se terminó el subárbol izquierdo de $e$, sigue el **derecho**, que empieza por su raíz $r$.

:::
:::{tab-item} Paso 6
![preorden, paso 6](images/ejpre5-06.svg)

> $n$ es la raíz del subárbol **izquierdo** de $r$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 7
![preorden, paso 7](images/ejpre5-07.svg)

> $c$ es la raíz del subárbol **izquierdo** de $n$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 8
![preorden, paso 8](images/ejpre5-08.svg)

> Como se terminó el subárbol izquierdo de $n$, sigue el **derecho**, que empieza por su raíz $s$.

:::
:::{tab-item} Paso 9
![preorden, paso 9](images/ejpre5-09.svg)

> Como se terminó el subárbol izquierdo de $p$, sigue el **derecho**, que empieza por su raíz $b$.

:::
:::{tab-item} Paso 10
![preorden, paso 10](images/ejpre5-10.svg)

> $t$ es la raíz del subárbol **izquierdo** de $b$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 11
![preorden, paso 11](images/ejpre5-11.svg)

> Como $t$ no tiene subárbol izquierdo, sigue el **derecho**, que empieza por su raíz $h$.

:::
:::{tab-item} Paso 12
![preorden, paso 12](images/ejpre5-12.svg)

> $f$ es la raíz del subárbol **izquierdo** de $h$: se visita apenas se entra a ese subárbol, antes que sus hijos.

:::
:::{tab-item} Paso 13
![preorden, paso 13](images/ejpre5-13.svg)

> Como se terminó el subárbol izquierdo de $b$, sigue el **derecho**, que empieza por su raíz $q$.

:::
:::{tab-item} Paso 14
![preorden, paso 14](images/ejpre5-14.svg)

> Como $q$ no tiene subárbol izquierdo, sigue el **derecho**, que empieza por su raíz $m$.

> **Preorden:** p – e – k – a – r – n – c – s – b – t – h – f – q – m.

:::
::::
:::::

### Inorden

**Ejemplo 1 (muy fácil).** Recorra el árbol en inorden (subárbol izquierdo, raíz, subárbol derecho).

![Árbol del ejemplo](images/ejin1-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![inorden, paso 1](images/ejin1-01.svg)

> Se baja siempre por la izquierda desde la raíz: $n$ → $r$. $r$ no tiene subárbol izquierdo: es el **primero**.

:::
:::{tab-item} Paso 2
![inorden, paso 2](images/ejin1-02.svg)

> Todo el subárbol izquierdo de $n$ ($r$) ya se recorrió: ahora toca $n$.

:::
:::{tab-item} Paso 3
![inorden, paso 3](images/ejin1-03.svg)

> $g$ no tiene subárbol izquierdo: se visita de inmediato.

> **Inorden:** r – n – g.

:::
::::
:::::

**Ejemplo 2 (fácil).** Recorra el árbol en inorden (subárbol izquierdo, raíz, subárbol derecho).

![Árbol del ejemplo](images/ejin2-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![inorden, paso 1](images/ejin2-01.svg)

> Se baja siempre por la izquierda desde la raíz: $e$ → $b$ → $d$. $d$ no tiene subárbol izquierdo: es el **primero**.

:::
:::{tab-item} Paso 2
![inorden, paso 2](images/ejin2-02.svg)

> Todo el subárbol izquierdo de $b$ ($d$) ya se recorrió: ahora toca $b$.

:::
:::{tab-item} Paso 3
![inorden, paso 3](images/ejin2-03.svg)

> $h$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 4
![inorden, paso 4](images/ejin2-04.svg)

> Todo el subárbol izquierdo de $e$ ($d$, $b$, $h$) ya se recorrió: ahora toca $e$.

:::
:::{tab-item} Paso 5
![inorden, paso 5](images/ejin2-05.svg)

> $c$ no tiene subárbol izquierdo: se visita de inmediato.

> **Inorden:** d – b – h – e – c.

:::
::::
:::::

**Ejemplo 3 (medio).** Recorra el árbol en inorden (subárbol izquierdo, raíz, subárbol derecho).

![Árbol del ejemplo](images/ejin3-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![inorden, paso 1](images/ejin3-01.svg)

> Se baja siempre por la izquierda desde la raíz: $k$ → $d$. $d$ no tiene subárbol izquierdo: es el **primero**.

:::
:::{tab-item} Paso 2
![inorden, paso 2](images/ejin3-02.svg)

> $f$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 3
![inorden, paso 3](images/ejin3-03.svg)

> Todo el subárbol izquierdo de $k$ ($d$, $f$) ya se recorrió: ahora toca $k$.

:::
:::{tab-item} Paso 4
![inorden, paso 4](images/ejin3-04.svg)

> $a$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 5
![inorden, paso 5](images/ejin3-05.svg)

> Todo el subárbol izquierdo de $j$ ($a$) ya se recorrió: ahora toca $j$.

:::
:::{tab-item} Paso 6
![inorden, paso 6](images/ejin3-06.svg)

> Todo el subárbol izquierdo de $p$ ($a$, $j$) ya se recorrió: ahora toca $p$.

:::
:::{tab-item} Paso 7
![inorden, paso 7](images/ejin3-07.svg)

> $s$ no tiene subárbol izquierdo: se visita de inmediato.

> **Inorden:** d – f – k – a – j – p – s.

:::
::::
:::::

**Ejemplo 4 (medio).** Recorra el árbol en inorden (subárbol izquierdo, raíz, subárbol derecho).

![Árbol del ejemplo](images/ejin4-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![inorden, paso 1](images/ejin4-01.svg)

> Se baja siempre por la izquierda desde la raíz: $h$ → $c$ → $e$. $e$ no tiene subárbol izquierdo: es el **primero**.

:::
:::{tab-item} Paso 2
![inorden, paso 2](images/ejin4-02.svg)

> $b$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 3
![inorden, paso 3](images/ejin4-03.svg)

> Todo el subárbol izquierdo de $c$ ($e$, $b$) ya se recorrió: ahora toca $c$.

:::
:::{tab-item} Paso 4
![inorden, paso 4](images/ejin4-04.svg)

> $n$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 5
![inorden, paso 5](images/ejin4-05.svg)

> Todo el subárbol izquierdo de $g$ ($n$) ya se recorrió: ahora toca $g$.

:::
:::{tab-item} Paso 6
![inorden, paso 6](images/ejin4-06.svg)

> Todo el subárbol izquierdo de $h$ ($e$, $b$, $c$, $n$, $g$) ya se recorrió: ahora toca $h$.

:::
:::{tab-item} Paso 7
![inorden, paso 7](images/ejin4-07.svg)

> $r$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 8
![inorden, paso 8](images/ejin4-08.svg)

> $t$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 9
![inorden, paso 9](images/ejin4-09.svg)

> Todo el subárbol izquierdo de $l$ ($t$) ya se recorrió: ahora toca $l$.

> **Inorden:** e – b – c – n – g – h – r – t – l.

:::
::::
:::::

**Ejemplo 5 (difícil).** Recorra el árbol en inorden (subárbol izquierdo, raíz, subárbol derecho).

![Árbol del ejemplo](images/ejin5-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![inorden, paso 1](images/ejin5-01.svg)

> Se baja siempre por la izquierda desde la raíz: $a$ → $q$ → $f$. $f$ no tiene subárbol izquierdo: es el **primero**.

:::
:::{tab-item} Paso 2
![inorden, paso 2](images/ejin5-02.svg)

> $k$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 3
![inorden, paso 3](images/ejin5-03.svg)

> Todo el subárbol izquierdo de $m$ ($k$) ya se recorrió: ahora toca $m$.

:::
:::{tab-item} Paso 4
![inorden, paso 4](images/ejin5-04.svg)

> Todo el subárbol izquierdo de $q$ ($f$, $k$, $m$) ya se recorrió: ahora toca $q$.

:::
:::{tab-item} Paso 5
![inorden, paso 5](images/ejin5-05.svg)

> $e$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 6
![inorden, paso 6](images/ejin5-06.svg)

> Todo el subárbol izquierdo de $z$ ($e$) ya se recorrió: ahora toca $z$.

:::
:::{tab-item} Paso 7
![inorden, paso 7](images/ejin5-07.svg)

> Todo el subárbol izquierdo de $a$ ($f$, $k$, $m$, $q$, $e$, $z$) ya se recorrió: ahora toca $a$.

:::
:::{tab-item} Paso 8
![inorden, paso 8](images/ejin5-08.svg)

> $n$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 9
![inorden, paso 9](images/ejin5-09.svg)

> $w$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 10
![inorden, paso 10](images/ejin5-10.svg)

> Todo el subárbol izquierdo de $d$ ($n$, $w$) ya se recorrió: ahora toca $d$.

:::
:::{tab-item} Paso 11
![inorden, paso 11](images/ejin5-11.svg)

> $h$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 12
![inorden, paso 12](images/ejin5-12.svg)

> $c$ no tiene subárbol izquierdo: se visita de inmediato.

:::
:::{tab-item} Paso 13
![inorden, paso 13](images/ejin5-13.svg)

> Todo el subárbol izquierdo de $j$ ($h$, $c$) ya se recorrió: ahora toca $j$.

:::
:::{tab-item} Paso 14
![inorden, paso 14](images/ejin5-14.svg)

> $y$ no tiene subárbol izquierdo: se visita de inmediato.

> **Inorden:** f – k – m – q – e – z – a – n – w – d – h – c – j – y.

:::
::::
:::::

> **En el ejemplo 5, $h$ va antes que $c$ aunque $c$ esté más abajo. ¿Por qué?**

:::{admonition} Respuesta
:class: dropdown
$c$ es hijo **derecho** de $h$. En inorden, un nodo va antes que todo su subárbol derecho, sin importar la profundidad. En el dibujo se nota: en inorden los nodos salen de izquierda a derecha, y $h$ está a la izquierda de $c$.
:::

### Postorden

**Ejemplo 1 (muy fácil).** Recorra el árbol en postorden (subárbol izquierdo, subárbol derecho, raíz).

![Árbol del ejemplo](images/ejpost1-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![postorden, paso 1](images/ejpost1-01.svg)

> Se baja por los subárboles izquierdos hasta la primera hoja: $c$ → $f$. Las hojas no tienen nada pendiente debajo: $f$ va **primero**.

:::
:::{tab-item} Paso 2
![postorden, paso 2](images/ejpost1-02.svg)

> $h$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 3
![postorden, paso 3](images/ejpost1-03.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($f$) y el derecho ($h$): ahora sí $c$. Es la raíz: va de **última**.

> **Postorden:** f – h – c.

:::
::::
:::::

**Ejemplo 2 (fácil).** Recorra el árbol en postorden (subárbol izquierdo, subárbol derecho, raíz).

![Árbol del ejemplo](images/ejpost2-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![postorden, paso 1](images/ejpost2-01.svg)

> Se baja por los subárboles izquierdos hasta la primera hoja: $m$ → $a$ → $k$. Las hojas no tienen nada pendiente debajo: $k$ va **primero**.

:::
:::{tab-item} Paso 2
![postorden, paso 2](images/ejpost2-02.svg)

> $d$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 3
![postorden, paso 3](images/ejpost2-03.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($k$) y el derecho ($d$): ahora sí $a$.

:::
:::{tab-item} Paso 4
![postorden, paso 4](images/ejpost2-04.svg)

> $p$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 5
![postorden, paso 5](images/ejpost2-05.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($k$, $d$, $a$) y el derecho ($p$): ahora sí $m$. Es la raíz: va de **última**.

> **Postorden:** k – d – a – p – m.

:::
::::
:::::

**Ejemplo 3 (medio).** Recorra el árbol en postorden (subárbol izquierdo, subárbol derecho, raíz).

![Árbol del ejemplo](images/ejpost3-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![postorden, paso 1](images/ejpost3-01.svg)

> Se baja por los subárboles izquierdos hasta la primera hoja: $b$ → $g$ → $e$ → $c$. Las hojas no tienen nada pendiente debajo: $c$ va **primero**.

:::
:::{tab-item} Paso 2
![postorden, paso 2](images/ejpost3-02.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($c$): ahora sí $e$.

:::
:::{tab-item} Paso 3
![postorden, paso 3](images/ejpost3-03.svg)

> Ya se recorrieron sus subárboles, el derecho ($c$, $e$): ahora sí $g$.

:::
:::{tab-item} Paso 4
![postorden, paso 4](images/ejpost3-04.svg)

> $f$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 5
![postorden, paso 5](images/ejpost3-05.svg)

> $h$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 6
![postorden, paso 6](images/ejpost3-06.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($f$) y el derecho ($h$): ahora sí $n$.

:::
:::{tab-item} Paso 7
![postorden, paso 7](images/ejpost3-07.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($c$, $e$, $g$) y el derecho ($f$, $h$, $n$): ahora sí $b$. Es la raíz: va de **última**.

> **Postorden:** c – e – g – f – h – n – b.

:::
::::
:::::

**Ejemplo 4 (medio).** Recorra el árbol en postorden (subárbol izquierdo, subárbol derecho, raíz).

![Árbol del ejemplo](images/ejpost4-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![postorden, paso 1](images/ejpost4-01.svg)

> Se baja por los subárboles izquierdos hasta la primera hoja: $t$ → $j$ → $a$ → $d$. Las hojas no tienen nada pendiente debajo: $d$ va **primero**.

:::
:::{tab-item} Paso 2
![postorden, paso 2](images/ejpost4-02.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($d$): ahora sí $a$.

:::
:::{tab-item} Paso 3
![postorden, paso 3](images/ejpost4-03.svg)

> $k$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 4
![postorden, paso 4](images/ejpost4-04.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($d$, $a$) y el derecho ($k$): ahora sí $j$.

:::
:::{tab-item} Paso 5
![postorden, paso 5](images/ejpost4-05.svg)

> $e$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 6
![postorden, paso 6](images/ejpost4-06.svg)

> $q$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 7
![postorden, paso 7](images/ejpost4-07.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($e$) y el derecho ($q$): ahora sí $w$.

:::
:::{tab-item} Paso 8
![postorden, paso 8](images/ejpost4-08.svg)

> Ya se recorrieron sus subárboles, el derecho ($e$, $q$, $w$): ahora sí $r$.

:::
:::{tab-item} Paso 9
![postorden, paso 9](images/ejpost4-09.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($d$, $a$, $k$, $j$) y el derecho ($e$, $q$, $w$, $r$): ahora sí $t$. Es la raíz: va de **última**.

> **Postorden:** d – a – k – j – e – q – w – r – t.

:::
::::
:::::

**Ejemplo 5 (difícil).** Recorra el árbol en postorden (subárbol izquierdo, subárbol derecho, raíz).

![Árbol del ejemplo](images/ejpost5-00.svg)

:::::{admonition} Paso a paso
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![postorden, paso 1](images/ejpost5-01.svg)

> Se baja por los subárboles izquierdos hasta la primera hoja: $h$ → $c$ → $m$ → $b$ → $s$. Las hojas no tienen nada pendiente debajo: $s$ va **primero**.

:::
:::{tab-item} Paso 2
![postorden, paso 2](images/ejpost5-02.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($s$): ahora sí $b$.

:::
:::{tab-item} Paso 3
![postorden, paso 3](images/ejpost5-03.svg)

> Ya se recorrieron sus subárboles, el derecho ($s$, $b$): ahora sí $m$.

:::
:::{tab-item} Paso 4
![postorden, paso 4](images/ejpost5-04.svg)

> $f$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 5
![postorden, paso 5](images/ejpost5-05.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($f$): ahora sí $g$.

:::
:::{tab-item} Paso 6
![postorden, paso 6](images/ejpost5-06.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($s$, $b$, $m$) y el derecho ($f$, $g$): ahora sí $c$.

:::
:::{tab-item} Paso 7
![postorden, paso 7](images/ejpost5-07.svg)

> $x$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 8
![postorden, paso 8](images/ejpost5-08.svg)

> Ya se recorrieron sus subárboles, el derecho ($x$): ahora sí $e$.

:::
:::{tab-item} Paso 9
![postorden, paso 9](images/ejpost5-09.svg)

> $k$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 10
![postorden, paso 10](images/ejpost5-10.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($k$): ahora sí $p$.

:::
:::{tab-item} Paso 11
![postorden, paso 11](images/ejpost5-11.svg)

> $v$ es hoja: no tiene subárboles pendientes, se visita.

:::
:::{tab-item} Paso 12
![postorden, paso 12](images/ejpost5-12.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($k$, $p$) y el derecho ($v$): ahora sí $a$.

:::
:::{tab-item} Paso 13
![postorden, paso 13](images/ejpost5-13.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($x$, $e$) y el derecho ($k$, $p$, $v$, $a$): ahora sí $r$.

:::
:::{tab-item} Paso 14
![postorden, paso 14](images/ejpost5-14.svg)

> Ya se recorrieron sus subárboles, el izquierdo ($s$, $b$, $m$, $f$, $g$, $c$) y el derecho ($x$, $e$, $k$, $p$, $v$, $a$, $r$): ahora sí $h$. Es la raíz: va de **última**.

> **Postorden:** s – b – m – f – g – c – x – e – k – p – v – a – r – h.

:::
::::
:::::

## 4. Notación infija, prefija y postfija

Los recorridos permiten escribir expresiones complejas: proposiciones compuestas, combinaciones de conjuntos y expresiones aritméticas. En una expresión aritmética con suma ($+$), resta ($-$), multiplicación ($*$), división ($/$) y potencia ($↑$), cada operador tiene dos operandos, así que la expresión se representa con un **árbol binario**: los nodos internos son operadores y las hojas son operandos.

Muestre un árbol binario que represente la expresión $((x+y)↑2)+((x-4)/3)$:

:::::{admonition} Árbol de ((x+y)↑2)+((x−4)/3)
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
![Árbol de expresión, paso 1](images/expr-00.svg)

> Se empieza por los paréntesis de adentro: $x+y$.

:::
:::{tab-item} Paso 2
![Árbol de expresión, paso 2](images/expr-01.svg)

> $(x+y)↑2$: el árbol de $x+y$ es el operando izquierdo de $↑$.

:::
:::{tab-item} Paso 3
![Árbol de expresión, paso 3](images/expr-02.svg)

> Por el otro lado, $x-4$.

:::
:::{tab-item} Paso 4
![Árbol de expresión, paso 4](images/expr-03.svg)

> $(x-4)/3$: el árbol de $x-4$ es el operando izquierdo de $/$.

:::
:::{tab-item} Paso 5
![Árbol de expresión, paso 5](images/expr-04.svg)

> El $+$ del centro se evalúa **último**: es la raíz, con los dos árboles como subárboles.

:::
::::
:::::

Los tres recorridos dan tres **notaciones**:

| Recorrido | Notación | Resultado |
|---|---|---|
| Inorden | infija | $((x + y) ↑ 2) + ((x - 4) / 3)$ |
| Preorden | prefija | `+ ↑ + x y 2 / − x 4 3` |
| Postorden | postfija | `x y + 2 ↑ x 4 − 3 / +` |

> **¿Por qué la notación infija necesita paréntesis y las otras dos no?**

:::{admonition} Respuesta
:class: dropdown
En inorden, $x + y ↑ 2$ puede venir de dos árboles distintos: $(x + y) ↑ 2$ o $x + (y ↑ 2)$. Los paréntesis deshacen la ambigüedad. En prefija y en postfija cada operador tiene exactamente dos operandos en un lugar fijo, así que el árbol se reconstruye sin ambigüedad.
:::

Represente en notación infija, prefija y postfija la expresión dada por el siguiente árbol:

![Árbol de expresión](images/ocho.svg)

:::{admonition} Respuesta
:class: dropdown
- Notación infija: $((8-6)↑3)+(10/(7-2))$
- Notación prefija: `+ ↑ − 8 6 3 / 10 − 7 2`
- Notación postfija: `8 6 − 3 ↑ 10 7 2 − / +`
:::

### Evaluar en notación prefija

Se busca el operador **más a la derecha** que esté seguido de dos números, se reemplaza por su resultado y se repite:

:::::{admonition} Evaluar + ↑ − 8 6 3 / 10 − 7 2
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
- **`+ ↑ − 8 6 3 / 10 − 7 2`** ←

> El operador más a la derecha seguido de dos números es `− 7 2`: se reemplaza por $5$.

:::
:::{tab-item} Paso 2
- `+ ↑ − 8 6 3 / 10 − 7 2`
- **`+ ↑ − 8 6 3 / 10 5`** ←

:::
:::{tab-item} Paso 3
- `+ ↑ − 8 6 3 / 10 − 7 2`
- `+ ↑ − 8 6 3 / 10 5`
- **`+ ↑ − 8 6 3 2`** ←

:::
:::{tab-item} Paso 4
- `+ ↑ − 8 6 3 / 10 − 7 2`
- `+ ↑ − 8 6 3 / 10 5`
- `+ ↑ − 8 6 3 2`
- **`+ ↑ 2 3 2`** ←

:::
:::{tab-item} Paso 5
- `+ ↑ − 8 6 3 / 10 − 7 2`
- `+ ↑ − 8 6 3 / 10 5`
- `+ ↑ − 8 6 3 2`
- `+ ↑ 2 3 2`
- **`+ 8 2`** ←

:::
:::{tab-item} Paso 6
- `+ ↑ − 8 6 3 / 10 − 7 2`
- `+ ↑ − 8 6 3 / 10 5`
- `+ ↑ − 8 6 3 2`
- `+ ↑ 2 3 2`
- `+ 8 2`
- **`10`** ←

> Queda un solo número: el valor es **10**.

:::
::::
:::::

### Evaluar en notación postfija

Al revés: se busca el operador **más a la izquierda** que esté precedido de dos números:

:::::{admonition} Evaluar 8 6 − 3 ↑ 10 7 2 − / +
:class: dropdown
::::{tab-set}
:::{tab-item} Paso 1
- **`8 6 − 3 ↑ 10 7 2 − / +`** ←

> El operador más a la izquierda precedido de dos números es `8 6 −`: se reemplaza por $2$.

:::
:::{tab-item} Paso 2
- `8 6 − 3 ↑ 10 7 2 − / +`
- **`2 3 ↑ 10 7 2 − / +`** ←

:::
:::{tab-item} Paso 3
- `8 6 − 3 ↑ 10 7 2 − / +`
- `2 3 ↑ 10 7 2 − / +`
- **`8 10 7 2 − / +`** ←

:::
:::{tab-item} Paso 4
- `8 6 − 3 ↑ 10 7 2 − / +`
- `2 3 ↑ 10 7 2 − / +`
- `8 10 7 2 − / +`
- **`8 10 5 / +`** ←

:::
:::{tab-item} Paso 5
- `8 6 − 3 ↑ 10 7 2 − / +`
- `2 3 ↑ 10 7 2 − / +`
- `8 10 7 2 − / +`
- `8 10 5 / +`
- **`8 2 +`** ←

:::
:::{tab-item} Paso 6
- `8 6 − 3 ↑ 10 7 2 − / +`
- `2 3 ↑ 10 7 2 − / +`
- `8 10 7 2 − / +`
- `8 10 5 / +`
- `8 2 +`
- **`10`** ←

> Queda un solo número: el valor es **10**.

:::
::::
:::::

Las dos dan $10$, el valor de $((8-6)↑3)+(10/(7-2)) = 2^3 + 2$.

## Ejercicios

Practique con los [ejercicios de recorridos](exercises.md).

## Fuentes

- Bedoya, O. *Árboles: recorridos de los árboles, notación infija, prefija y postfija*. Diapositivas del curso, Universidad del Valle.
- Aristizábal, A. *Árboles $n$-arios* (preorden en un árbol $n$-ario). Computación y Estructuras Discretas I, Universidad Icesi, 2026.
- Vargas Forero, V. M. *Estructuras de datos: recorrido de árboles binarios* (preorden, inorden, postorden y por niveles). Universidad del Valle.
- Rosen, K. H. *Discrete Mathematics and Its Applications*, 7.ª ed. McGraw-Hill, 2011. Sección 11.3.

---

*Material adaptado del material original de los profesores Oscar Bedoya y Andrés Aristizábal.*
