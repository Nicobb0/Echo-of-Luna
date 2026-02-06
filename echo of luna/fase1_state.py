import pygame
from classes import Echo, Obstáculos, largura, altura
from game_over_state import GameOverState

VELOCIDADE_EXTRA = 2
DISTANCIA = 400
QUANTIDADE = 6

class Fase1State:
    def __init__(self, game):
        self.game = game

    def enter(self):
        self.echo = Echo()

        self.bg = pygame.image.load("Imagens jogo max/lado direito.png").convert()
        self.bg = pygame.transform.scale(self.bg, (largura, altura))

        self.obstaculos = [Obstáculos(largura + i * DISTANCIA) for i in range(QUANTIDADE)]

        self.pontos = 0
        self.fonte = pygame.font.Font(None, 50)

        self.aguardando_inicio = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if self.aguardando_inicio:
                self.aguardando_inicio = False
                return

            if event.key == pygame.K_SPACE:
                self.echo.pular()

    def update(self, dt):

        if self.aguardando_inicio:
            return

        self.echo.atualizar()

        for obs in self.obstaculos:
            obs.x -= VELOCIDADE_EXTRA
            obs.atualizar()

            if obs.colidiu(self.echo):
                self.game.states.change(GameOverState(self.game, self.pontos))
                return

            if obs.passou(self.echo):
                self.pontos += 1
                setattr(obs, "pontuado", True)

        if self.obstaculos[0].x + self.obstaculos[0].largura < 0:
            self.obstaculos.pop(0)
            novo_x = self.obstaculos[-1].x + DISTANCIA
            self.obstaculos.append(Obstáculos(novo_x))

        if self.echo.y > altura or self.echo.y < 0:
            self.game.states.change(GameOverState(self.game, self.pontos))

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        for obs in self.obstaculos:
            obs.desenhar(screen)

        self.echo.desenhar(screen)

        texto = self.fonte.render(str(self.pontos), True, (255, 0, 0))
        screen.blit(texto, (largura // 2 - 20, 30))

        if self.aguardando_inicio:
            aviso = self.fonte.render("PRESSIONE QUALQUER TECLA", True, (255, 255, 255))
            rect = aviso.get_rect(center=(largura // 2, altura // 2))
            screen.blit(aviso, rect)