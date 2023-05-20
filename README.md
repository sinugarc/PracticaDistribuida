# PracticaDistribuida
Sinhue García Gil, Cristina Hernando Esperanza, Daniel Martínez Martín

Nuestro juego consiste en acertar a la diana opuesta tantas veces como podamos y defender contra el otro jugador chocándonos con él. 

## Instrucciones:

-Moverse para arriba y abajo con la tecla Up/Down

-Cambiar el angulo con la tecla Left/Right

-Lanzar el laser con la tecla Space

-Salir del juego con la tecla Escape


## Archivos    

### SALAF.PY

Es el archivo "broker" que controla los movimientos de los jugadores, recibiendo información y enviandola a los respectivos players.

La clase player inicializa con los atributos de posición y lado, el ángulo así como un booleano que nos permitirá saber si se ha disparado o no.
Los métodos dentro de la clase player se encargan de actualizar la posición y ángulo según la informacion recibida de playerf.py de las teclas presionadas.

La clase sword se inicializa en una posición fuera de la pantalla, con velocidad 0 y ángulo 0. El método update actualiza la posicion del sword si se ha lanzado y comprueba si se ha salido del tablero; devolviendo un booleano indicando si se ha salido del tablero. El método throw actualiza la posición y ángulo desde donde se lanza (atributos de player), cambiando la velocidad para que se mueva.

La clase target se inicializa con el lado, la posición y la velocidad. El método update actualiza la posición en el eje Y y comprueba que no se salga del área de juego, cambiando el sentido de la velocidad si fuera necesario.

La clase Game se inicializa generando listas compartidas de jugadores, dianas, espadas y la puntuación. También crea una variable running y un semáforo lock que garantice la exclusión mutua de los elementos compartidos. Tiene métodos para actualizar la información. El método get_info crea un diccionario con la información necesaria para enviarsela a los jugadores. Los collide se encargarán de reinicializar la información de los swords y actualizar la puntuación si es necesario. El método throw de la clase game comprueba si el jugador ya ha lanzado para no lanzar dos a la vez y si no llama al método throw de la clase sword pasandole como argumento con la posición y ángulo del jugador.

Fuera de las clases, existe una función player que recibe la información de eventos realizados por los jugadores y ejecuta los métodos de la clase Game acorde a dicha información. Luego envía la información actualizada a los jugadores.

### PLAYERF.PY

Cada jugador ejecuta el archivo para conectarse al juego pasandole como argumento la direccion ip del ordenador donde se haya ejecutado salaf.py.

Las clase player, sword y target se inicializan solo con los atributos necesarios para la creación de sus sprites correspondientes.

La clase Game actualiza todas las clases según la información recibida de sala. 

Para mostrar por pantalla el juego, generamos la clase Display que controlla todos los sprites juntandolos en un grupo all_sprites. El método refresh actualiza todos los sprites con respecto a la información que tiene en ese momento las clases player, sword y target, previamente actualizada por la clase Game.
Utiliza el método analyse_events que recibe la información de las teclas presionadas, controla también los collide entre los sprites, tanto collide entre sword y target como entre dos swords; y devuelve esta lista de eventos para ser enviada a la sala.

### SWORD_THROW.PY

Contiene nuestra version inicial de un solo jugador, sin el módulo multiprocessing para familiarizarnos con pygame. Tiene las mismas funciones y movimientos que la versión final
excepto aquellas de las que se encargan de las interacciones entre dos jugadores.


