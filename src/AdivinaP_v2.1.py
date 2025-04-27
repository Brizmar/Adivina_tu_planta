import pygame
import numpy
from utils import cargar_json, cargar_imagen, cargar_sonido, salir_juego, agregar_nueva_planta
from diseño import obtener_fuentes, dibujar_pregunta, dibujar_plantas, Boton, InputBox

pygame.init()
ANCHO, ALTO = 1000, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Adivina tu planta")

# -------------------
# CARGA DE DATOS
# -------------------
preguntas = cargar_json("preguntas.json")
plantas_raw = cargar_json("plantas.json")
sonido_click = cargar_sonido("click.wav")

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
    boton = Boton(x, y, ancho, alto, texto, accion, fuente)
    boton.sonido = sonido_click  # ← Asignar sonido
    return boton

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

    preguntas[indice_pregunta]["respuesta_usuario"] = opcion_seleccionada  # ← Guarda la respuesta del usuario
    indice_pregunta += 1

    if indice_pregunta >= len(preguntas):
        # Ya se respondieron todas las preguntas: ahora sí decidir
        plantas_disponibles = [planta for planta in plantas if planta["nombre"] not in tachadas]

        if not plantas_disponibles:
            mostrar_pantalla_sin_coincidencias()
        elif len(plantas_disponibles) == 1:
            mostrar_pantalla_victoria(plantas_disponibles[0]["nombre"])
        else:
            mostrar_pantalla_victoria(plantas_disponibles[0]["nombre"])  # ← Puedes ajustar aquí si quieres elegir entre varias
    else:
        # Todavía hay preguntas, seguir preguntando
        actualizar_botones()

# -------------------
# RESULTADOS FINALES
# -------------------
def mostrar_pantalla_sin_coincidencias():
    fuente = fuentes["grande"]
    fuente_normal = fuentes["normal"]
    input_box = InputBox(ANCHO//2 - 100, ALTO//2, 200, 50, fuente_normal)
    agregar = False
    salir = False

    def confirmar_agregado():
        nonlocal agregar
        agregar = True

    def cancelar():
        salir_juego()

    boton_agregar = Boton(ANCHO//2 - 220, ALTO//2 + 100, 200, 60, "Agregar nueva planta", confirmar_agregado, fuente_normal)
    boton_salir = Boton(ANCHO//2 + 20, ALTO//2 + 100, 200, 60, "Salir", cancelar, fuente_normal)

    while not (agregar or salir):
        pantalla.fill((255, 255, 255))

        mensaje = fuente.render("Lo sentimos, no encontramos una planta ideal.", True, (200, 50, 50))
        pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 150))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
            input_box.handle_event(evento)
            boton_agregar.manejar_evento(evento, None)
            boton_salir.manejar_evento(evento, None)

        input_box.update()
        input_box.draw(pantalla)
        boton_agregar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(30)

    if agregar:
        # Crear nueva planta con respuestas dadas
        nombre = input_box.text.strip()
        if nombre:
            respuestas_actuales = {}
            for i in range(len(preguntas)):
                atributo = preguntas[i]["atributo"]
                respuestas_actuales[atributo] = preguntas[i]["respuesta_usuario"]
            imagen = nombre.lower().replace(" ", "_") + ".png"
            agregar_nueva_planta(respuestas_actuales, nombre, imagen)
        salir_juego()

def mostrar_pantalla_victoria(planta_ganadora):
    fuente = fuentes["grande"]
    fuente_normal = fuentes["normal"]

    while True:
        pantalla.fill((255, 255, 255))
        mensaje = fuente.render(f"¡Tu planta ideal es {planta_ganadora}!", True, (34, 139, 34))
        pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 200))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()

        pygame.display.flip()
        reloj.tick(30)

# -------------------
# BUCLE PRINCIPAL
# -------------------
reloj = pygame.time.Clock()
botones_opciones = generar_botones_opciones(preguntas[indice_pregunta], fuentes["normal"])

def actualizar_botones():
    global botones_opciones
    if indice_pregunta < len(preguntas):
        botones_opciones = generar_botones_opciones(preguntas[indice_pregunta], fuentes["normal"])

# -------------------
# MENÚ DE INICIO
# -------------------
def mostrar_menu_inicio():
    fuente = fuentes["grande"]
    jugar = False  # Control de flujo

    def iniciar_juego_local():
        nonlocal jugar
        jugar = True

    boton_jugar = Boton(ANCHO // 2 - 220, ALTO // 2, 200, 60, "Jugar", iniciar_juego_local, fuente)
    boton_jugar.sonido = sonido_click

    boton_salir = Boton(ANCHO // 2 + 20, ALTO // 2, 200, 60, "Salir", salir_juego, fuente)
    boton_salir.sonido = sonido_click

    while not jugar:
        pantalla.fill((255, 255, 255))
        titulo = fuente.render("Adivina tu planta", True, (34, 139, 34))
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
            boton_jugar.manejar_evento(evento, None)
            boton_salir.manejar_evento(evento, None)

        boton_jugar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)
        pygame.display.flip()

    return True  # Cuando se presiona jugar


def iniciar_juego():
    global en_menu
    en_menu = False

# -------------------
# INICIO DEL PROGRAMA
# -------------------
if mostrar_menu_inicio():
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