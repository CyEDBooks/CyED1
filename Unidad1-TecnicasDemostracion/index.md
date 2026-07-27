---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 1: Métodos de demostración"
---

# Unidad 1: Métodos de demostración

---
**· Contenido adicional ·**

## La lógica formal

es una rama de la filosofía y las matemáticas que estudia los principios del razonamiento válido mediante estructuras simbólicas precisas. A diferencia de la lógica informal, que se enfoca en la argumentación cotidiana y su contenido, la lógica formal abstrae el contenido de los enunciados y se centra únicamente en su forma, utilizando símbolos y reglas bien definidas.

### Objetivo principal

Determinar si un argumento es válido, es decir, si la conclusión se sigue necesariamente de las premisas. Para ello, emplea sistemas formales como la lógica proposicional y la lógica de predicados, que permiten representar y analizar argumentos mediante fórmulas simbólicas.

### Usos

Esta disciplina es fundamental no solo en filosofía, sino también en áreas como la computación, la lingüística, las ciencias cognitivas y la inteligencia artificial, donde el análisis riguroso del razonamiento es esencial. Estudiar lógica formal proporciona herramientas poderosas para mejorar la claridad, coherencia y rigor en el pensamiento y la argumentación.

## Reglas de inferencia

- A partir de un conjunto de sentencias que son ciertas, permite conocer otras que se derivan de dicho conjunto.

1. Si es viernes entonces hay carullazo
2. Hoy es viernes

$\therefore$ Hay carullazo, **modus ponens(1,2)**

$$
\begin{array}{c}
p \to q\\
p\\ \hline
\therefore\ q
\end{array}
$$

Otro ejemplo:

1. El carro es rojo o es negro
2. El carro no es rojo

$\therefore$ El carro es negro, **silogismo disyuntivo(1,2)**

$$
\begin{array}{c}
p \vee q\\
\neg p\\ \hline
\therefore\ q
\end{array}
$$

### Tabla de reglas de inferencia

| Regla | Nombre | Regla | Nombre |
|---|---|---|---|
| $\begin{array}{c} p \wedge q \\ \hline \therefore p \end{array}$ | Simplificación | $\begin{array}{c} p \to q \\ p \\ \hline \therefore q \end{array}$ | Modus ponens |
| $\begin{array}{c} p \vee q \\ \neg p \\ \hline \therefore q \end{array}$ | Silogismo disyuntivo | $\begin{array}{c} p \to q \\ q \to r \\ \hline \therefore p \to r \end{array}$ | Silogismo hipotético |
| $\begin{array}{c} p \to q \\ \neg q \\ \hline \therefore \neg p \end{array}$ | Modus tollens | $\begin{array}{c} p \\ \hline \therefore p \vee q \end{array}$ | Adición |

### Aplicar las siguientes reglas

- **Simplificación** sobre

  $1.\ \neg q \wedge \neg t$

- **Silogismo disyuntivo** sobre

  $1.\ t \vee \neg p$
  $2.\ p$

- **Modus tollens** sobre

  $1.\ \neg q \to \neg t$
  $2.\ t$

### Ejemplo guiado 1

Suponga que se conoce que las siguientes sentencias son verdaderas:

1. $\neg p \wedge q$
2. $r \to p$
3. $\neg r \to s$
4. $s \to t$

Demuestre que $t$ es cierto.

:::{dropdown} Demostración
5. $\neg p$, simplificación(1)
6. $\neg r$, modus tollens(2,5)
7. $s$, modus ponens(3,6)
8. $t$, modus ponens(4,7)
:::

### Ejemplo guiado 2

Suponga que se conoce que las siguientes sentencias son verdaderas:

1. $s \to q$
2. $\neg p \to r$
3. $r \to s$

Demuestre que $\neg p \to q$ es cierto.

:::{dropdown} Demostración
4. $\neg p \to s$, silogismo hipotético(2,3)
5. $\neg p \to q$, silogismo hipotético(4,1)
:::

### Ejemplo guiado 3

Suponga que se conoce que las siguientes sentencias son verdaderas:

1. $p \to \neg q$
2. $\neg r$
3. $\neg p \to s$
4. $\neg q \to r$

:::{dropdown} Demostración
5. $q$, modus tollens(2,4)
6. $\neg p$, modus tollens(1,5)
7. $s$, modus ponens(3,6)
:::

### Ejemplo guiado 4

Suponga que se conoce que las siguientes sentencias son verdaderas:

1. $p \vee \neg q$
2. $\neg p \wedge r$
3. $\neg q \to \neg s$
4. $s \vee t$

:::{dropdown} Demostración
5. $\neg p$, simplificación(2)
6. $\neg q$, silogismo disyuntivo(1,5)
7. $\neg s$, modus ponens(3,6)
8. $t$, silogismo disyuntivo(4,7)
:::

### Ejemplo guiado 5

Suponga que se conoce que las siguientes sentencias son verdaderas:

1. $u \vee w$
2. $p \wedge \neg q$
3. $t \to q$
4. $\neg w \vee s$
5. $u \to t$

:::{dropdown} Demostración
6. $\neg q$, simplificación(2)
7. $\neg t$, modus tollens(3,6)
8. $\neg u$, modus tollens(5,7)
9. $w$, silogismo disyuntivo(1,8)
10. $s$, silogismo disyuntivo(4,9)
:::

## Demostración directa

- Se parte de la hipótesis y se intenta llegar a la conclusión.

**Demuestre que si $n$ y $m$ son impares, la suma es par.**

Si $n$ y $m$ son números impares, se pueden expresar de la forma:

$$
\begin{align*}
n &= 2 \cdot k_1 + 1\\
m &= 2 \cdot k_2 + 1
\end{align*}
$$

La suma $n+m$ será:

$$
\begin{align*}
n + m &= (2 \cdot k_1 + 1) + (2 \cdot k_2 + 1)\\
      &= 2 \cdot k_1 + 2 \cdot k_2 + 2\\
      &= 2 \cdot (k_1 + k_2 + 1)\\
      &= 2 \cdot k_3
\end{align*}
$$

Por lo tanto, $n+m$ debe ser un número par.

**Demuestre que si $n$ es impar, entonces $3n+2$ es impar.**

Si $n$ es impar, se puede expresar de la forma:

$$
n = 2 \cdot k_1 + 1
$$

Al calcular $3n+2$ se tiene:

$$
\begin{align*}
3n+2 &= 3(2 \cdot k_1 + 1) + 2\\
     &= 6 \cdot k_1 + 3 + 2\\
     &= 6 \cdot k_1 + 4 + 1\\
     &= 2(3 \cdot k_1 + 2) + 1\\
     &= 2 \cdot k_2 + 1
\end{align*}
$$

Por lo tanto, $3n+2$ debe ser un número impar.

**Demuestre que si $n$ es impar, entonces $n^2$ es impar.**

Si $n$ es impar, se puede expresar de la forma:

$$
n = 2 \cdot k_1 + 1
$$

Al calcular $n^2$ se tiene:

$$
\begin{align*}
n^2 &= (2 \cdot k_1 + 1)^2\\
    &= (2 \cdot k_1)^2 + 2 \cdot 2 \cdot k_1 \cdot 1 + 1^2\\
    &= 4 \cdot k_1^2 + 4 \cdot k_1 + 1\\
    &= 2(2k_1^2 + 2k_1) + 1\\
    &= 2 \cdot k_3 + 1
\end{align*}
$$

Por lo tanto, $n^2$ debe ser un número impar.

**Demuestre que si $n$ es impar, entonces $n^3+5$ es par.**

Si $n$ es impar, se puede expresar de la forma:

$$
n = 2 \cdot k_1 + 1
$$

Al calcular $n^3+5$ se tiene:

$$
\begin{align*}
n^3 &= (2 \cdot k_1 + 1)^3 + 5\\
    &= (2 \cdot k_1)^3 + 3 \cdot (2k_1)^2 \cdot 1 + 3 \cdot 2k_1 \cdot 1^2 + 1^3 + 5\\
    &= 8 \cdot k_1^3 + 12 \cdot k_1^2 + 6 \cdot k_1 + 6\\
    &= 2(4 \cdot k_1^3 + 6 \cdot k_1^2 + 3 \cdot k_1 + 3)\\
    &= 2 \cdot k_2
\end{align*}
$$

Por lo tanto, $n^3+5$ debe ser un número par.

**Demuestre que si $n$ es par y $m$ es impar, entonces $m-2n$ es impar.**

Si $n$ es par y $m$ es impar, se pueden expresar de la forma:

$$
\begin{align*}
n &= 2 \cdot k_1\\
m &= 2 \cdot k_2 + 1
\end{align*}
$$

Al calcular $m-2n$ se tiene:

$$
\begin{align*}
m - 2n &= (2 \cdot k_2 + 1) - 2(2 \cdot k_1)\\
       &= 2 \cdot k_2 + 1 - 4k_1\\
       &= 2(k_2 - 2 \cdot k_1) + 1\\
       &= 2 \cdot k_3 + 1
\end{align*}
$$

Por lo tanto, $m-2n$ debe ser un número impar.

**Demuestre que si $m$ es impar y $n$ es par, entonces $m^2+2 \cdot m \cdot n+n^2$ es impar.**

Si $m$ es impar y $n$ es par, se pueden expresar de la forma:

$$
\begin{align*}
m &= 2 \cdot k_1 + 1\\
n &= 2 \cdot k_2
\end{align*}
$$

Al calcular $m^2+2 \cdot m \cdot n+n^2$ se tiene:

$$
\begin{align*}
m^2+2 \cdot m \cdot n+n^2 &= (2 \cdot k_1+1)^2+2(2 \cdot k_1+1)(2 \cdot k_2)+(2 \cdot k_2)^2\\
    &= 4 \cdot k_1^2 + 4 \cdot k_1 + 1 + 8 \cdot k_1 \cdot k_2 + 4 \cdot k_2 + 4 \cdot k_2^2\\
    &= 2(2 \cdot k_1^2 + 2 \cdot k_1 + 4 \cdot k_1 \cdot k_2 + 2 \cdot k_2 + 2 \cdot k_2^2) + 1\\
    &= 2 \cdot k_3 + 1
\end{align*}
$$

Por lo tanto, $m^2+2 \cdot m \cdot n+n^2$ debe ser un número impar.

## Demostración indirecta

- Utiliza la contrapositiva de $p \rightarrow q$, $\neg q \rightarrow \neg p$.
- Toma como hipótesis $\neg q$ e intenta llegar a la conclusión $\neg p$.

**Demuestre que si $3n+2$ es impar, entonces $n$ es impar.**

Se demuestra que "si $n$ es par, entonces $3n+2$ es par".

Si $n$ es par, se puede expresar de la forma:

$$
n = 2 \cdot k_1
$$

Al calcular $3n+2$ se tiene:

$$
\begin{align*}
3n+2 &= 3(2 \cdot k_1) + 2\\
     &= 6 \cdot k_1 + 2\\
     &= 2(3 \cdot k_1 + 1)\\
     &= 2 \cdot k_2 \text{, es decir, } 3n+2 \text{ es par}
\end{align*}
$$

**Demuestre que si $n^2$ es par, entonces el número $n$ es par.**

Se demuestra que "si $n$ es impar, entonces $n^2$ es impar".

Si $n$ es impar, se puede expresar de la forma:

$$
n = 2 \cdot k_1 + 1
$$

Al calcular $n^2$ se tiene:

$$
\begin{align*}
n^2 &= (2 \cdot k_1 + 1)^2\\
    &= (2 \cdot k_1)^2 + 2 \cdot 2 \cdot k_1 \cdot 1 + 1^2\\
    &= 4 \cdot k_1^2 + 4 \cdot k_1 + 1\\
    &= 4(k_1^2 + k_1) + 1\\
    &= 4 \cdot k_2 + 1 \text{, es decir, } n^2 \text{ es impar}
\end{align*}
$$

**Demuestre que si $7n-4$ es par, entonces $n$ es par.**

Se demuestra que "si $n$ es impar, entonces $7n-4$ es impar".

Si $n$ es impar, se puede expresar de la forma:

$$
n = 2 \cdot k_1 + 1
$$

Al calcular $7n-4$ se tiene:

$$
\begin{align*}
7n-4 &= 7(2 \cdot k_1 + 1) - 4\\
     &= 14 \cdot k_1 + 7 - 4\\
     &= 14 \cdot k_1 + 3\\
     &= 14 \cdot k_1 + 2 + 1\\
     &= 2(7 \cdot k_1 + 1) + 1\\
     &= 2 \cdot k_2 + 1 \text{, es decir, } 7n-4 \text{ es impar}
\end{align*}
$$

**Demuestre que si $5n-6$ es impar, entonces $n$ es impar.**

Se demuestra que "si $n$ es par, entonces $5n-6$ es par".

Si $n$ es par, se puede expresar de la forma:

$$
n = 2 \cdot k_1
$$

Al calcular $5n-6$ se tiene:

$$
\begin{align*}
5n-6 &= 5(2 \cdot k_1) - 6\\
     &= 10 \cdot k_1 - 6\\
     &= 2(5 \cdot k_1 - 3)\\
     &= 2 \cdot k_2 \text{, es decir, } 5n-6 \text{ es par}
\end{align*}
$$

---
**· Contenido adicional ·**

### Demostración por Reducción al Absurdo

Se asume que la proposición es falsa y se llega a una contradicción lógica.

**Ejemplo:**

Demostrar que $\sqrt{2}$ es irracional.

**Demostración:**

Supongamos que $\sqrt{2}$ es racional. Entonces se puede escribir como $\frac{p}{q}$, con $p$ y $q$ enteros primos entre sí. Elevando al cuadrado,

$$
2 = \frac{p^2}{q^2} \Rightarrow p^2 = 2q^2
$$

Esto implica que $p^2$ es par, lo que implica que $p$ también es par. Sea $p = 2k$, entonces,

$$
(2k)^2 = 2q^2 \Rightarrow 4k^2 = 2q^2 \Rightarrow q^2 = 2k^2
$$

Por lo tanto, $q^2$ es par, lo que implica que $q$ también es par. Pero esto contradice la suposición de que $p$ y $q$ son primos entre sí. Por lo tanto, $\sqrt{2}$ es irracional.

### Disyunción por casos

Si una afirmación se cumple en todos los casos posibles, entonces se cumple siempre.

**Ejemplo**

Demuestre que $|xy| = |x||y|$ para $x, y \in \mathbb{R}$

Recordemos la definición del valor absoluto:

$$
|a| =
\begin{cases}
a & \text{si } a \geq 0 \\
-a & \text{si } a < 0
\end{cases}
$$

**Demostración**

Procedemos por casos, considerando los signos de $x$ y $y$:

**Caso 1:** $x \geq 0$, $y \geq 0$

Entonces $xy \geq 0$, por lo que:

- $|x| = x$
- $|y| = y$
- $|xy| = xy$

Luego:

$$
|xy| = xy = x \cdot y = |x||y|
$$

**Caso 2:** $x \geq 0$, $y < 0$

Entonces $xy < 0$, por lo que:

- $|x| = x$
- $|y| = -y$
- $|xy| = -(xy) = -x \cdot y$

Pero $|x||y| = x \cdot (-y) = -xy$

Luego:

$$
|xy| = -xy = |x||y|
$$

**Caso 3:** $x < 0$, $y \geq 0$

Análogo al caso anterior. $xy < 0$, entonces:

- $|x| = -x$
- $|y| = y$
- $|xy| = -(xy) = -x \cdot y$

Y:

$$
|x||y| = (-x) \cdot y = -xy = |xy|
$$

**Caso 4:** $x < 0$, $y < 0$

Entonces $xy > 0$, porque el producto de dos negativos es positivo. Entonces:

- $|x| = -x$
- $|y| = -y$
- $|xy| = xy$

Y:

$$
|x||y| = (-x)(-y) = xy = |xy|
$$

**Conclusión:**

En todos los casos se cumple que:

$$
|xy| = |x||y|
$$

Por tanto, para todo $x, y \in \mathbb{R}$:

$$
\boxed{|xy| = |x||y|}
$$

## Demostración por contraejemplo

- Se muestra un caso donde no se cumple una expresión cuantificada universalmente.

- Todos los primos son impares
  - 2 es un contraejemplo ya que es par y primo

- Para cada número primo $n$, se cumple que $n+2$ es primo
  - $n=7$ es un contraejemplo ya que 7 es primo pero 9 no

- $n^2+n+41$ es un número primo para todos los enteros no negativos $n$
  - $n=40$ es un contraejemplo ya que
    $$
    40^2+40+41=1681
    $$
    no es primo (es divisible entre 41)

### Otras afirmaciones para refutar

- Todos los primos son impares
- Para cada número primo $n$, se cumple que $n+2$ es primo
- $n^2+n+41$ es un número primo para todos los enteros no negativos $n$
- $\forall x \; x^2 \ge x$
- $\forall x \forall y \; (x+y = x-y)$
- $\forall x \forall y \; ((x>0 \land y>0) \rightarrow x-y>0)$

---
**· Contenido adicional ·**

### Demostración por contraejemplo (repaso)

Una demostración por contraejemplo se utiliza para refutar una afirmación universal, es decir, una afirmación que dice que algo es cierto para todos los elementos de un conjunto.

**Ejemplo**

Todos los números primos son impares

**Demostración**

Consideremos el número:

$$
2
$$

- $2$ es **mayor que 1**
- Los únicos divisores positivos de $2$ son $1$ y $2$
- Entonces, **$2$ es primo**
- Pero **$2$ es par**

**Conclusión:**

Hemos encontrado un número primo que **no es impar**: el número **2**.

Por lo tanto, la afirmación:

$$
\text{"Todos los números primos son impares"}
$$

es **falsa**.

### Demostración por equivalencia

Una demostración por equivalencia se usa cuando queremos probar que dos afirmaciones son lógicamente iguales, es decir, que una es verdadera si y solo si la otra también lo es.

**Ejemplo:**

Demuestre que si $n$ es par si y solo si $(n+1)$ es impar

Esto es una proposición de equivalencia lógica. Escribimos:

**Demostración**

Para probar una equivalencia, debemos demostrar **ambas direcciones**:

**Caso 1:** Si $n$ es par, entonces $(n+1)$ es impar

Por definición:

- Un número **par** es un entero que se puede escribir como $n = 2k$ para algún $k \in \mathbb{Z}$.
- Entonces, $(n+1) = 2k + 1$.

Esto es exactamente la forma de un número **impar**.

Por lo tanto, si $n$ es par, entonces $(n+1)$ es impar.

**Caso 2:** Si $(n+1)$ es impar, entonces $n$ es par

Si $(n+1)$ es impar, entonces por definición:

- $(n+1) = 2k + 1$ para algún $k \in \mathbb{Z}$.
- Entonces, $n = (2k + 1) - 1 = 2k$.

Esto es exactamente la forma de un número **par**.

Por lo tanto, $n$ es par.

**Conclusión:**

Como se ha demostrado **en ambos sentidos**:

$$
n \text{ es par } \iff (n+1) \text{ es impar}
$$

### Demostración por Inducción Matemática

Se usa para demostrar afirmaciones sobre los números naturales.

**Ejemplo:**

Demostrar que para todo $n \geq 1$:

$$
1 + 2 + \dots + n = \frac{n(n+1)}{2}
$$

**Paso Base:**

Para $n = 1$:

$$
1 = \frac{1(1+1)}{2} = 1
$$

Lo cual es cierto.

**Paso Inductivo:**

Supongamos que la fórmula es cierta para algún $n = k$, es decir:

$$
1 + 2 + \dots + k = \frac{k(k+1)}{2}
$$

Demostramos que es cierta para $n = k + 1$:

$$
1 + 2 + \dots + k + (k+1) = \frac{k(k+1)}{2} + (k+1)
$$

Sacamos factor común $(k+1)$:

$$
= \frac{k(k+1) + 2(k+1)}{2} = \frac{(k+1)(k+2)}{2}
$$

Que es la fórmula para $n = k+1$. Por lo tanto, la afirmación es verdadera para todo $n \geq 1$.

*(La inducción matemática se retomará en profundidad más adelante en el curso; aquí se introduce solo como método de demostración adicional.)*

---

Continúa con los [ejercicios de la Unidad 1](exercises.md).

*Material adaptado del material original del profesor Oscar Bedoya, con contenido adicional del profesor Marlon Gomez.*
