def crear_matriz(tamaño:int) -> list:
    """
    Crea y devuelve una matriz cuadrada de tamaño x tamaño con todos sus elementos en cero
    
    Parametros:
    tamaño (int): cantidad de filas y columnas de la matriz
    
    Devuelve:
    list: matriz bidimensional con ceros
    """
    matriz = []
    for i in range(tamaño):
        fila = []
        for j in range(tamaño):
            fila.append(0)
        matriz.append(fila)
    return matriz

def obtener_tamaño(nivel:str) -> int:
    """
    Devuelve el tamaño de la matriz segun el nivel elegido
    
    Parametros:
    nivel (str): nivel de dificultad puede ser facil medio o dificil
    
    Devuelve:
    int: tamaño de la matriz 10 para facil 20 para medio y 40 para dificil
    """
    tamaño = 10
    if nivel == "medio":
        tamaño = 20
    elif nivel == "dificil":
        tamaño = 40
    return tamaño

def obtener_multiplicador(nivel:str) -> int:
    """
    Devuelve un multiplicador segun el nivel elegido
    
    Parametros:
    nivel (str): nivel de dificultad puede ser facil medio o dificil
    
    Devuelve:
    int: multiplicador 1 para facil 2 para medio y 3 para dificil
    """
    mult = 1
    if nivel == "medio":
        mult = 2
    elif nivel == "dificil":
        mult = 3
    return mult

def obtener_tamaño_casilla(nivel:str) -> int:
    """
    Devuelve el tamaño de cada casilla segun el nivel elegido
    
    Parametros:
    nivel (str): nivel de dificultad puede ser facil medio o dificil
    
    Devuelve:
    int: tamaño de la casilla 24 para facil 19 para medio y 14 para dificil
    """
    tam = 24
    if nivel == "medio":
        tam = 19
    elif nivel == "dificil":
        tam = 14
    return tam
