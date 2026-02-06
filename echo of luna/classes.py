import pygame
import random
import os

largura = 800
altura = 600
gravidade = 0.5
impulso = -10
velocidade_cano = 3

CAMINHO_IMG = "Imagens jogo max"

class Echo:
    def __init__(self):
        self.x = 80
        self.y = altura // 2
        self.velocidade = 0
        self.raio = 20

        # carregar sprite
        sprite = pygame.image.load(os.path.join(CAMINHO_IMG, "robo.png")).convert_alpha()

        # redimensionar sprite (ajuste se quiser maior/menor)
        self.sprite = pygame.transform.scale(sprite, (80, 80))

    def pular(self):
        self.velocidade = impulso

    def atualizar(self):
        self.velocidade += gravidade
        self.y += self.velocidade

    def desenhar(self, tela):
        rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
        tela.blit(self.sprite, rect)

    def get_rect(self):
        rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
        return rect


class Obstáculos:
    def __init__(self, x):
        self.x = x
        self.largura = 100
        self.altura_topo = random.randint(100, 300)
        self.espaco = 250

    def atualizar(self):
        self.x -= velocidade_cano

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 255), (self.x, 0, self.largura, self.altura_topo))
        pygame.draw.rect(
            tela,
            (255, 255, 255),
            (self.x, self.altura_topo + self.espaco, self.largura, altura)
        )

    def colidiu(self, echo: Echo):
        rect = echo.get_rect()
        topo = pygame.Rect(self.x, 0, self.largura, self.altura_topo)
        base = pygame.Rect(self.x, self.altura_topo + self.espaco, self.largura, altura)
        return rect.colliderect(topo) or rect.colliderect(base)

    def passou(self, echo: Echo):
        return self.x + self.largura < echo.x and not hasattr(self, 'pontuado')