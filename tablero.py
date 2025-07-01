import random

def colocar_barcos(matriz:list, mult:int) -> None:
    barcos = [
        [4 * mult, 1],  #submarinos(1 casilla)
        [3 * mult, 2],  #destructores(2 casillas)
        [2 * mult, 3],  #cruceros(3 casillas)
        [1 * mult, 4]   #acorazado(4 casillas)
    ]
    filas = len(matriz)
    columnas = len(matriz[0])
    
    for i in range(len(barcos)):
        cantidad = barcos[i][0]
        tamaño_barco = barcos[i][1]
        
        for j in range(cantidad):
            colocado = False
            
            while not colocado:
                sentido = random.choice(["horizontal", "vertical"])
                
                if sentido == "horizontal":
                    fila = random.randint(0, filas - 1)
                    columna = random.randint(0, columnas - tamaño_barco)
                    libre = True
                    for k in range(tamaño_barco):
                        if matriz[fila][columna + k] != 0:
                            libre = False
                    if libre:
                        for k in range(tamaño_barco):
                            matriz[fila][columna + k] = 1
                        colocado = True
                else: #vertical
                    fila = random.randint(0, filas - tamaño_barco)
                    columna = random.randint(0, columnas - 1)
                    libre = True
                    for k in range(tamaño_barco):
                        if matriz[fila + k][columna] != 0:
                            libre = False
                    if libre:
                        for k in range(tamaño_barco):
                            matriz[fila + k][columna] = 1
                        colocado = True



def barco_hundido(tablero, fila_inicial, columna_inicial):
    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba
    casillas_visitadas = []
    casillas_por_visitar = []
    casillas_por_visitar.append((fila_inicial, columna_inicial))
    tamaño_barco = 0
    esta_hundido = True

    while len(casillas_por_visitar) > 0:
        casilla_actual = casillas_por_visitar[0]
        casillas_por_visitar.pop(0)
        fila_actual = casilla_actual[0]
        columna_actual = casilla_actual[1]

        # Verificar si ya visitamos esta casilla
        ya_visitada = False
        for casilla in casillas_visitadas:
            if casilla[0] == fila_actual and casilla[1] == columna_actual:
                ya_visitada = True
                break

        # Si no fue visitada y es parte tocada del barco (2)
        if not ya_visitada and tablero[fila_actual][columna_actual] == 2:
            casillas_visitadas.append((fila_actual, columna_actual))
            tamaño_barco = tamaño_barco + 1

            # Chequear casillas vecinas (derecha, abajo, izquierda, arriba)
            for i in range(len(direcciones)):
                fila_vecina = fila_actual + direcciones[i][0]
                columna_vecina = columna_actual + direcciones[i][1]

                # Revisar que la casilla vecina esté dentro del tablero
                if fila_vecina >= 0 and fila_vecina < len(tablero) and \
                   columna_vecina >= 0 and columna_vecina < len(tablero[0]):

                    # Si la casilla vecina también está tocada (2), la agregamos para visitar
                    if tablero[fila_vecina][columna_vecina] == 2:
                        casillas_por_visitar.append((fila_vecina, columna_vecina))

    # Verificar si alrededor del barco hay alguna parte sin tocar (1)
    for casilla in casillas_visitadas:
        fila_casilla = casilla[0]
        columna_casilla = casilla[1]
        for i in range(len(direcciones)):
            fila_vecina = fila_casilla + direcciones[i][0]
            columna_vecina = columna_casilla + direcciones[i][1]

            if fila_vecina >= 0 and fila_vecina < len(tablero) and \
               columna_vecina >= 0 and columna_vecina < len(tablero[0]):

                if tablero[fila_vecina][columna_vecina] == 1:
                    esta_hundido = False

    return [esta_hundido, tamaño_barco]


def calcular_puntaje(puntaje_actual, acierto, hundido, tamaño_barco):
    nuevo_puntaje = puntaje_actual
    if acierto:
        nuevo_puntaje = nuevo_puntaje + 5
        if hundido:
            nuevo_puntaje = nuevo_puntaje + (10 * tamaño_barco)
    else:
        nuevo_puntaje = nuevo_puntaje - 1
    return nuevo_puntaje

