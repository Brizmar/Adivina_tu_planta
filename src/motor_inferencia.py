import unicodedata

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode().lower().strip()

def obtener_recomendacion(plantas, respuestas):
    opciones = plantas.copy()
    for clave, valor in respuestas.items():
        valor_norm = normalizar(valor)
        opciones = [
            p for p in opciones
            if clave in p and normalizar(p[clave]) == valor_norm
        ]
    return opciones[0] if opciones else None
