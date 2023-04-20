# PracticaDistribuida


SALA:
Hacer dos players 

Cambio de throw de sword: añadir clase bullet
Cambio de nombres ball/player etc
move_sword (lanzar bullet bullseye:cambio de puntuaciones o fuera de rango)
Falta el def player con comandos

PLAYER
Falta el angulo https://www.youtube.com/watch?v=5M_-cJP5rk8
animaciones y graficos


MEJORAS
-Un sprite que reduzca o aumente la velocidad de los targets
-Un sprite que aumente el tamaño de los swords
-Un sprite que protecta el target( shield)



SALA: Listener (acepta dos clients:players)
- class con pos y funciones de mover
-Game con manager y lista de objetos, movimientos con locks y get_info
-Player con connection

PLAYER:Client
-class con parametros y set_pos
-class game con lista de objetos y update segun get_info
-sprites (no funciones de moviento, solo update segun get_pos de los objetos anteriores)
-display (analyse events, teclas, graficos, ...)
