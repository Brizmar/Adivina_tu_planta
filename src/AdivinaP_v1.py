import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import json
import os

# --- Constantes globales de rutas ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATA = os.path.join(BASE_DIR, "..", "data")
RUTA_IMG = os.path.join(BASE_DIR, "..", "img")

# --- Utilidades de archivos JSON ---
def leer_json(ruta):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def escribir_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# --- Cargar datos desde archivos JSON ---
def cargar_datos(nombre_archivo):
    ruta_completa = os.path.join(RUTA_DATA, nombre_archivo)
    return leer_json(ruta_completa)

# --- Obtener ruta de imagen según nombre ---
def obtener_ruta_imagen(nombre):
    return os.path.join(RUTA_IMG, f"{nombre.lower()}.png")

# --- Mostrar imagen en ventana emergente ---
def mostrar_imagen(nombre):
    ruta = obtener_ruta_imagen(nombre)
    print("Ruta completa de la imagen:", ruta)
    print("Archivo existe:", os.path.exists(ruta))

    if os.path.exists(ruta):
        ventana = tk.Toplevel()
        ventana.title(f"Tu planta ideal: {nombre}")

        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize((250, 250), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)

            etiqueta = tk.Label(ventana, image=imagen_tk)
            etiqueta.image = imagen_tk
            etiqueta.pack()

            ventana.grab_set()
            ventana.wait_window()
        except Exception as e:
            print("Error al mostrar imagen:", e)
            messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")

# --- Agregar nueva planta a base de datos ---
def agregar_nueva_planta(nombre, respuestas):
    ruta_archivo = os.path.join(RUTA_DATA, "plantas.json")
    plantas = leer_json(ruta_archivo)

    nueva_planta = {"nombre": nombre, **respuestas}
    plantas.append(nueva_planta)

    escribir_json(ruta_archivo, plantas)
    print(f"✅ Planta agregada a: {ruta_archivo}")

# --- Motor de inferencia ---
def obtener_recomendacion(plantas, respuestas):
    opciones = plantas.copy()
    for clave, valor in respuestas.items():
        opciones = [p for p in opciones if p.get(clave) == valor]
    return opciones[0] if opciones else None

# --- Aplicación principal ---
def main():
    root = tk.Tk()
    root.withdraw()

    preguntas = cargar_datos("preguntas.json")
    plantas = cargar_datos("plantas.json")
    respuestas = {}

    for pregunta in preguntas:
        atributo = pregunta["atributo"]
        texto = pregunta["pregunta"]
        opciones = pregunta["opciones"]

        opciones_texto = "\n".join(f"- {op}" for op in opciones)
        mensaje_completo = f"{texto}\n\nOpciones:\n{opciones_texto}"

        respuesta = simpledialog.askstring("Pregunta", mensaje_completo)
        if respuesta:
            respuesta = respuesta.strip().lower()
            if respuesta in [op.lower() for op in opciones]:
                respuestas[atributo] = respuesta
            else:
                messagebox.showinfo("Opción no válida", f"'{respuesta}' no es una opción válida.")
                return
        else:
            messagebox.showinfo("Aviso", "Se canceló el proceso.")
            return

    resultado = obtener_recomendacion(plantas, respuestas)
    if resultado:
        messagebox.showinfo("Resultado", f"Tu planta ideal es: {resultado['nombre']}")
        mostrar_imagen(resultado["nombre"])
    else:
        messagebox.showinfo("Sin resultados", "No se encontró una planta con esas características.")
        agregar = messagebox.askyesno("Agregar planta", "¿Deseas agregar una nueva planta con estas características?")
        if agregar:
            nombre = simpledialog.askstring("Nueva planta", "Escribe el nombre de la nueva planta:")
            if nombre and nombre.strip():
                agregar_nueva_planta(nombre.strip(), respuestas)
                messagebox.showinfo("Guardado", f"La planta '{nombre.strip()}' fue agregada.")

if __name__ == "__main__":
    main()
