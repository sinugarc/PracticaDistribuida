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
Existe una clase para jugador, espada y diana aparte de la clase general Game que inicializa las clase anteriores y controla el juego.
Actualiza el score según la información transmitida a través del gameinfo.


SWORD_THROW.PY

Contiene una version de un solo jugador, sin el módulo multiprocessing
Para familiarizarnos con pygame. Tiene las mismas funciones y movimientos que la versión final
excepto aquellas de las que se encargan de las interacciones entre dos jugadores.

