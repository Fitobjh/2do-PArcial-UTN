def crear_matriz(tamaño:int) -> list:
    matriz = []
    for i in range(tamaño):
        fila = []
        for j in range(tamaño):
            fila.append(0)
        matriz.append(fila)
    return matriz

def obtener_tamaño(nivel:str) -> int:
    tamaño = 10
    if nivel == "medio":
        tamaño = 20
    elif nivel == "dificil":
        tamaño = 40
    return tamaño

def obtener_multiplicador(nivel:str) -> int:
    mult = 1
    if nivel == "medio":
        mult = 2
    elif nivel == "dificil":
        mult = 3
    return mult

def obtener_tamaño_casilla(nivel:str) -> int:
    tam = 24
    if nivel == "medio":
        tam = 19
    elif nivel == "dificil":
        tam = 14
    return tam

