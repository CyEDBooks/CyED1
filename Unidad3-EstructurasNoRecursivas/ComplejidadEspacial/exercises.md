---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Complejidad espacial: Ejercicios"
---

# Complejidad espacial: Ejercicios

Use esta página después de leer el [material de estudio de Complejidad espacial](index.md).

## Ejercicios

Determine la complejidad espacial auxiliar de los siguientes algoritmos:

- Un algoritmo que invierte un arreglo **en sitio** (sin crear uno nuevo), usando solo una variable temporal.
- Un algoritmo que crea una copia de un arreglo de $n$ enteros y luego la ordena.
- La función recursiva `fibonacci(n)` que calcula el $n$-ésimo número de Fibonacci retornando `fibonacci(n-1) + fibonacci(n-2)`.
- Búsqueda binaria implementada de forma **iterativa** sobre un arreglo ordenado.

Para el siguiente pseudocódigo, calcule la complejidad espacial auxiliar:

```
buildTable(n):
  tabla <- nuevo arreglo[n]
  i <- 1
  while i <= n:
    tabla[i] <- i * i
    i <- i + 1
  return tabla
```

¿Cambia el resultado si `tabla` se declara **fuera** de la función y se pasa como parámetro?

## Consulta

- ¿Por qué Merge Sort tiene espacio auxiliar $O(n)$ mientras que Heap Sort tiene $O(1)$? Explique con base en lo que hace cada algoritmo internamente.
- ¿En qué situaciones prácticas es preferible un algoritmo con mayor complejidad espacial pero menor complejidad temporal?

---

*Material adaptado del material original del profesor Oscar Bedoya.*
