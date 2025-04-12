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
def mostrar_imagen(nombre):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir, "..", "img", f"{nombre.lower()}.png")

    print("Ruta completa de la imagen:", ruta)
    print("Archivo existe:", os.path.exists(ruta))

    if os.path.exists(ruta):
        # Creamos una nueva ventana
        ventana = tk.Toplevel()
        ventana.title(f"Tu planta ideal: {nombre}")

        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize((250, 250), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)

            etiqueta = tk.Label(ventana, image=imagen_tk)
            etiqueta.image = imagen_tk  # evita que se borre por el recolector
            etiqueta.pack()

            ventana.grab_set()  # fuerza a que interactúes con esa ventana
            ventana.wait_window()  # espera a que se cierre antes de seguir
        except Exception as e:
            print("Error al mostrar imagen:", e)
            messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")

# Esta función te da la ruta absoluta basada en donde está tu script
def ruta_relativa(desde, archivo):
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, desde, archivo)

def agregar_nueva_planta(nombre, respuestas, archivo_relativo="../data/plantas.json"):
    ruta_archivo = ruta_relativa("", archivo_relativo)  # "" si plantas.json ya está en data/

    nueva_planta = {"nombre": nombre}
    nueva_planta.update(respuestas)

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            try:
                plantas = json.load(f)
            except json.JSONDecodeError:
                plantas = []
    else:
        plantas = []

    plantas.append(nueva_planta)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(plantas, f, indent=4, ensure_ascii=False)

    print(f"✅ Planta agregada a: {ruta_archivo}")

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
        
        agregar = messagebox.askyesno("Agregar planta", "¿Deseas agregar una nueva planta con estas características?")
        if agregar:
            nombre = simpledialog.askstring("Nueva planta", "Escribe el nombre de la nueva planta:")
            if nombre:
                agregar_nueva_planta(nombre, respuestas)
                messagebox.showinfo("Guardado", f"La planta '{nombre}' fue agregada.")
                
if __name__ == "__main__":
    main()
