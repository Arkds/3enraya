import pygame as pg
import sys

# Dimensiones de la ventana y del tablero
ANCHO = 300
ALTO = 300
LINEA_ANCHO = 15
FILAS_TABLERO = 3
COLUMNAS_TABLERO = 3
TAMANO_CASILLA = ANCHO // COLUMNAS_TABLERO
RADIO_CIRCULO = TAMANO_CASILLA // 3
OFFSET_CRUZ = 50
ANCHO_CRUZ = 25
FPS = 30

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Inicializar Pygame
pg.init()

# Crear la pantalla
pantalla = pg.display.set_mode((ANCHO, ALTO))
pg.display.set_caption("Tres en Raya")

# Fuentes de texto
fuente_grande = pg.font.Font(None, 36)
fuente_pequena = pg.font.Font(None, 24)

# Función para mostrar texto
def mostrar_texto(texto, x, y, fuente):
    texto_superficie = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_superficie, (x, y))

# Función para dibujar el menú principal
def dibujar_menu():
    pantalla.fill(NEGRO)
    mostrar_texto("TRES EN RAYA", 50, 50, fuente_grande)

    mostrar_texto("Selecciona tu símbolo:", 50, 150, fuente_pequena)

    # Botones para elegir el símbolo
    pg.draw.rect(pantalla, ROJO, (50, 200, 100, 50))
    pg.draw.rect(pantalla, AZUL, (150, 200, 100, 50))

    mostrar_texto("X", 85, 215, fuente_grande)
    mostrar_texto("O", 185, 215, fuente_grande)

# Función para dibujar el tablero de juego
def dibujar_tablero():
    pantalla.fill(NEGRO)
    dibujar_lineas()
    dibujar_figuras()

# Función para dibujar las líneas del tablero
def dibujar_lineas():
    pg.draw.line(pantalla, BLANCO, (0, TAMANO_CASILLA), (ANCHO, TAMANO_CASILLA), LINEA_ANCHO)
    pg.draw.line(pantalla, BLANCO, (0, 2 * TAMANO_CASILLA), (ANCHO, 2 * TAMANO_CASILLA), LINEA_ANCHO)
    pg.draw.line(pantalla, BLANCO, (TAMANO_CASILLA, 0), (TAMANO_CASILLA, ALTO), LINEA_ANCHO)
    pg.draw.line(pantalla, BLANCO, (2 * TAMANO_CASILLA, 0), (2 * TAMANO_CASILLA, ALTO), LINEA_ANCHO)

# Función para dibujar las figuras (X y O) en el tablero
def dibujar_figuras():
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] == 1:
                pg.draw.circle(pantalla, ROJO, (col * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), RADIO_CIRCULO, LINEA_ANCHO)
            elif tablero[fila][col] == 2:
                texto_superficie = fuente_grande.render("X", True, AZUL)
                texto_superficie = pg.transform.scale(texto_superficie, (TAMANO_CASILLA-30, TAMANO_CASILLA-30))  # Escalar el texto
                text_rect = texto_superficie.get_rect(center=(col * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2))
                pantalla.blit(texto_superficie, text_rect)

# Función para inicializar el tablero de juego
def inicializar_tablero():
    return [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

# Función para verificar si el tablero está lleno
def esta_tablero_lleno(tablero):
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] == 0:
                return False
    return True

# Función para verificar si hay un ganador
def hay_ganador(tablero, jugador):
    for i in range(FILAS_TABLERO):
        if all(casilla == jugador for casilla in tablero[i]):
            return True
    for j in range(COLUMNAS_TABLERO):
        if all(tablero[i][j] == jugador for i in range(FILAS_TABLERO)):
            return True
    if all(tablero[i][i] == jugador for i in range(FILAS_TABLERO)):
        return True
    if all(tablero[i][FILAS_TABLERO - i - 1] == jugador for i in range(FILAS_TABLERO)):
        return True
    return False

# Función para verificar si el juego ha terminado
def test_terminal(tablero):
    return hay_ganador(tablero, 1) or hay_ganador(tablero, 2) or esta_tablero_lleno(tablero)

# Función para obtener las acciones posibles en el tablero
def acciones(tablero):
    movimientos = []
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] == 0:
                movimientos.append((fila, col))
    return movimientos

# Función para realizar un movimiento en el tablero
def resultado(tablero, accion, jugador):
    fila, col = accion
    nuevo_tablero = [fila[:] for fila in tablero]
    nuevo_tablero[fila][col] = jugador
    return nuevo_tablero

# Función para calcular la utilidad del tablero
# Función para calcular la utilidad del tablero
def utilidad(tablero):
    if hay_ganador(tablero, simbolo_maquina):
        return -1
    elif hay_ganador(tablero, simbolo_jugador):
        return 1
    elif esta_tablero_lleno(tablero):
        return 0
    else:
        return None

# Función para obtener el mejor movimiento usando Minimax
def mejor_movimiento(tablero):
    mejor_movimiento = None
    mejor_eval = float('inf')
    for accion in acciones(tablero):
        eval = minimax(resultado(tablero, accion, simbolo_maquina), True)
        if eval < mejor_eval:
            mejor_eval = eval
            mejor_movimiento = accion
    return mejor_movimiento

# Algoritmo Minimax para determinar el mejor movimiento
def minimax(tablero, maximizando_jugador):
    if test_terminal(tablero):
        return utilidad(tablero)

    if maximizando_jugador:
        max_eval = float('-inf')
        for accion in acciones(tablero):
            eval = minimax(resultado(tablero, accion, simbolo_jugador), False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for accion in acciones(tablero):
            eval = minimax(resultado(tablero, accion, simbolo_maquina), True)
            min_eval = min(min_eval, eval)
        return min_eval


# Función para determinar qué jugador comienza
def jugador(tablero):
    count_X = sum(fila.count(simbolo_jugador) for fila in tablero)
    count_O = sum(fila.count(simbolo_maquina) for fila in tablero)
    if count_X <= count_O:
        return simbolo_jugador
    else:
        return simbolo_maquina

# Función para mostrar la pantalla de resultado
def mostrar_resultado(resultado_texto):
    pantalla.fill(NEGRO)
    
    if(resultado_texto == "Perdiste"):
        victoria_imagen = pg.image.load("jajaja.png")
        victoria_imagen = pg.transform.scale(victoria_imagen, (90, 80))
        pantalla.blit(victoria_imagen, (100, 100))
    elif(resultado_texto == "Ganaste"):
        victoria_imagen = pg.image.load("ganaste.jpg")
        victoria_imagen = pg.transform.scale(victoria_imagen, (90, 80))
        pantalla.blit(victoria_imagen, (100, 100))
    else:
        victoria_imagen = pg.image.load("empate.jpg")
        victoria_imagen = pg.transform.scale(victoria_imagen, (300, 300))
        pantalla.blit(victoria_imagen, (0, 0))
    mostrar_texto(resultado_texto, 50, 50, fuente_grande)
    pg.draw.rect(pantalla, AZUL, (100, 200, 100, 50))
    mostrar_texto("Menú", 125, 215, fuente_pequena)

# Variable para controlar el estado del juego
estado_juego = "MENU"
simbolo_jugador = None
simbolo_maquina = None
tablero = None

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            ejecutando = False
            pg.quit()
            sys.exit()
        
        if estado_juego == "MENU":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if 50 <= mouseX <= 150 and 200 <= mouseY <= 250:
                    simbolo_jugador = 2  # X
                    simbolo_maquina = 1
                    tablero = inicializar_tablero()
                    estado_juego = "JUGANDO"
                elif 150 <= mouseX <= 250 and 200 <= mouseY <= 250:
                    simbolo_jugador = 1  # O
                    simbolo_maquina = 2
                    tablero = inicializar_tablero()
                    estado_juego = "JUGANDO"
        
        elif estado_juego == "JUGANDO":
            if evento.type == pg.MOUSEBUTTONDOWN or simbolo_maquina == jugador(tablero):
                if simbolo_jugador == jugador(tablero):
                    mouseX, mouseY = pg.mouse.get_pos()
                    if not test_terminal(tablero):
                        fila = mouseY // TAMANO_CASILLA
                        columna = mouseX // TAMANO_CASILLA
                        if tablero[fila][columna] == 0:
                            tablero = resultado(tablero, (fila, columna), simbolo_jugador)
                            if test_terminal(tablero):
                                if utilidad(tablero) == 1:
                                    resultado_texto = "Ganaste"
                                elif utilidad(tablero) == -1:
                                    resultado_texto = "Perdiste"
                                else:
                                    resultado_texto = "Empate"
                                estado_juego = "RESULTADO"
                else:
                    if not test_terminal(tablero):
                        movimiento = mejor_movimiento(tablero)
                        tablero = resultado(tablero, movimiento, simbolo_maquina)
                        if test_terminal(tablero):
                            if utilidad(tablero) == 1:
                                resultado_texto = "Ganaste"
                            elif utilidad(tablero) == -1:
                                resultado_texto = "Perdiste"
                            else:
                                resultado_texto = "Empate"
                            estado_juego = "RESULTADO"

        elif estado_juego == "RESULTADO":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if 100 <= mouseX <= 200 and 200 <= mouseY <= 250:
                    estado_juego = "MENU"

    if estado_juego == "MENU":
        dibujar_menu()

    elif estado_juego == "JUGANDO":
        dibujar_tablero()
        dibujar_figuras()

    elif estado_juego == "RESULTADO":
        mostrar_resultado(resultado_texto)

    pg.display.update()
    pg.time.Clock().tick(FPS)
