import pygame
import os
from constantes import *


def dibujar_matriz(pantalla:pygame.Surface, matriz:list, inicio_x:int, inicio_y:int, ocultar:bool, tam_casilla:int):
    """
    Dibuja una matriz de juego en la pantalla usando rectángulos coloreados según el valor de cada casilla.
    
    Parámetros:
    pantalla (pygame.Surface): superficie de Pygame donde se dibujará la matriz.
    matriz (list): matriz bidimensional que representa el estado del juego, donde:
        - 0: agua (casilla vacía)
        - 1: parte de barco no visible si `ocultar` es True
        - 2: parte de barco tocada (acierto)
        - 3: casilla marcada como fallo
    inicio_x (int): coordenada X (en píxeles) donde comienza el dibujo de la matriz.
    inicio_y (int): coordenada Y (en píxeles) donde comienza el dibujo de la matriz.
    ocultar (bool): si es True, las casillas con valor 1 (barcos) no se muestran (se dibujan como agua).
    tam_casilla (int): tamaño en píxeles de cada casilla cuadrada que se dibuja.
    
    Descripción:
    Recorre la matriz y dibuja un rectángulo en la posición correspondiente para cada casilla,
    con un color que depende del valor y del estado de `ocultar`.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            y = inicio_y + i * (tam_casilla + MARGEN)
            x = inicio_x + j * (tam_casilla + MARGEN)
            
            valor = matriz[i][j]
            
            # Por defecto: agua
            color = COLOR_CASILLA_AGUA
            
            if valor == 1 and not ocultar:
                color = COLOR_CASILLA_BARCOS
            elif valor == 2:
                color = COLOR_ACIERTO
            elif valor == 3:
                color = COLOR_FALLO
                
            pygame.draw.rect(pantalla, color, (x, y, tam_casilla, tam_casilla))


def dibujar_boton(pantalla:pygame.Surface, rect:pygame.rect, texto:str, fuente:pygame.font.Font, mouse_pos:tuple):
    """
    Dibuja un boton en la pantalla con cambio de color al pasar el mouse por encima.
    
    Parametros:
    pantalla (pygame.Surface): superficie donde se dibuja el boton.
    rect (pygame.Rect): rectangulo que define la posicion y tamaño del boton.
    texto (str): texto que se muestra en el boton.
    fuente (pygame.font.Font): fuente usada para renderizar el texto.
    mouse_pos (tuple): posicion actual del mouse (x, y).
    
    Descripcion:
    Si el puntero del mouse esta sobre el boton, cambia el color a COLOR_BOTON_SECUNDARIO,
    sino usa COLOR_BOTON. Luego dibuja el rectangulo con bordes redondeados,
    renderiza el texto centrado y lo dibuja encima del boton.
    """
    if rect.collidepoint(mouse_pos):
        color = COLOR_BOTON_SECUNDARIO
    else:
        color = COLOR_BOTON
        
    pygame.draw.rect(pantalla, color, rect, border_radius=5)
    texto_render = fuente.render(texto, True, COLOR_TEXTO_BLANCO)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)

def menu_nivel(pantalla:pygame.Surface, fuente:pygame.font.Font, ancho_ventana:int, alto_ventana:int)->None|str:
    """
    Muestra un menú gráfico para seleccionar el nivel de dificultad o volver.
    
    Parámetros:
    - pantalla (pygame.Surface): La superficie donde se dibuja el menú.
    - fuente (pygame.font.Font): La fuente utilizada para renderizar textos.
    - ancho_ventana (int): Ancho de la ventana en píxeles.
    - alto_ventana (int): Alto de la ventana en píxeles.
    
    Devuelve:
    - str o None: Retorna el nivel seleccionado como cadena: "facil", "medio" o "dificil".
        Retorna None si se cierra la ventana o se selecciona "volver".
    """
    botones = {
        "facil": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 - 60, 300, 50),
        "medio": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2, 300, 50),
        "dificil": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 + 60, 300, 50),
        "volver": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 + 130, 300, 50)
    }
    
    resultado = None
    ejecutar = True
    while ejecutar:
        pantalla.fill(COLOR_FONDO)
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                resultado = None
                ejecutar = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for nivel, rect in botones.items():
                    if rect.collidepoint(evento.pos):
                        if nivel == "volver":
                            resultado = None
                        else:
                            resultado = nivel
                        ejecutar = False
                        break
                if not ejecutar:
                    break
        
        texto_titulo = fuente.render("Seleccione dificultad", True, COLOR_TEXTO_BLANCO)
        pantalla.blit(texto_titulo, (ancho_ventana//2 - texto_titulo.get_width()//2, 50))
        
        for nivel, rect in botones.items():
            if nivel == "volver":
                texto_btn = "Volver"
            else:
                texto_btn = nivel.capitalize()
            dibujar_boton(pantalla, rect, texto_btn, fuente, mouse_pos)
        
        pygame.display.flip()
    
    return resultado



def mostrar_puntajes(pantalla:pygame.Surface, fuente:pygame.font.Font, ancho_ventana:int, alto_ventana:int):
    """
    Muestra en pantalla los 3 mejores puntajes leídos desde un archivo "puntajes.txt" y un botón para volver.
    
    Parámetros:
    - pantalla (pygame.Surface): Superficie donde se dibuja el menú.
    - fuente (pygame.font.Font): Fuente para renderizar textos.
    - ancho_ventana (int): Ancho de la ventana en píxeles.
    - alto_ventana (int): Alto de la ventana en píxeles.
    
    No devuelve nada. La función muestra la ventana y se cierra cuando se presiona "Volver" o se cierra la ventana.
    """
    
    puntajes = []
    
    if os.path.exists("puntajes.txt"):
        archivo = open("puntajes.txt", "r", encoding="utf-8")
        for linea in archivo:
            if ',' in linea:
                partes = linea.strip().split(",", 1)
                if len(partes) == 2:
                    nick = partes[0]
                    punt_str = partes[1]
                    if punt_str.isdigit():
                        puntaje = int(punt_str)
                        puntajes.append([nick, puntaje])
        archivo.close()
        
    # Ordenar manualmente de mayor a menor sin lambda
    for i in range(len(puntajes)):
        for j in range(i + 1, len(puntajes)):
            if puntajes[j][1] > puntajes[i][1]:
                temp = puntajes[i]
                puntajes[i] = puntajes[j]
                puntajes[j] = temp
                
    # Solo los 3 mejores
    mejores = []
    for i in range(len(puntajes)):
        if i < 3:
            mejores.append(puntajes[i])
        else:
            break
        
    boton_volver = pygame.Rect(ancho_ventana//2 - 100, alto_ventana - 80, 200, 50)
    
    corriendo = True
    while corriendo:
        pantalla.fill(COLOR_FONDO)
        mouse_pos = pygame.mouse.get_pos()
        
        titulo = fuente.render("Top 3 Puntajes", True, COLOR_TEXTO_BLANCO)
        pantalla.blit(titulo, ((ancho_ventana - titulo.get_width()) // 2, 40))
        
        for i in range(len(mejores)):
            nick = mejores[i][0]
            punt = mejores[i][1]
            texto_puntaje = fuente.render(str(i + 1) + ". " + nick + ": " + str(punt), True, COLOR_TEXTO_BLANCO)
            pantalla.blit(texto_puntaje, (ancho_ventana//2 - texto_puntaje.get_width()//2, 100 + i * 40))
            
        if boton_volver.collidepoint(mouse_pos):
            color = COLOR_BOTON_SECUNDARIO
        else:
            color = COLOR_BOTON
        
        pygame.draw.rect(pantalla, color, boton_volver, border_radius=5)
        
        texto_btn = fuente.render("Volver", True, COLOR_TEXTO_BLANCO)
        texto_rect = texto_btn.get_rect()
        texto_rect.center = boton_volver.center
        pantalla.blit(texto_btn, texto_rect)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            else:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if boton_volver.collidepoint(evento.pos):
                            corriendo = False
                            
        pygame.display.flip()


def dibujar_boton_reiniciar(pantalla, fuente, mouse_pos, centro_x: int, abajo_y: int) -> pygame.Rect:
    """
    Dibuja el botón 'Reiniciar' debajo del tablero.
    
    Parámetros:
        pantalla (pygame.Surface): La pantalla de juego.
        fuente (pygame.font.Font): Fuente para el texto del botón.
        mouse_pos (tuple): Posición actual del mouse.
        centro_x (int): Centro horizontal del tablero (para centrar el botón).
        abajo_y (int): Coordenada vertical donde termina el tablero (para ubicar el botón debajo).
        
    Retorna:
        pygame.Rect: Rectángulo del botón para detección de clics.
    """
    boton_ancho = 140
    boton_alto = 40
    x = centro_x - boton_ancho // 2
    y = abajo_y + 20  # 20px debajo del tablero
    
    boton_rect = pygame.Rect(x, y, boton_ancho, boton_alto)
    if boton_rect.collidepoint(mouse_pos):
        color = COLOR_BOTON_SECUNDARIO
    else:
        color = COLOR_BOTON
    pygame.draw.rect(pantalla, color, boton_rect, border_radius=6)
    
    texto = fuente.render("Reiniciar", True, COLOR_TEXTO_BLANCO)
    texto_rect = texto.get_rect(center=boton_rect.center)
    pantalla.blit(texto, texto_rect)
    
    return boton_rect

def pedir_nick(pantalla:pygame.Surface, fuente_general:pygame.font.Font, sonido_activado:bool) -> str:
    """
    Muestra una pantalla para que el usuario ingrese su nombre (nick).
    Permite edición básica y confirma con ENTER.
    
    Parámetros:
    - pantalla (pygame.Surface): Superficie donde se dibuja la interfaz.
    - fuente_general (pygame.font.Font): Fuente para mostrar el texto ingresado.
    - sonido_activado (bool): Indica si la música está activada; si está apagada, pausa la música.
    
    Devuelve:
    - str: El nombre ingresado por el usuario. Si no se ingresa nada, devuelve "SinNombre".
    """
    
    if sonido_activado == False:
        pygame.mixer.music.pause()
        
    entrada = ""
    activo = True
    clock = pygame.time.Clock()
    
    ancho_ventana, alto_ventana = pantalla.get_size()
    
    tamaño_fuente = max(18, alto_ventana // 20)  # tamaño dinámico mínimo 18
    fuente = pygame.font.SysFont(None, tamaño_fuente)
    
    resultado = "SinNombre"
    
    while activo:
        pantalla.fill(COLOR_FONDO)
        
        texto = fuente.render("Ingresá tu nombre (ENTER para confirmar):", True, COLOR_TEXTO_BLANCO)
        input_box = fuente_general.render(entrada, True, COLOR_TEXTO_BLANCO)
        
        texto_x = (ancho_ventana - texto.get_width()) // 2
        texto_y = alto_ventana // 3
        input_x = (ancho_ventana - input_box.get_width()) // 2
        input_y = texto_y + tamaño_fuente + 10
        
        pantalla.blit(texto, (texto_x, texto_y))
        pantalla.blit(input_box, (input_x, input_y))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                activo = False
            else:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        activo = False
                    else:
                        if evento.key == pygame.K_BACKSPACE:
                            entrada = entrada[:-1]
                        else:
                            if len(entrada) < 20:
                                entrada = entrada + evento.unicode
                                
        pygame.display.flip()
        clock.tick(30)
        
    if entrada.strip() != "":
        resultado = entrada.strip()
        
    return resultado


def guardar_puntaje(nick: str, puntaje: int):
    """
    Guarda un puntaje asociado a un nick en el archivo "puntajes.txt".
    
    Parámetros:
    - nick (str): Nombre o alias del jugador.
    - puntaje (int): Puntaje obtenido por el jugador.
    
    No devuelve nada. Agrega una línea al archivo con el formato "nick,puntaje".
    """
    with open("puntajes.txt", "a", encoding="utf-8") as f:
        f.write(f"{nick},{puntaje}\n")

