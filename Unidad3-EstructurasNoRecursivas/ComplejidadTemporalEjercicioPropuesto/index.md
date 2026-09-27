---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Complejidad temporal: Ejercicio propuesto"
---

# Complejidad temporal: Ejercicio propuesto

Después de estudiar [Crecimiento de funciones y Análisis de algoritmos](../CrecimientoFuncionesAnalisisAlgoritmos/index.md) y completar sus [ejercicios](../CrecimientoFuncionesAnalisisAlgoritmos/exercises.md), resuelva el siguiente ejercicio integrador de análisis de complejidad temporal.

---

## Enunciado: Conteo cruzado con función auxiliar

Dado un arreglo $a[0..n-1]$ de números, se define la función auxiliar `contarMenores(a, n, valor)`, que cuenta cuántos elementos del arreglo son menores que `valor`. Con ella, `procesar` construye primero una matriz de sumas por pares y luego, para **cada** pareja $(i,j)$, cuenta cuántos elementos del arreglo son menores que esa suma.

**Pseudocódigo — función auxiliar:**

```
function contarMenores(a, n, valor)
    contador <- 0
    for (k = 0; k < n; k++)
        if (a[k] < valor)
            contador <- contador + 1
    return contador
```

**Pseudocódigo — función `procesar`:**

```
function procesar(a, n)
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            suma[i][j] <- a[i] + a[j]

    total <- 0
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            total <- total + contarMenores(a, n, suma[i][j])

    return total
```

---

## Tabla de análisis (1/2): `contarMenores`

| # | Instrucción | Costo | Veces |
|---|---|---|---|
| 1 | $\text{contador} \leftarrow 0$ | $e_1$ | **?** |
| 2 | **for** $(k = 0;\ k < n;\ k{+}{+})$ | $e_2$ | **?** |
| 3 | &nbsp;&nbsp;**if** $(a[k] < \text{valor})$ | $e_3$ | **?** |
| 4 | &nbsp;&nbsp;&nbsp;&nbsp;$\text{contador} \leftarrow \text{contador} + 1$ | $e_4$ | **?** |
| 5 | **return** $\text{contador}$ | $e_5$ | **?** |

**Antes de seguir:** calcule $T_{\text{contarMenores}}(n)$, el costo de **una sola llamada** a esta función. Lo va a necesitar en la siguiente tabla.

---

## Tabla de análisis (2/2): `procesar`

| # | Instrucción | Costo | Veces |
|---|---|---|---|
| 1 | **for** $(i = 0;\ i < n;\ i{+}{+})$ | $c_1$ | **?** |
| 2 | &nbsp;&nbsp;**for** $(j = 0;\ j < n;\ j{+}{+})$ | $c_2$ | **?** |
| 3 | &nbsp;&nbsp;&nbsp;&nbsp;$\text{suma}[i][j] \leftarrow a[i] + a[j]$ | $c_3$ | **?** |
| 4 | $\text{total} \leftarrow 0$ | $c_4$ | **?** |
| 5 | **for** $(i = 0;\ i < n;\ i{+}{+})$ | $c_5$ | **?** |
| 6 | &nbsp;&nbsp;**for** $(j = 0;\ j < n;\ j{+}{+})$ | $c_6$ | **?** |
| 7 | &nbsp;&nbsp;&nbsp;&nbsp;$\text{total} \leftarrow \text{total} + \texttt{contarMenores}(a, n, \text{suma}[i][j])$ | $c_7 + T_{\text{contarMenores}}(n)$ | **?** |
| 8 | **return** $\text{total}$ | $c_8$ | **?** |

**Ojo con la línea 7:** no es una instrucción de costo constante. Cada vez que se ejecuta dispara una llamada **completa** a `contarMenores`, cuyo costo ya dedujo en la tabla anterior. Para conocer el costo real de esa línea debe **sustituir** $T_{\text{contarMenores}}(n)$ y multiplicarlo por el número de veces que la línea se ejecuta.

---

## Preguntas para resolver antes de programar

1. Complete ambas tablas (columna **Veces**) y calcule $T_{\text{contarMenores}}(n)$.
2. Sustituya ese resultado en la línea 7 de `procesar` y calcule $T_{\text{procesar}}(n)$.
3. ¿A qué clase de complejidad asintótica pertenece $T_{\text{procesar}}(n)$? Justifique con la definición de $O(\cdot)$.
4. A simple vista, `procesar` solo tiene ciclos `for` anidados dos niveles (nunca tres). ¿Por qué el resultado no es $O(n^2)$?

**Pista:** en el análisis de algoritmos con funciones auxiliares (como en el capítulo de *análisis de algoritmos estructurados*), el costo de una llamada a función nunca es constante si el cuerpo de esa función depende de $n$ — hay que **expandir** la llamada, no solo contar las líneas visibles en el ciclo que la invoca.

---

## Qué debe entregar

1. Un archivo `.java` propio (por ejemplo `ConteoCruzado.java`) con **dos métodos separados** — `contarMenores` y `procesar` — que repliquen exactamente la estructura de ciclos del pseudocódigo (`procesar` debe seguir llamando a `contarMenores`, no debe quedar todo aplanado en un solo método).
2. Un arreglo de tamaños $n$ crecientes y, para cada uno, el tiempo medido con `System.nanoTime()` al ejecutar `procesar`. Como la complejidad es mayor que en los ejemplos de clase, use tamaños más pequeños (por ejemplo $100, 200, 400, 800, 1600$) para que el programa termine en un tiempo razonable.
3. Use una notebook `analisis_empirico.ipynb` para:
   - cargar sus parejas $(n, \text{tiempo})$ medidas,
   - graficar el tiempo medido contra $n$,
   - graficar en escala log-log y estimar la pendiente (el exponente de la función de complejidad),
   - comparar esa pendiente contra el exponente teórico de $T_{\text{procesar}}(n)$ que dedujo.
4. Una conclusión corta: ¿la pendiente empírica coincide con el exponente teórico? Si no coincide exactamente, ¿qué factores (JIT, caché, recolector de basura) pueden explicar la diferencia?

---

¿Ya intentó resolverlo por su cuenta? Revise la [solución completa, paso a paso](solucion.md).
