---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Crecimiento de funciones y Análisis de algoritmos: Ejercicios"
---

# Crecimiento de funciones y Análisis de algoritmos: Ejercicios

Use esta página después de leer el [material de estudio de Crecimiento de funciones y Análisis de algoritmos](index.md).

---
**· Contenido adicional ·**

### Ejercicios de análisis de complejidad

Determine la complejidad temporal de cada uno de los siguientes fragmentos de código.

**Ejercicio 1**

```java
public void ejercicio1(int N, int M) {
    int a = 0, b = 0;
    for (int i = 0; i < N; i++) {
        a = a + rand();
    }
    for (int j = 0; j < M; j++) {
        b = b + rand();
    }
}

private int rand() {
    Random aleatorio = new Random();
    return aleatorio.nextInt((int) (System.currentTimeMillis() % 100));
}

```

**Ejercicio 2**

```java
public int ejercicio2(int[] arr) {
    int a = 0;
    for (int i = 0; i < arr.length; i++) {
        for (int j = arr.length - 1; j > i; j--) {
            a = a + i + arr[j];
        }
    }
    return a;
}

```

**Ejercicio 3**

```java
public int ejercicio3(int[] arr) {
    int i, j, k = 0;
    int n = arr.length;
    for (i = n / 2; i <= n; i++) {
        for (j = 2; j <= n; j = j * 2) {
            k = k + n / 2;
        }
    }
    return k;
}

```

**Ejercicio 4**

```java
public int ejercicio4(int[] arr) {
    int k = 0;
    int j = 2;
    int n = arr.length;
    int i = n / 2;

    while (i <= n) {
        while (j <= n) {
            k = i + j + k;
            ++j;
        }
        ++i;
    }
    return k;
}
```

**Ejercicio 5**

```java
public static LinkedList<Integer> ejercicio5(int n) {
    boolean A[] = new boolean[n + 1];
    for (int i = 0; i < n; i++)
        A[i] = true;

    for (int p = 2; p * p <= n; p++) {
        if (A[p] == true) {
            for (int i = p * 2; i <= n; i += p)
                A[i] = false;
        }
    }

    LinkedList<Integer> B = new LinkedList<>();
    for (int i = 1; i < A.length; i++) {
        if (A[i])
            B.add(i);
    }

    return B;
}

```

---

## Hoja de trabajo — Algoritmos de Ordenamiento

Crea una clase `Ordenamiento.java` con los métodos estáticos. Todos ordenan un `int[]` de menor a mayor **en sitio** (sin crear nuevo arreglo).

### Paso 1: implementa `bubbleSort(int[] a)`

Dos ciclos anidados:
- El ciclo exterior `i` va de `0` hasta `n-2` (controla cuántas pasadas).
- El ciclo interior `j` va de `0` hasta `n-i-2` (cada pasada fija el mayor al final).
- Si `a[j] > a[j+1]`, intercambia.

:::{dropdown} Pista — bubbleSort

```java
public static void bubbleSort(int[] a) {
    int n = a.length;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                int t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
            }
        }
    }
}
```
:::

### Paso 2: implementa `insertionSort(int[] a)`

Un solo ciclo exterior `i` desde `1`. En cada iteración:
1. Guarda `key = a[i]`.
2. Mueve hacia la derecha todos los elementos mayores que `key`.
3. Inserta `key` en el hueco resultante.

:::{dropdown} Pista — insertionSort

```java
public static void insertionSort(int[] a) {
    for (int i = 1; i < a.length; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}
```
:::

### Main — ejecuta y verifica

```java
import java.util.Arrays;

public class MainOrdenamiento {
    public static void main(String[] args) {
        int[] original = {5, 3, 1, 4, 2};

        // BubbleSort
        int[] b = original.clone();
        Ordenamiento.bubbleSort(b);
        System.out.println("BubbleSort:    " + Arrays.toString(b));
        // Esperado: BubbleSort:    [1, 2, 3, 4, 5]

        // InsertionSort
        int[] c = original.clone();
        Ordenamiento.insertionSort(c);
        System.out.println("InsertionSort: " + Arrays.toString(c));
        // Esperado: InsertionSort: [1, 2, 3, 4, 5]

        // Verificar contra Arrays.sort (referencia de Java)
        int[] d = original.clone();
        Arrays.sort(d);
        System.out.println("Arrays.sort:   " + Arrays.toString(d));
        // Esperado: Arrays.sort:   [1, 2, 3, 4, 5]

        // Caso borde: arreglo ya ordenado (mejor caso para InsertionSort)
        int[] sorted = {1, 2, 3, 4, 5};
        Ordenamiento.insertionSort(sorted);
        System.out.println("Ya ordenado:   " + Arrays.toString(sorted));
        // Esperado: Ya ordenado:   [1, 2, 3, 4, 5]

        // Caso borde: arreglo en reversa (peor caso para BubbleSort)
        int[] rev = {5, 4, 3, 2, 1};
        Ordenamiento.bubbleSort(rev);
        System.out.println("En reversa:    " + Arrays.toString(rev));
        // Esperado: En reversa:    [1, 2, 3, 4, 5]

        // Caso borde: un solo elemento
        int[] one = {42};
        Ordenamiento.bubbleSort(one);
        System.out.println("Un elemento:   " + Arrays.toString(one));
        // Esperado: Un elemento:   [42]
    }
}
```

### Tabla de complejidad (referencia)

| Algoritmo     | Mejor caso | Peor caso | Espacio extra |
|---------------|-----------|-----------|---------------|
| BubbleSort    | O(n)      | O(n²)     | O(1)          |
| InsertionSort | O(n)      | O(n²)     | O(1)          |

El mejor caso de InsertionSort es O(n) porque, si el arreglo ya está ordenado, el `while` interno nunca ejecuta ninguna iteración.

---

*Material adaptado del material original de los profesores Oscar Bedoya y Marlon Gomez.*
