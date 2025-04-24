import pygame

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (34, 139, 34)

def obtener_fuentes():
    fuente_grande = pygame.font.SysFont("arial", 36)
    fuente_normal = pygame.font.SysFont("arial", 28)
    return {"grande": fuente_grande, "normal": fuente_normal}

class Boton:
    def __init__(self, x, y, ancho, alto, texto, accion, fuente):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.accion = accion
        self.fuente = fuente
        self.color = VERDE

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        texto_render = self.fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def manejar_evento(self, evento, sonido_click):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                if sonido_click:
                    sonido_click.play()
                self.accion()

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = ''
        self.font = font
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.terminado = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en el cuadro de entrada
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.terminado = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Ajustar el ancho del cuadro si es necesario
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Dibujar el texto
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Dibujar el rectángulo del cuadro de entrada
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Escala de grises para una imagen
def imagen_a_grises(imagen):
    arr = pygame.surfarray.array3d(imagen)
    gris = arr.mean(axis=2).astype('uint8')
    arr[:, :, 0] = gris
    arr[:, :, 1] = gris
    arr[:, :, 2] = gris
    return pygame.surfarray.make_surface(arr).convert_alpha()

# Dibujar pregunta
def dibujar_pregunta(pantalla, texto, fuente, ancho_ventana):
    pregunta_render = fuente.render(texto, True, VERDE)
    rect_pregunta = pregunta_render.get_rect(center=(ancho_ventana // 2, 60))
    pygame.draw.rect(pantalla, (200, 255, 200), rect_pregunta.inflate(40, 20), border_radius=12)
    pantalla.blit(pregunta_render, rect_pregunta)

# Dibujar cuadrícula de plantas
def dibujar_plantas(pantalla, plantas, tachadas, fuente, columnas=4, tamaño=(100, 100), margen=30, offset_y=100):
    ancho = pantalla.get_width()
    x_inicio = (ancho - ((tamaño[0] + margen) * columnas - margen)) // 2

    for i, planta in enumerate(plantas):
        fila = i // columnas
        col = i % columnas
        x = x_inicio + col * (tamaño[0] + margen)
        y = offset_y + fila * (tamaño[1] + 40)

        imagen = planta["imagen"]
        if planta["nombre"] in tachadas:
            imagen = imagen_a_grises(imagen)
        
        pantalla.blit(imagen, (x, y))
        texto = fuente.render(planta["nombre"], True, NEGRO)
        texto_rect = texto.get_rect(center=(x + tamaño[0] // 2, y + tamaño[1] + 15))
        pantalla.blit(texto, texto_rect)