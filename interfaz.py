import pygame
from config import *


def dibujar_matriz(pantalla, matriz, inicio_x, inicio_y, ocultar, tam_casilla):
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


def dibujar_boton(pantalla, rect, texto, fuente, mouse_pos):
    color = COLOR_BOTON_HOVER if rect.collidepoint(mouse_pos) else COLOR_BOTON
    pygame.draw.rect(pantalla, color, rect, border_radius=5)
    texto_render = fuente.render(texto, True, COLOR_TEXTO_BLANCO)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)

def menu_nivel(pantalla, fuente, ancho_ventana, alto_ventana):
    botones = {
        "facil": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 - 60, 300, 50),
        "medio": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2, 300, 50),
        "dificil": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 + 60, 300, 50),
        "volver": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 + 130, 300, 50)
    }
    while True:
        pantalla.fill(COLOR_FONDO)
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for nivel, rect in botones.items():
                    if rect.collidepoint(evento.pos):
                        return None if nivel == "volver" else nivel
        texto_titulo = fuente.render("Seleccione dificultad", True, COLOR_TEXTO_BLANCO)
        pantalla.blit(texto_titulo, (ancho_ventana//2 - texto_titulo.get_width()//2, 50))
        for nivel, rect in botones.items():
            texto_btn = nivel.capitalize() if nivel != "volver" else "Volver"
            dibujar_boton(pantalla, rect, texto_btn, fuente, mouse_pos)
        pygame.display.flip()

import os

def mostrar_puntajes(pantalla, fuente, ancho_ventana, alto_ventana):
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
            texto_puntaje = fuente.render(f"{i+1}. {nick}: {punt}", True, COLOR_TEXTO_BLANCO)
            pantalla.blit(texto_puntaje, (ancho_ventana//2 - texto_puntaje.get_width()//2, 100 + i * 40))

        color = COLOR_BOTON_HOVER if boton_volver.collidepoint(mouse_pos) else COLOR_BOTON
        pygame.draw.rect(pantalla, color, boton_volver, border_radius=5)
        texto_btn = fuente.render("Volver", True, COLOR_TEXTO_BLANCO)
        texto_rect = texto_btn.get_rect(center=boton_volver.center)
        pantalla.blit(texto_btn, texto_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
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
    color = COLOR_BOTON_HOVER if boton_rect.collidepoint(mouse_pos) else COLOR_BOTON
    pygame.draw.rect(pantalla, color, boton_rect, border_radius=6)

    texto = fuente.render("Reiniciar", True, COLOR_TEXTO_BLANCO)
    texto_rect = texto.get_rect(center=boton_rect.center)
    pantalla.blit(texto, texto_rect)

    return boton_rect

def pedir_nick(pantalla, fuente_general, sonido_activado) -> str:
    if not sonido_activado:
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
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                else:
                    if len(entrada) < 20:
                        entrada += evento.unicode

        pygame.display.flip()
        clock.tick(30)

    if entrada.strip() != "":
        resultado = entrada.strip()

    return resultado


def guardar_puntaje(nick: str, puntaje: int):
    with open("puntajes.txt", "a", encoding="utf-8") as f:
        f.write(f"{nick},{puntaje}\n")
