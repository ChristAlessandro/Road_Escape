# Road_Escape
Mini juego 2D de carreras desarrollado con Python y asistencia de IA

------------- 1er promt -------------

Quiero desarrollar un mini-juego 2D de carreras en Python utilizando pygame.

La idea es que el jugador controle un automóvil que circula por una carretera vertical y debe esquivar otros vehículos que aparecen desde la parte superior de la pantalla.

Para esta primera versión quiero únicamente crear la estructura básica del juego:

* Una ventana de juego.
* Una carretera vertical con varios carriles.
* Un automóvil controlado por el jugador.
* Movimiento del automóvil hacia la izquierda y derecha mediante las teclas de dirección.
* Un bucle principal del juego.
* Una estructura de código clara y fácil de entender.

No agregues todavía enemigos, colisiones, puntuación, sonidos ni menú.

Utiliza código sencillo y comenta las partes importantes para que pueda comprender cómo funciona cada sección.

------------- 2do promt -------------

Continuemos con el mini-juego 2D de carreras desarrollado en Python utilizando pygame.

Actualmente el juego ya cuenta con:

* Una ventana de juego.
* Una carretera vertical con varios carriles.
* Un automóvil controlado por el jugador.
* Movimiento hacia la izquierda y derecha mediante las teclas de dirección.
* Un bucle principal del juego.

Ahora quiero agregar los vehículos enemigos.

Requisitos:

* Los vehículos enemigos deben aparecer desde la parte superior de la carretera.
* Deben desplazarse verticalmente hacia la parte inferior de la pantalla.
* Deben aparecer en diferentes carriles de forma aleatoria.
* Debe existir una pequeña separación entre los vehículos para evitar que aparezcan todos juntos.
* Cuando un vehículo enemigo salga por la parte inferior de la pantalla, debe eliminarse y generarse otro.
* Debe poder existir más de un vehículo enemigo en pantalla al mismo tiempo.
* La velocidad de los enemigos debe ser ligeramente mayor que la velocidad visual del movimiento del escenario.
* Mantén el código organizado y fácil de entender.
* Utiliza funciones o clases solamente cuando realmente ayuden a organizar el código.
* Comenta las partes importantes del código.

Todavía NO agregues:

* Colisiones.
* Game Over.
* Puntuación.
* Sonidos.
* Menú principal.

Quiero que esta modificación conserve todo lo que ya funcionaba en la primera versión.

------------- 3er promt -------------

Continuemos trabajando sobre la versión actual del mini-juego 2D de carreras desarrollado en Python utilizando pygame.

Después de probar la versión actual encontré algunos problemas que quiero corregir antes de continuar agregando nuevas mecánicas.

### Problemas encontrados

1. Actualmente aparecen hasta 3 vehículos enemigos al mismo tiempo y pueden ocupar demasiados carriles, dejando poco o ningún espacio para que el jugador pueda esquivarlos.
2. Los vehículos enemigos no aparecen de una manera suficientemente aleatoria.
3. En ocasiones los 3 vehículos aparecen prácticamente al mismo tiempo.
4. El apartado visual todavía es muy básico y quiero mejorarlo.

### Cambios que quiero realizar

#### Vehículos enemigos

* Modifica el sistema de generación de enemigos para que aparezcan de manera aleatoria.
* No deben aparecer los 3 vehículos enemigos al mismo tiempo.
* La cantidad de enemigos en pantalla debe variar.
* Debe existir un tiempo aleatorio entre la aparición de cada vehículo.
* Evita generar un enemigo inmediatamente junto a otro si esto hace imposible o demasiado difícil esquivarlos.
* Siempre debe existir al menos una posibilidad razonable de que el jugador pueda cambiar de carril y esquivar los vehículos.
* Los enemigos deben utilizar diferentes carriles de manera aleatoria.
* Mantén una dificultad equilibrada.
* Cuando un enemigo salga de la pantalla, debe poder generarse otro después de un intervalo aleatorio.

#### Mejoras visuales

Mejora el aspecto visual sin utilizar imágenes externas todavía:

* Mejorar el diseño de la carretera.
* Hacer más visibles los carriles.
* Mejorar visualmente el automóvil del jugador.
* Mejorar visualmente los vehículos enemigos.
* Agregar elementos visuales al entorno para que la carretera no se vea como simples rectángulos.
* Agregar una interfaz sencilla que muestre información del juego.
* Mantener una estética coherente de juego de carreras.
* Evitar que el diseño sea excesivamente complejo.

#### Colisiones

Ahora quiero agregar la primera mecánica principal del juego:

* Detectar cuando el automóvil del jugador colisiona con un vehículo enemigo.
* Cuando ocurra una colisión, detener la partida.
* Mostrar un mensaje de "GAME OVER".
* Mostrar una opción para reiniciar la partida.
* Al reiniciar, los vehículos enemigos deben comenzar nuevamente desde un estado limpio.
* El movimiento del jugador debe mantenerse igual que en las versiones anteriores.

### Importante

No agregues todavía:

* Sonidos.
* Música.
* Sistema de puntuación.
* Menú principal completo.
* Tienda o mejoras de vehículos.

Quiero que mantengas las funcionalidades que ya existen y que el código siga siendo sencillo de entender.

También quiero que indiques brevemente qué partes del código modificaste para solucionar los problemas encontrados y por qué realizaste esos cambios.

------------- 4to promt -------------

Continuemos trabajando sobre la versión actual del mini-juego 2D de carreras desarrollado en Python utilizando pygame.

La mecánica principal ya funciona correctamente: el jugador puede controlar su automóvil, aparecen vehículos enemigos de manera aleatoria, existe una posibilidad razonable de esquivarlos y las colisiones provocan el Game Over.

Ahora quiero realizar una nueva iteración enfocada principalmente en mejorar el apartado visual.

### Automóviles

Los vehículos actuales se ven demasiado simples. Quiero que tanto el automóvil del jugador como los vehículos enemigos tengan una apariencia más reconocible como automóviles.

Sin utilizar imágenes externas todavía, mejora los vehículos utilizando formas básicas de pygame:

* Carrocería.
* Ventanas delanteras y traseras.
* Llantas.
* Luces delanteras y traseras.
* Parachoques.
* Diferentes colores para distinguir los vehículos enemigos.
* El vehículo del jugador debe ser fácilmente identificable.

Los vehículos deben conservar sus dimensiones y comportamiento actuales para no romper las colisiones ni el movimiento.

### Carretera

Mejora visualmente la carretera:

* Agregar líneas divisorias entre carriles.
* Agregar bordes de la carretera.
* Crear un efecto visual de movimiento para las líneas.
* Agregar un entorno sencillo a ambos lados de la carretera.
* Mantener una apariencia limpia y coherente.

### Interfaz

Mejora la interfaz sin agregar todavía un menú principal completo:

* Mostrar claramente el nombre del juego.
* Crear una pequeña zona para información del jugador.
* Mejorar el diseño del mensaje de Game Over.
* Mostrar instrucciones básicas de los controles.
* Mantener una interfaz sencilla y fácil de leer.

### Requisitos importantes

* No utilizar imágenes externas todavía.
* No cambiar la lógica de movimiento existente.
* No eliminar las mecánicas que ya funcionan.
* No modificar innecesariamente el sistema de generación de enemigos.
* Mantener las colisiones funcionando correctamente.
* Mantener el código organizado y fácil de entender.
* Comentar las partes nuevas o modificadas.
* Priorizar formas y elementos gráficos dibujados directamente con pygame.

Antes de finalizar, explica brevemente qué cambios realizaste y qué partes del código fueron modificadas.

------------- 5to promt -------------

Continuemos trabajando sobre la versión actual del mini-juego 2D de carreras desarrollado en Python utilizando pygame.

La versión actual ya cuenta con:

* Carretera con varios carriles.
* Automóvil del jugador con diseño visual mejorado.
* Vehículos enemigos con diseño visual mejorado.
* Generación aleatoria de enemigos.
* Movimiento del jugador.
* Colisiones.
* Sistema de Game Over.
* Reinicio de la partida.
* Interfaz visual básica.

Ahora quiero agregar los principales sistemas de progresión del juego.

### 1. Sistema de puntuación

Implementa un sistema de puntuación:

* El jugador debe obtener puntos mientras permanece con vida.
* La puntuación debe aumentar progresivamente con el tiempo.
* Mostrar la puntuación durante la partida.
* Mostrar la puntuación final cuando ocurre el Game Over.
* La puntuación debe reiniciarse al comenzar una nueva partida.

La puntuación debe estar relacionada con el tiempo o distancia recorrida y no depender únicamente de la cantidad de enemigos que aparecen.

### 2. Dificultad progresiva

Implementa un sistema de dificultad progresiva:

* Al comenzar, la velocidad de los enemigos debe ser moderada.
* Conforme aumenta la puntuación o el tiempo de supervivencia, la velocidad debe aumentar gradualmente.
* La dificultad no debe aumentar demasiado rápido.
* El sistema de generación de enemigos debe seguir garantizando que el jugador tenga una posibilidad razonable de esquivarlos.
* Evita que la dificultad llegue a un punto en el que el juego sea imposible de jugar.

La dificultad debe poder aumentar varias veces durante una partida.

### 3. Récord / High Score

Agrega un sistema de puntuación máxima:

* Guardar la puntuación más alta alcanzada por el jugador.
* Mostrar el récord durante la partida o en la pantalla de Game Over.
* Si el jugador supera el récord, actualizarlo.
* El récord debe mantenerse cuando el jugador reinicia una partida.
* Si es sencillo de implementar, guardar el récord en un archivo local para que permanezca después de cerrar y volver a abrir el juego.

### 4. Interfaz

Mejora la información mostrada en pantalla:

* Puntuación actual.
* Récord.
* Nivel o indicador de dificultad.
* Game Over.
* Puntuación obtenida en la partida.
* Instrucción para reiniciar.

La información debe ser clara y no cubrir elementos importantes de la carretera.

### 5. Mantener lo existente

Es muy importante que esta modificación conserve las funcionalidades actuales:

* No eliminar el movimiento del jugador.
* No eliminar la generación aleatoria de enemigos.
* No eliminar las colisiones.
* No eliminar el Game Over.
* No eliminar las mejoras visuales.
* No cambiar innecesariamente el diseño de los vehículos.

Mantén el código organizado y fácil de entender.

### 6. Validación

Al finalizar, explica brevemente:

* Qué funciones o clases nuevas agregaste.
* Cómo funciona el sistema de puntuación.
* Cómo aumenta la dificultad.
* Cómo se guarda y actualiza el récord.
* Qué partes del código existente modificaste.

No agregues todavía sonidos, música ni un menú principal completo. Esas funcionalidades se implementarán en una siguiente iteración.

