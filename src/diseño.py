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
