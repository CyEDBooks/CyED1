---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Relaciones y Funciones: Ejercicios"
---

# Relaciones y Funciones: Ejercicios

Use esta página después de leer el [material de estudio de Relaciones y Funciones](index.md).

---

### Ejercicios Funciones

**Ejercicio 1**
Calcule estos valores:

1. $\lfloor 1.1 \rfloor$
2. $\lceil 1.1 \rceil$
3. $\lfloor -0.1 \rfloor$
4. $\lceil -0.1 \rceil$
5. $\lceil 2.99 \rceil$
6. $\lceil -2.99 \rceil$
7. $\left\lfloor \frac{1}{2} + \lceil \frac{1}{2} \rceil \right\rfloor$
8. $\left\lceil \lfloor \frac{1}{2} \rfloor + \lceil \frac{1}{2} \rceil + \frac{1}{2} \right\rceil$

**Ejercicio 2**
Calcule estos valores:

1. $\lceil \frac{3}{4} \rceil$
2. $\lfloor \frac{7}{8} \rfloor$
3. $\lceil -\frac{3}{4} \rceil$
4. $\lfloor -\frac{7}{8} \rfloor$
5. $\lceil 3 \rceil$
6. $\lfloor -1 \rfloor$
7. $\left\lfloor \frac{1}{2} + \lceil \frac{3}{2} \rceil \right\rfloor$
8. $\left\lfloor \frac{1}{2} \cdot \lfloor \frac{5}{2} \rfloor \right\rfloor$

**Ejercicio 3**
Sea $S = \{-1, 0, 2, 4, 7\}$. Halle $f(S)$ si:

1. $f(x) = 1$
2. $f(x) = 2x + 1$
3. $f(x) = \left\lceil \frac{x}{5} \right\rceil$
4. $f(x) = \left\lfloor \frac{x^2 + 1}{3} \right\rfloor$

**Ejercicio 4**
Sea $f(x) = \left\lfloor \frac{x^2}{3} \right\rfloor$. Halle $f(S)$ si:

1. $S = \{-2, -1, 0, 1, 2, 3\}$
2. $S = \{0, 1, 2, 3, 4, 5\}$
3. $S = \{1, 5, 7, 11\}$
4. $S = \{2, 6, 10, 14\}$

**Ejercicio 5**
Sea $f(x) = 2x$. ¿Cuáles son?

1. $f(\mathbb{Z})$
2. $f(\mathbb{N})$
3. $f(\mathbb{R})$

**Ejercicio 6**
Suponga que $g$ es una función de $A$ en $B$ y $f$ es una función de $B$ en $C$.

1. Demuestre que si tanto $f$ como $g$ son funciones inyectivas entonces $f \circ g$ también lo es.
2. Demuestre que si tanto $f$ como $g$ son funciones sobreyectivas, entonces $f \circ g$ también lo es.

**Ejercicio 7**
Demuestre que si $f \circ g$ es inyectiva entonces $g$ es inyectiva.

**Ejercicio 8**
Calcule $f \circ g$ y $g \circ f$ donde $f(x) = x^2 + 1$ y $g(x) = x + 2$ son funciones de $\mathbb{R}$ en $\mathbb{R}$.

**Ejercicio 9**
Sean $f(x) = ax + b$ y $g(x) = cx + d$, donde $a$, $b$, $c$ y $d$ son constantes. Determine para qué valores se cumple que $f \circ g = g \circ f$.

**Ejercicio 10**
Demuestre que la función $f(x) = ax + b$ de $\mathbb{R}$ a $\mathbb{R}$ es invertible, donde $a \ne 0$, y halle la función inversa de $f$.

**Ejercicio 11**
Sea $f$ la función del conjunto $A$ en el conjunto $B$. Sean $S$ y $T$ subconjuntos de $A$. Demuestre que:

1. $f(S \cup T) = f(S) \cup f(T)$
2. $f(S \cap T) \subseteq f(S) \cap f(T)$

**Ejercicio 12**
Sea $f$ una función de $A$ en $B$, y sean $S$ y $T$ subconjuntos de $B$. Demuestre que:

1. $f^{-1}(S \cup T) = f^{-1}(S) \cup f^{-1}(T)$
2. $f^{-1}(S \cap T) = f^{-1}(S) \cap f^{-1}(T)$

**Ejercicio 13**
Sea $f$ una función de $A$ en $B$. Sea $S$ un subconjunto de $B$. Muestre que $f^{-1}(S^c) = (f^{-1}(S))^c$.

**Ejercicio 14**
Demuestre que si $x$ es un número real, entonces $\lceil x \rceil - \lfloor x \rfloor = 1$ si $x$ no es entero y $0$ si $x$ es un número entero.

**Ejercicio 15**
Demuestre que si $x$ es un número real y $m$ un entero, entonces $\lceil x + m \rceil = \lceil x \rceil + m$.

**Ejercicio 16**
Demuestre que si $n$ es un número entero, entonces $\lfloor n/2 \rfloor = n/2$ si $n$ es par y $(n - 1)/2$ si $n$ es impar.

**Ejercicio 17**
Demuestre que si $x$ es un número real, entonces $\lfloor -x \rfloor = -\lceil x \rceil$ y $\lceil -x \rceil = -\lfloor x \rfloor$

---

*Material adaptado del material original del profesor Marlon Gomez.*

---

## Sección Final: Ejercicios de Exámenes (Función Inversa y Composición de Funciones)

Los siguientes ejercicios fueron tomados de los **Exámenes 2** (versiones A, B, C y D, semestre 2025-2) del curso *Matemáticas Discretas y sus Aplicaciones* (PUJ). Se agrupan por tema: imagen inversa, función inversa y composición de funciones. Cada ejercicio incluye su solución explicada, oculta en un desplegable.

### Imagen inversa (preimágenes)

**Ejercicio 18** (Examen 2 - A)
Sea $g(x) = \lfloor x \rfloor$. Halle:

a) $g^{-1}(\{0\})$
b) $g^{-1}(\{-1, 0, 1\})$
c) $g^{-1}(\{x \mid 0 < x < 1\})$

:::{dropdown} Solución
La imagen inversa de un conjunto $S$ bajo $g$ es $g^{-1}(S) = \{x \in \mathbb{R} \mid g(x) \in S\}$.

a) $g(x) = 0 \iff \lfloor x \rfloor = 0 \iff 0 \le x < 1$. Entonces $g^{-1}(\{0\}) = [0, 1)$.

b) Se une la preimagen de cada valor:
- $g(x)=-1 \iff x \in [-1,0)$
- $g(x)=0 \iff x \in [0,1)$
- $g(x)=1 \iff x \in [1,2)$

Entonces $g^{-1}(\{-1,0,1\}) = [-1,0) \cup [0,1) \cup [1,2) = [-1, 2)$.

c) Se busca $x$ tal que $\lfloor x \rfloor$ sea un número **estrictamente entre 0 y 1**. Como $\lfloor x \rfloor$ siempre es un entero, y no existe ningún entero en el intervalo abierto $(0,1)$, no hay ningún $x$ que cumpla la condición.

Por lo tanto $g^{-1}(\{x \mid 0 < x < 1\}) = \varnothing$.
:::

**Ejercicio 19** (Examen 2 - D)
Sea $f$ la función de $\mathbb{R}$ en $\mathbb{R}$ definida por $f(x) = x^2$. Halle:

a) $f^{-1}(\{1\})$
b) $f^{-1}(\{x \mid 0 < x < 1\})$
c) $f^{-1}(\{x \mid x > 4\})$

:::{dropdown} Solución
a) $x^2 = 1 \iff x = \pm 1$. Entonces $f^{-1}(\{1\}) = \{-1, 1\}$.

b) $0 < x^2 < 1 \iff 0 < |x| < 1$, es decir $x$ está cerca de 0 pero no es 0. Entonces
$$f^{-1}(\{x \mid 0<x<1\}) = (-1,0)\cup(0,1).$$

c) $x^2 > 4 \iff |x| > 2 \iff x < -2 \text{ o } x > 2$. Entonces
$$f^{-1}(\{x \mid x>4\}) = (-\infty,-2)\cup(2,\infty).$$
:::

### Función inversa

**Ejercicio 20** (Examen 2 - B)
Halle las inversas de las siguientes funciones y especifique el dominio de dichas inversas.

a) $f(x) = x^2 - 2x + 3$, dominio $[1, \infty)$
b) $h(x) = |x|$, dominio $(-\infty, 0)$
c) $g(x) = 9 - x^2$, dominio $\mathbb{R}^{+}$

:::{dropdown} Solución
**a)** Se completa el cuadrado: $f(x) = (x-1)^2 + 2$. Como el dominio es $x \ge 1$, se tiene $x - 1 \ge 0$, y el rango es $[2, \infty)$ (función creciente en este dominio).

Despejando: $y = (x-1)^2+2 \Rightarrow (x-1)^2 = y - 2 \Rightarrow x - 1 = \sqrt{y-2}$ (raíz positiva, pues $x\ge1$) $\Rightarrow x = 1 + \sqrt{y-2}$.

$$f^{-1}(x) = 1 + \sqrt{x-2}, \quad \text{dominio } [2,\infty).$$

**b)** Para $x < 0$ se cumple $|x| = -x$, así que en este dominio $h(x) = -x$. Cuando $x$ recorre $(-\infty, 0)$, $h(x) = -x$ recorre $(0, \infty)$ (el rango).

Despejando $y = -x \Rightarrow x = -y$.

$$h^{-1}(x) = -x, \quad \text{dominio } (0,\infty).$$

**c)** Con $x > 0$, la función $g(x) = 9-x^2$ es decreciente, así que es inyectiva. Cuando $x \to 0^+$, $g \to 9^-$; cuando $x \to \infty$, $g \to -\infty$. El rango es $(-\infty, 9)$.

Despejando: $y = 9 - x^2 \Rightarrow x^2 = 9-y \Rightarrow x = \sqrt{9-y}$ (raíz positiva, pues $x>0$).

$$g^{-1}(x) = \sqrt{9-x}, \quad \text{dominio } (-\infty, 9).$$
:::

**Ejercicio 21** (Examen 2 - C)
Halle las inversas de las siguientes funciones:

a) $y = 3x + 2$
b) $y = \dfrac{1}{4-x}$
c) $y = \dfrac{x+2}{x+5}$
d) $y = x^3 + 1$

:::{dropdown} Solución
**a)** $y = 3x+2 \Rightarrow x = \dfrac{y-2}{3}$.
$$f^{-1}(x) = \frac{x-2}{3}$$

**b)** $y = \dfrac{1}{4-x} \Rightarrow y(4-x) = 1 \Rightarrow 4y - xy = 1 \Rightarrow x = \dfrac{4y-1}{y} = 4 - \dfrac{1}{y}$.
$$f^{-1}(x) = 4 - \frac{1}{x} = \frac{4x-1}{x}$$

**c)** $y = \dfrac{x+2}{x+5} \Rightarrow y(x+5) = x+2 \Rightarrow xy + 5y = x + 2 \Rightarrow x(y-1) = 2-5y \Rightarrow x = \dfrac{2-5y}{y-1}$.
$$f^{-1}(x) = \frac{2-5x}{x-1}$$

*Comprobación:* si $x=1$, $y = 3/6 = 0.5$; sustituyendo $y=0.5$ en la inversa: $\frac{2-2.5}{0.5-1} = \frac{-0.5}{-0.5}=1$. ✓

**d)** $y = x^3+1 \Rightarrow x^3 = y-1 \Rightarrow x = \sqrt[3]{y-1}$.
$$f^{-1}(x) = \sqrt[3]{x-1}$$
:::

### Composición de funciones

**Ejercicio 22** (Examen 2 - A)
Considere $f(x) = 4-x^2$, $g(x) = \sqrt{x+3}$, $h(x) = \dfrac{1}{2x}$. Evalúe:

a) $(f \circ g)(1)$
b) $(g \circ h)(1)$
c) $(f \circ g)(x)$
d) $(g \circ h)(x)$
e) $(h \circ g)(x)$
f) $(f \circ g)(x^2)$
g) $(f \circ g \circ h)(x)$

:::{dropdown} Solución
**a)** $g(1) = \sqrt{1+3} = 2$; $f(2) = 4-4 = 0$.
$$(f\circ g)(1) = 0$$

**b)** $h(1) = \frac{1}{2}$; $g(\frac12) = \sqrt{\frac12+3} = \sqrt{\frac72} = \frac{\sqrt{14}}{2}$.
$$(g\circ h)(1) = \frac{\sqrt{14}}{2} \approx 1.87$$

**c)** $(f\circ g)(x) = 4 - \left(\sqrt{x+3}\right)^2 = 4-(x+3) = 1-x$, válido cuando $x+3\ge0$, es decir $x \ge -3$ (dominio de $g$).
$$(f\circ g)(x) = 1-x, \quad x \ge -3$$

**d)** $(g\circ h)(x) = \sqrt{h(x)+3} = \sqrt{\dfrac{1}{2x}+3}$. Se necesita $x\ne0$ y $\dfrac{1}{2x}+3 \ge 0$, es decir $\dfrac{1+6x}{2x}\ge0$. Analizando signos: la desigualdad se cumple para $x \le -\frac16$ o $x>0$.
$$(g\circ h)(x) = \sqrt{3+\frac{1}{2x}}, \quad \text{dominio } \left(-\infty,-\tfrac16\right]\cup(0,\infty)$$

**e)** $(h\circ g)(x) = \dfrac{1}{2\,g(x)} = \dfrac{1}{2\sqrt{x+3}}$. Se requiere $x+3>0$ (estrictamente, para que el denominador no sea 0).
$$(h\circ g)(x) = \frac{1}{2\sqrt{x+3}}, \quad x > -3$$

**f)** Usando el resultado de (c), $(f\circ g)(t) = 1-t$ para $t\ge-3$. Con $t=x^2\ge0\ge-3$ (siempre cierto):
$$(f\circ g)(x^2) = 1-x^2, \quad \text{para todo } x\in\mathbb{R}$$

**g)** $(f\circ g\circ h)(x) = (f\circ g)(h(x)) = 1-h(x) = 1-\dfrac{1}{2x}$, usando de nuevo (c). El dominio es el mismo que en (d), pues se necesita $x$ en el dominio de $h$ y $h(x)$ en el dominio de $g$:
$$(f\circ g\circ h)(x) = 1-\frac{1}{2x}, \quad \text{dominio } \left(-\infty,-\tfrac16\right]\cup(0,\infty)$$
:::

**Ejercicio 23** (Examen 2 - B)

a) Sean $s(x)=\sqrt{x}$ y $t(x)=x^2+2x+1$. Evalúe $(s\circ t)(x)$ e indique su dominio y rango.
b) Sea $f(x)=\sqrt{\dfrac{1}{x^2+2}}$. Escriba $f(x)$ como la composición de dos o más funciones.

:::{dropdown} Solución
**a)** Note que $t(x) = x^2+2x+1 = (x+1)^2$, que siempre es $\ge0$, así que está siempre en el dominio de $s$.
$$(s\circ t)(x) = \sqrt{(x+1)^2} = |x+1|$$
Dominio: $\mathbb{R}$ (todo real es válido, pues $(x+1)^2\ge0$ siempre).
Rango: como $x+1$ recorre todo $\mathbb{R}$ cuando $x$ recorre $\mathbb{R}$, $|x+1|$ recorre $[0,\infty)$.

**b)** Se identifican tres funciones más simples:
$$u(x) = x^2+2, \qquad v(x) = \frac{1}{x}, \qquad w(x) = \sqrt{x}$$
De modo que
$$f = w \circ v \circ u, \qquad f(x) = w(v(u(x))) = \sqrt{\frac{1}{x^2+2}}$$
:::

**Ejercicio 24** (Examen 2 - C)
Escriba cada una de las siguientes funciones como la composición de dos o más funciones más simples:

a) $\sqrt{x^3-1}$
b) $(3x-4)^3$
c) $\dfrac{1}{x^2-1}$
d) $x$

:::{dropdown} Solución
**a)** Con $u(x)=x^3-1$ y $w(x)=\sqrt{x}$: $f = w\circ u$, es decir $f(x) = w(u(x)) = \sqrt{x^3-1}$.

**b)** Con $u(x)=3x-4$ y $w(x)=x^3$: $f = w\circ u$, es decir $f(x)=(3x-4)^3$.

**c)** Con $u(x)=x^2-1$ y $w(x)=\dfrac1x$: $f=w\circ u$, es decir $f(x) = \dfrac{1}{x^2-1}$.

**d)** La función identidad se puede escribir como la composición de una función y su inversa, por ejemplo con $u(x)=x^3$ y $w(x)=\sqrt[3]{x}$:
$$(w\circ u)(x) = \sqrt[3]{x^3} = x$$
:::

**Ejercicio 25** (Examen 2 - D)
Para los siguientes pares de funciones $f$ y $g$, halle las funciones compuestas $f\circ g$ y $g\circ f$, junto con sus dominios.

a) $f = 2x-5$, $g = x^2-3x$
b) $f = \sqrt{3x-1}$, $g = x^2$
c) $f = \sqrt{3x-1}$, $g = \dfrac{1}{x}$
d) $f = \sqrt{3x-1}$, $g = \dfrac{x^2+1}{x}$
e) $f = x^2-3$, $g = |x|$

:::{dropdown} Solución
**a)**
$$(f\circ g)(x) = 2(x^2-3x)-5 = 2x^2-6x-5, \quad \text{dominio } \mathbb{R}$$
$$(g\circ f)(x) = (2x-5)^2-3(2x-5) = 4x^2-20x+25-6x+15 = 4x^2-26x+40, \quad \text{dominio } \mathbb{R}$$

**b)**
$$(f\circ g)(x) = \sqrt{3x^2-1}$$
Se necesita $3x^2-1\ge0 \iff x^2\ge\frac13 \iff |x|\ge\frac{1}{\sqrt3}$. Dominio: $\left(-\infty,-\frac{\sqrt3}{3}\right]\cup\left[\frac{\sqrt3}{3},\infty\right)$.
$$(g\circ f)(x) = \left(\sqrt{3x-1}\right)^2 = 3x-1$$
Aunque la fórmula $3x-1$ está definida en todo $\mathbb{R}$, para poder aplicar $f$ primero se necesita $3x-1\ge0$. Dominio: $x\ge\frac13$.

**c)**
$$(f\circ g)(x) = \sqrt{\frac{3}{x}-1} = \sqrt{\frac{3-x}{x}}$$
Se necesita $x\ne0$ y $\dfrac{3-x}{x}\ge0$. Analizando signos, esto ocurre para $0<x\le3$.
$$(g\circ f)(x) = \frac{1}{\sqrt{3x-1}}$$
Se necesita $3x-1>0$ (estrictamente, pues está en el denominador), es decir $x>\frac13$.

**d)**
$$(f\circ g)(x) = \sqrt{3\cdot\frac{x^2+1}{x}-1} = \sqrt{\frac{3x^2-x+3}{x}}$$
El numerador $3x^2-x+3$ tiene discriminante $1-36=-35<0$, por lo que siempre es positivo. Entonces el signo de la fracción depende solo de $x$, y se necesita $x>0$. Dominio: $x>0$.
$$(g\circ f)(x) = \frac{(3x-1)+1}{\sqrt{3x-1}} = \frac{3x}{\sqrt{3x-1}}$$
Se necesita $3x-1>0$, es decir $x>\frac13$.

**e)**
$$(f\circ g)(x) = |x|^2-3 = x^2-3, \quad \text{dominio } \mathbb{R}$$
$$(g\circ f)(x) = |x^2-3|, \quad \text{dominio } \mathbb{R}$$
:::

---

*Ejercicios de imagen inversa, función inversa y composición de funciones tomados de los Exámenes 2 (2025-2, versiones A, B, C y D) del curso Matemáticas Discretas y sus Aplicaciones, PUJ.*
