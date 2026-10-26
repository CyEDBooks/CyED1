---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 4: Árboles binarios ordenados y de búsqueda"
---

# Unidad 4: Árboles binarios ordenados y de búsqueda

## 1. El problema

En una bolsa hay $27$ fichas, cada una con una llave. **Buscar la llave $45$.**

{{GEN:fig-bolsa}}

:::{admonition} Respuesta
:class: dropdown
Sin ningún orden, no queda más que sacar fichas una por una: $28, 38, 8, 7, 12, 19, 32, 4, 9, 16, 21, 1, 5, 45$. Se necesitan **$14$ comparaciones**, y en el peor caso, $27$.
:::

Si las llaves estuvieran en una **lista ordenada**, se podría usar la **búsqueda binaria**: dividir sucesivamente la lista por la mitad hasta encontrar el elemento. Buscar $6$ en la lista $1, 2, 5, 6, 10, 22, 26, 32, 40, 50$:

{{GEN:binaria}}

Pero en una lista, insertar o quitar una llave obliga a correr las demás. Las mismas $27$ llaves de la bolsa, organizadas en un árbol:

{{GEN:fig-bed}}

{{GEN:buscar-45}}

**¿Qué propiedad del árbol permite descartar la mitad de las llaves en cada comparación?**

## 2. Árbol binario de búsqueda

**Árbol binario de búsqueda (ABB).** Es un árbol binario en el que cada vértice tiene una **llave**. La llave de un vértice es **mayor** que las llaves de los vértices de su subárbol izquierdo y **menor** que las llaves de los vértices de su subárbol derecho.

{{GEN:fig-def-bed}}

Con llaves repetidas, la propiedad se escribe con $\le$ y $\ge$. Sea $x$ un nodo del árbol:

- si $y$ es un nodo del subárbol **izquierdo** de $x$, entonces $key[y] \le key[x]$;
- si $y$ es un nodo del subárbol **derecho** de $x$, entonces $key[y] \ge key[x]$.

{{GEN:fig-def-and}}

A un árbol binario en el que todos los elementos del subárbol izquierdo son menores que la raíz, todos los del derecho son mayores y ambos subárboles son a su vez ordenados, también se le llama **árbol binario ordenado**.

> **Recorra el árbol de la derecha en inorden. ¿Qué observa?**

:::{admonition} Respuesta
:class: dropdown
$1, 20, 21, 24, 26, 30, 34$: si se recorre en inorden, un ABB produce la lista de sus llaves **ordenada ascendentemente**. En inorden se visita primero todo lo menor (el subárbol izquierdo), luego la raíz y luego todo lo mayor.

```text
INORDER-TREE-WALK(x)
1  if x ≠ NIL
2      INORDER-TREE-WALK(left[x])
3      print key[x]
4      INORDER-TREE-WALK(right[x])
```

Visita cada nodo una vez: toma $\Theta(n)$ en un árbol de $n$ nodos.
:::

Las operaciones básicas (insertar, borrar, buscar) toman un tiempo **proporcional a la altura** del árbol. Para un árbol binario completo con $n$ nodos toman $\Theta(\log n)$; si el árbol se construye como una cadena lineal de $n$ nodos, toman $\Theta(n)$.

## 3. Consultas

Las consultas sobre un ABB son: **buscar** una llave, el **mínimo**, el **máximo**, el **sucesor** y el **predecesor** de un nodo. Cada una recorre un solo camino del árbol: todas toman $O(h)$, con $h$ la altura del árbol.

### Buscar

Para buscar un nodo con llave $k$ empezando en el nodo $x$ (la raíz): si $x$ es `nil` o tiene la llave $k$, terminar. Si $k$ es menor, buscar en el subárbol izquierdo; si es mayor, en el derecho.

```text
TREE-SEARCH(x, k)                       ITERATIVE-TREE-SEARCH(x, k)
1  if x = NIL or k = key[x]             1  while x ≠ NIL and k ≠ key[x]
2      return x                         2      if k < key[x]
3  if k < key[x]                        3          x ← left[x]
4      return TREE-SEARCH(left[x], k)   4      else x ← right[x]
5  else return TREE-SEARCH(right[x], k) 5  return x
```

Si la llave no está, la búsqueda baja hasta un subárbol vacío:

{{GEN:buscar-11}}

### Mínimo y máximo

> **¿En un ABB dónde se ubica el elemento mínimo? ¿Y el máximo?**

{{GEN:fig-minmax}}

:::{admonition} Respuesta
:class: dropdown
El mínimo: se siguen los apuntadores al hijo **izquierdo** desde la raíz hasta que se encuentre `nil`. El máximo: se siguen los apuntadores al hijo **derecho**.

| Mínimo | Máximo |
|---|---|
| {{GEN:fig-min}} | {{GEN:fig-max}} |

```text
TREE-MINIMUM(x)                 TREE-MAXIMUM(x)
1  while left[x] ≠ NIL          1  while right[x] ≠ NIL
2      x ← left[x]              2      x ← right[x]
3  return x                     3  return x
```

Este árbol tiene llaves repetidas: hay tres $4$ y dos $7$. La propiedad con $\le$ y $\ge$ se cumple, y el mínimo y el máximo se encuentran igual.
:::

### Sucesor y predecesor

Dado un nodo $x$ con $key[x] = k$:

- El **sucesor** de $x$ es el nodo $y$ tal que $key[y]$ es la **menor** llave mayor que $key[x]$: el que sigue a $x$ en inorden.
- El **predecesor** de $x$ es el nodo $y$ tal que $key[y]$ es la **mayor** llave menor que $key[x]$.

En el árbol de la sección 1, el sucesor de $19$ es $21$ y el de $21$ es $24$. Para encontrarlos hay dos casos:

{{GEN:succ-19}}

{{GEN:succ-21}}

```text
TREE-SUCCESSOR(x)
1  if right[x] ≠ NIL
2      return TREE-MINIMUM(right[x])
3  y ← p[x]
4  while y ≠ NIL and x = right[y]
5      x ← y
6      y ← p[y]
7  return y
```

> **¿Cuál es el sucesor de $53$?**

:::{admonition} Respuesta
:class: dropdown
No tiene: $53$ es el máximo. No tiene subárbol derecho, y al subir siempre se llega desde un hijo derecho ($53$ es hijo derecho de $51$, $51$ de $48$, $48$ de $43$ y $43$ de $24$) hasta la raíz, cuyo padre es `nil`. `TREE-SUCCESSOR` devuelve `nil`.
:::

## 4. Inserción

Para insertar el nodo $z$, se baja como en una búsqueda: $x$ es el nodo actual y $y$ va un paso atrás (el padre de $x$). Cuando $x$ llega a `nil`, $z$ se cuelga de $y$, como hoja.

```text
TREE-INSERT(T, z)
1  y ← NIL
2  x ← root[T]
3  while x ≠ NIL
4      y ← x
5      if key[z] < key[x]
6          x ← left[x]
7      else x ← right[x]
8  p[z] ← y
9  if y = NIL
10     root[T] ← z            // el árbol estaba vacío
11 else if key[z] < key[y]
12     left[y] ← z
13 else right[y] ← z
```

Explique el código anterior para el caso de `TREE-INSERT(z)` con $key[z] = 5$:

{{GEN:insertar}}

### El orden de inserción importa

> **¿Qué árbol resulta al insertar $1, 2, 3, 4, 5$, en ese orden?**

:::{admonition} Respuesta
:class: dropdown
{{GEN:fig-degenerado}}

Cada llave es mayor que todas las anteriores y siempre va a la derecha: el árbol es una **cadena** de altura $n$. Buscar $5$ toma $5$ comparaciones, igual que en la bolsa.
:::

Si el árbol se construye bien, la altura es cercana a $\log_2 n$; si es una cadena, es $n$. Los **árboles AVL** de la siguiente página evitan el caso malo.

## 5. Eliminación

Para borrar un nodo $z$ hay tres casos.

**Caso 1: $z$ no tiene hijos.** `TREE-DELETE(T, z)` con $key[z] = 5$. ¿Qué se debe hacer?

{{GEN:caso1}}

**Caso 2: $z$ tiene un solo hijo.** `TREE-DELETE(T, z)` con $key[z] = 10$. ¿Qué se debe hacer?

{{GEN:caso2}}

**Caso 3: $z$ tiene dos hijos.** `TREE-DELETE(T, z)` con $key[z] = 12$. ¿Qué se debe hacer?

{{GEN:caso3}}

```text
TREE-DELETE(T, z)
1  if left[z] = NIL or right[z] = NIL
2      y ← z                       // casos 1 y 2: se separa z
3  else y ← TREE-SUCCESSOR(z)      // caso 3: se separa el sucesor
4  if left[y] ≠ NIL
5      x ← left[y]
6  else x ← right[y]
7  if x ≠ NIL
8      p[x] ← p[y]
9  if p[y] = NIL
10     root[T] ← x
11 else if y = left[p[y]]
12     left[p[y]] ← x
13 else right[p[y]] ← x
14 if y ≠ z
15     key[z] ← key[y]             // la llave del sucesor reemplaza la de z
16 return y
```

## 6. Ejemplos

Cinco ejemplos, de muy fácil a difícil: se construye el ABB insertando las llaves una por una y luego se busca o se borra. En las figuras, el **anillo rojo** señala el nodo del que habla cada paso; las **sombras** marcan subárboles (azul, el izquierdo; naranja, el derecho); en verde, lo que se encontró. Cada ejemplo cierra comprobando que el resultado **es** un ABB.

{{GEN:ej1}}

{{GEN:ej2}}

{{GEN:ej3}}

{{GEN:ej4}}

{{GEN:ej5}}

## 7. Formalización

- Si $x$ es la raíz de un subárbol con $n$ nodos, `INORDER-TREE-WALK(x)` toma $\Theta(n)$ y lista las llaves en orden.
- `SEARCH`, `MINIMUM`, `MAXIMUM`, `SUCCESSOR`, `PREDECESSOR`, `INSERT` y `DELETE` toman $O(h)$ en un ABB de altura $h$.
- Para un árbol binario lleno con $n$ nodos, $h = \Theta(\log n)$; si el árbol es una cadena, $h = \Theta(n)$.

## Ejercicios

Practique con los [ejercicios de árboles binarios de búsqueda](exercises.md).

## Fuentes

- Aristizábal, A. *Árboles de búsqueda binaria* (propiedad, consultas, inserción, eliminación). Computación y Estructuras Discretas I, Universidad Icesi, 2026.
- Bedoya, O. *Árboles: árboles binarios de búsqueda* (buscar la llave 45, construir un ABB con una estructura dada). Diapositivas del curso, Universidad del Valle.
- Vargas Forero, V. M. *Estructuras de datos: árboles binarios ordenados, búsqueda binaria*. Universidad del Valle.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Capítulo 12.

---

*Material adaptado del material original de los profesores Andrés Aristizábal y Oscar Bedoya.*
