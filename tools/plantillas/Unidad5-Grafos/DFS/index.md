---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 5: Recorrido en profundidad (DFS)"
---

# Unidad 5: Recorrido en profundidad (DFS)


## 1. El problema

Usted está dentro de un laberinto con un ovillo de hilo. Cada cruce es un vértice y cada pasillo es una arista. **¿Cómo recorrer todos los cruces sin perderse y sin dar vueltas para siempre?**

Una estrategia natural:

1. Tome un pasillo que lleve a un cruce **nuevo** y siga avanzando todo lo que pueda.
2. Cuando no haya pasillos hacia cruces nuevos, **regrese** por el hilo al cruce anterior y vuelva al paso 1 desde allí.

Esa es la idea del recorrido en profundidad. En BFS se avanzaba por capas usando una cola; aquí se avanza por un camino hasta el fondo, y el «hilo» es una **pila** (la pila de llamadas de la recursión).

**Recorrido en profundidad (DFS, *depth-first search*).** Se explora siempre desde el vértice descubierto **más recientemente** que todavía tenga aristas sin explorar; cuando no le quedan, se regresa al vértice desde el que fue descubierto.

### Ejemplo 1

El mismo árbol que se usó en BFS, desde la raíz $A$, con los hijos revisados de izquierda a derecha. Junto a cada vértice se anotan dos tiempos: $d$, cuando se **descubre**, y $f$, cuando se **termina** (ya no tiene vecinos por explorar). Un vértice con solo $d$ (por ejemplo `3/`) está en proceso.

{{GEN:ej1}}

Orden de descubrimiento: {{GEN:ej1-orden}}. En BFS el orden era $A, B, G, C, D, E, H, F, I$. DFS baja por $B$ hasta el fondo antes de tocar $G$.

## 2. El algoritmo

Como en BFS, cada vértice tiene un **color**: blanco (no descubierto), gris (descubierto, en la pila de llamadas) y negro (terminado). Además, una variable global `tiempo` sirve para poner las **marcas de tiempo** $u.d$ y $u.f$.

```text
DFS(G)
1  for cada vértice u ∈ G.V
2      u.color = BLANCO
3      u.π = NIL
4  tiempo = 0
5  for cada vértice u ∈ G.V
6      if u.color == BLANCO
7          DFS-VISIT(G, u)

DFS-VISIT(G, u)
1  tiempo = tiempo + 1          // u se acaba de descubrir
2  u.d = tiempo
3  u.color = GRIS
4  for cada v ∈ G.Adj[u]        // explorar la arista (u, v)
5      if v.color == BLANCO
6          v.π = u
7          DFS-VISIT(G, v)
8  u.color = NEGRO              // u terminó
9  tiempo = tiempo + 1
10 u.f = tiempo
```

A diferencia de BFS, `DFS(G)` no recibe un origen: si después de una búsqueda quedan vértices blancos, arranca otra desde el siguiente vértice blanco (línea 5). Por eso el resultado puede ser **varios árboles**: un **bosque DF**.

### Ejemplo 2

Grafo dirigido; los vértices y las listas de adyacencia se recorren en orden alfabético.

{{GEN:fig-ej2}}

Las aristas en azul son las del bosque DF. Las punteadas son aristas que no descubren a nadie; la letra indica su tipo (sección 3).

{{GEN:ej2}}

Resultado:

{{GEN:ej2-final}}

> **¿Por qué hubo dos búsquedas?** Desde $u$ no se puede llegar a $w$ ni a $z$. Cuando termina la búsqueda desde $u$, el ciclo de `DFS(G)` encuentra a $w$ todavía blanco y arranca otra. El bosque DF tiene dos árboles: uno con raíz $u$ y otro con raíz $w$.

### Ejemplo 3

DFS sobre un grafo **no dirigido**, empezando por el vértice $1$, con listas en orden numérico.

{{GEN:fig-ej3}}

{{GEN:ej3}}

{{GEN:ej3-final}}

El árbol DF es el camino $1 - 2 - 3 - 4 - 5$: DFS se fue «hasta el fondo». En BFS desde $1$ el árbol sería mucho más bajo, porque $2$ y $5$ son vecinos de $1$ y quedarían en el nivel $1$.

## 3. Lo que dejan las marcas de tiempo

### Estructura de paréntesis

Escriba «$(u$» cuando se descubre $u$ y «$u)$» cuando termina. Para el Ejemplo 2:

```text
{{GEN:ej2-parens}}
```

Los paréntesis quedan **bien anidados**: nunca aparece algo como $(u\ (v\ u)\ v)$. Para cualquier par de vértices $u$ y $v$, los intervalos $[u.d, u.f]$ y $[v.d, v.f]$ son **disjuntos** o uno está **contenido** en el otro. Si $[v.d, v.f] \subset [u.d, u.f]$, entonces $v$ es descendiente de $u$ en el bosque DF.

### Clasificación de aristas

Cada arista $(u, v)$ se clasifica según el color de $v$ en el momento en que se explora:

| Tipo | Cuándo | Qué indica |
|---|---|---|
| **T** de árbol | $v$ es blanco | $v$ se descubre por esa arista |
| **B** de retorno | $v$ es gris | $v$ es antecesor de $u$: hay un **circuito** |
| **F** de avance | $v$ es negro y $u.d < v.d$ | $v$ es descendiente de $u$, pero ya se había descubierto por otro camino |
| **C** de cruce | $v$ es negro y $u.d > v.d$ | $v$ no es antecesor ni descendiente de $u$ (puede estar en otro árbol) |

Para el Ejemplo 2:

{{GEN:ej2-cls}}

> **¿Qué tipos de arista pueden aparecer en un grafo no dirigido?**

:::{admonition} Respuesta
:class: dropdown
Solo **de árbol** y **de retorno**. Cada arista $\{u, v\}$ se explora primero desde el extremo que se descubrió antes; si en ese momento el otro extremo ya fue descubierto, sigue gris, porque es un antecesor. En el Ejemplo 3 todas las aristas que no son del árbol son de retorno.
:::

**Consecuencia.** Un grafo dirigido tiene un circuito **si y solo si** DFS encuentra una arista de retorno.

## 4. Complejidad

- Los ciclos de `DFS(G)` (sin contar las llamadas) cuestan $\Theta(V)$.
- `DFS-VISIT` se llama exactamente una vez por vértice: solo se llama sobre vértices blancos, y lo primero que hace es pintarlos de gris.
- Dentro de `DFS-VISIT(G, u)` el ciclo recorre $G.Adj[u]$ una vez. Sumando sobre todos los vértices: $\sum_{u} |G.Adj[u]| = \Theta(E)$.

$$
T_{DFS}(V, E) = \Theta(V + E)
$$

## 5. Aplicación: orden topológico

Un profesor tiene que vestirse; una flecha $a \to b$ significa «$a$ va antes que $b$» (las medias antes que los zapatos, por ejemplo). El reloj no depende de nada.

{{GEN:fig-ropa}}

**¿En qué orden puede ponerse la ropa?** Hace falta un **orden topológico**: una lista de los vértices de un grafo dirigido **acíclico** en la que toda arista $(u, v)$ va de izquierda a derecha.

**Método.** Correr DFS y listar los vértices de **mayor a menor $f$**.

{{GEN:fig-ropa-df}}

Ordenando por $f$ decreciente:

**{{GEN:ropa-orden}}**

Funciona porque, en un grafo sin circuitos, toda arista $(u, v)$ cumple $v.f < u.f$: cuando se explora $(u, v)$, el vértice $v$ no puede ser gris (sería una arista de retorno, es decir, un circuito), así que es blanco y termina antes que $u$, o ya es negro y terminó antes.

## 6. Formalización

Las propiedades que se usaron en los ejemplos (Cormen et al., sección 22.3):

- **Subgrafo de predecesores.** $G_\pi = (V, E_\pi)$ con $E_\pi = \{(v.\pi, v) \mid v \in V \wedge v.\pi \neq \text{NIL}\}$. Es un **bosque DF** formado por uno o varios **árboles DF** disjuntos.
- $u = v.\pi$ si y solo si se llamó `DFS-VISIT(G, v)` mientras se recorría la lista de adyacencia de $u$. La forma del bosque DF es la forma del árbol de llamadas recursivas.
- Para todo $u$: $1 \le u.d < u.f \le 2|V|$. $u$ es blanco antes de $u.d$, gris entre $u.d$ y $u.f$, y negro después.
- **Teorema del paréntesis.** Para todo par $u, v$, exactamente una de estas condiciones se cumple: los intervalos $[u.d, u.f]$ y $[v.d, v.f]$ son disjuntos y ninguno es descendiente del otro; $[u.d, u.f] \subset [v.d, v.f]$ y $u$ es descendiente de $v$; o $[v.d, v.f] \subset [u.d, u.f]$ y $v$ es descendiente de $u$.
- **Teorema del camino blanco.** $v$ es descendiente de $u$ en el bosque DF si y solo si, en el instante $u.d$, existe un camino de $u$ a $v$ formado solo por vértices blancos.
- En un grafo no dirigido, toda arista es de árbol o de retorno.

## Ejercicios

Practique con los [ejercicios de DFS](exercises.md).

## Fuentes

- Aristizábal, A. y Gómez, M. *Grafos: recorridos (BFS y DFS)*. Computación y Estructuras Discretas I, Universidad Icesi, 2025.
- Bedoya, O. *Búsqueda no informada*. Diapositivas del curso, Universidad del Valle.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. *Introduction to Algorithms*, 3.ª ed. The MIT Press, 2009. Secciones 22.3 y 22.4.

---

*Material adaptado del material original de los profesores Andrés Aristizábal, Marlon Gómez y Oscar Bedoya.*
