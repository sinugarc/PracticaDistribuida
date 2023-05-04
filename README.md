# PracticaDistribuida
Sinhue García Gil, Cristina Hernando Esperanza, Daniel Martínez Martín


      
PLAYERF.PY

Se ejecuta una vez por cada jugador, pasandole como argumento la direccion ip del ordenador donde se ejecute salaf.py.
Se asigna un side 0 ó 1 a cada jugador para diferenciar el lado. 

La clase player tiene como atributos el lado, el ángulo y la posición. El movimiento hacia arriba y abajo se controla con las teclas de Up y Down,
mientras que en la rotación, el ángulo se modifica con las flechas de los lados. Se actualizan estos datos de la clase a través del PlayerSprite.
La imagen que genera PayerSrite es el lightsaber.

La clase sword tiene como atributos el lado, el ángulo y la posición. Su análogo SwordSprite genera la imagen del laser, desde sala se inicializa fuera de pantalla 
y al ejecutarse el método throw() se lanza desde la posición de su player correspondiente.

La clase target tiene como atributos el lado y la posición en eje X y eje Y y la velocidad, que se mantendrá constante durante el juego. El TargetSprite se mueve
constantemente durante el juego rebotando en eje Y. La imagen que genera es una diana.

La clase Game actualiza todas las clases según la información recibida de sala en el formato de gameinfo.

Para mostrar por pantalla el juego, generamos la clase Display que controlla todos los sprites juntandolos en un grupo all_sprites. Utiliza el método analyse_events
que recibe la información de las teclas presionadas, controla también los collide entre los sprites, tanto collide entre sword y target como entre dos swords. 


SALAF.PY

Es el archivo "broker" que controla los movimientos de los jugadores, recibiendo información y enviandola a los respectivos players.

La clase player inicializa con los atributos de posición y lado, el ángulo así como un booleano que nos permitirá saber si se ha disparado o no.
Los métodos dentro de la clase player se encargan de actualizar la posición y ángulo.

La clase sword se inicializa en una posición fuera de la pantalla, con velocidad 0 y ángulo 0. El método update actualiza la posicion del sword si se ha lanzado y comprueba si se ha salido del tablero; devolviendo un booleano indicando si se ha salido del tablero. El método throw actualiza la posición y ángulo desde donde se lanza aumentando la velocidad para que se mueva.

La clase target se inicializa con el lado, la posición y la velocidad. El método update actualiza la posición en y comprobando que no se salga del área de juego.

La clase Game se inicializa generando listas compartidas de jugadores, dianas, espadas y la puntuación. También crea una variable running y un semáforo lock que garantice la exclusión mutua de los elementos compartidos. Tiene métodos para actualizar la información. El método ger_info crea un diccionario con la información necesaria para enviarsela a los jugadores. Los collide se encaragan de reinicializar la información de los swords y actualizar la puntuación si es necesario. El método throw comprueba si el jugador ya ha lanzado  y si no llama al método throw de la clase sword con la posición y ángulo del jugador.

Fuera de las clases en la función player se recibe la información de los jugadores y ejecuta los métodos de la clase Game acorde a dicha información. Además se encarga de llamar a los métodos que actualizan la posición del target y sword, luego envía la información actualizada a los jugadores.

SWORD_THROW.PY

Contiene una version de un solo jugador, sin el módulo multiprocessing
Para familiarizarnos con pygame. Tiene las mismas funciones y movimientos que la versión final
excepto aquellas de las que se encargan de las interacciones entre dos jugadores.

