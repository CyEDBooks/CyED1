---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Unidad 2: Conjuntos"
---

# Unidad 2: Conjuntos

## Definición de conjunto

Un conjunto es una colección de objetos. Algunos ejemplos:

- Conjunto de vocales del alfabeto

$$
A=\{a,e,i,o,u\}
$$

- Conjunto de enteros positivos menores que 100

$$
B=\{1,2,3,4,\dots,99\}
$$

- Conjunto de números naturales

$$
C=\{0,1,2,3,4,5,6,\dots\}
$$

- Conjunto de operadores aritméticos conmutativos

$$
D=\{+,\times\}
$$

**¿Los conjuntos $A$ y $B$ son iguales?**

$$
A=\{a,e,i,o,u\}
$$

$$
B=\{u,o,i,e,a\}
$$

:::{dropdown} Observación
Un conjunto es una colección desordenada de objetos.
:::

**¿Los conjuntos $A$ y $B$ son iguales?**

$$
A=\{a,a,a,a,e,e,e,e,i,o,u\}
$$

$$
B=\{a,e,i,o,u\}
$$

:::{dropdown} Observación
Dos conjuntos son iguales si tienen los mismos elementos sin importar la cantidad.
:::

**Conjunto vacío**

Representa el conjunto que no tiene elementos, se puede expresar de las dos siguientes maneras:

- $\{\}$
- $\varnothing$

---

### Conjunto

**Definición:** Es una colección desordenada de objetos.

**Ejemplos:**
- $V = \{a,e,i,o,u\}$, el conjunto de las vocales.
- $\mathbb{N} = \{0,1,2,3,\dots\}$, el conjunto de los números naturales.
- $\mathbb{Z} = \{ \dots, -3,-2,-1,0,1,2,3,\dots\}$, el conjunto de los números enteros.

### Elemento de un conjunto

**Definición:** Los objetos de un conjunto se llaman también *elementos* o *miembros* del conjunto. Se dice que un conjunto contiene a sus elementos. Cuando un objeto es un elemento de un conjunto, se dice que **pertenece** a dicho conjunto.

**Ejemplos:**
- $a \in \{ a,e,i,o,u \}$,
- $-1 \notin \mathbb{N}$
- $0 \in \mathbb{Z}$

### Representación de conjuntos

Se puede representar por **extensión** o por **comprensión**.

**Ejemplos:**
- **Por extensión:**
$a \in \{ a,e,i,o,u \}$

- **Por comprensión:**
$\{ x \mid x \text{ es una vocal} \}$

### Igualdad entre conjuntos

**Definición:** Dos conjuntos $A$ y $B$ son iguales si, y sólo si, tienen los mismos elementos.

**Axioma de extensionalidad:** Si todo elemento de $A$ pertenece a $B$ y todo elemento de $B$ pertenece a $A$, entonces los conjuntos son iguales. Escribimos:
$A = B$

**Ejemplos:**
- $\{1,2,3\} = \{3,2,1\}$
- $\{1,2,3\} = \{1,1,1,1,2,2,2,3,3\}$

**Nota:** Para probar que dos conjuntos son iguales, se debe demostrar que:
$A \subseteq B$ y $B \subseteq A$

### Diagrama de Venn

**Definición:** Representación gráfica de conjuntos.

**Ejemplo:**

:::{image} images/venn-numbers.png
:alt: Diagrama de Venn
:width: 100%
:::

---

**Determine si los siguientes conjuntos son iguales:**

- $\{1,3,3,3,3,3,5,5,5\}$ y $\{5,3,1\}$

- $\{\{1\}\}$ y $\{1\}$

- $\{\{1,1,1,1\},1,1,1,1\}$ y $\{1,\{1\}\}$

- $\{\}$ y $\{\varnothing,\{\}\}$

- $\{\varnothing\}$ y $\{\{\},\varnothing\}$

- $\{x \mid x \text{ es un entero positivo menor que 5}\}$ y $\{1,2,3,4\}$

:::{dropdown} Respuesta
- $\{1,3,3,3,3,3,5,5,5\}$ y $\{5,3,1\}$, **sí**

- $\{\{1\}\}$ y $\{1\}$, **no**

- $\{\{1,1,1,1\},1,1,1,1\}$ y $\{1,\{1\}\}$, **sí**

- $\{\}$ y $\{\varnothing,\{\}\}$, **no**

- $\{\varnothing\}$ y $\{\{\},\varnothing\}$, **sí**

- $\{x \mid x \text{ es un entero positivo menor que 5}\}$ y $\{1,2,3,4\}$, **sí**
:::

**Pertenencia sobre conjuntos**

- $x \in A$ para indicar que el elemento $x$ pertenece al conjunto $A$

- $x \notin A$ para el caso contrario

Sea $A=\{1,2,\{3,4\},5,\{5,6\}\}$ responda falso o verdadero:

- $1 \in A$
- $\{3,4\} \in A$
- $\varnothing \in A$
- $5 \in A$
- $\{5\} \in A$
- $\{3,4,5\} \in A$

:::{dropdown} Respuesta
- $1 \in A$, **verdadero**
- $\{3,4\} \in A$, **verdadero**
- $\varnothing \in A$, **falso**
- $5 \in A$, **verdadero**
- $\{5\} \in A$, **falso**
- $\{3,4,5\} \in A$, **falso**
:::

Sea $A=\{1,2,\{3,4\},5,\{5,6\}\}$ responda falso o verdadero:

- $\{1,2\} \in A$
- $\{5,6\} \in A$
- $4 \in A$
- $\{\} \in A$

:::{dropdown} Respuesta
- $\{1,2\} \in A$, **falso**
- $\{5,6\} \in A$, **verdadero**
- $4 \in A$, **falso**
- $\{\} \in A$, **falso**
:::

## Subconjunto y subconjunto propio

**Subconjunto $\subseteq$**

El conjunto $A$ es subconjunto de $B$, $A \subseteq B$, si y solo si todo elemento de $A$ es también un elemento de $B$.

- $\{1,2\} \subseteq \{1,2,3,4,5\}$

- $\{1,2,6\} \nsubseteq \{1,2,3,4,5\}$

**Propiedad**
- Para cualquier conjunto $S$, se cumple que $\varnothing \subseteq S$.
- Para cualquier conjunto $S$, se cumple que $S \subseteq S$.

**Subconjunto propio $\subset$**

El conjunto $A$ es **subconjunto propio** de $B$, $A \subset B$, si y solo si

$$
A \subseteq B \;\text{ y }\; A \neq B.
$$

Sean $P=\{1,2\}$, $Q=\{1,2,3\}$, $R=\{1,2,3\}$, se cumple:

- $P \subseteq R$ y $P \subset R$

- $Q \subseteq R$ pero $Q \not\subset R$

---

### Relación de inclusión

**Definición:** Se dice que el conjunto $A$ es subconjunto de $B$, denotado por $A \subseteq B$, si todo elemento de $A$ es elemento de $B$.

**Ejemplos:**
- $\{ e,u \} \subseteq \{ a,e,i,o,u \}$
- $\{ -1,0,1 \} \subseteq \mathbb{Z}$

### Conjunto vacío

**Definición:** En ocasiones, existen en matemáticas conjuntos que carecen de elementos. A este conjunto se le denomina **Conjunto vacío**. Se puede simbolizar como $\{\}$ o $\emptyset$.

La existencia de este conjunto se establece como un axioma.

**Axioma del conjunto vacío:** Existe un conjunto que no tiene elementos.

### Subconjuntos

**Teorema:** Para cualquier conjunto $S$ se cumple:
- $\emptyset \subseteq S$
- $S \subseteq S$

---

**Determine si cada una de las siguientes expresiones es falsa o verdadera:**

- $x \in \{x\}$

- $\{x,y\} \subseteq \{x\}$

- $\{x\} \subset \{x\}$

- $\{x\} \in \{x\}$

- $\{x\} \in \{\{x\}, y, z\}$

- $\varnothing \subseteq \{x\}$

- $\varnothing \in \{x\}$

- $\varnothing \subset \{x\}$

:::{dropdown} Respuesta
- $x \in \{x\}$, **verdadero**

- $\{x,y\} \subseteq \{x\}$, **falso**

- $\{x\} \subset \{x\}$, **falso**

- $\{x\} \in \{x\}$, **falso**

- $\{x\} \in \{\{x\}, y, z\}$, **verdadero**

- $\varnothing \subseteq \{x\}$, **verdadero**

- $\varnothing \in \{x\}$, **falso**

- $\varnothing \subset \{x\}$, **verdadero**
:::

**Determine si cada una de las siguientes expresiones es falsa o verdadera:**

- $0 \in \varnothing$

- $\varnothing \in \{0\}$

- $\{0\} \subset \varnothing$

- $\varnothing \subset \{0\}$

- $\{0\} \in \{0,\{0,0\}\}$

- $\{0\} \subset \{0\}$

- $\{0\} \subseteq \{0\}$

:::{dropdown} Respuesta
- $0 \in \varnothing$, **falso**

- $\varnothing \in \{0\}$, **falso**

- $\{0\} \subset \varnothing$, **falso**

- $\varnothing \subset \{0\}$, **verdadero**

- $\{0\} \in \{0,\{0,0\}\}$, **verdadero**

- $\{0\} \subset \{0\}$, **falso**

- $\{0\} \subseteq \{0\}$, **verdadero**
:::

## Cardinalidad de un conjunto

**Cardinalidad de un conjunto $|S|$**

La cardinalidad de un conjunto $S$, denotado por $|S|$, indica la cantidad de elementos diferentes.

Por ejemplo:

- Para $A=\{3,3,3,3,1,1,1,2,2,2\}$, se tiene $|A|=3$

- Para $A=\{1,2,3,\{4,5\}\}$, se tiene $|A|=4$

- Para $A=\varnothing$, se tiene $|A|=0$

**Indique la cardinalidad de los siguientes conjuntos:**

- $\{x \mid x \text{ es un entero positivo impar menor que 10}\}$

- $\{a\}$

- $\{\{a,b\}\}$

- $\{a,\{a\}\}$

- $\{a,a,\{a,a\},\{a,a,a\}\}$

:::{dropdown} Respuesta
- $\{x \mid x \text{ es un entero positivo impar menor que 10}\}$, **5**

- $\{a\}$, **1**

- $\{\{a,b\}\}$, **1**

- $\{a,\{a\}\}$, **2**

- $\{a,a,\{a,a\},\{a,a,a\}\}$, **2**
:::

**Indique la cardinalidad de los siguientes conjuntos:**

- $\{a,\{a\},\{a,\{a\}\}\}$

- $\{3,\varnothing\}$

- $\{\varnothing\}$

- $\{\varnothing,\varnothing,\varnothing,\{\}\}$

:::{dropdown} Respuesta
- $\{a,\{a\},\{a,\{a\}\}\}$, **3**

- $\{3,\varnothing\}$, **2**

- $\{\varnothing\}$, **1**

- $\{\varnothing,\varnothing,\varnothing,\{\}\}$, **1**
:::

---

### Cardinalidad

**Definición:** El número de elementos distintos de un conjunto $A$ se denomina **Cardinalidad** de $A$. Se simboliza como $\#(A)$, $Car(A)$ o $|A|$.

**Ejemplos:**
- $| \{ a,e,i,o,u \} | = 5$
- $| \{ x \mid x \text{ es un dígito} \} | = 10$
- $|\emptyset| = 0$

**Definición adicional:** Un conjunto **finito** es un conjunto con una cantidad finita de elementos. De lo contrario, se denomina conjunto **infinito**.

---

## Producto cartesiano

**Producto cartesiano $A \times B$**

Dados dos conjuntos $A$ y $B$, se define:

$$
A \times B = \{(a,b)\mid a\in A \land b\in B\}
$$

Sea:

$$
A=\{1,2,3\}
\qquad
B=\{a,b\}
$$

Entonces:

$$
\begin{aligned}
A \times B = \{&(1,a),(1,b),\\
               &(2,a),(2,b),\\
               &(3,a),(3,b)\}
\end{aligned}
$$

$$
\begin{aligned}
B \times A = \{&(a,1),(a,2),(a,3),\\
               &(b,1),(b,2),(b,3)\}
\end{aligned}
$$

**Cardinalidad**

$$
|A \times B| = |A|\cdot|B|
$$

## Conjunto potencia

**Conjunto potencia $P(S)$**

Dado un conjunto $S$, el conjunto potencia es aquel que tiene todos los subconjuntos de $S$.

Dado:

$$
A=\{1,2,3\}
$$

se tiene:

$$
P(A)=
\{\varnothing,\{1\},\{2\},\{3\},
\{1,2\},\{1,3\},\{2,3\},
\{1,2,3\}\}
$$

**Cardinalidad de Conjunto potencia**

En general, dado un conjunto $A$ con $n$ elementos, el conjunto $P(A)$ tiene $2^n$ elementos.

Sea

$$
S=\{1,\{2,3\},4\}
$$

Su conjunto potencia es:

$$
\begin{aligned}
P(S)=\{&
\varnothing,\{1\},\{\{2,3\}\},\{4\},\\
&\{1,\{2,3\}\},\{1,4\},\{\{2,3\},4\},\\
&\{1,\{2,3\},4\}
\}
\end{aligned}
$$

Sea

$$
S=\varnothing
$$

Su conjunto potencia es:

$$
P(S)=\{\varnothing\}
$$

Encuentre el siguiente conjunto:

$$
P(P(\varnothing))
$$

Primero:

$$
P(\varnothing)=\{\varnothing\}
$$

Luego:

$$
P(P(\varnothing))
=
P(\{\varnothing\})
=
\{\varnothing,\{\varnothing\}\}
$$

Encuentre los siguientes conjuntos potencia:

- $P(\{\{a,c\},\{a,b\}\})$
- $P(\{1,2,3,4\})$

$$
P(\{\{a,c\},\{a,b\}\})
=
\{\varnothing,\{\{a,c\}\},\{\{a,b\}\},\{\{a,c\},\{a,b\}\}\}
$$

$$
\begin{aligned}
P(\{1,2,3,4\})=\{&
\varnothing,\{1\},\{2\},\{3\},\{4\},\\
&\{1,2\},\{1,3\},\{1,4\},\{2,3\},\{2,4\},\{3,4\},\\
&\{1,2,3\},\{1,2,4\},\{1,3,4\},\{2,3,4\},\\
&\{1,2,3,4\}
\}
\end{aligned}
$$

**Determine si cada una de las siguientes sentencias es falsa o verdadera:**

- $\{\varnothing\} \subseteq P(\{\varnothing\})$

- $\{\varnothing,\{\varnothing\}\} \subseteq P(P(\{\varnothing\}))$

- $|\{a,b,c\}\times\{1,2\}| \;<\; |P(\{a,b\})|$

:::{dropdown} Respuesta
$$
\{\varnothing\} \subseteq \{\varnothing,\{\varnothing\}\}
\quad \textbf{verdadero}
$$

$$
\{\varnothing,\{\varnothing\}\}
\subseteq
\{\varnothing,\{\varnothing\},\{\{\varnothing\}\},\{\varnothing,\{\varnothing\}\}\}
\quad \textbf{verdadero}
$$

$$
|\{a,b,c\}\times\{1,2\}| = 6
\quad\text{y}\quad
|P(\{a,b\})| = 4
$$

$$
6 < 4
\quad \textbf{falso}
$$
:::

## Operaciones con conjuntos

Las operaciones fundamentales entre conjuntos son:

- Unión
- Intersección
- Diferencia
- Complemento

Se definen de forma compacta como:

$$
\begin{aligned}
A\cup B &= \{x \mid x\in A \lor x\in B\} \\
A\cap B &= \{x \mid x\in A \land x\in B\} \\
A-B     &= \{x \mid x\in A \land x\notin B\} \\
\overline{A} &= \{x \mid x\notin A\}
\end{aligned}
$$

Como ejemplo, considere:

$$
U=\{1,2,3,4,5,6,7,8,9\}
\qquad
A=\{1,2,3,5,9\}
\qquad
B=\{3,7,9\}
$$

Dados

$$
A=\{1,2,3,5,9\}, \quad
B=\{3,7,9\}, \quad
U=\{1,2,3,4,5,6,7,8,9\}
$$

indique los resultados de las siguientes operaciones:

- $\overline{A\cup B}\;\cap\;\overline{(B-A)}$
- $(A\cap \overline{B})\;\cup\;(B\cap \overline{A})$

Se tiene:

$$
\overline{A\cup B}\;\cap\;\overline{(B-A)}
=
\{4,6,8\}\cap\{1,2,3,4,5,6,8,9\}
=
\{4,6,8\}
$$

$$
(A\cap \overline{B})\;\cup\;(B\cap \overline{A})
=
\{1,2,5\}\cup\{7\}
=
\{1,2,5,7\}
$$

Dados

$$
A=\{a,b,c,d,e\},\;
B=\{a,b,c,d,e,f,g,h\},\;
U=\{a,b,c,d,e,f,g,h,i,j,k\}
$$

encuentre:

- $\overline{A\cap B}$
- $\overline{B-A}\cup(A-B)$
- $\overline{(A-B)}-(A\cup B)$
- $\overline{(B\cap A)\cup(B-A)}$

Los resultados son:

$$
\overline{A\cap B}=\{f,g,h,i,j,k\}
$$

$$
\overline{B-A}\cup(A-B)=\{a,b,c,d,e,i,j,k\} \cup \varnothing = \{a,b,c,d,e,i,j,k\}
$$

$$
\overline{(A-B)}-(A\cup B)= \{a,b,c,d,e,f,g,h,i,j,k\} -  \{a,b,c,d,e,f,g,h\} = \{i,j,k\}
$$

$$
\overline{(B\cap A)\cup(B-A)}=\{i,j,k\}
$$

Dados

$$
A=\{1,3,5,7,8,9\},\;
B=\{2,4,5,6\},\;
U=\{1,2,3,4,5,6,7,8,9,10\}
$$

encuentre:

- $\overline{A-B}\cap \overline{A}$
- $(B\cap A)\cup \overline{(A\cup B)}$
- $\overline{(A\cap B)}\cap (B-A)$

:::{dropdown} Respuesta
Los resultados son:

$$
A-B=\{1,3,7,8,9\}
\qquad
\overline{A-B}=\{2,4,5,6,10\}
\qquad
\overline{A}=\{2,4,6,10\}
$$

$$
\overline{A-B}\cap \overline{A}
=\{2,4,6,10\}
$$

$$
B\cap A=\{5\}
\qquad
A\cup B=\{1,2,3,4,5,6,7,8,9\}
\qquad
\overline{(A\cup B)}=\{10\}
$$

$$
(B\cap A)\cup \overline{(A\cup B)}
=\{5,10\}
$$

$$
\overline{A\cap B}=\{1,2,3,4,6,7,8,9,10\}
\qquad
B-A=\{2,4,6\}
$$

$$
\overline{(A\cap B)}\cap (B-A)
=\{2,4,6\}
$$
:::

Dados

$$
A=\{a,b,c\},\;
B=\{b,d\},\;
U=\{a,b,c,d,e,f\}
$$

encuentre y compare:

- $\overline{A\cup B}$, $\overline{A}\cap \overline{B}$
- $\overline{A\cap B}$, $\overline{A}\cup \overline{B}$

:::{dropdown} Respuesta
Para la primera comparación:

$$
A\cup B=\{a,b,c,d\}
\qquad
\overline{A\cup B}=\{e,f\}
$$

$$
\overline{A}=\{d,e,f\},\quad
\overline{B}=\{a,c,e,f\}
$$

$$
\overline{A}\cap \overline{B}=\{e,f\}
$$

$$
\textbf{Ambos son } \{e,f\}
$$

Para la segunda comparación:

$$
A\cap B=\{b\}
\qquad
\overline{A\cap B}=\{a,c,d,e,f\}
$$

$$
\overline{A}\cup \overline{B}
=\{a,c,d,e,f\}
$$

$$
\textbf{Ambos son } \{a,c,d,e,f\}
$$
:::

## Identidades entre conjuntos

Las siguientes tablas resumen las identidades más importantes entre conjuntos.

| Identidad | Nombre |
|---|---|
| $\overline{(A \cup B)} = \overline{A} \cap \overline{B}$ | Leyes de De Morgan |
| $\overline{(A \cap B)} = \overline{A} \cup \overline{B}$ | |
| $A \cup (A \cap B) = A$ | Leyes de absorción |
| $A \cap (A \cup B) = A$ | |
| $A \cup \overline{A} = \; U$ | Leyes de complemento |
| $A \cap \overline{A} = \; \varnothing$ | |

| Identidad | Nombre |
|---|---|
| $A \cup \varnothing = \; A$ | Leyes de identidad |
| $A \cap U = \; A$ | |
| $A \cup U = U$ | Leyes de dominación |
| $A \cap \varnothing = \varnothing$ | |
| $A \cup A = A$ | Leyes de idempotencia |
| $A \cap A = A$ | |
| $\overline{\overline{A}} = A$ | Ley de complementación |

| Identidad | Nombre |
|---|---|
| $A \cup B = B \cup A$ | Leyes conmutativas |
| $A \cap B = B \cap A$ | |
| $A \cup (B \cup C) = (A \cup B) \cup C$ | Leyes asociativas |
| $A \cap (B \cap C) = (A \cap B) \cap C$ | |
| $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ | Leyes distributivas |
| $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$ | |

**Cómo probar identidades**

Se tienen dos métodos:

- Construir una tabla de pertenencia

- Utilizar la notación de conjuntos y las equivalencias lógicas

**Tabla de pertenencia**

Se considera cada combinación de conjuntos en los que un elemento puede pertenecer y se verifica que los elementos en la misma combinación de conjuntos pertenecen a ambos conjuntos en la identidad.

**Probar** $\overline{A \cap B} = \overline{A} \cup \overline{B}$

$1$ representa $x\in$ conjunto, $0$ representa $x\notin$ conjunto.

| $A$ | $B$ | $\overline{A}$ | $\overline{B}$ | $A\cap B$ | $\overline{A\cap B}$ | $\overline{A}\cup\overline{B}$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| 0 | 0 | 1 | 1 | 0 | 1 | 1 |

**Las columnas coinciden $\Rightarrow$ la identidad es verdadera.**

**Probar**

$$
\overline{A \cup (\overline{A}\cap B)}
=
\overline{A}\cap (A\cup \overline{B})
$$

| $A$ | $B$ | $\overline A$ | $\overline B$ | $\overline A\cap B$ | $A\cup(\overline A\cap B)$ | $\overline{A\cup(\overline A\cap B)}$ | $A\cup \overline B$ | $\overline A\cap(A\cup\overline B)$ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 |

**Las columnas coinciden $\Rightarrow$ la identidad es verdadera.**

**Complete la tabla para** $(A-B)$

| $A$ | $B$ | $A-B$ |
|---|---|---|
| 1 | 1 | 0 |
| 1 | 0 | 1 |
| 0 | 1 | 0 |
| 0 | 0 | 0 |

**Recordemos:** $A-B = A \cap \overline{B}$

**Probar** $A \cap (B-A) = \varnothing$

:::{dropdown} Respuesta
| $A$ | $B$ | $B-A$ | $A\cap(B-A)$ |
|---|---|---|---|
| 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 0 | 0 | 0 | 0 |

**La columna final es todo 0 $\Rightarrow$ el resultado es $\varnothing$.**
:::

**Probar** $A \cup (B-A) = A \cup B$

:::{dropdown} Respuesta
| $A$ | $B$ | $B-A$ | $A\cup(B-A)$ | $A\cup B$ |
|---|---|---|---|---|
| 1 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 1 | 1 |
| 0 | 0 | 0 | 0 | 0 |

**Las columnas coinciden $\Rightarrow$ la identidad es verdadera.**
:::

**Ejercicio**

Probar que

$$
\overline{\overline{A} \cap \overline{(B - A)}}
=
\overline{\overline{A} \cap \overline{B}}
$$

**Cómo probar identidades**

Se tienen dos métodos:

- Construir una tabla de pertenencia.

- Utilizar la notación de conjuntos y las equivalencias lógicas.

A continuación, un resumen formal de las operaciones fundamentales:

| Operación | Definición formal |
|---|---|
| $A \cup B$ | $\{\, x \mid x \in A \;\vee\; x \in B \,\}$ |
| $A \cap B$ | $\{\, x \mid x \in A \;\wedge\; x \in B \,\}$ |
| $A - B$ | $\{\, x \mid x \in A \;\wedge\; x \notin B \,\}$ |
| $\overline{A}$ | $\{\, x \mid x \notin A \,\}$ |

**Probar** $\overline{A \cap B} = \overline{A} \cup \overline{B}$

$$
\begin{align*}
\overline{A \cap B}
&= \{\, x \mid x \notin A \cap B \,\} \\[6pt]
&= \{\, x \mid \neg(x \in A \cap B) \,\} \\[6pt]
&= \{\, x \mid \neg(x \in A \wedge x \in B) \,\} \\[6pt]
&= \{\, x \mid \neg(x \in A) \vee \neg(x \in B) \,\} \\[6pt]
&= \{\, x \mid (x \notin A) \vee (x \notin B) \,\} \\[6pt]
&= \{\, x \mid (x \in \overline{A}) \vee (x \in \overline{B}) \,\} \\[6pt]
&= \overline{A} \cup \overline{B}
\end{align*}
$$

**Probar**

$$
\overline{A \cup (B \cap C)} = \overline{A} \cap \overline{(B \cap C)}
$$

$$
\begin{align*}
\overline{A \cup (B \cap C)}
&= \{\, x \mid x \notin A \cup (B \cap C) \,\} \\
&= \{\, x \mid \neg(x \in A \cup (B \cap C)) \,\} \\
&= \{\, x \mid \neg[(x \in A) \vee (x \in (B \cap C))] \,\} \\
&= \{\, x \mid \neg(x \in A) \wedge \neg(x \in (B \cap C)) \,\} \\
&= \{\, x \mid (x \notin A) \wedge (x \notin (B \cap C)) \,\} \\
&= \{\, x \mid (x \in \overline{A}) \wedge (x \in \overline{(B \cap C)}) \,\} \\
&= \overline{A} \cap \overline{(B \cap C)}
\end{align*}
$$

**Probar:**

$$
A \cap (B - A) = \varnothing
$$

:::{dropdown} Demostración
$$
\begin{align*}
A \cap (B - A)
&= \{x \mid x \in A \cap (B - A)\} \\[4pt]
&= \{x \mid (x \in A) \wedge (x \in B - A)\} \\[4pt]
&= \{x \mid (x \in A) \wedge (x \in B \wedge x \notin A)\} \\[4pt]
&= \{x \mid (x \in A) \wedge (x \in B) \wedge (x \notin A)\} \\[4pt]
&= \{x \mid ((x \in A) \wedge (x \notin A)) \wedge (x \in B)\} \\[4pt]
&= \{x \mid (x \in \varnothing) \wedge (x \in B)\} \\[4pt]
&= \{x \mid x \in \varnothing\} \\[4pt]
&= \varnothing
\end{align*}
$$
:::

**Probar**

$$
\overline{A} \cap \overline{(B-A)} = \overline{A} \cap \overline{B}
$$

:::{dropdown} Demostración
$$
\begin{align*}
\overline{A} \cap \overline{(B-A)}
&= \{x \mid x \in \overline{A} \cap \overline{(B-A)}\} \\[4pt]
&= \{x \mid x \in \overline{A} \land x \in \overline{(B-A)}\} \\[4pt]
&= \{x \mid x \in \overline{A} \land \neg(x \in (B-A))\} \\[4pt]
&= \{x \mid x \in \overline{A} \land \neg(x \in B \land x \notin A)\} \\[4pt]
&= \{x \mid x \in \overline{A} \land [\neg(x \in B) \lor \neg(x \notin A)]\} \\[4pt]
&= \{x \mid x \in \overline{A} \land [\neg(x \in B) \lor x \in A]\} \\[4pt]
&= \{x \mid (x \in \overline{A} \land \neg(x \in B))
\lor (x \in \overline{A} \land x \in A)\} \\[4pt]
&= \{x \mid (x \in \overline{A} \land \neg(x \in B))
\lor \varnothing\} \\[4pt]
&= \{x \mid x \in \overline{A} \land \neg(x \in B)\} \\[4pt]
&= \{x \mid x \in \overline{A} \land x \in \overline{B}\}
= \overline{A} \cap \overline{B}
\end{align*}
$$
:::

**Probar** $A \cup (B - A) = A \cup B$

:::{dropdown} Demostración
$$
\begin{align*}
A \cup (B - A)
&= \{x \mid x \in A \cup (B - A)\} \\
&= \{x \mid (x \in A) \vee (x \in (B - A))\} \\
&= \{x \mid (x \in A) \vee [(x \in B) \wedge (x \notin A)]\} \\
&= \{x \mid [(x \in A) \vee (x \in B)]
\wedge [(x \in A) \vee (x \notin A)]\} \\
&= \{x \mid [(x \in A) \vee (x \in B)]
\wedge (x \in U)\} \\
&= \{x \mid (x \in A) \vee (x \in B)\} \\
&= A \cup B
\end{align*}
$$
:::

## Conjuntos en Java (Interfaz `Set`)

La interfaz `Set` pertenece al **Java Collections Framework** y representa una colección que:

- No permite elementos duplicados.
- No garantiza un orden específico (esto depende de la implementación).
- Modela el concepto matemático de conjunto.

`Set` está en el paquete:

```java
import java.util.Set;
```

### Jerarquía de la interfaz `Set`

La interfaz `Set` extiende `Collection`, y tiene varias implementaciones concretas.

![Jerarquía Set](https://www.programiz.com/sites/tutorial2program/files/java-set-implementation.png)

Nos centraremos en tres implementaciones principales:

- `HashSet`
- `LinkedHashSet`
- `TreeSet`

### ¿Qué es `Set`?

`Set<E>` es una interfaz genérica que define el comportamiento de un conjunto de elementos únicos.

Ejemplo básico:

```java
import java.util.Set;
import java.util.HashSet;

public class Main {
    public static void main(String[] args) {

        Set<Integer> numbers = new HashSet<>();

        numbers.add(1);
        numbers.add(2);
        numbers.add(2);

        System.out.println(numbers);
    }
}
```

Salida posible:

```
[1, 2]
```

El segundo `2` no se agrega porque los conjuntos no permiten duplicados.

### HashSet

**Características**

- Implementado mediante **tabla hash**.
- No mantiene orden de inserción.
- Permite un elemento `null`.
- Operaciones `add`, `remove`, `contains` son O(1) promedio.

**Instanciación**

```java
Set<String> names = new HashSet<>();
```

**Ejemplo**

```java
Set<String> names = new HashSet<>();

names.add("Ana");
names.add("Luis");
names.add("Carlos");
names.add("Ana");

System.out.println(names);
```

El orden puede variar:

```
[Luis, Ana, Carlos]
```

**Caso de uso típico**

- Cuando solo importa la unicidad.
- Cuando se requiere máxima eficiencia.
- Cuando el orden no es relevante.

### LinkedHashSet

**Características**

- Mantiene el **orden de inserción**.
- Basado en hash + lista enlazada.
- Permite un elemento `null`.
- Rendimiento ligeramente inferior a `HashSet`.

**Instanciación**

```java
Set<String> names = new LinkedHashSet<>();
```

**Ejemplo**

```java
Set<String> names = new LinkedHashSet<>();

names.add("Ana");
names.add("Luis");
names.add("Carlos");

System.out.println(names);
```

Salida:

```
[Ana, Luis, Carlos]
```

Respeta el orden en que fueron agregados.

**Caso de uso típico**

- Cuando se necesita unicidad y orden de inserción.
- Para mostrar resultados en el mismo orden en que se agregaron.

### TreeSet

**Características**

- Implementado como **árbol rojo-negro**.
- Mantiene los elementos **ordenados naturalmente**.
- No permite `null`.
- Operaciones son O(log n).

**Instanciación**

```java
Set<Integer> numbers = new TreeSet<>();
```

**Ejemplo**

```java
Set<Integer> numbers = new TreeSet<>();

numbers.add(5);
numbers.add(1);
numbers.add(3);

System.out.println(numbers);
```

Salida:

```
[1, 3, 5]
```

Siempre ordenado.

También puede usar un `Comparator` personalizado:

```java
Set<String> names = new TreeSet<>((a, b) -> b.compareTo(a));
```

Esto ordena en orden descendente.

**Caso de uso típico**

- Cuando se necesita mantener los datos ordenados.
- Cuando se requieren operaciones como `first()`, `last()`, `higher()`, `lower()`.

### Operaciones comunes en los tres

Estas operaciones funcionan igual en `HashSet`, `LinkedHashSet` y `TreeSet`:

```java
set.add(element);        // Agregar
set.remove(element);     // Eliminar
set.contains(element);   // Si el conjunto tiene el elemento o no
set.size();              // Tamaño
set.isEmpty();           // Si el conjunto es vacío o no
set.clear();             // Limpiar (volver un conjunto vacío)
```

### Operaciones tipo teoría de conjuntos

Java no tiene métodos directos para unión, intersección o diferencia, pero se pueden simular:

**Unión**

```java
Set<Integer> a = new HashSet<>(Set.of(1,2,3));
Set<Integer> b = new HashSet<>(Set.of(3,4,5));

a.addAll(b);

System.out.println(a);  //[1,2,3,4,5]
```

**Intersección**

```java
Set<Integer> a = new HashSet<>(Set.of(1,2,3));
Set<Integer> b = new HashSet<>(Set.of(2,3,4));

a.retainAll(b);

System.out.println(a); //[2,3]
```

**Diferencia**

```java
Set<Integer> a = new HashSet<>(Set.of(1,2,3));
Set<Integer> b = new HashSet<>(Set.of(2,3));

a.removeAll(b);

System.out.println(a); // [1]
```

Estas operaciones funcionan igual en las tres implementaciones.

### Comparación resumida

| Implementación | Orden | Permite null | Complejidad promedio | Caso ideal |
|---|---|---|---|---|
| HashSet | No garantiza | Sí | O(1) | Máximo rendimiento |
| LinkedHashSet | Inserción | Sí | O(1) | Orden + unicidad |
| TreeSet | Orden natural | No | O(log n) | Datos ordenados |

### Conclusión

La interfaz `Set` modela conjuntos matemáticos en Java:

- No hay duplicados.
- El comportamiento específico depende de la implementación.
- `HashSet` prioriza rendimiento.
- `LinkedHashSet` mantiene orden de inserción.
- `TreeSet` mantiene orden natural.

Elegir la implementación correcta depende de:

- ¿Importa el orden?
- ¿Importa el rendimiento?
- ¿Se necesita ordenamiento automático?

---

### Interface Set

La interfaz Set es parte del framework de colecciones de Java (paquete java.util) y representa una colección de elementos únicos, es decir:

* No permite elementos duplicados — si intentas agregar un elemento que ya existe no se duplica.
* No define orden por índice; no puedes obtener elementos por posición como en una List.
* Está diseñada para modelar matemáticamente la idea de un conjunto.

La interfaz Set extiende Collection, por lo que hereda métodos como add, remove, contains, size, isEmpty y iterator. Las colecciones que implementan la interfaz Set en Java permiten almacenar elementos sin duplicados, pero varían significativamente en su comportamiento interno y eficiencia. La siguiente tabla compara tres implementaciones comunes —HashSet, LinkedHashSet y TreeSet— destacando sus principales características y diferencias para facilitar su elección según el caso de uso.

| Características | HashSet | LinkedHashSet | TreeSet |
|---|---|---|---|
| Permite duplicados | No | No | No |
| Ordena los elementos | No | Orden de inserción | Orden alfabético |
| Complejidad | O(1) | O(1) | O(log(n)) |
| Permite (null) | Sí, 1 valor | Sí, 1 valor | No |
| Estructura | Tabla Hash | Tabla Hash + Lista enlazada | Árbol Rojo-Negro |

#### Algunos métodos clave que verás en la interfaz:

* `boolean add(E e)` – Agrega un elemento si no está presente.
* `boolean remove(Object o)` – Elimina un elemento del conjunto.
* `boolean contains(Object o)` – Comprueba si el elemento está presente.
* `int size()` – Retorna el número de elementos (cardinalidad).
* `boolean isEmpty()` – Indica si el conjunto está vacío.
* `Iterator<E> iterator()` – Permite recorrer los elementos.

Además puedes usar métodos que operan con conjuntos completos, como:

* `addAll(Collection<? extends E>)` — unión
* `retainAll(Collection<?>)` — intersección
* `removeAll(Collection<?>)` — diferencia

#### Ejemplo

- [InterfaceSet](https://github.com/marlongv098/Estructuras/tree/master/2_Conjuntos_Funciones/1_Conjuntos/InterfaceSetUp)

#### Estructuras base

- [Tabla Hash](https://marlongv098.github.io/Libros/Estructuras_Discretas_I/3_Estructuras_NO_Recursivas/3_Generics/3_Diccionario/TablasHash.html)
- [Listas Enlazada](https://marlongv098.github.io/Libros/Estructuras_Discretas_I/3_Estructuras_NO_Recursivas/3_Generics/2_LinkedListPersonas/listaEnlazada2.html)

#### Árbol Rojo-Negro

Comparación del árbol Rojo-Negro con un árbol de búsqueda binaria.

| Características | BST | Árbol Rojo-Negro |
|---|---|---|
| Orden | I < R < D | I < R < D |
| Balanceo automático | No | Sí |
| Complejidad | O(N) en el peor caso (desbalanceado) | O(log(n)) |
| Coloración de nodos | No usa | Nodo Rojo-Negro |
| Uso en Java | `TreeSet` o `TreeMap` (No recomendado) | `TreeSet` o `TreeMap` (Sí recomendado) |

**¿Qué es un Árbol Rojo-Negro?**
Es un *árbol binario de búsqueda (BST) balanceado*, donde cada nodo tiene un color *rojo* o *negro* y sigue estas reglas:

- Cada nodo es *rojo* o *negro*.
- La *raíz* siempre es *negra*.
- Un *nodo rojo* no puede tener un hijo rojo (*no hay nodos rojos consecutivos*).
- Cada camino desde la *raíz hasta una hoja* tiene el mismo número de nodos negros (*propiedad de balanceo*).
- Si un *nodo es rojo*, sus *hijos deben ser negros*.
- Un *nodo negro* puede tener *hijos negros*.

Estas reglas garantizan que el árbol esté siempre balanceado, manteniendo la altura en **O(log N)**, lo que lo hace más eficiente que un BST simple.

**¿Cuándo usar un Árbol Rojo-Negro?**

- Cuando necesitas búsquedas, inserciones y eliminaciones rápidas (*O(log N)*).
- Cuando el *orden es importante* (como en `TreeSet` y `TreeMap`).
- Cuando quieres evitar que un *BST se desbalancee*.

**Conclusión**

Permitir que un *nodo negro tenga hijos negros* ayuda a:
- Mantener la propiedad de *balanceo* del árbol rojo-negro.
- Evitar que la altura crezca demasiado, garantizando *O(log N)*.
- Reducir la necesidad de demasiadas *rotaciones y recoloreos*.

En resumen, un *nodo negro puede tener hijos negros* porque es una estrategia clave para el balanceo del árbol y su eficiencia.

---

Continúa con los [ejercicios de Conjuntos](exercises.md).

*Material adaptado del material original de los profesores Oscar Bedoya y Marlon Gomez.*
