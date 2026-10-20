---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Espacios de estados y juegos: Ejercicios"
---

# Espacios de estados y juegos: Ejercicios

Use esta página después de leer el [material de estudio](index.md). Cada ejercicio trae **pistas** y una **solución general**; intente resolverlo antes de abrirlas.

---

### Ejercicio 1

Aplique búsqueda preferente por amplitud en cada árbol. Las metas están subrayadas con doble borde. **¿Cuál meta encuentra? Liste los nodos creados y los nodos expandidos.**

a) $L$ y $D$ son los nodos meta.

{{GEN:fig-t2}}

b) $L$ y $A$ son los nodos meta.

{{GEN:fig-t3}}

:::{admonition} Pistas
:class: dropdown
- Expandir = verificar si es meta y, si no lo es, crear los hijos.
- Al expandir un nodo meta no se crean sus hijos.
- Lleve la tabla «Estado de la cola / Iteración» como en el Ejemplo 1.
:::

:::{admonition} Solución general
:class: dropdown
- a) {{GEN:t2-bfs-res}}
- b) {{GEN:t3-bfs-res}}

En b), $A$ está en el nivel $2$ y $L$ en el $3$: gana $A$ aunque $L$ esté más a la izquierda.
:::

### Ejercicio 2

Aplique búsqueda preferente por **profundidad** a los dos árboles del Ejercicio 1. ¿Encuentra las mismas metas?

:::{admonition} Pistas
:class: dropdown
- La pila deja arriba el hijo de más a la izquierda: se baja por la primera rama hasta el fondo antes de pasar a la siguiente.
:::

:::{admonition} Solución general
:class: dropdown
- a) {{GEN:t2-dfs-res}}
- b) {{GEN:t3-dfs-res}}
:::

### Ejercicio 3

Aplique búsqueda preferente por amplitud para ir de Arad a Bucarest en el mapa de Rumania del material de estudio. Evite devolverse. Los hijos se crean en el orden de esta lista: Ara, Zer, Ora, Sib, Tim, Lug, Meh, Dro, Cra, Rim, Fag, Pit, Buc. Luego haga lo mismo desde Sibiu.

:::{admonition} Pistas
:class: dropdown
- Ignore las distancias: esta búsqueda cuenta tramos.
- Bucarest está a tres tramos de Arad (por Sibiu y Fagaras) y a dos de Sibiu.
:::

:::{admonition} Solución general
:class: dropdown
- Desde Arad: nodos expandidos {{GEN:ara-exp}}. Ruta **{{GEN:ara-path}}** ({{GEN:ara-n}} nodos creados).
- Desde Sibiu: nodos expandidos {{GEN:rom-exp}}. Ruta **{{GEN:rom-path}}** ({{GEN:rom-n}} nodos creados).

{{GEN:fig-ara}}

La ruta encontrada tiene la menor cantidad de tramos, pero no la menor cantidad de kilómetros: por Rimnicu y Pitesti son $418$ km contra $450$ por Fagaras. La búsqueda por amplitud no es óptima.
:::

### Ejercicio 4

Aplique búsqueda preferente por amplitud. El ratón (verde) busca el queso; las casillas grises están bloqueadas. Se mueve a una casilla vecina libre en el orden ↑, ←, →, ↓. **No** evite devolverse.

{{GEN:fig-raton}}

:::{admonition} Pistas
:class: dropdown
- Sin evitar devolverse, un hijo puede repetir el estado del padre.
- El queso está a dos movimientos.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:raton-sol}}
:::

### Ejercicio 5

**El mundo de la aspiradora.** Hay dos cuartos, izquierdo y derecho; cada uno puede tener mugre o no, y la aspiradora está en uno de los dos. Formule el problema: estados, operadores (mover a la izquierda I, mover a la derecha D, aspirar A), prueba de meta y costo de ruta, si aspirar cuesta $3$ y desplazarse cuesta $1$. Escriba en pseudocódigo los operadores `MOVER-IZQUIERDA` y `ASPIRAR`. Luego aplique búsqueda preferente por amplitud **sin evitar devolverse**, desde la aspiradora a la izquierda y los dos cuartos con mugre, con los operadores en el orden A, D, I. Un operador que no cambia el estado (aspirar un cuarto limpio, moverse a la izquierda estando a la izquierda) no se aplica.

:::{admonition} Pistas
:class: dropdown
- Un estado necesita tres datos: dónde está la aspiradora y si cada cuarto tiene mugre. ¿Cuántos estados hay?
- La meta: no hay mugre en ninguno de los cuartos, esté donde esté la aspiradora.
:::

:::{admonition} Solución general
:class: dropdown
Hay $2 \cdot 2 \cdot 2 = 8$ estados. `MOVER-IZQUIERDA` solo cambia la posición de la aspiradora; `ASPIRAR` quita la mugre del cuarto donde está.

{{GEN:aspiradora}}

{{GEN:aspiradora-res}} Algunos nodos repiten un estado de su rama (moverse a la derecha y luego otra vez a la izquierda): los ciclos no afectan la búsqueda en amplitud, solo crean más nodos.
:::

### Ejercicio 6

Construya el árbol de juego y analícelo. En cada uno la jugada es de X (el jugador 1). ¿Con qué jugada empezaría?

{{GEN:fig-gato-ej}}

:::{admonition} Pistas
:class: dropdown
- Hay tres casillas libres: el árbol tiene a lo sumo $3 \cdot 2 \cdot 1$ hojas.
- Marque cada hoja con «gana», «pierde» o «empate» del jugador 1 y suba: en los niveles de O se supone que O juega lo mejor para O.
:::

:::{admonition} Solución general
:class: dropdown
{{GEN:gato-ej-sol}}
:::

### Ejercicio 7

Hay una jarra de **4 litros** y una de **3 litros**, sin marcas, y una llave de agua. Se puede llenar una jarra, vaciarla, o pasar agua de una a otra hasta que la que recibe se llene o la que entrega quede vacía. Formule el problema y aplique búsqueda preferente por amplitud, sin crear estados que ya se crearon, para conseguir **exactamente 2 litros en la jarra de 4**. Los operadores en orden: llenar 4, llenar 3, vaciar 4, vaciar 3, pasar 4→3, pasar 3→4.

:::{admonition} Pistas
:class: dropdown
- Un estado es un par $(a, b)$: litros en la jarra de 4 y en la de 3. El inicial es $(0, 0)$.
- Desde $(4, 1)$, «pasar 4→3» mueve $\min(4,\ 3 - 1) = 2$ litros.
:::

:::{admonition} Solución general
:class: dropdown
Solución: {{GEN:jarras-sol}}. Son $6$ movimientos; como la búsqueda va por niveles, no hay solución con menos. Se crearon {{GEN:jarras-n}} nodos.
:::

### Ejercicio 8

Construya el árbol del juego NIM con **5** fichas (cada jugador toma $1$, $2$ o $3$; pierde quien toma la última; empieza J1). ¿J1 puede asegurar la victoria? ¿Con qué jugada?

:::{admonition} Pistas
:class: dropdown
- El subárbol que empieza con $4$ fichas ya se analizó en el material de estudio, pero ahora en ese nodo juega **J2**.
- Con $1$ ficha, el que juega pierde.
:::

:::{admonition} Solución general
:class: dropdown
J1 **no** puede asegurar la victoria: con $5$ fichas, tome lo que tome, deja $4$, $3$ o $2$ fichas, y desde cualquiera de esas posiciones J2 puede dejarle $1$ ficha. Las posiciones perdedoras para quien mueve son $1, 5, 9, \dots$ fichas.
:::

### Ejercicio 9

**Misioneros y caníbales.** Tres misioneros y tres caníbales deben cruzar un río en un bote donde caben máximo dos personas. Si en alguna orilla hay más caníbales que misioneros (y hay al menos un misionero), los misioneros son devorados. Formule el problema (estados, operadores, prueba de meta y costo de ruta) y aplique búsqueda preferente por amplitud, sin crear estados que ya se crearon. Reporte la solución y el número de nodos creados.

---

*Material adaptado del material original del profesor Oscar Bedoya.*
