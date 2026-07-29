---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "TAD: Ejercicios"
---

# TAD: Ejercicios

Use esta página después de leer el [material de estudio de TAD](index.md).

## Ejercicios

Diseñe un Tipo Abstracto de Dato para:

- Curso

---

### Ejercicios

Diseñe un Tipo Abstracto de Dato para:

- Números racionales
- Curso

---

## Hoja de trabajo: Implementación de una Lista Enlazada en Java

Sigue los pasos en orden: **escribe primero**, luego despliega la pista solo si estás atascado. Al final ejecuta el `Main` proporcionado y verifica que la salida en terminal coincida exactamente con lo esperado.

### Paso 1: crea la clase `Nodo<T>`

Crea el archivo `Nodo.java`. La clase necesita:
- un campo `dato` de tipo `T` (el valor del nodo)
- un campo `siguiente` de tipo `Nodo<T>` (apunta al próximo)
- un constructor que reciba `dato` e inicialice `siguiente` en `null`

:::{dropdown} Pista — Nodo.java
```java
public class Nodo<T> {
    public T dato;
    public Nodo<T> siguiente;

    public Nodo(T dato) {
        this.dato = dato;
        this.siguiente = null;
    }
}
```
:::

### Paso 2: crea el esqueleto de `ListaEnlazada<T>`

Crea el archivo `ListaEnlazada.java`. Por ahora, solo el campo `cabeza` y el constructor que lo inicializa en `null`. Deja comentarios marcando dónde irán los métodos.

:::{dropdown} Pista — esqueleto ListaEnlazada.java
```java
public class ListaEnlazada<T> {
    private Nodo<T> cabeza;

    public ListaEnlazada() {
        cabeza = null;
    }

    // agregarAlInicio, agregarAlFinal, imprimir, contiene, eliminar
}
```
:::

### Paso 3: implementa `agregarAlInicio(T dato)`

Tres instrucciones en este orden:
1. Crea un nodo nuevo con el dato.
2. Haz que `nuevo.siguiente` apunte a `cabeza`.
3. Actualiza `cabeza` para que apunte a `nuevo`.

> Costo: O(1) — no importa cuántos nodos haya.

:::{dropdown} Pista — agregarAlInicio
```java
public void agregarAlInicio(T dato) {
    Nodo<T> nuevo = new Nodo<>(dato);
    nuevo.siguiente = cabeza;
    cabeza = nuevo;
}
```
:::

### Paso 4: implementa `agregarAlFinal(T dato)`

Caso especial: si la lista está vacía, `cabeza = nuevo` directamente.
Caso general: recorre con un auxiliar `actual` hasta que `actual.siguiente == null`, luego enlaza.

:::{dropdown} Pista — agregarAlFinal
```java
public void agregarAlFinal(T dato) {
    Nodo<T> nuevo = new Nodo<>(dato);
    if (cabeza == null) {
        cabeza = nuevo;
        return;
    }
    Nodo<T> actual = cabeza;
    while (actual.siguiente != null)
        actual = actual.siguiente;
    actual.siguiente = nuevo;
}
```
:::

### Paso 5: implementa `imprimir()`

Usa una variable auxiliar (no muevas `cabeza`). Imprime cada dato seguido de `" -> "` y al final imprime `"null"`.

:::{dropdown} Pista — imprimir
```java
public void imprimir() {
    Nodo<T> actual = cabeza;
    while (actual != null) {
        System.out.print(actual.dato + " -> ");
        actual = actual.siguiente;
    }
    System.out.println("null");
}
```
:::

### Paso 6: implementa `contiene(T dato)`

Recorre la lista con un auxiliar. En cada nodo usa `.equals()` para comparar. Retorna `true` si lo encuentra, `false` si llega a `null`.

:::{dropdown} Pista — contiene
```java
public boolean contiene(T dato) {
    Nodo<T> actual = cabeza;
    while (actual != null) {
        if (actual.dato.equals(dato))
            return true;
        actual = actual.siguiente;
    }
    return false;
}
```
:::

### Paso 7: implementa `eliminar(T dato)`

Tres casos que debes manejar en orden:
1. Lista vacía → no hacer nada.
2. El dato está en `cabeza` → `cabeza = cabeza.siguiente`.
3. El dato está en algún nodo interior → avanza un puntero `prev` hasta que `prev.siguiente` sea el nodo a eliminar, luego salta: `prev.siguiente = prev.siguiente.siguiente`.

:::{dropdown} Pista — eliminar
```java
public void eliminar(T dato) {
    if (cabeza == null) return;
    if (cabeza.dato.equals(dato)) {
        cabeza = cabeza.siguiente;
        return;
    }
    Nodo<T> prev = cabeza;
    while (prev.siguiente != null &&
           !prev.siguiente.dato.equals(dato))
        prev = prev.siguiente;
    if (prev.siguiente != null)
        prev.siguiente = prev.siguiente.siguiente;
}
```
:::

### Main — ejecuta y verifica

Crea `MainListaEnlazada.java` con el siguiente `main` exactamente como está. La salida en terminal **debe** coincidir con los comentarios.

```java
public class MainListaEnlazada {
    public static void main(String[] args) {
        ListaEnlazada<Integer> l = new ListaEnlazada<>();

        l.agregarAlInicio(30);
        l.agregarAlInicio(20);
        l.agregarAlInicio(10);
        l.imprimir();
        // Esperado: 10 -> 20 -> 30 -> null

        l.agregarAlFinal(40);
        l.imprimir();
        // Esperado: 10 -> 20 -> 30 -> 40 -> null

        System.out.println(l.contiene(20));
        // Esperado: true

        System.out.println(l.contiene(99));
        // Esperado: false

        l.eliminar(20);
        l.imprimir();
        // Esperado: 10 -> 30 -> 40 -> null

        l.eliminar(10);   // elimina la cabeza
        l.imprimir();
        // Esperado: 30 -> 40 -> null

        l.eliminar(40);   // elimina el último
        l.imprimir();
        // Esperado: 30 -> null
    }
}
```

*Material adaptado del material original de los profesores Andrés Aristizábal y Marlon Gomez.*
