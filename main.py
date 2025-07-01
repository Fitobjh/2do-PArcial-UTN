# main.py
import pygame
import pygame.mixer as mixer
from config import *
from utilidades import *
from tablero import colocar_barcos,calcular_puntaje,barco_hundido
from interfaz import *

def jugar_battleship(nivel, sonido_activado):
    pygame.init()
    mixer.init()
    
    if sonido_activado:
        mixer.music.load('2do Parcial/Multimedia/Vanished.mp3')
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)
    
    disparo_acertado_sonido = mixer.Sound("2do Parcial/Multimedia/Explosion.mp3")
    disparo_errado_sonido = mixer.Sound("2do Parcial/Multimedia/errado.mp3")

    tamaño = obtener_tamaño(nivel)
    mult = obtener_multiplicador(nivel)
    tam_casilla = obtener_tamaño_casilla(nivel)

    enemigo = crear_matriz(tamaño)
    colocar_barcos(enemigo, mult)

    ancho_matriz = tamaño * tam_casilla + (tamaño - 1) * MARGEN
    alto_matriz = tamaño * tam_casilla + (tamaño - 1) * MARGEN

    margen_superior = 60
    ancho_ventana = ancho_matriz + 100
    alto_ventana = alto_matriz + margen_superior + 40

    pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
    pygame.display.set_caption("Battleship")

    fondo = pygame.image.load('2do Parcial/Multimedia/mar.jpg')
    fondo_ajustado = pygame.transform.scale(fondo, (ancho_ventana, alto_ventana))

    mixer.music.load('2do Parcial/Multimedia/Vanished.mp3')
    mixer.music.set_volume(0.4)
    mixer.music.play()

    fuente = pygame.font.SysFont(None, 28)
    inicio_x = (ancho_ventana - ancho_matriz) // 2
    inicio_y = (alto_ventana - alto_matriz) // 2

    nick = pedir_nick(pantalla, fuente,sonido_activado)

    corriendo = True
    puntaje = 0

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_reiniciar.collidepoint(evento.pos):
                    enemigo = crear_matriz(tamaño)
                    colocar_barcos(enemigo, mult)
                    puntaje = 0
                else:
                    mouse_x, mouse_y = evento.pos
                    col = (mouse_x - inicio_x) // (tam_casilla + MARGEN)
                    fila = (mouse_y - inicio_y) // (tam_casilla + MARGEN)

                    if 0 <= fila < tamaño and 0 <= col < tamaño:
                        valor_casilla = enemigo[fila][col]
                        if valor_casilla == 1:
                            enemigo[fila][col] = 2
                            hundido, tamaño_barco = barco_hundido(enemigo, fila, col)
                            puntaje = calcular_puntaje(puntaje, True, hundido, tamaño_barco)
                            disparo_acertado_sonido.play()
                        elif valor_casilla == 0:
                            enemigo[fila][col] = 3
                            puntaje = calcular_puntaje(puntaje, False, False, 0)
                            disparo_errado_sonido.play() 

        pantalla.blit(fondo_ajustado, (0, 0))
        inicio_x = (ancho_ventana - ancho_matriz) // 2
        inicio_y = (alto_ventana - alto_matriz) // 2
        centro_x = ancho_ventana // 2
        abajo_y = inicio_y + alto_matriz

        dibujar_matriz(pantalla, enemigo, inicio_x, inicio_y, True, tam_casilla)
        mouse_pos = pygame.mouse.get_pos()
        boton_reiniciar = dibujar_boton_reiniciar(pantalla, fuente, mouse_pos, centro_x, abajo_y)

        texto_puntaje = fuente.render(f"Puntaje: {puntaje:04}", True, COLOR_TEXTO_BLANCO)
        pantalla.blit(texto_puntaje, (20, 20))

        pygame.display.flip()

        # **Chequeo si quedan barcos sin tocar (valor 1)**
        quedan_barcos = False
        for fila_matriz in enemigo:
            if 1 in fila_matriz:
                quedan_barcos = True
                break
        
        if not quedan_barcos:
            # Guardar puntaje
            guardar_puntaje(nick, puntaje)
            # Terminar el juego y volver al menú
            corriendo = False



def main():
    pygame.init()
    mixer.init()

    ancho_ventana = 600
    alto_ventana = 400
    pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
    pygame.display.set_caption("Battleship - Menu Principal")
    fuente = pygame.font.SysFont(None, 36)

    nivel_seleccionado = None
    sonido_activado = True

    icono = pygame.image.load('2do Parcial/Multimedia/batalla_naval.jpg')
    pygame.display.set_icon(icono)
    # Cargar música y reproducirla (con volumen)
    mixer.music.load('2do Parcial/Multimedia/Vanished.mp3')
    mixer.music.set_volume(0.4)
    mixer.music.play(-1)  # Loop infinito

    botones_menu = {
        "nivel": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 - 90, 300, 50),
        "jugar": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 - 20, 300, 50),
        "puntajes": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 + 50, 300, 50),
        "sonido": pygame.Rect(ancho_ventana//2 - 150, alto_ventana//2 + 120, 140, 50),  # Botón sonido
        "salir": pygame.Rect(ancho_ventana//2 + 10, alto_ventana//2 + 120, 140, 50),
    }

    corriendo = True
    while corriendo:
        pantalla.fill(COLOR_FONDO)
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botones_menu["nivel"].collidepoint(evento.pos):
                    nivel = menu_nivel(pantalla, fuente, ancho_ventana, alto_ventana)
                    if nivel:
                        nivel_seleccionado = nivel
                elif botones_menu["jugar"].collidepoint(evento.pos):
                    if nivel_seleccionado is None:
                        aviso = fuente.render("Debe seleccionar nivel primero!", True, (255, 0, 0))
                        pantalla.blit(aviso, (ancho_ventana//2 - aviso.get_width()//2, alto_ventana - 60))
                        pygame.display.flip()
                        pygame.time.delay(1500)
                    else:
                        jugar_battleship(nivel_seleccionado, sonido_activado)
                        pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))  # Reset tamaño ventana
                elif botones_menu["puntajes"].collidepoint(evento.pos):
                    mostrar_puntajes(pantalla, fuente, ancho_ventana, alto_ventana)
                elif botones_menu["sonido"].collidepoint(evento.pos):
                    # Cambiar estado sonido
                    sonido_activado = not sonido_activado
                    if sonido_activado:
                        mixer.music.unpause()
                    else:
                        mixer.music.pause()
                elif botones_menu["salir"].collidepoint(evento.pos):
                    corriendo = False

        # Dibujar botones
        for nombre, rect in botones_menu.items():
            texto = nombre.capitalize()
            if nombre == "sonido":
                texto = "Sonido: ON" if sonido_activado else "Sonido: OFF"
            dibujar_boton(pantalla, rect, texto, fuente, mouse_pos)

        texto_nivel = "Nivel: " + (nivel_seleccionado.capitalize() if nivel_seleccionado else "No seleccionado")
        pantalla.blit(fuente.render(texto_nivel, True, COLOR_TEXTO_BLANCO), (20, 20))
        pygame.display.flip()

    pygame.quit()
