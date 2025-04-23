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
