---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Generics: Ejercicios"
---

# Generics: Ejercicios

Use esta página después de leer el [material de estudio de Generics](index.md).

---

### Ejercicio: sistema de entidades con lista enlazada genérica

Se requiere construir un sistema que gestione diferentes tipos de entidades:

- Ciudadanos, identificados por cédula (`String`)
- Estudiantes, identificados por código (`Integer`)
- Productos, identificados por código (`String`)

El sistema debe permitir:

- Agregar elementos
- Obtener elementos por índice
- Buscar elementos
- Eliminar elementos

Todo debe hacerse usando una lista enlazada genérica como estructura de datos.

**Estructura del sistema**

```
src/
  estructuras/
    Nodo.java                  (Genérica)
    ListaEnlazada.java         (Genérica)
  modelo/
    Ciudadano.java             (id: String)
    Estudiante.java            (id: Integer)
    Producto.java              (id: String, precio: double)
  gestor/
    Gestor.java                (Gestor<T> con ListaEnlazada<T>)
  ui/
    Main.java                  (Debe de haber al menos un: agregar, obtener, eliminar y buscar por cada uno de los modelos)
```

**Tenga en cuenta lo siguiente:**

- Los modelos deben ser independientes.
- Desarrolle un gestor genérico.
- Busque el elemento por contenido. Ejemplo: usar `equals` en cada modelo.
- Eliminar debe retornar el elemento de tipo genérico.

**Modelos de dominio**

Cada clase debe tener sus propios atributos:

- Ciudadano: cédula, nombre y apellido
- Estudiante: código, nombre, apellido y carrera
- Producto: código, nombre y precio

Cada clase debe tener un método buscar; al usar `equals`, la clase debe tener un identificador único:

- Ciudadano: cédula
- Estudiante: código
- Producto: código

---

*Material adaptado del material original del profesor Marlon Gomez.*
