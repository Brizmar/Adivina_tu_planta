import os
import json
import pygame
import sys

def cargar_sonido(nombre_archivo):
    ruta = os.path.join("sounds", nombre_archivo)
    try:
        return pygame.mixer.Sound(ruta)
    except pygame.error as e:
        print(f"Error al cargar el sonido: {e}")
        return None

def cargar_imagen(nombre_archivo, tamaño=None):
    ruta = os.path.join("img", nombre_archivo)
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        if tamaño:
            imagen = pygame.transform.scale(imagen, tamaño)
        return imagen
    except pygame.error as e:
        print(f"Error al cargar la imagen: {e}")
        return None

def cargar_json(nombre_archivo):
    ruta = os.path.join("data", nombre_archivo)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado.")
        return []

def agregar_nueva_planta(respuestas, nombre, imagen, ruta_archivo="data/preguntas.json"):
    # Construir ruta absoluta al JSON dentro de 'data'
    ruta = os.path.join("data", os.path.basename(ruta_archivo))

    # Preparar el nuevo objeto planta
    nueva_planta = respuestas.copy()
    nueva_planta["nombre"] = nombre
    nueva_planta["imagen"] = imagen

    # Cargar las plantas existentes
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            try:
                plantas = json.load(f)
            except json.JSONDecodeError:
                plantas = []
    else:
        plantas = []

    # Agregar y guardar
    plantas.append(nueva_planta)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(plantas, f, indent=4, ensure_ascii=False)

    print(f"La planta '{nombre}' ha sido agregada exitosamente en {ruta}.")

def salir_juego():
    pygame.quit()  # Finaliza todos los módulos de Pygame
    sys.exit()     # Termina el programa