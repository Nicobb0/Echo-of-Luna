import pygame
from classes import largura, altura

CAMINHO = "Imagens jogo max"
FONTE = "fontes/PressStart2P.ttf"

class GameOverState:
    def __init__(self, game, score):
        self.game = game
        self.score = score

    def enter(self):
        self.bg = pygame.image.load(f"{CAMINHO}/fundo.png").convert()
        self.bg = pygame.transform.scale(self.bg, (largura, altura))

        self.titulo = pygame.image.load(f"{CAMINHO}/titulo.png").convert_alpha()
        self.titulo = pygame.transform.scale(self.titulo, (400, 120))

        self.font_score = pygame.font.Font(FONTE, 22)
        self.font_button = pygame.font.Font(FONTE, 18)

        self.botao_rect = pygame.Rect(0, 0, 260, 60)
        self.botao_rect.center = (largura // 2, altura // 2 + 120)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_rect.collidepoint(event.pos):
                from fase1_state import Fase1State
                self.game.states.change(Fase1State(self.game))

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        titulo_rect = self.titulo.get_rect(center=(largura//2, altura//2 - 80))
        screen.blit(self.titulo, titulo_rect)

        texto = self.font_score.render(f"PONTOS: {self.score}", True, (255, 255, 255))
        screen.blit(texto, texto.get_rect(center=(largura//2, altura//2 + 10)))

        mouse = pygame.mouse.get_pos()
        cor = (200, 60, 60) if self.botao_rect.collidepoint(mouse) else (120, 40, 40)

        pygame.draw.rect(screen, cor, self.botao_rect, border_radius=8)

        texto_botao = self.font_button.render("REINICIAR", True, (255, 255, 255))
        screen.blit(texto_botao, texto_botao.get_rect(center=self.botao_rect.center))