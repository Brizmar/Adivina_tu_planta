import tkinter as tk                            # Ventanas emergentes
from tkinter import simpledialog, messagebox    # Para pedir y mostrar datos
from PIL import Image, ImageTk                  # Para abrir y mostrar imagenes
import json                                     # Para cargar la base de datos
import os                                       # Para verificar si una imagen existe

# Cargar archivos JSON
def cargar_datos(nombre_archivo):
    """
    Carga un archivo JSON desde la carpeta 'data', sin importar desde dónde se ejecute el script.
    """
    ruta_base = os.path.dirname(__file__)  # Obtiene la ruta del archivo actual (main.py)
    ruta_completa = os.path.join(ruta_base, "..", "data", nombre_archivo)

    with open(ruta_completa, encoding="utf-8") as archivo:
        return json.load(archivo)

# Mostrar imagen en una ventana emergente
def mostrar_imagen(imagen_nombre):
    # Añadimos la extensión '.jpg' al nombre de la imagen.
    ruta = os.path.join("..", "img", f"{imagen_nombre.lower()}.png")
    print(f"Ruta completa de la imagen: {ruta}")

    if os.path.exists(ruta):
        ventana = tk.Toplevel()
        ventana.title(f"Tu planta ideal")

        # Cargamos y redimensionamos la imagen.
        imagen = Image.open(ruta)
        imagen = imagen.resize((250, 250))  # Cambié de 'Image.resize()' a 'imagen.resize()'
        imagen_tk = ImageTk.PhotoImage(imagen)

        etiqueta = tk.Label(ventana, image=imagen_tk)
        etiqueta.image = imagen_tk  # Evita que se pierda la referencia de la imagen
        etiqueta.pack()

    else:
        messagebox.showinfo("Imagen no encontrada", f"No hay imagen para {imagen_nombre}.")

# Motor de inferencia simple
def obtener_recomendacion(plantas, respuestas):
    opciones = plantas.copy()
    for clave, valor in respuestas.items():
        opciones = [p for p in opciones if p.get(clave) == valor]
    return opciones[0] if opciones else None

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

        # Mostrar opciones al usuario en el mensaje
        opciones_texto = "\n".join(f"- {op}" for op in opciones)
        mensaje_completo = f"{texto}\n\nOpciones:\n{opciones_texto}"

        respuesta = simpledialog.askstring("Pregunta", mensaje_completo)
        if respuesta:
            respuesta = respuesta.strip().lower()
            if respuesta in opciones:
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

if __name__ == "__main__":
    main()
