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
