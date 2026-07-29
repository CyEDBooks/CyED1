---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Repaso: Ejercicios"
---

# Repaso: Ejercicios

Use esta página después de leer el [material de estudio del
repaso](index.md).

## Ejercicios

**1) Indique cuáles de las siguientes expresiones son proposiciones:**

- 11 es un número primo
- Andrés vivirá 60 años
- Cali no va a ganar el torneo
- Camila tiene un promedio de 4.5

:::{dropdown} Respuesta
Las cuatro son proposiciones: todas son oraciones declarativas que, en
principio, tienen un único valor de verdad (aunque en "Andrés vivirá 60
años" y "Cali no va a ganar el torneo" ese valor todavía no se conozca).
:::

**2) Represente las siguientes proposiciones compuestas usando los
conectivos lógicos:**

1. Hoy es martes y la temperatura es de 21º C
2. Si no llueve hoy entonces voy a la clase de discretas
3. No es cierto que Juan perdió el examen
4. Cali perdió contra el Junior y no clasificó a la final
5. Javier perdió Discretas o Cálculo

:::{dropdown} Respuesta
1. $p\wedge q$, con $p$: "hoy es martes", $q$: "la temperatura es de 21º C"
2. $\neg p\to q$, con $p$: "llueve hoy", $q$: "voy a la clase de discretas"
3. $\neg p$, con $p$: "Juan perdió el examen"
4. $p\wedge\neg q$, con $p$: "Cali perdió contra el Junior", $q$: "Cali
   clasificó a la final"
5. $p\vee q$, con $p$: "Javier perdió Discretas", $q$: "Javier perdió
   Cálculo"
:::

**3) Clasifique la siguiente proposición compuesta como tautología,
contradicción o contingencia:**

$$
(\neg p\wedge\neg q)\oplus(\neg p\to q)
$$

:::{dropdown} Respuesta
| $p$ | $q$ | $\neg p$ | $\neg q$ | $\neg p\wedge\neg q$ | $\neg p\to q$ | $(\neg p\wedge\neg q)\oplus(\neg p\to q)$ |
|---|---|---|---|---|---|---|
| V | V | F | F | F | V | V |
| V | F | F | V | F | V | V |
| F | V | V | F | F | V | V |
| F | F | V | V | V | F | V |

Es verdadera en todas las filas, por lo tanto es una **tautología**.
:::

**4) Aplique la ley que se indica en cada caso:**

- Distributiva sobre $\neg p\vee(p\wedge\neg q)$
- De Morgan sobre $\neg(p\wedge\neg q)$
- De Morgan sobre $\neg(q\vee(\neg p\vee r))$

:::{dropdown} Respuesta
- $\neg p\vee(p\wedge\neg q) \equiv (\neg p\vee p)\wedge(\neg p\vee\neg q)$
- $\neg(p\wedge\neg q) \equiv \neg p\vee\neg(\neg q) \equiv \neg p\vee q$
  (De Morgan y luego doble negación)
- $\neg(q\vee(\neg p\vee r)) \equiv \neg q\wedge\neg(\neg p\vee r) \equiv
  \neg q\wedge(\neg(\neg p)\wedge\neg r) \equiv \neg q\wedge(p\wedge\neg r)$
  (De Morgan aplicada dos veces y luego doble negación)
:::

**5) Aplique la ley $p\to q \equiv \neg p\vee q$ en los siguientes casos:**

- $(\neg p\wedge r)\to q$
- $(p\vee q)\to(\neg q\vee r)$

:::{dropdown} Respuesta
- $(\neg p\wedge r)\to q \equiv \neg(\neg p\wedge r)\vee q \equiv
  (p\vee\neg r)\vee q$ (aplicando además De Morgan)
- $(p\vee q)\to(\neg q\vee r) \equiv \neg(p\vee q)\vee\neg q\vee r \equiv
  (\neg p\wedge\neg q)\vee\neg q\vee r \equiv \neg q\vee r$ (aplicando
  además De Morgan y la ley de absorción)
:::

**6) Pruebe la equivalencia:**

$$
\neg[(p\wedge q)\to(p\to q)] \equiv F
$$

:::{dropdown} Demostración
$$
\begin{align*}
(p\wedge q)\to(p\to q)
&\equiv \neg(p\wedge q)\vee(p\to q)
&&p\to q\equiv\neg p\vee q\\
&\equiv (\neg p\vee\neg q)\vee(\neg p\vee q)
&&\text{De Morgan y }p\to q\equiv\neg p\vee q\\
&\equiv \neg p\vee(\neg q\vee q)
&&\text{Asociativa/conmutativa}\\
&\equiv \neg p\vee V
&&\text{Negación}\\
&\equiv V
&&\text{Dominación}
\end{align*}
$$

Como $(p\wedge q)\to(p\to q) \equiv V$, su negación es
$\neg[(p\wedge q)\to(p\to q)] \equiv F$.
:::

---

*Material adaptado del material original del profesor Oscar Bedoya.*
