import pygame
from utils import cargar_json, cargar_imagen, salir_juego
from diseño import obtener_fuentes, dibujar_pregunta, dibujar_plantas, Boton

pygame.init()
ANCHO, ALTO = 1000, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Adivina tu planta")

# -------------------
# CARGA DE DATOS
# -------------------
preguntas = cargar_json("preguntas.json")
plantas_raw = cargar_json("plantas.json")

# Agregar imágenes ya cargadas
plantas = []
for planta in plantas_raw:
    img = cargar_imagen(planta["imagen"], tamaño=(100, 100))
    if img:
        plantas.append({**planta, "imagen": img})

# -------------------
# VARIABLES DE ESTADO
# -------------------
fuentes = obtener_fuentes()
indice_pregunta = 0
tachadas = set()

# -------------------
# BOTONES DE OPCIONES
# -------------------
def crear_boton_opcion(texto, x, y, ancho, alto, fuente, accion):
    return Boton(x, y, ancho, alto, texto, accion, fuente)

def generar_botones_opciones(pregunta_actual, fuente):
    opciones = pregunta_actual["opciones"]
    botones = []
    ancho_total = len(opciones) * 180 + (len(opciones) - 1) * 20
    inicio_x = (ANCHO - ancho_total) // 2

    for i, opcion in enumerate(opciones):
        x = inicio_x + i * 200
        def accion(op=opcion): filtrar_plantas(op)
        boton = crear_boton_opcion(opcion.capitalize(), x, ALTO - 80, 180, 50, fuente, accion)
        botones.append(boton)
    return botones

# -------------------
# FILTRADO DE PLANTAS
# -------------------
def filtrar_plantas(opcion_seleccionada):
    global indice_pregunta, tachadas
    if indice_pregunta >= len(preguntas):
        return

    atributo = preguntas[indice_pregunta]["atributo"]
    for planta in plantas:
        if planta["nombre"] in tachadas:
            continue
        if planta.get(atributo) != opcion_seleccionada:
            tachadas.add(planta["nombre"])

    indice_pregunta += 1
    if indice_pregunta < len(preguntas):
        actualizar_botones()

# -------------------
# BUCLE PRINCIPAL
# -------------------
reloj = pygame.time.Clock()
botones_opciones = generar_botones_opciones(preguntas[indice_pregunta], fuentes["normal"])

def actualizar_botones():
    global botones_opciones
    if indice_pregunta < len(preguntas):
        botones_opciones = generar_botones_opciones(preguntas[indice_pregunta], fuentes["normal"])

running = True
while running:
    pantalla.fill((255, 255, 255))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salir_juego()
        for boton in botones_opciones:
            boton.manejar_evento(evento, None)

    # Dibujar título y pregunta
    pygame.draw.rect(pantalla, (255, 255, 255), (0, 0, ANCHO, 80))
    if indice_pregunta < len(preguntas):
        pregunta_texto = preguntas[indice_pregunta]["pregunta"]
        dibujar_pregunta(pantalla, pregunta_texto, fuentes["grande"], ANCHO)

    # Dibujar plantas y botones
    dibujar_plantas(pantalla, plantas, tachadas, fuentes["normal"])
    for boton in botones_opciones:
        boton.dibujar(pantalla)

    pygame.display.flip()
    reloj.tick(60)
