---
# Copyright (c) 2026 Angela Villota, and collaborators from the CyED block
# Licensed under the PolyForm Noncommercial License 1.0.0.
# Commercial use is prohibited without prior written authorization.
title: "Desacoplamiento: Inyección de dependencias"
---

# Desacoplamiento: Inyección de dependencias

Un diseño desacoplado reduce las dependencias entre los componentes de un sistema. Cuando una clase depende de una abstracción en vez de una implementación concreta, se puede cambiar esa implementación sin tocar el código que la usa. Ese cambio de una clase concreta a una abstracción es lo que separa un sistema rígido de uno que se puede extender sin reescribir lo que ya funciona.

Este ejemplo aplica el principio a un servicio de notificaciones: un mismo `ServicioNotificacion` envía mensajes por Email, SMS o WhatsApp sin conocer ningún detalle de esos canales.

## Diseño

```
Notificador (abstracta)
   ├── NotificadorEmail
   ├── NotificadorSMS
   └── NotificadorWhastApp

ServicioNotificacion  --(recibe en el constructor)-->  Notificador
```

`ServicioNotificacion` solo conoce el contrato `Notificador`; no crea ni conoce ninguna clase concreta de notificación.

## ¿Por qué está desacoplado?

- `ServicioNotificacion` recibe un `Notificador` por el constructor (inyección de dependencias), en vez de instanciar `new NotificadorEmail()` dentro de sí misma.
- Agregar un canal nuevo, por ejemplo `NotificadorPush`, no exige tocar `ServicioNotificacion`: basta con extender `Notificador`.
- `Notificador` es una clase abstracta, no una clase concreta con un método vacío. El compilador obliga a cada subclase a implementar `enviarMensaje`, así que no existe un "notificador" que silenciosamente no hace nada.
- Las pruebas usan un `Notificador` falso (`NotificadorEspia`) que solo registra el último mensaje recibido, en vez de enviar un email o un SMS real.

## Estructura del proyecto

Proyecto Maven estándar. Haga clic en cada carpeta para ver su contenido y su código.

```
NotificacionesDesacoplado/
├── pom.xml
└── src/
    ├── main/java/
    │   ├── main/Main.java
    │   ├── notificacion/
    │   │   ├── Notificador.java
    │   │   ├── NotificadorEmail.java
    │   │   ├── NotificadorSMS.java
    │   │   └── NotificadorWhastApp.java
    │   └── servicio/ServicioNotificacion.java
    └── test/java/
        └── servicio/ServicioNotificacionTest.java
```

:::{dropdown} 📂 notificacion — contrato y canales concretos

**`Notificador.java`** — el contrato. Declarar `enviarMensaje` como `abstract` impide instanciar un notificador que no hace nada.

```java
package notificacion;

/**
 * Contrato para cualquier canal de notificación. Se declara abstracta (en vez de
 * una clase concreta con un método vacío) para que sea imposible instanciar un
 * "notificador" que no hace nada por error — el compilador obliga a cada subclase
 * a implementar enviarMensaje.
 */
public abstract class Notificador {
    public abstract void enviarMensaje(String mensaje);
}
```

**`NotificadorEmail.java`**

```java
package notificacion;

public class NotificadorEmail extends Notificador {
    @Override
    public void enviarMensaje(String mensaje) {
        System.out.println("Enviando Email: " + mensaje);
    }
}
```

**`NotificadorSMS.java`**

```java
package notificacion;

public class NotificadorSMS extends Notificador {
    @Override
    public void enviarMensaje(String mensaje) {
        System.out.println("Enviando SMS: " + mensaje);
    }
}
```

**`NotificadorWhastApp.java`**

```java
package notificacion;

public class NotificadorWhastApp extends Notificador {
    @Override
    public void enviarMensaje(String mensaje) {
        System.out.println("Enviando WhatsApp: " + mensaje);
    }
}
```
:::

:::{dropdown} 📂 servicio — la clase que no depende de nada concreto

**`ServicioNotificacion.java`**

```java
package servicio;

import notificacion.Notificador;

public class ServicioNotificacion {
    private final Notificador notificador;

    //Inyeccion de dependencia por constructor
    public ServicioNotificacion(Notificador notificador) {
        this.notificador = notificador;
    }

    public void enviar(String mensaje) {
        notificador.enviarMensaje(mensaje);
    }
}
```
:::

:::{dropdown} 📂 main — punto de entrada

**`Main.java`**

```java
package main;

import notificacion.Notificador;
import notificacion.NotificadorEmail;
import notificacion.NotificadorSMS;
import notificacion.NotificadorWhastApp;
import servicio.ServicioNotificacion;

public class Main {
    public static void main(String[] args) {
        //Crear instancias de notificaciones especificas
        Notificador email = new NotificadorEmail();
        Notificador sms = new NotificadorSMS();
        Notificador whatsApp = new NotificadorWhastApp();

        //Inyectar la dependencia en el servicio
        ServicioNotificacion servicioEmail = new ServicioNotificacion(email);
        servicioEmail.enviar("Hola, este es un correo electrónico!");

        ServicioNotificacion servicioSMS = new ServicioNotificacion(sms);
        servicioSMS.enviar("Hola, este es un mensaje de texto!");

        ServicioNotificacion servicioWhatsApp = new ServicioNotificacion(whatsApp);
        servicioWhatsApp.enviar("Hola, este es un mensaje de WhatsApp!");
    }
}
```

Salida esperada:

```
Enviando Email: Hola, este es un correo electrónico!
Enviando SMS: Hola, este es un mensaje de texto!
Enviando WhatsApp: Hola, este es un mensaje de WhatsApp!
```
:::

:::{dropdown} 📂 test — pruebas unitarias (JUnit 5)

**`ServicioNotificacionTest.java`** — prueba `ServicioNotificacion` con un `Notificador` falso, sin enviar nada real, y confirma que cada canal concreto recibe su propio mensaje.

```java
package servicio;

import notificacion.Notificador;
import notificacion.NotificadorEmail;
import notificacion.NotificadorSMS;
import notificacion.NotificadorWhastApp;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ServicioNotificacionTest {

    /** Notificador de prueba (test double) que solo registra el último mensaje recibido. */
    static class NotificadorEspia extends Notificador {
        String ultimoMensaje;

        @Override
        public void enviarMensaje(String mensaje) {
            this.ultimoMensaje = mensaje;
        }
    }

    @Test
    void delegaElEnvioAlNotificadorInyectado() {
        NotificadorEspia espia = new NotificadorEspia();
        ServicioNotificacion servicio = new ServicioNotificacion(espia);

        servicio.enviar("mensaje de prueba");

        assertEquals("mensaje de prueba", espia.ultimoMensaje);
    }

    @Test
    void funcionaConCadaImplementacionConcretaSinLanzarExcepcion() {
        //Cubre un bug real de una version anterior: se reusaba servicioSMS para
        //"enviar" el WhatsApp en Main.java. Aqui se prueba cada notificador de
        //forma aislada para que ese tipo de error no pase inadvertido.
        for (Notificador n : new Notificador[]{new NotificadorEmail(), new NotificadorSMS(), new NotificadorWhastApp()}) {
            ServicioNotificacion servicio = new ServicioNotificacion(n);
            assertDoesNotThrowSending(servicio);
        }
    }

    private void assertDoesNotThrowSending(ServicioNotificacion servicio) {
        org.junit.jupiter.api.Assertions.assertDoesNotThrow(() -> servicio.enviar("hola"));
    }
}
```
:::

## Complejidad

Cada envío (`enviar`, `enviarMensaje`) es una llamada directa a un método, sin ciclos ni estructuras de datos de por medio: $O(1)$ en tiempo y en espacio, sin importar cuántos canales de notificación existan.

Este ejemplo no interesa por su complejidad algorítmica. Interesa porque agregar un canal nuevo cuesta $O(1)$ (una clase nueva) en vez de exigir modificar código que ya funciona. Esa es la propiedad de diseño que ilustra: el principio abierto/cerrado.

## Descarga el proyecto completo

::::{grid} 1
:::{card} 📥 NotificacionesDesacoplado.zip
Proyecto Maven completo: `pom.xml`, el código fuente (`src/main/java`) y las pruebas JUnit 5 (`src/test/java`). Ábralo directamente en IntelliJ o Eclipse como proyecto Maven, o ejecútelo con:

```bash
mvn compile
mvn test
mvn exec:java
```

{download}`Descargar NotificacionesDesacoplado.zip <files/NotificacionesDesacoplado.zip>`
:::
::::

---

*Ejemplo adaptado del material de clase de Marlon Gómez y Andrés Aristizabal.*
