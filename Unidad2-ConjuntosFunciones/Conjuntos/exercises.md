---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Conjuntos: Ejercicios"
---

# Conjuntos: Ejercicios

Use esta página después de leer el [material de estudio de Conjuntos](index.md).

## Ejercicios

Estas actividades practican: pertenencia, subconjuntos, cardinalidad con operaciones,
producto cartesiano explícito, conjunto potencia y operaciones combinadas.

### A) Pertenencia y descripción por comprensión

Defina:

- $A = \lbrace x \in \mathbb{Z} \mid -4 \le x \le 6 \text{ y } x \text{ es par} \rbrace$
- $B = \lbrace -3,-1,0,2,4,7 \rbrace$

1. Escriba explícitamente el conjunto $A$.
2. Determine si:
   - $4 \in A$
   - $5 \in A$
   - $-1 \in B$
   - $6 \in B$
3. Calcule $A \cap B$.

:::{dropdown} Solución
1.
$A = \lbrace -4,-2,0,2,4,6 \rbrace$

2.
- $4 \in A$ → Verdadero
- $5 \in A$ → Falso
- $-1 \in B$ → Verdadero
- $6 \in B$ → Falso

3.
$A \cap B = \lbrace 0,2,4 \rbrace$
:::

### B) Subconjuntos

Defina:

- $C = \lbrace 1,2,3,4,5 \rbrace$
- $D = \lbrace 1,2,3,4,5 \rbrace$
- $E = \lbrace 2,4 \rbrace$
- $F = \lbrace 1,2,3,4,5,6 \rbrace$

Determine cuáles afirmaciones son verdaderas:

1. $C = D$
2. $E \subset C$
3. $E \subseteq D$
4. $C \subset F$
5. $F \subseteq C$

:::{dropdown} Solución
1. $C = D$ → Verdadero
2. $E \subset C$ → Verdadero
3. $E \subseteq D$ → Verdadero
4. $C \subset F$ → Verdadero
5. $F \subseteq C$ → Falso
:::

### C) Cardinalidad con operaciones

Sea:

- $G = \lbrace 1,2,3,4,5,6,7,8,9 \rbrace$
- $H = \lbrace 2,4,6,8,10,12 \rbrace$
- $I = \lbrace 1,3,5,7,9,11 \rbrace$

1. Calcule:
   - $|G \cap H|$
   - $|G \cup H|$
   - $|(G \cup H) \setminus I|$

2. Verifique que:
$|G \cup H| = |G| + |H| - |G \cap H|$

:::{dropdown} Solución
$G \cap H = \lbrace 2,4,6,8 \rbrace$
→ $|G \cap H| = 4$

$G \cup H = \lbrace 1,2,3,4,5,6,7,8,9,10,12 \rbrace$
→ $|G \cup H| = 11$

$(G \cup H) \setminus I = \lbrace 2,4,6,8,10,12 \rbrace$
→ cardinalidad = 6

Verificación:

$|G| = 9$
$|H| = 6$
$|G \cap H| = 4$

$9 + 6 - 4 = 11$ ✔
:::

### D) Producto cartesiano

Sea:

- $J = \lbrace 1,2,3 \rbrace$
- $K = \lbrace a,b,c,d \rbrace$

1. Escriba completamente $J \times K$.
2. Escriba completamente $K \times J$.
3. Escriba el conjunto:
   $L = \lbrace (x,y) \in J \times J \mid x < y \rbrace$

:::{dropdown} Solución
$J \times K =$

$\lbrace$
$(1,a),(1,b),(1,c),(1,d),$
$(2,a),(2,b),(2,c),(2,d),$
$(3,a),(3,b),(3,c),(3,d)$
$\rbrace$

$K \times J =$

$\lbrace$
$(a,1),(a,2),(a,3),$
$(b,1),(b,2),(b,3),$
$(c,1),(c,2),(c,3),$
$(d,1),(d,2),(d,3)$
$\rbrace$

$L = \lbrace (1,2),(1,3),(2,3) \rbrace$
:::

### E) Conjunto potencia

Sea:

$M = \lbrace p,q,r \rbrace$

1. ¿Cuántos elementos tiene $\mathcal{P}(M)$?
2. ¿Cuántos subconjuntos de $M$ tienen exactamente 2 elementos?
3. Escriba todos los subconjuntos de 2 elementos.
4. Determine si:
   - $\lbrace p,r \rbrace \in \mathcal{P}(M)$
   - $\lbrace p,q,r,s \rbrace \in \mathcal{P}(M)$

:::{dropdown} Solución
$|\mathcal{P}(M)| = 2^3 = 8$

Subconjuntos de 2 elementos:

$\lbrace p,q \rbrace, \lbrace p,r \rbrace, \lbrace q,r \rbrace$

$\lbrace p,r \rbrace \in \mathcal{P}(M)$ → Verdadero
$\lbrace p,q,r,s \rbrace \in \mathcal{P}(M)$ → Falso
:::

### F) Operaciones combinadas

Sea:

- $P = \lbrace 1,2,3,5,7,9 \rbrace$
- $Q = \lbrace 2,4,6,8,9 \rbrace$
- $R = \lbrace 1,3,5,7 \rbrace$

1. Calcule:
   - $P \cup Q$
   - $P \cap Q$
   - $P \setminus Q$

2. Calcule:
   $(P \cup Q) \setminus R$

3. Calcule:
   $P \cap (Q \cup R)$

:::{dropdown} Solución
$P \cup Q = \lbrace 1,2,3,4,5,6,7,8,9 \rbrace$

$P \cap Q = \lbrace 2,9 \rbrace$

$P \setminus Q = \lbrace 1,3,5,7 \rbrace$

$(P \cup Q) \setminus R = \lbrace 2,4,6,8,9 \rbrace$

$Q \cup R = \lbrace 1,2,3,4,5,6,7,8,9 \rbrace$

$P \cap (Q \cup R) = \lbrace 1,2,3,5,7,9 \rbrace$
:::

### G) Complemento y leyes de De Morgan

Universo:

$U = \lbrace 1,2,3,4,5,6,7,8,9,10,11,12 \rbrace$

Conjuntos:

- $S = \lbrace 2,3,5,7,11 \rbrace$
- $T = \lbrace 1,3,4,7,8,12 \rbrace$

1. Calcule:
   - $\overline{S}$
   - $\overline{T}$

2. Calcule:
   $\overline{S \cup T}$

3. Verifique que:
   $\overline{S \cup T} = \overline{S} \cap \overline{T}$

:::{dropdown} Solución
$\overline{S} = \lbrace 1,4,6,8,9,10,12 \rbrace$

$\overline{T} = \lbrace 2,5,6,9,10,11 \rbrace$

$S \cup T = \lbrace 1,2,3,4,5,7,8,11,12 \rbrace$

$\overline{S \cup T} = \lbrace 6,9,10 \rbrace$

$\overline{S} \cap \overline{T} = \lbrace 6,9,10 \rbrace$ ✔
:::

---
**· Contenido adicional ·**

### Ejercicios teoría de conjuntos

**Ejercicio 1**
Supongamos que $A \times B = \emptyset$, donde $A$ y $B$ son conjuntos. ¿Qué se puede concluir? Demuéstrelo.

**Ejercicio 2**
¿Cuántos elementos distintos tiene $A \times B$ si $A$ tiene $m$ elementos y $B$ tiene $n$?

**Ejercicio 3**
Sean $A = \{a, b, c\}$, $B = \{x, y\}$ y $C = \{0, 1\}$. Obtenga:

1. $A \times B \times C$
2. $C \times B \times A$
3. $C \times A \times B$
4. $B \times B \times B$

**Ejercicio 4**
Demuestre que $A \times B \ne B \times A$ para conjuntos $A$ y $B$ no vacíos a no ser que $A = B$.

**Ejercicio 5**
Sea $A$ un conjunto. Demuestre que:

1. $A \cup \emptyset = A$
2. $A \cap \emptyset = \emptyset$
3. $A \cup A = A$
4. $A \cap A = A$
5. $A - \emptyset = A$
6. $A \cup U = U$
7. $A \cap U = A$
8. $\emptyset - A = \emptyset$

**Ejercicio 6**
Sean $A$ y $B$ conjuntos. Demuestre que $A \cup (A \cap B) = A$.

**Ejercicio 7**
Sean $A$, $B$ y $C$ conjuntos. Demuestre que:

1. $(A \cup B) \subseteq (A \cup B \cup C)$
2. $(A \cap B \cap C) \subseteq (A \cap B)$
3. $(A - B) - C \subseteq A - C$
4. $(A - C) \cap (C - B) = \emptyset$
5. $(B - A) \cup (C - A) = (B \cup C) - A$

**Ejercicio 8**
Demuestre que si $A$ y $B$ son conjuntos, entonces $A - B = A \cap B$.

**Ejercicio 9**
Demuestre que si $A$ y $B$ son conjuntos, entonces $(A \cap B) \cup (A \cap B) = A$.

**Ejercicio 10**
Sea $A_i = \{..., -2, -1, 0, 1, ..., i\}$. Halle
$\bigcup\limits_{i=1}^n A_i$ y $\bigcap\limits_{i=1}^n A_i$

---

## Ejercicios: Conjuntos en Java (Interfaz `Set`)

### Problema: Señales Nuevas

**Contexto**

Un radar espacial detecta N señales representadas como enteros. El sistema
cuenta con una base de datos de M señales ya conocidas y catalogadas.

El objetivo es determinar **cuántas señales DISTINTAS captó el radar que
no estaban en la base de datos** (señales genuinamente nuevas).

> Dos capturas de la misma señal desconocida cuentan como UNA sola señal nueva.

**Entrada**

```
Primera línea:  N M
                N = cantidad de señales captadas   (1 ≤ N ≤ 100 000)
                M = cantidad de señales conocidas  (1 ≤ M ≤ 50 000)

Segunda línea:  M enteros — señales en la base de datos

Tercera línea:  N enteros — señales captadas por el radar
                (enteros, 1 ≤ valor ≤ 10^9, pueden repetirse)
```

**Salida**

```
Un único entero: cantidad de señales nuevas y distintas.
```

**Ejemplos**

Ejemplo 1

Entrada:
```
8 3
5 10 15
3 5 7 3 10 7 2 9
```

Salida:
```
4
```

Explicación:

| Señal captada | ¿Está en la base de datos? | ¿Ya fue vista antes? | ¿Cuenta? |
|:---:|:---:|:---:|:---:|
| 3  | No | No  | ✅ Sí |
| 5  | Sí | —   | ❌ No |
| 7  | No | No  | ✅ Sí |
| 3  | No | Sí  | ❌ No |
| 10 | Sí | —   | ❌ No |
| 7  | No | Sí  | ❌ No |
| 2  | No | No  | ✅ Sí |
| 9  | No | No  | ✅ Sí |

Señales nuevas y distintas: `{3, 7, 2, 9}` → **4**

Ejemplo 2

Entrada:
```
5 5
1 2 3 4 5
1 1 2 3 4
```

Salida:
```
0
```

Ejemplo 3

Entrada:
```
6 1
99
4 4 4 4 4 4
```

Salida:
```
1
```

**Actividad**

Implemente el método `contarSenalesNuevas` que resuelve el problema.

El `Main.java` que lee la entrada y llama su método ya está dado:

```java
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), m = sc.nextInt();

        int[] conocidas = new int[m];
        for (int i = 0; i < m; i++) {
            conocidas[i] = sc.nextInt();
        }

        int[] captadas = new int[n];
        for (int i = 0; i < n; i++) {
            captadas[i] = sc.nextInt();
        }

        sc.close();

        int resultado = contarSenalesNuevas(captadas, conocidas);
        System.out.println(resultado);
    }

    // TODO: implemente este método
    public static int contarSenalesNuevas(int[] captadas, int[] conocidas) {
        // su solución aquí
        return 0;
    }
}
```

**Restricción de eficiencia:** su solución debe ser capaz de manejar
N = 100 000 y M = 50 000 dentro de un límite de tiempo razonable.

:::{dropdown} Solución

**Estrategia**

El problema requiere dos operaciones que se repiten para cada una
de las N señales captadas:

1. **¿Está esta señal en la base de datos?** → membresía en un conjunto
2. **¿Ya contamos esta señal antes?** → deduplicación automática

Ambas operaciones sobre una **colección sin orden relevante** son la
definición exacta de lo que hace un `Set`. La pregunta es cuál de las
tres implementaciones usar.

**Comparación de implementaciones de `Set`**

| Operación necesaria             | `ArrayList`    | `LinkedHashSet` | `TreeSet`    | `HashSet`        |
|---------------------------------|----------------|-----------------|--------------|------------------|
| `contains(x)`                   | O(N) lineal    | O(1)            | O(log N)     | **O(1)**         |
| `add(x)` con deduplicación      | O(N) manual    | O(1)            | O(log N)     | **O(1)**         |
| ¿Mantiene orden de inserción?   | —              | Sí (overhead)   | No           | No               |
| ¿Mantiene orden natural sorted? | —              | No              | Sí (overhead)| No               |
| ¿El problema necesita orden?    | —              | ❌ No           | ❌ No        | ✅ Tampoco, y es el más rápido |

- **`LinkedHashSet`**: funciona correctamente pero consume memoria extra
  manteniendo una lista doblemente enlazada para preservar el orden de
  inserción — información que nadie solicitó en este problema.
- **`TreeSet`**: funciona correctamente pero paga O(log N) por cada
  `add` y `contains` porque mantiene un árbol Red-Black ordenado —
  orden que tampoco fue solicitado.
- **`HashSet`**: O(1) amortizado para todo, sin estructuras auxiliares.
  **Es la elección óptima.**

**El costo de no usar Set**

Con `ArrayList`, el código ingenuo sería:

```java
for (int senal : captadas) {
    if (!listaConocidas.contains(senal)) {  // O(M) — recorre toda la lista
        if (!listaNuevas.contains(senal)) { // O(N) — recorre toda la lista
            listaNuevas.add(senal);
        }
    }
}
```

Cada iteración puede costar hasta O(N + M). Para N = 100 000 y M = 50 000
esto es en el peor caso **~15 mil millones de comparaciones** → `TLE`.

Con `HashSet` ambas comprobaciones son O(1) → **100 000 operaciones en total**.

**Solución Completa**

```java
import java.util.HashSet;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), m = sc.nextInt();

        int[] conocidas = new int[m];
        for (int i = 0; i < m; i++) {
            conocidas[i] = sc.nextInt();
        }

        int[] captadas = new int[n];
        for (int i = 0; i < n; i++) {
            captadas[i] = sc.nextInt();
        }

        sc.close();

        int resultado = contarSenalesNuevas(captadas, conocidas);
        System.out.println(resultado);
    }

    public static int contarSenalesNuevas(int[] captadas, int[] conocidas) {

        // HashSet 1: base de datos — permite consulta O(1)
        HashSet<Integer> baseDatos = new HashSet<>();
        for (int s : conocidas) {
            baseDatos.add(s);
        }

        // HashSet 2: acumulador de señales nuevas
        // add() ignora automáticamente duplicados → deduplicación gratuita
        HashSet<Integer> nuevas = new HashSet<>();
        for (int senal : captadas) {
            if (!baseDatos.contains(senal)) {  // O(1)
                nuevas.add(senal);             // O(1), duplicado = no-op
            }
        }

        return nuevas.size();
    }
}
```

**Traza del Ejemplo 1**

```
conocidas = {5, 10, 15}   ← HashSet construido en O(M)

Procesando captadas: [3, 5, 7, 3, 10, 7, 2, 9]

senal=3  → baseDatos.contains(3)? No  → nuevas.add(3)  → nuevas={3}
senal=5  → baseDatos.contains(5)? Sí  → ignorar
senal=7  → baseDatos.contains(7)? No  → nuevas.add(7)  → nuevas={3,7}
senal=3  → baseDatos.contains(3)? No  → nuevas.add(3)  → sin cambio (ya está)
senal=10 → baseDatos.contains(10)? Sí → ignorar
senal=7  → baseDatos.contains(7)? No  → nuevas.add(7)  → sin cambio (ya está)
senal=2  → baseDatos.contains(2)? No  → nuevas.add(2)  → nuevas={3,7,2}
senal=9  → baseDatos.contains(9)? No  → nuevas.add(9)  → nuevas={3,7,2,9}

nuevas.size() = 4  ✓
```

**Complejidad**

| Fase                          | Costo       |
|-------------------------------|-------------|
| Construir `baseDatos`         | O(M)        |
| Procesar N señales captadas   | O(N)        |
| **Total tiempo**              | **O(N + M)**|
| **Espacio adicional**         | **O(N + M)**|

Con N = 100 000 y M = 50 000 → ~150 000 operaciones.
Frente a la solución con `ArrayList` → ~15 000 000 000 operaciones.
**El uso de `HashSet` representa una mejora de ~100 000x en este caso.**
:::

---
**· Contenido adicional ·**

### Ejercicios Interface Set

**Operaciones con conjuntos**

* El método realizarOperacionesTexto solo demuestra la operación de unión. Agrega
código a este método para calcular e imprimir la intersección y la diferencia de
mySet1 y mySet6.

* Modifica el método ejecutarOperaciones() para comparar mySet2 y mySet4. Determina
qué elementos están en mySet2 pero no en mySet4, y luego imprime el
resultado.

* El código no muestra explícitamente el método removeAll() en realizarOperacionesTexto.
Dados los datos iniciales, si se realizara una operación removeAll() sobre la
union de mySet1 y mySet6 con un nuevo conjunto que contenga "Igor" y "Tanya1",
¿qué contendría el conjunto union final?. Muestra el resultado en consola.

**Palabras únicas**

* Modifica la clase PalabrasUnicas para que incluya un nuevo método público llamado
eliminarPalabra(String palabra). Este método debe recibir una palabra como argumento
y eliminarla del conjunto palabrasUnicas si existe. Utiliza la clase modificada.
Agrega la oración:

"Un buen programador es un programador que piensa el codigo antes de escribirlo"

* Después de agregar la oración, elimina la palabra "un" y "que". Muestra la cantidad
de palabras únicas restantes y el conjunto final.

---

## Hoja de trabajo: Implementaciones de `Set` en Java

Cada problema indica qué implementación de `Set` resulta más apropiada
y por qué. Las soluciones están ocultas — intenta resolverlo primero.

### Problema 1 — Primera Repetición
**Estructura sugerida: `HashSet`**

Una central de seguridad registra `N` intentos de acceso con IDs de usuario.
Se sabe que el sistema fue comprometido en el momento exacto en que
un usuario intenta acceder **por segunda vez**. Encuentra ese ID.
Si ningún ID se repite, imprime `-1`.

**Entrada**
```
Primera línea:  N  (1 ≤ N ≤ 100 000)
Segunda línea:  N enteros — IDs de acceso en orden cronológico
                (1 ≤ ID ≤ 10^9)
```

**Salida**
```
El primer ID que se repite, o -1 si no hay ninguno.
```

**Ejemplo**
```
Entrada:        Salida:
8               7
4 9 2 7 1 3 7 5
```

```
Entrada:        Salida:
4               -1
1 2 3 4
```

**¿Por qué `HashSet`?**
El método `add()` de `HashSet` retorna `false` si el elemento **ya estaba
presente**. Esto permite detectar duplicados en una sola pasada O(n),
sin necesidad de una segunda estructura auxiliar.
Con `ArrayList`, `contains()` costaría O(n) por llamado → O(n²) total.
Ni `LinkedHashSet` ni `TreeSet` aportan beneficio extra aquí: no se
necesita orden de ningún tipo.

:::{dropdown} Ver solución

```java
import java.util.*;

public class PrimeraRepeticion {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        HashSet<Integer> vistos = new HashSet<>();
        int resultado = -1;
        for (int i = 0; i < n; i++) {
            int id = sc.nextInt();
            if (!vistos.add(id)) {
                resultado = id;
                break;
            }
        }
        System.out.println(resultado);
        sc.close();
    }
}
```

`vistos.add(id)` retorna `false` cuando `id` ya existía — condición de
duplicado en una sola operación O(1), sin llamado extra a `contains`.
:::

### Problema 2 — Feed Sin Repetidos
**Estructura sugerida: `LinkedHashSet`**

Una plataforma recibe `N` publicaciones en orden cronológico, identificadas
por un entero. Algunas son republicaciones del mismo contenido (mismo ID).
El sistema debe mostrarle al usuario cada publicación **solo la primera vez**
que aparece, respetando ese orden de aparición.

Luego llegan `Q` consultas. Cada consulta es un entero `K` y pregunta:
*¿cuál es el ID de la K-ésima publicación única?*

**Entrada**
```
Primera línea:  N  (1 ≤ N ≤ 200 000)
Segunda línea:  N enteros — IDs en orden de llegada
Tercera línea:  Q  (1 ≤ Q ≤ 100 000)
Siguientes Q:   un entero K por línea  (1 ≤ K ≤ número de publicaciones únicas)
```

**Salida**
```
Por cada consulta, el ID de la K-ésima publicación única (en orden de primera aparición).
```

**Ejemplo**
```
Entrada:                Salida:
9                       101
101 305 101 200 305     200
101 412 200 412         412
3
1
3
4
```

**¿Por qué `LinkedHashSet`?**
`LinkedHashSet` deduplica automáticamente **y** mantiene el orden en que
cada elemento fue insertado por primera vez. Convertirlo luego a
`ArrayList` permite responder consultas por índice en O(1).

Con `HashSet` se pierde el orden de inserción — imposible responder las consultas.
Con `TreeSet` los IDs quedarían ordenados numéricamente, no cronológicamente.
Sin Set: habría que mantener una lista + un Set por separado, duplicando código.

:::{dropdown} Ver solución

```java
import java.util.*;

public class FeedSinRepetidos {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        LinkedHashSet<Integer> feed = new LinkedHashSet<>();
        for (int i = 0; i < n; i++) feed.add(sc.nextInt());

        List<Integer> orden = new ArrayList<>(feed);

        int q = sc.nextInt();
        StringBuilder sb = new StringBuilder();
        while (q-- > 0) {
            int k = sc.nextInt();
            sb.append(orden.get(k - 1)).append('\n');
        }
        System.out.print(sb);
        sc.close();
    }
}
```

`new ArrayList<>(feed)` copia los elementos en el orden de inserción
del `LinkedHashSet` — una sola línea que reemplaza toda la lógica
manual de "ya lo vi antes, ¿en qué posición lo agregué?".
:::

### Problema 3 — Score Más Cercano
**Estructura sugerida: `TreeSet`**

Un torneo en línea registra los puntajes de sus participantes.
Dado el marcador actual y `Q` consultas, cada consulta entrega un valor `X`
y pregunta dos cosas:

1. ¿Cuál es el **mayor puntaje ≤ X** registrado? (`NONE` si no existe)
2. ¿Cuál es el **menor puntaje ≥ X** registrado? (`NONE` si no existe)

**Entrada**
```
Primera línea:  N  (1 ≤ N ≤ 100 000) — puntajes registrados
Segunda línea:  N enteros (pueden repetirse, 1 ≤ puntaje ≤ 10^9)
Tercera línea:  Q  (1 ≤ Q ≤ 100 000)
Siguientes Q:   un entero X por línea
```

**Salida**
```
Por cada consulta: "p s" donde p es el piso y s es el techo.
Usar NONE si no existe.
```

**Ejemplo**
```
Entrada:            Salida:
6                   5 9
3 9 5 14 5 22       9 9
4                   14 22
7                   NONE 3
9
15
2
```

**¿Por qué `TreeSet`?**
`TreeSet.floor(x)` y `TreeSet.ceiling(x)` resuelven ambas preguntas en
**O(log n)** gracias al árbol Red-Black interno. El set también deduplica
automáticamente, así que puntajes repetidos no afectan el resultado.

Con cualquier lista ordenada se podría hacer búsqueda binaria, pero
se necesitaría deduplicación manual previa y más código.
`HashSet` o `LinkedHashSet` no tienen orden: imposible hacer floor/ceiling.

:::{dropdown} Ver solución

```java
import java.util.*;

public class ScoreMasCercano {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        TreeSet<Integer> scores = new TreeSet<>();
        for (int i = 0; i < n; i++) scores.add(sc.nextInt());

        int q = sc.nextInt();
        StringBuilder sb = new StringBuilder();
        while (q-- > 0) {
            int x = sc.nextInt();
            Integer piso  = scores.floor(x);
            Integer techo = scores.ceiling(x);
            sb.append(piso  != null ? piso  : "NONE").append(' ')
              .append(techo != null ? techo : "NONE").append('\n');
        }
        System.out.print(sb);
        sc.close();
    }
}
```
:::

### Problema 4 — Alumnos en Todos los Grupos
**Estructura sugerida: `HashSet`**

Una universidad tiene `K` grupos de estudio. Cada grupo tiene una lista
de IDs de alumnos. Se necesita saber cuántos alumnos están inscritos
en **absolutamente todos** los grupos, e imprimir sus IDs en orden ascendente.

**Entrada**
```
Primera línea:  K  (2 ≤ K ≤ 50) — número de grupos
Por cada grupo: una línea con M seguido de M enteros (IDs de alumnos)
                (1 ≤ M ≤ 10 000, 1 ≤ ID ≤ 10^6)
```

**Salida**
```
Primera línea:  cantidad de alumnos en todos los grupos
Segunda línea:  sus IDs en orden ascendente (o vacía si no hay ninguno)
```

**Ejemplo**
```
Entrada:                Salida:
3                       2
5 10 20 30 40 50        10 40
4 10 40 60 70
6 5 10 15 40 80 90
```

**¿Por qué `HashSet`?**
`HashSet.retainAll(otroSet)` calcula la **intersección en una sola línea**,
modificando el set en O(n). Encadenar esto para K grupos es directo y legible.

Sin Set: necesitarías comparar cada par de listas con bucles anidados → O(M² × K).
`TreeSet` funcionaría pero pagaría O(log n) innecesario en cada `add` durante
la carga; el orden solo se necesita al final, y para eso basta un `Collections.sort`.
`LinkedHashSet` no aporta nada: el orden de inserción no es relevante aquí.

:::{dropdown} Ver solución

```java
import java.util.*;

public class AlumnosTodosGrupos {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int k = sc.nextInt();

        HashSet<Integer> comunes = null;
        for (int i = 0; i < k; i++) {
            int m = sc.nextInt();
            HashSet<Integer> grupo = new HashSet<>();
            for (int j = 0; j < m; j++) grupo.add(sc.nextInt());
            if (comunes == null) comunes = grupo;
            else comunes.retainAll(grupo);
        }

        List<Integer> resultado = new ArrayList<>(comunes);
        Collections.sort(resultado);

        System.out.println(resultado.size());
        StringBuilder sb = new StringBuilder();
        for (int id : resultado) sb.append(id).append(' ');
        System.out.println(sb.toString().trim());
        sc.close();
    }
}
```

`comunes.retainAll(grupo)` elimina de `comunes` todo lo que no esté en
`grupo` — intersección completa en una llamada, sin bucles explícitos.
:::

### Problema 5 — El K-ésimo Único
**Estructura sugerida: `TreeSet`**

Dado un arreglo de `N` enteros con posibles repeticiones y `Q` consultas,
cada consulta entrega un valor `K` y pregunta: *¿cuál es el K-ésimo entero
más pequeño considerando solo valores distintos?*
Si no existe el K-ésimo único, imprime `-1`.

**Entrada**
```
Primera línea:  N  (1 ≤ N ≤ 200 000)
Segunda línea:  N enteros (pueden repetirse, −10^9 ≤ valor ≤ 10^9)
Tercera línea:  Q  (1 ≤ Q ≤ 100 000)
Siguientes Q:   un entero K por línea
```

**Salida**
```
Por cada consulta: el K-ésimo valor distinto en orden ascendente, o -1.
```

**Ejemplo**
```
Entrada:                    Salida:
8                           1
4 1 7 1 3 7 3 9             4
5                           7
1                           -1
3
5
7
2
```

*Valores distintos ordenados: hay 5 únicos.*

**¿Por qué `TreeSet`?**
`TreeSet` deduplica **y** mantiene orden natural en una sola estructura.
Al convertirlo a `ArrayList`, las consultas por índice cuestan O(1) cada una
tras un preprocesamiento O(n log n).

Con `HashSet` habría que ordenar manualmente después de deduplicar.
Con `LinkedHashSet` ídem — el orden de inserción no es el orden numérico.
Sin Set: ordenar + deduplicar con lógica manual requiere más código y
es más propenso a errores de índice.

:::{dropdown} Ver solución

```java
import java.util.*;

public class KesimoUnico {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        TreeSet<Integer> set = new TreeSet<>();
        for (int i = 0; i < n; i++) set.add(sc.nextInt());

        List<Integer> unicos = new ArrayList<>(set);

        int q = sc.nextInt();
        StringBuilder sb = new StringBuilder();
        while (q-- > 0) {
            int k = sc.nextInt();
            sb.append(k <= unicos.size() ? unicos.get(k - 1) : -1).append('\n');
        }
        System.out.print(sb);
        sc.close();
    }
}
```

`new ArrayList<>(set)` produce directamente la lista de valores únicos
en orden ascendente — `TreeSet` hizo el trabajo de ordenar y deduplicar
durante las inserciones, sin ningún paso extra.
:::

*Material adaptado del material original del profesor Oscar Bedoya, con contenido adicional del profesor Marlon Gomez.*
