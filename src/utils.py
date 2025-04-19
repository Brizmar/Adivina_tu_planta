import os
import json
import pygame

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

def agregar_nueva_planta(respuestas, ruta_archivo="data/plantas.json"):
    nombre = input("Ingrese el nombre de la nueva planta: ")
    imagen = input("Ingrese el nombre del archivo de imagen (e.g., 'nueva_planta.png'): ")

    nueva_planta = respuestas.copy()
    nueva_planta["nombre"] = nombre
    nueva_planta["imagen"] = imagen

    # Verificar si el archivo existe
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            try:
                plantas = json.load(archivo)
            except json.JSONDecodeError:
                plantas = []
    else:
        plantas = []

    plantas.append(nueva_planta)

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(plantas, archivo, indent=4, ensure_ascii=False)

    print(f"La planta '{nombre}' ha sido agregada exitosamente.")