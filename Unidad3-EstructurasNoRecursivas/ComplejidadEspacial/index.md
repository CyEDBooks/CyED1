---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 3: Complejidad espacial"
---

# Unidad 3: Complejidad espacial

## ¿Qué es la Complejidad Espacial?

**Motivación**

Hasta ahora hemos analizado **cuánto tiempo** tarda un algoritmo en función del tamaño de la entrada.

Pero también debemos preguntarnos: **¿cuánta memoria consume?**

- En dispositivos con poca RAM (sistemas embebidos, móviles) el espacio es un recurso crítico.
- Un algoritmo *rápido* pero que consume demasiada memoria puede ser inutilizable en la práctica.
- Al diseñar algoritmos debemos equilibrar **tiempo** y **espacio**.

**Definición formal**

La **complejidad espacial** de un algoritmo es la cantidad **total** de memoria que necesita en función del tamaño de la entrada $n$. Se compone de dos partes:

$$
S(n) = \underbrace{\text{Espacio de entrada}}_{\text{input space}} \;+\; \underbrace{\text{Espacio auxiliar}}_{\text{auxiliary space}}
$$

- **Espacio de entrada:** memoria ocupada por los datos que recibe el algoritmo (los parámetros).
- **Espacio auxiliar:** memoria *extra* que el algoritmo utiliza internamente (variables temporales, estructuras intermedias, pila de llamadas).

**Espacio auxiliar vs. complejidad espacial**

:::{dropdown} Confusión frecuente
Muchas fuentes usan "complejidad espacial" cuando en realidad hablan de "espacio auxiliar".
:::

Ejemplo con algoritmos de ordenamiento sobre un arreglo de $n$ elementos:

| Algoritmo | Espacio auxiliar | Complejidad espacial |
|---|---|---|
| Insertion Sort | $O(1)$ | $O(n)$ |
| Heap Sort | $O(1)$ | $O(n)$ |
| Merge Sort | $O(n)$ | $O(n)$ |

La *complejidad espacial total* incluye siempre el arreglo de entrada ($O(n)$), por eso todos resultan $O(n)$. Lo que diferencia a Merge Sort es su **espacio auxiliar**.

## Componentes de la Complejidad Espacial

**¿Qué ocupa espacio en un algoritmo?**

- **Variables simples** (enteros, booleanos, flotantes): espacio constante $O(1)$ cada una.
- **Arreglos / listas** de tamaño $n$: espacio $O(n)$.
- **Matrices** de $n \times n$: espacio $O(n^2)$.
- **Pila de llamadas recursivas**: cada llamada agrega un *frame* a la pila; la profundidad de recursión determina el espacio.

Al igual que con el tiempo, usamos la **notación $O$** para expresar el crecimiento del espacio en el **peor caso**.

**Espacio de la pila de llamadas (call stack)**

Cada vez que una función llama a otra (o a sí misma), se reserva un **frame** en la pila con:

- La dirección de retorno.
- Los parámetros de la función.
- Las variables locales.

Cuando la función termina, el frame se libera. Lo importante es el **máximo número de frames simultáneos**.

:::{dropdown} Clave
El espacio de la pila depende de la **profundidad máxima** de recursión, no del número total de llamadas.
:::

## Tipos de Complejidad Espacial

**Complejidad $O(1)$ — Espacio constante**

El algoritmo usa una cantidad **fija** de memoria sin importar el tamaño de la entrada.

Ejemplo: suma de un arreglo.

```
sum(arr, n):
  total <- 0        // 1 variable
  i <- 1            // 1 variable
  while i <= n:
    total <- total + arr[i]
    i <- i + 1
  return total
```

Análisis:

- `total` e `i`: 2 variables de tamaño fijo.
- No se crean estructuras adicionales.
- El arreglo `arr` es la *entrada*, no cuenta como auxiliar.

$$
S_{\text{aux}}(n) = O(1)
$$

**Complejidad $O(n)$ — Espacio lineal**

La memoria crece **proporcionalmente** al tamaño de la entrada.

Ejemplo: copiar un arreglo.

```
copy(arr, n):
  result <- nuevo arreglo[n]
  i <- 1
  while i <= n:
    result[i] <- arr[i]
    i <- i + 1
  return result
```

Análisis:

- `result`: arreglo de $n$ elementos $\Rightarrow O(n)$.
- `i`: variable simple $\Rightarrow O(1)$.
- Total auxiliar: $O(n) + O(1) = O(n)$.

$$
S_{\text{aux}}(n) = O(n)
$$

**Complejidad $O(n^2)$ — Espacio cuadrático**

Ocurre cuando se crea una **estructura bidimensional** de tamaño $n \times n$.

Ejemplo: crear una tabla de distancias.

```
initMatrix(n):
  M <- nueva matriz[n][n]
  i <- 1
  while i <= n:
    j <- 1
    while j <= n:
      M[i][j] <- 0
      j <- j + 1
    i <- i + 1
  return M
```

Análisis:

- `M`: matriz de $n^2$ elementos $\Rightarrow O(n^2)$.
- `i`, `j`: variables simples $\Rightarrow O(1)$.

$$
S_{\text{aux}}(n) = O(n^2)
$$

Impráctico para $n$ grande (ej. $n = 10\,000 \Rightarrow 10^8$ celdas).

**Resumen de tipos de complejidad espacial**

| Notación | Nombre | Ejemplo típico |
|---|---|---|
| $O(1)$ | Constante | Variables simples, intercambio in-place |
| $O(\log n)$ | Logarítmica | Búsqueda binaria recursiva (pila) |
| $O(n)$ | Lineal | Copiar arreglo, recursión lineal |
| $O(n^2)$ | Cuadrática | Matriz $n \times n$, tabla de adyacencia |

## Análisis de Espacio en Algoritmos Iterativos

**Método: análisis línea a línea**

Para calcular el espacio auxiliar de un algoritmo iterativo:

1. Identificar **todas** las variables y estructuras declaradas.
2. Determinar si su tamaño **depende de $n$** o es constante.
3. Sumar los aportes de cada componente.
4. Expresar el resultado con la cota asintótica más ajustada.

:::{dropdown} Regla práctica
Variables simples (`int`, `bool`, `float`) $\Rightarrow O(1)$.
Arreglos / estructuras de tamaño $n$ $\Rightarrow O(n)$.
Matrices $n \times n$ $\Rightarrow O(n^2)$.
:::

**Ejemplo iterativo: suma de matrices**

| # | Instrucción | Espacio |
|---|---|---|
| 1 | $i \leftarrow 1$ | $O(1)$ |
| 2 | $j \leftarrow 1$ | $O(1)$ |
| 3 | $mat3 \leftarrow$ nueva matriz $[n][n]$ | $O(n^2)$ |
| 4 | **while** $i \leq n$ | --- |
| 5 | &nbsp;&nbsp;**while** $j \leq n$ | --- |
| 6 | &nbsp;&nbsp;&nbsp;&nbsp;$mat3[i][j] \leftarrow mat1[i][j] + mat2[i][j]$ | --- |
| 7 | &nbsp;&nbsp;&nbsp;&nbsp;$j \leftarrow j + 1$ | --- |
| 8 | &nbsp;&nbsp;$i \leftarrow i + 1$ | --- |

**Entrada:** $mat1$, $mat2$ de $n \times n$ $\Rightarrow$ no cuentan como auxiliar.

**Auxiliar:**
- $mat3$: nueva matriz $n \times n$ $\Rightarrow O(n^2)$
- $i$, $j$: enteros $\Rightarrow O(1)$

$$
S_{\text{aux}}(n) = O(n^2) + O(1) = O(n^2)
$$

El término dominante es la matriz resultado.

**Ejemplo iterativo: búsqueda lineal**

| # | Instrucción | Espacio |
|---|---|---|
| 1 | $i \leftarrow 1$ | $O(1)$ |
| 2 | **while** $i \leq n$ | --- |
| 3 | &nbsp;&nbsp;**if** $arr[i] = target$ | --- |
| 4 | &nbsp;&nbsp;&nbsp;&nbsp;**return** $i$ | --- |
| 5 | &nbsp;&nbsp;$i \leftarrow i + 1$ | --- |
| 6 | **return** $-1$ | --- |

**Entrada:** $arr$ de $n$ elementos, $target$ $\Rightarrow$ no cuentan como auxiliar.

**Auxiliar:**
- $i$: un entero $\Rightarrow O(1)$
- No se crea ninguna estructura adicional.

$$
S_{\text{aux}}(n) = O(1)
$$

Independientemente del tamaño del arreglo, solo se usa una variable extra.

---
**· Contenido adicional ·**

### Complejidad espacial: memoria de instrucciones, pila y datos

**¿Para qué se requiere memoria dentro de un algoritmo?**

Para guardar:

- Instrucciones del programa
- Valores constantes
- Valores variables
- ...

**¿Cómo se define la complejidad espacial?**

La cantidad total de **memoria computacional** necesaria para completar la ejecución de un algoritmo.

**¿Cuáles son las razones por las que un programa utiliza memoria computacional?**

- **Espacio de instrucciones** (versión compilada del programa).
- **Espacio de la pila** (información de funciones en ejecución).
- **Espacio de datos** (variables y constantes).

**Nota:** al analizar la **complejidad espacial**, solo se considera el **espacio de datos**.

**¿Qué cantidad de memoria se requiere para guardar distintos tipos de datos?**

| Tipo de dato | Tamaño |
|---|---|
| Entero (`int`) | 32 bits (4 bytes) |
| Punto flotante (`float`) | 32 bits (4 bytes) |
| Carácter (`char`) | 16 bits (2 bytes) |
| Doble precisión (`double`) | 64 bits (8 bytes) |
| ... | ... |

**¿Cómo se realizaría el análisis de complejidad espacial para este fragmento de código?**

```c
int sum(int A[i], int n){
	int sum = 0;
	for (int i = 0; i < n; i++) {
	    sum += A[i];
	}    
	return sum	    
}
```

**Tabla de memoria utilizada:**

| Tipo | Variable | Tamaño de 1 valor atómico | Cantidad de valores atómicos |
|---|---|---|---|
| Entrada | `A` | 32 bits | `n` |
| | `n` | 32 bits | `1` |
| Auxiliar | `i` | 32 bits | `1` |
| Salida | `sum` | 32 bits | `1` |

- Complejidad Espacial Total $= \text{Entrada} + \text{Auxiliar} + \text{Salida} = n + 3 = \Theta(n)$
- Complejidad Espacial Auxiliar $= 1 = \Theta(1)$
- Complejidad Espacial Auxiliar + Salida $= 1 + 1 = \Theta(1)$

---

## Análisis de Espacio en Algoritmos Recursivos

**Recursión y la pila de llamadas**

En los algoritmos recursivos, **cada llamada activa** agrega un frame a la pila.

Lo relevante para el espacio es la **profundidad máxima** de la pila en cualquier momento de la ejecución.

:::{dropdown} Fórmula
$$
S_{\text{pila}}(n) = \text{profundidad máxima de recursión} \times O(1) \text{ por frame}
$$
:::

:::{dropdown} Importante
Tener muchas llamadas en total **no implica** que todas estén activas al mismo tiempo.
:::

**Ejemplo recursivo: suma acumulada**

```
add(n):
  if n <= 0:
    return 0
  return n + add(n - 1)
```

Traza para $n = 4$:

- `add(4)` llama a `add(3)`
- `add(3)` llama a `add(2)`
- `add(2)` llama a `add(1)`
- `add(1)` llama a `add(0)`
- `add(0)` retorna 0 (base)

Análisis: la pila tiene **simultáneamente** los frames de `add(4)`, `add(3)`, …, `add(0)`.

Profundidad máxima $= n + 1 \approx n$.

$$
S_{\text{aux}}(n) = O(n)
$$

Aunque el número de llamadas totales también es $n$, aquí coincide porque son *todas* simultáneas.

**Cuidado: no todas las llamadas son simultáneas**

```
addSequence(n):
  sum <- 0
  i <- 1
  while i < n:
    sum <- sum + pairSum(i, i+1)
    i <- i + 1
  return sum

pairSum(x, y):
  return x + y
```

Análisis: `pairSum` es llamada $\approx n$ veces en total, pero **de una en una**: cuando termina, su frame se libera antes de la siguiente llamada.

En cualquier momento solo hay **1 frame** de `pairSum` en la pila.

$$
S_{\text{aux}}(n) = O(1)
$$

:::{dropdown} Conclusión clave
El espacio de la pila depende de las llamadas **activas simultáneamente**, no del total de llamadas realizadas.
:::

**Ejemplo recursivo: factorial**

```
factorial(n):
  if n <= 1:
    return 1
  return n * factorial(n - 1)
```

Traza para $n = 5$:

$$
5! \to 4! \to 3! \to 2! \to 1!
$$

Pila activa simultáneamente:

$$
\underbrace{f(5), f(4), f(3), f(2), f(1)}_{n \text{ frames}}
$$

Análisis del espacio:

- Cada frame ocupa espacio para el parámetro $n$ y la dirección de retorno: $O(1)$ por frame.
- La profundidad máxima de la pila es $n$.

$$
S_{\text{aux}}(n) = O(n)
$$

Contraste: una versión *iterativa* del factorial solo usa $O(1)$ de espacio auxiliar.

## Comparación Tiempo vs. Espacio

**Relación entre tiempo y espacio**

El tiempo y el espacio son dos **recursos independientes** que deben equilibrarse según el contexto.

| Algoritmo | Tiempo | Espacio auxiliar |
|---|---|---|
| Búsqueda lineal | $O(n)$ | $O(1)$ |
| Búsqueda binaria iterativa | $O(\log n)$ | $O(1)$ |
| Búsqueda binaria recursiva | $O(\log n)$ | $O(\log n)$ |
| Merge Sort | $O(n \log n)$ | $O(n)$ |
| Insertion Sort | $O(n^2)$ | $O(1)$ |

Merge Sort es más *rápido* que Insertion Sort para entradas grandes, pero requiere más *espacio*.

**La disyuntiva espacio-tiempo**

Ganar tiempo a costa de espacio:

- Guardar resultados pre-calculados en una tabla (memoización).
- Usar una tabla hash para búsquedas $O(1)$ en vez de $O(n)$.

Ganar espacio a costa de tiempo:

- Reemplazar recursión por iteración.
- Recalcular valores en lugar de almacenarlos.
- Ordenar in-place (Heap Sort, Insertion Sort).

:::{dropdown} Principio general
No existe una opción universalmente mejor: la elección depende de los **recursos disponibles** y los **requisitos del sistema**.
:::

---

Continúa con los [ejercicios de Complejidad espacial](exercises.md).

*Material adaptado del material original de los profesores Oscar Bedoya y Marlon Gomez.*
