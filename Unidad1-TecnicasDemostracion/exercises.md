---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 1: Ejercicios"
---

# Unidad 1: Ejercicios

Use esta página después de leer el [material de estudio de la Unidad 1](index.md).

## Ejercicios

**1) Demuestre $q$ a partir de las siguientes sentencias:**

1. $p \lor \neg t$
2. $\neg s \lor w$
3. $t \land \neg r$
4. $p \rightarrow \neg w$
5. $\neg q \rightarrow s$

:::{dropdown} Demostración por Derivación Lógica

**Paso 1:** De la premisa 3, tenemos:
$$t \land \neg r$$

Por la regla de simplificación (eliminación de conjunción):
$$t \quad \text{...(A)}$$
$$\neg r \quad \text{...(B)}$$

**Paso 2:** De la premisa 1 tenemos $p \lor \neg t$.

Como $t$ es verdadero (de A), entonces $\neg t$ es falso.

Por la regla de disyunción (eliminación del $\lor$), como $\neg t$ es falso, debe ser que $p$ es verdadero:
$$p \quad \text{...(C)}$$

**Paso 3:** De la premisa 4 tenemos $p \rightarrow \neg w$.

Como $p$ es verdadero (de C), por modus ponens:
$$\neg w \quad \text{...(D)}$$

**Paso 4:** De la premisa 2 tenemos $\neg s \lor w$.

Como $\neg w$ es verdadero (de D), entonces $w$ es falso.

Por la regla de disyunción, como $w$ es falso, debe ser que $\neg s$ es verdadero:
$$\neg s \quad \text{...(E)}$$

Es decir:
$$s \text{ es falso} \quad \text{...(F)}$$

**Paso 5:** De la premisa 5 tenemos $\neg q \rightarrow s$.

La contraposición de esta proposición es:
$$\neg s \rightarrow q$$

Como $\neg s$ es verdadero (de E), por modus ponens:
$$q \quad \text{...(CONCLUSIÓN)}$$
:::

**2) Demuestre de forma directa que si $n$ y $m$ son impares, entonces**

$$
\frac{n^2 + m^2}{2}
$$

**es impar.**

:::{dropdown} Deostración 
**Supongamos que $n$ y $m$ son números enteros impares.**

**Por definición, existen enteros $k$ y $j$ tales que:**
$$n = 2k + 1$$
$$m = 2j + 1$$

**Calculamos $n^2$:**
$$n^2 = (2k + 1)^2 = 4k^2 + 4k + 1$$

**Calculamos $m^2$:**
$$m^2 = (2j + 1)^2 = 4j^2 + 4j + 1$$

**Sumamos:**
$$n^2 + m^2 = 4k^2 + 4k + 1 + 4j^2 + 4j + 1$$

**Agrupamos:**
$$n^2 + m^2 = 4k^2 + 4k + 4j^2 + 4j + 2$$

**Factorizamos:**
$$n^2 + m^2 = 4(k^2 + k + j^2 + j) + 2$$

**Dividimos entre 2:**
$$\frac{n^2 + m^2}{2} = \frac{4(k^2 + k + j^2 + j) + 2}{2}$$

$$\frac{n^2 + m^2}{2} = 2(k^2 + k + j^2 + j) + 1$$

**Sea $p = k^2 + k + j^2 + j$. Como $k$ y $j$ son enteros:**
- $k^2 + k + j^2 + j$ es un entero
- Por lo tanto, $p$ es un entero

**Expresamos:**
$$\frac{n^2 + m^2}{2} = 2p + 1$$

**Por definición de número impar, $\frac{n^2 + m^2}{2}$ es impar.**
:::

**3) Sea $n$ un entero positivo, demuestre que $n$ es par si y sólo si $7n + 4$ es par.**


:::{dropdown} Demostración

## Demostración Bidireccional

### Dirección 1: Si $n$ es par, entonces $7n + 4$ es par (⟹)

**Supongamos que $n$ es par.** Entonces existe un entero $k$ tal que:
$$n = 2k$$

**Calculamos $7n + 4$:**
$$7n + 4 = 7(2k) + 4 = 14k + 4 = 2(7k + 2)$$

**Sea $m = 7k + 2$, que es un entero.** Entonces:
$$7n + 4 = 2m$$

**Por definición, $7n + 4$ es par.**

### Dirección 2: Si $7n + 4$ es par, entonces $n$ es par (⟸)

**Supongamos que $7n + 4$ es par.** Entonces existe un entero $m$ tal que:
$$7n + 4 = 2m$$

**Despejamos:**
$$7n = 2m - 4 = 2(m - 2)$$

**Sea $p = m - 2$, que es un entero.** Entonces:
$$7n = 2p$$

**Esto significa que $7n$ es par. Dado que $7$ es impar, y un número impar multiplicado por $n$ es par, entonces $n$ debe ser par.**

**Demostración formal de la afirmación anterior:**

Supongamos que $n$ es impar. Entonces $n = 2j + 1$ para algún entero $j$. Así:
$$7n = 7(2j + 1) = 14j + 7 = 2(7j + 3) + 1$$

Esto significa que $7n$ es impar, lo que contradice que $7n = 2p$ (par).

**Por lo tanto, $n$ debe ser par.**

### Conclusión

$$n \text{ es par} \iff 7n + 4 \text{ es par}$$
:::

**4) Demuestre por contradicción que la siguiente afirmación no es correcta:**

> "$2^{n}+1$ es un número primo para todos los enteros no negativos $n$"

:::{dropdown} Demostracion (Refutación)

**Supongamos, por el contrario,** que "$2^n + 1$ es primo para todo entero no negativo $n$".

**Evaluemos para diferentes valores de $n$:**

**Para $n = 0$:**
$$2^0 + 1 = 1 + 1 = 2$$
2 es primo.

**Para $n = 1$:**
$$2^1 + 1 = 2 + 1 = 3$$
3 es primo.

**Para $n = 2$:**
$$2^2 + 1 = 4 + 1 = 5$$
5 es primo.

**Para $n = 3$:**
$$2^3 + 1 = 8 + 1 = 9$$

**Análisis:** ¿Es 9 primo?
$$9 = 3 \times 3$$
9 no es primo.

**Conclusión** Encontramos un contraejemplo: para $n = 3$, tenemos $2^3 + 1 = 9$, que **no es un número primo**. Por lo tanto, la afirmación "$2^n + 1$ es primo para todos los enteros no negativos $n$" **es falsa**.

:::

**5) Demuestre que el cuadrado de un número par es un número par utilizando una demostración directa.**

:::{dropdown} Demostración
**Supongamos que** $n$ es un número par.

**Por definición de número par,** existe un entero $k$ tal que:
$$n = 2k$$

**Elevamos al cuadrado ambos lados:**
$$n^2 = (2k)^2$$

**Desarrollamos el cuadrado:**
$$n^2 = 4k^2$$

**Factorizamos para expresar el resultado en forma de "2 por algo":**
$$n^2 = 2 \cdot (2k^2)$$

**Sea** $m = 2k^2$. Dado que $k$ es un entero:
- $k^2$ es un entero
- $2k^2$ es un entero
- Por lo tanto, $m$ es un entero

**Conclusión:** Como $n^2 = 2m$ donde $m$ es un entero, por definición de número par, $n^2$ es un número par.
:::

**6) Demuestre que el cuadrado de un número par es un número par utilizando una demostración por reducción al absurdo.**

:::{dropdown} Demostración (Reducción al Absurdo)

**Supongamos, por el contrario,** que $n$ es par pero $n^2$ es impar.

**Por definición de número par,** existe un entero $k$ tal que:
$$n = 2k$$

**Elevamos al cuadrado:**
$$n^2 = (2k)^2 = 4k^2 = 2(2k^2)$$

**Sea $m = 2k^2$, que es un entero.** Entonces:
$$n^2 = 2m$$

**Esto significa que $n^2$ es par.**

**Pero esto contradice nuestra suposición de que $n^2$ es impar.**

**Por lo tanto, nuestra suposición es falsa. Concluimos que si $n$ es par, entonces $n^2$ es par.**
:::


**7) Demuestre que todo entero impar es una diferencia de cuadrados utilizando una demostración directa.**

:::{dropdown} Demostración Directa

**Sea $n$ un número entero impar.**

**Por definición, existe un entero $k$ tal que:**
$$n = 2k + 1$$

**Expresamos $n$ como una diferencia de cuadrados. Consideremos:**
$$(k+1)^2 - k^2$$

**Desarrollamos:**
$$(k+1)^2 - k^2 = k^2 + 2k + 1 - k^2 = 2k + 1 = n$$

**Por lo tanto:**
$$n = (k+1)^2 - k^2$$

**Conclusión:** Todo número impar $n$ puede expresarse como la diferencia de dos cuadrados consecutivos: $(k+1)^2 - k^2$.
:::

**8) Demuestre que la suma de dos impares es par.**

:::{dropdown} Demostración
**Sean $m$ y $n$ números enteros impares.**

**Por definición de número impar, existen enteros $k$ y $j$ tales que:**
$$m = 2k + 1$$
$$n = 2j + 1$$

**Sumamos:**
$$m + n = (2k + 1) + (2j + 1) = 2k + 2j + 2$$

**Factorizamos:**
$$m + n = 2(k + j + 1)$$

**Sea $p = k + j + 1$. Como $k$ y $j$ son enteros:**
- $k + j + 1$ es un entero
- Por lo tanto, $p$ es un entero

**Conclusión:** Como $m + n = 2p$ donde $p$ es entero, por definición, $m + n$ es par.
:::

**9) Demuestre que si $n$ es un entero y $3n + 2$ es par, entonces $n$ es par usando:**

1. Una demostración indirecta.
2. Una demostración por reducción al absurdo.


:::{dropdown} Demostraciones (Indirecta y Reducción al Absurdo)
## Parte 1: Demostración Indirecta (Contraposición)

**Demostraremos la contraposición:** Si $n$ es impar, entonces $3n + 2$ es impar.

**Supongamos que $n$ es impar.** Entonces existe un entero $k$ tal que:
$$n = 2k + 1$$

**Calculamos $3n + 2$:**
$$3n + 2 = 3(2k + 1) + 2 = 6k + 3 + 2 = 6k + 5$$

**Reescribimos:**
$$3n + 2 = 2(3k + 2) + 1$$

**Sea $m = 3k + 2$, que es un entero.** Entonces:
$$3n + 2 = 2m + 1$$

**Por definición, $3n + 2$ es impar.**

**Por contraposición:** Si $3n + 2$ es par, entonces $n$ debe ser par.


## Parte 2: Demostración por Reducción al Absurdo

**Supongamos, por el contrario,** que $3n + 2$ es par pero $n$ es impar.

**Si $n$ es impar,** existe un entero $k$ tal que:
$$n = 2k + 1$$

**Entonces:**
$$3n + 2 = 3(2k + 1) + 2 = 6k + 5 = 2(3k + 2) + 1$$

**Esto significa que $3n + 2$ es impar.**

**Pero esto contradice nuestra suposición de que $3n + 2$ es par.**

**Por lo tanto, $n$ debe ser par.**

:::

**10) Demuestre que se cumple, o que no, que el producto de dos números irracionales es irracional.**

:::{dropdown} Demostración
## Respuesta: NO. El producto de dos irracionales puede ser racional o irracional.

**Consideremos:**
$$a = \sqrt{2} \quad \text{(irracional)}$$
$$b = \sqrt{8} = 2\sqrt{2} \quad \text{(irracional)}$$

**Calculamos el producto:**
$$a \cdot b = \sqrt{2} \cdot 2\sqrt{2} = 2 \cdot (\sqrt{2})^2 = 2 \cdot 2 = 4$$

**El resultado es $4$, que es racional.**

**Conclusión:** El producto de dos números irracionales no es necesariamente irracional. Puede ser racional, como en este caso.
:::

**11) Demuestre que se cumple, o que no, que el producto de dos números racionales es racional.**

:::{dropdown} Demostración ¿Es Racional?
## Respuesta: SÍ. El enunciado es verdadero.

**Sean $x$ y $y$ números racionales.**

**Por definición de número racional, existen enteros $a, b, c, d$ con $b \neq 0$ y $d \neq 0$, tales que:**
$$x = \frac{a}{b} \quad \text{y} \quad y = \frac{c}{d}$$

**Calculamos el producto:**
$$x \cdot y = \frac{a}{b} \cdot \frac{c}{d} = \frac{ac}{bd}$$

**Observamos que:**
- $ac$ es un entero (producto de dos enteros)
- $bd$ es un entero (producto de dos enteros)
- $bd \neq 0$ (producto de dos enteros no nulos)

**Por definición de número racional:**
$$x \cdot y = \frac{ac}{bd} \text{ es un número racional}$$
:::

**12) Demuestre que se cumple, o que no, que el producto de un número racional distinto de cero y un número irracional es un número irracional.**


:::{dropdown} Demostración ¿Es Irracional?

## Respuesta: SÍ. El enunciado es verdadero.

## Demostración por Reducción al Absurdo

**Sean $r$ un número racional distinto de cero e $i$ un número irracional.**

**Supongamos, por el contrario,** que $r \cdot i$ es racional.

**Por definición de número racional, existen enteros $a, b, c, d$ con $b \neq 0, d \neq 0$, tales que:**
$$r = \frac{a}{b} \quad \text{y} \quad r \cdot i = \frac{c}{d}$$

**Además, como $r \neq 0$, tenemos $a \neq 0$.**

**Despejamos $i$:**
$$i = \frac{r \cdot i}{r} = \frac{\frac{c}{d}}{\frac{a}{b}} = \frac{c}{d} \cdot \frac{b}{a} = \frac{bc}{ad}$$

**Observamos que:**
- $bc$ es un entero
- $ad$ es un entero no nulo (pues $a \neq 0$ y $d \neq 0$)

**Por lo tanto:**
$$i = \frac{bc}{ad} \text{ es racional}$$

**Pero esto contradice que $i$ es irracional.**

**Concluimos que nuestra suposición es falsa. Por lo tanto, $r \cdot i$ debe ser irracional.**
:::


**13) Demuestre que si $x$ es un número racional distinto de cero, entonces $1/x$ es racional.**


:::{dropdown} Demostración

**Sea $x$ un número racional distinto de cero.**

**Por definición de número racional, existen enteros $a$ y $b$ con $b \neq 0$, tales que:**
$$x = \frac{a}{b}$$

**Como $x \neq 0$, tenemos $a \neq 0$.**

**Calculamos el recíproco:**
$$\frac{1}{x} = \frac{1}{\frac{a}{b}} = \frac{b}{a}$$

**Observamos que:**
- $b$ es un entero
- $a$ es un entero distinto de cero

**Por definición de número racional:**
$$\frac{1}{x} = \frac{b}{a} \text{ es un número racional}$$
:::

*Material adaptado del material original de los profesores Oscar Bedoya y Marlon Gomez.*
