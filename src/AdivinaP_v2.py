import pygame
import sys
from diseño import Boton, BLANCO, NEGRO, obtener_fuentes, InputBox
from utils import cargar_sonido, cargar_imagen, cargar_json, agregar_nueva_planta, salir_juego

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🌱 Elige tu Planta Ideal")

# Cargar fuentes y sonidos
fuentes = obtener_fuentes()
FUENTE_GRANDE = fuentes["grande"]
FUENTE_NORMAL = fuentes["normal"]
sonido_click = cargar_sonido("click.wav")

# Cargar preguntas y plantas
preguntas = cargar_json("preguntas.json")
plantas = cargar_json("plantas.json")

# Variables de estado
pantalla_actual = "menu"
indice_pregunta = 0
respuestas = {}
planta_recomendada = None
botones_opciones = []
input_box = InputBox(ANCHO // 2 - 100, ALTO // 2, 200, 40, FUENTE_NORMAL)
esperando_nombre = False

# Funciones del juego
def iniciar_juego():
    global pantalla_actual, indice_pregunta, respuestas, planta_recomendada
    pantalla_actual = "juego"
    indice_pregunta = 0
    respuestas = {}
    planta_recomendada = None
    crear_botones_pregunta()

def crear_botones_pregunta():
    global botones_opciones
    botones_opciones = []
    if indice_pregunta < len(preguntas):
        pregunta = preguntas[indice_pregunta]
        opciones = pregunta["opciones"]
        for i, opcion in enumerate(opciones):
            boton = Boton(
                x=ANCHO // 2 - 100,
                y=250 + i * 70,
                ancho=200,
                alto=50,
                texto=opcion,
                accion=lambda o=opcion: manejar_respuesta(o),
                fuente=FUENTE_NORMAL
            )
            botones_opciones.append(boton)

def manejar_respuesta(opcion_seleccionada):
    global indice_pregunta, pantalla_actual, planta_recomendada
    atributo = preguntas[indice_pregunta]["atributo"]
    respuestas[atributo] = opcion_seleccionada
    indice_pregunta += 1
    if indice_pregunta < len(preguntas):
        crear_botones_pregunta()
    else:
        planta_recomendada = obtener_recomendacion(plantas, respuestas)
        pantalla_actual = "resultado"

def obtener_recomendacion(plantas, respuestas):
    for planta in plantas:
        if all(planta.get(attr) == valor for attr, valor in respuestas.items()):
            return planta
    return None

def mostrar_resultado():
    global pantalla_actual, esperando_nombre, input_box
    pantalla.fill(BLANCO)
    if planta_recomendada:
        nombre = planta_recomendada["nombre"]
        imagen_nombre = planta_recomendada["imagen"]
        imagen = cargar_imagen(imagen_nombre, tamaño=(200, 200))
        if imagen:
            pantalla.blit(imagen, (ANCHO // 2 - 100, 150))
        mensaje = FUENTE_GRANDE.render(f"¡Felicidades! Tu planta ideal es:", True, NEGRO)
        nombre_texto = FUENTE_GRANDE.render(nombre, True, NEGRO)
        pantalla.blit(mensaje, mensaje.get_rect(center=(ANCHO // 2, 50)))
        pantalla.blit(nombre_texto, nombre_texto.get_rect(center=(ANCHO // 2, 100)))
        # Cambiar al estado 'fin' después de mostrar el resultado
        pantalla_actual = "fin"
    else:
        mensaje = "No se encontró una planta que coincida con tus preferencias."
        texto = FUENTE_NORMAL.render(mensaje, True, NEGRO)
        pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2)))
        pygame.display.flip()
        pygame.time.wait(2000)  # Esperar 2 segundos antes de solicitar entrada
        # Cambiar al estado 'agregar' para solicitar el nombre de la nueva planta
        pantalla_actual = "agregar"
        esperando_nombre = True
        input_box = InputBox(ANCHO // 2 - 100, ALTO // 2, 200, 40, FUENTE_NORMAL)

# Configuración del botón de inicio
boton_iniciar = Boton(
    x=ANCHO // 2 - 100,
    y=ALTO // 2,
    ancho=200,
    alto=60,
    texto="Iniciar Juego",
    accion=iniciar_juego,
    fuente=FUENTE_NORMAL
)
# Botón para salir del juego
boton_salir = Boton(
    x=ANCHO // 2 - 100,
    y=ALTO // 2 + 100,
    ancho=200,
    alto=50,
    texto="Salir",
    accion=lambda: salir_juego(),
    fuente=FUENTE_NORMAL
)

# Bucle principal del juego
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    pantalla.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if pantalla_actual == "menu":
            boton_iniciar.manejar_evento(evento, sonido_click)
            boton_salir.manejar_evento(evento, sonido_click)  # Agregar manejo de evento para el botón de salir
        elif pantalla_actual == "juego":
            for boton in botones_opciones:
                boton.manejar_evento(evento, sonido_click)
        elif pantalla_actual == "agregar":
            input_box.handle_event(evento)
            if input_box.terminado:
                nombre_nuevo = input_box.text.strip()
                if nombre_nuevo:
                    imagen_nueva = nombre_nuevo.lower().replace(" ", "_") + ".png"
                    agregar_nueva_planta(respuestas, nombre_nuevo, imagen_nueva)
                    esperando_nombre = False
                    pantalla_actual = "menu"  # Volver al menú principal o reiniciar

    if pantalla_actual == "menu":
        titulo = FUENTE_GRANDE.render("🌿 Bienvenido al Selector de Plantas 🌿", True, NEGRO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ALTO // 3)))
        boton_iniciar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)  # Dibujar el botón de salir en el menú
    elif pantalla_actual == "juego":
        pregunta_actual = preguntas[indice_pregunta]["pregunta"]
        pregunta = FUENTE_GRANDE.render(pregunta_actual, True, NEGRO)
        pantalla.blit(pregunta, pregunta.get_rect(center=(ANCHO // 2, 100)))
        for boton in botones_opciones:
            boton.dibujar(pantalla)
    elif pantalla_actual == "resultado":
        mostrar_resultado()
    elif pantalla_actual == "agregar":
        mensaje = FUENTE_GRANDE.render("Ingresa el nombre de la nueva planta:", True, NEGRO)
        pantalla.blit(mensaje, mensaje.get_rect(center=(ANCHO // 2, ALTO // 2 - 50)))
        input_box.update()
        input_box.draw(pantalla)
    elif pantalla_actual == "fin":
        mensaje = FUENTE_GRANDE.render("¿Deseas salir?", True, NEGRO)  # Ajustar mensaje para salir
        pantalla.blit(mensaje, mensaje.get_rect(center=(ANCHO // 2, 100)))
        boton_salir.dibujar(pantalla)  # Mostrar el botón de salir

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
