---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Complejidad temporal: Ejercicio propuesto resuelto"
---

# Complejidad temporal: Ejercicio propuesto resuelto

Solución paso a paso del [ejercicio propuesto de conteo cruzado con función auxiliar](index.md). Se recomienda intentar resolverlo por su cuenta antes de revisar esta solución.

---

## a) Análisis de `contarMenores`

Peor caso: todo el arreglo es menor que `valor`, por lo que la línea 4 se ejecuta las $n$ veces.

| # | Instrucción | Veces |
|---|---|---|
| 1 | $\text{contador} \leftarrow 0$ | $1$ |
| 2 | **for** $(k = 0;\ k < n;\ k{+}{+})$ | $n+1$ |
| 3 | &nbsp;&nbsp;**if** $(a[k] < \text{valor})$ | $n$ |
| 4 | &nbsp;&nbsp;&nbsp;&nbsp;$\text{contador} \leftarrow \text{contador} + 1$ | $n$ |
| 5 | **return** $\text{contador}$ | $1$ |

Asumiendo costo unitario por instrucción (una asignación, una evaluación de condición o un `return` cuestan $1$), $T_{\text{contarMenores}}(n)$ es la suma de la columna **Veces**:

$$
T_{\text{contarMenores}}(n) = \underbrace{1}_{\#1} + \underbrace{(n+1)}_{\#2} + \underbrace{n}_{\#3} + \underbrace{n}_{\#4} + \underbrace{1}_{\#5} = 3n+3
$$

$$
\boxed{T_{\text{contarMenores}}(n) = 3n+3 = O(n)}
$$

Una sola llamada a `contarMenores` **nunca es de costo constante**: crece linealmente con $n$ (con pendiente $3$) porque su cuerpo recorre todo el arreglo.

---

## b) Análisis de `procesar`

Los dos bloques de ciclos no dependen de los datos, por lo que las cuentas son iguales en cualquier caso; la línea 7 hereda el peor caso de `contarMenores`.

| # | Instrucción | Veces |
|---|---|---|
| 1 | **for** $(i = 0;\ i < n;\ i{+}{+})$ | $n+1$ |
| 2 | &nbsp;&nbsp;**for** $(j = 0;\ j < n;\ j{+}{+})$ | $n(n+1)$ |
| 3 | &nbsp;&nbsp;&nbsp;&nbsp;$\text{suma}[i][j] \leftarrow a[i] + a[j]$ | $n^2$ |
| 4 | $\text{total} \leftarrow 0$ | $1$ |
| 5 | **for** $(i = 0;\ i < n;\ i{+}{+})$ | $n+1$ |
| 6 | &nbsp;&nbsp;**for** $(j = 0;\ j < n;\ j{+}{+})$ | $n(n+1)$ |
| 7 | &nbsp;&nbsp;&nbsp;&nbsp;$\text{total} \leftarrow \text{total} + \texttt{contarMenores}(a,n,\text{suma}[i][j])$ | $n^2(3n+4) = 3n^3+4n^2$ |
| 8 | **return** $\text{total}$ | $1$ |

**Sustitución en la línea 7:** a diferencia de las demás filas, esta línea *no* cuesta $1$ por ejecución, porque dispara una llamada completa a `contarMenores`. El costo real por ejecución es $1$ (la asignación $\text{total}\leftarrow\text{total}+(\cdot)$ en sí misma) más $T_{\text{contarMenores}}(n)=3n+3$ (ejecutar las 5 líneas de esa función para el arreglo completo):

$$
\underbrace{1}_{\text{asignación propia}} + \underbrace{(3n+3)}_{T_{\text{contarMenores}}(n)} = 3n+4.
$$

Y esa línea se ejecuta $n^2$ veces, porque está dentro de *dos* `for` anidados (líneas 5 y 6), cada uno con $n$ iteraciones verdaderas ($i=0,\ldots,n-1$ y, por cada $i$, $j=0,\ldots,n-1$): el producto de esas $n$ iteraciones de $i$ por las $n$ de $j$ da $n\cdot n=n^2$ ejecuciones del cuerpo del ciclo, que es donde vive la línea 7.

Multiplicando costo por ejecución ($3n+4$) por número de ejecuciones ($n^2$), el aporte total de la línea 7 a $T_{\text{procesar}}(n)$ —ya el valor anotado en la tabla— es

$$
\boxed{n^2\,(3n+4) = 3n^3+4n^2}
$$

---

## c) Cálculo de $T_{\text{procesar}}(n)$

Suma de la columna **Veces**, con costo unitario $1$ por instrucción y sustituyendo ya la línea 7 por su costo real $3n^3+4n^2$:

$$
\begin{align*}
T_{\text{procesar}}(n)
  &= (n{+}1) + n(n{+}1) + n^2 + 1 + (n{+}1) + n(n{+}1) + \bigl(3n^3+4n^2\bigr) + 1 \\
  &= (n{+}1) + (n^2{+}n) + n^2 + 1 + (n{+}1) + (n^2{+}n) + 3n^3+4n^2 + 1 \\
  &= 3n^3 + \underbrace{(1+1+1+4)}_{7}n^2 + \underbrace{(1+1+1+1)}_{4}n + \underbrace{(1+1+1+1)}_{4}
\end{align*}
$$

$$
\boxed{T_{\text{procesar}}(n) = 3n^3+7n^2+4n+4}
$$

---

## d) Clasificación asintótica

Por definición, $T(n)=O(g(n))$ si existen constantes $c>0$ y $n_0\geq 1$ tales que $T(n)\leq c\,g(n)$ para todo $n\geq n_0$. Tomando $g(n)=n^3$ y, para $n\geq 1$ (donde $n\leq n^2\leq n^3$):

$$
T_{\text{procesar}}(n) = 3n^3+7n^2+4n+4 \;\leq\; (3+7+4+4)\,n^3 = 18\,n^3
\quad\text{para todo } n\geq 1,
$$

por lo que basta $c=18$ y $n_0=1$. Luego

$$
\boxed{T_{\text{procesar}}(n) = O(n^3)}
$$

---

## e) ¿Por qué no es $O(n^2)$ si solo hay dos niveles de `for` anidados?

Porque `procesar` no tiene ciclos de costo constante en su interior: en la línea 7, cada una de las $n^2$ iteraciones del doble `for` *no* cuesta $O(1)$, sino $3n+4$, porque dispara una llamada completa a `contarMenores`, la cual internamente recorre el arreglo con su propio ciclo `for` de $n$ iteraciones. Ese ciclo interno, oculto dentro de la función auxiliar, actúa como un **tercer nivel de anidamiento efectivo**: $n^2$ (los dos `for` visibles) $\times\; (3n+4)$ (el costo real de la línea 7, dominado por el `for` escondido en `contarMenores`) $= 3n^3+4n^2$.

Si se tratara —incorrectamente— la línea 7 como $O(1)$, se obtendría $T(n)=O(n^2)$; contar solo las líneas visibles en el ciclo que invoca la función subestima el costo real. Hay que **expandir** $T_{\text{contarMenores}}(n)=3n+3$ y sustituirlo, tal como se hizo en el inciso b), para llegar al verdadero $T_{\text{procesar}}(n)=3n^3+7n^2+4n+4=O(n^3)$.

---

## f) Verificación empírica — `ConteoCruzado.java`

Para confirmar el análisis anterior se instrumentó cada línea del pseudocódigo con un contador estático (`e1..e5` para `contarMenores`, `c1..c8` para `procesar`) y se comparó la suma de los 13 contadores contra $T_{\text{procesar}}(n)=3n^3+7n^2+4n+4$.

Los contadores `e1..e5` son **estáticos a propósito**: como `contarMenores` se llama $n^2$ veces, deben **acumular** sus ejecuciones a través de todas esas llamadas — así el conteo real refleja, línea por línea, la sustitución de $T_{\text{contarMenores}}(n)$ dentro de la línea 7 que se hizo en el inciso b). Se usa un arreglo *dummy* de puros $1$: así $\text{suma}[i][j]=2$ siempre y todo $a[k]=1<2$, forzando el peor caso de `contarMenores` en cada una de las $n^2$ llamadas.

```java
import java.util.Scanner;

public class ConteoCruzado {

    static long e1 = 0, e2 = 0, e3 = 0, e4 = 0, e5 = 0;

    static long c1 = 0, c2 = 0, c3 = 0, c4 = 0, c5 = 0, c6 = 0, c7 = 0, c8 = 0;

    public static int contarMenores(int[] a, int n, int valor) {
        int contador = 0;
        e1++;

        int k = 0;
        while (++e2 >= 0 && k < n) {
            e3++;
            if (a[k] < valor) {
                e4++;
                contador = contador + 1;
            }
            k = k + 1;
        }

        e5++;
        return contador;
    }

    public static int procesar(int[] a, int n) {
        int[][] suma = new int[n][n];

        int i = 0;
        while (++c1 >= 0 && i < n) {
            int j = 0;
            while (++c2 >= 0 && j < n) {
                suma[i][j] = a[i] + a[j];
                c3++;
                j = j + 1;
            }
            i = i + 1;
        }

        int total = 0;
        c4++;

        int i2 = 0;
        while (++c5 >= 0 && i2 < n) {
            int j2 = 0;
            while (++c6 >= 0 && j2 < n) {
                total = total + contarMenores(a, n, suma[i2][j2]);
                c7++;
                j2 = j2 + 1;
            }
            i2 = i2 + 1;
        }

        c8++;
        return total;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Ingrese el tamaño n del arreglo: ");
        int n = sc.nextInt();
        sc.close();

        int[] a = new int[n];
        for (int k = 0; k < n; k++) a[k] = 1;

        int resultado = procesar(a, n);

        long nn = n;
        System.out.println("\nConteo de ejecuciones por línea (n = " + n + "):\n");

        System.out.println("-- contarMenores (acumulado en las n² llamadas) --");
        System.out.println("e1 (contador<-0)   : " + e1 + "  -> esperado: " + (nn * nn));
        System.out.println("e2 (while k<n)     : " + e2 + "  -> esperado: " + (nn * nn * (nn + 1)));
        System.out.println("e3 (if a[k]<valor) : " + e3 + "  -> esperado: " + (nn * nn * nn));
        System.out.println("e4 (contador++)    : " + e4 + "  -> esperado: " + (nn * nn * nn));
        System.out.println("e5 (return)        : " + e5 + "  -> esperado: " + (nn * nn));

        System.out.println("\n-- procesar --");
        System.out.println("c1 (for i, 1er bloque) : " + c1 + "  -> esperado: " + (nn + 1));
        System.out.println("c2 (for j, 1er bloque) : " + c2 + "  -> esperado: " + (nn * (nn + 1)));
        System.out.println("c3 (suma[i][j]<-...)   : " + c3 + "  -> esperado: " + (nn * nn));
        System.out.println("c4 (total<-0)          : " + c4 + "  -> esperado: " + 1);
        System.out.println("c5 (for i, 2do bloque) : " + c5 + "  -> esperado: " + (nn + 1));
        System.out.println("c6 (for j, 2do bloque) : " + c6 + "  -> esperado: " + (nn * (nn + 1)));
        System.out.println("c7 (total<-total+...)  : " + c7 + "  -> esperado: " + (nn * nn));
        System.out.println("c8 (return total)      : " + c8 + "  -> esperado: " + 1);

        long sumaContadores = e1 + e2 + e3 + e4 + e5
                            + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8;
        long tProcesarTeorico = 3 * nn * nn * nn + 7 * nn * nn + 4 * nn + 4;

        System.out.println("\nSuma de los 13 contadores        : " + sumaContadores);
        System.out.println("T_procesar(n) = 3n³+7n²+4n+4     : " + tProcesarTeorico);
        System.out.println(sumaContadores == tProcesarTeorico
                ? "COINCIDEN -> el análisis es consistente con el conteo real."
                : "NO COINCIDEN -> revisar el análisis o la instrumentación.");

        System.out.println("\n(resultado de procesar, solo para evitar que el JIT elimine la llamada: "
                + resultado + ")");
    }
}
```

**Resultados** (suma de los 13 contadores vs. la fórmula teórica, para distintos $n$):

| $n$ | Suma de contadores | $3n^3+7n^2+4n+4$ | ¿Coinciden? |
|---|---|---|---|
| 2 | 64 | 64 | Sí |
| 3 | 160 | 160 | Sí |
| 5 | 574 | 574 | Sí |
| 10 | 3744 | 3744 | Sí |

El conteo real de instrucciones ejecutadas coincide **exactamente** con la fórmula teórica para todo $n$ probado, lo que confirma que el análisis de los incisos a)–e) es correcto.

---

¿Quiere volver a intentar el ejercicio desde cero? Vuelva al [enunciado](index.md).
