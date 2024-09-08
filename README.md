# roguelike_cli
Un juego Roguelike en consola que implementa hilos.

## Como jugar?
El simbolo del jugador es el siguiente:
```
X
```
Los controles para moverse en el juego son los siguientes:
```
w - arriba
a - izquierda
s - abajo
d - derecha
```
Utiliza los controles e intenta llegar hacia el enemigo.
```
O
```
Una vez hayas llegado al enemigo con pasar encima de el es suficiente para eliminarlo.
Despues es necesario dirigirse hacia la puerta.
```
⊱
```

## Dónde se implementan los hilos?
Hay dos hilos que se estan ejecutando:
```
terrain_gen_thread
gameplay_loop_thread
```
El primero es para la generación de la tierra del mapa añadiendo los siguientes simbolos de forma aleatoria: "~", "^", ".", "Y", "T".
El segunddo es el que se encarga del ciclo de la partida y en verificar si ya fue ganada.
En el main_gameplay() se verifica si estos hilos siguen activos y se imprime el resultado, de igual forma en el hilo de la generación de terrenos se verifica cuando se va a dormir el hilo.

## Ejecución

Para correr el programa es necesario ejecutar el siguiente archivo.
```
python main.py
```
Se encuentra dentro de la carpeta ASCIIPY con el siguiente comando se puede acceder a esta mediante consola.
```
cd ASCIIPY
```

## Screenshots

![App Screenshot](https://github.com/Valeria-Lee/roguelike_cli/blob/main/ss_09_07_24)

