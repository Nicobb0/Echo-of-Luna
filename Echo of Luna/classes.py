import pygame
import random

largura = 800
altura = 600
gravidade = 0.5
impulso = -10
velocidade_cano = 3
distancia_cano = 200


class Orion:
    def __init__(self):
        self.x = 50
        self.y = altura // 2
        self.velocidade = 0
        self.raio = 20
        self.pontosParaBoost = 0
        self.boost_ativado = False
        self.boost_liberado = False

    def pular(self):
        self.velocidade = impulso

    def atualizar(self):
        self.velocidade += gravidade
        self.y += self.velocidade

    def desenhar(self, tela):
        cor = (255, 255, 0) if self.boost_liberado else (255, 0, 0)
        pygame.draw.circle(tela, cor, (int(self.x), int(self.y)), self.raio)

    def get_rect(self):
        return pygame.Rect(self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2)

    def adicionar_ponto(self):
        self.pontosParaBoost += 1
        if self.pontosParaBoost >= 5:
            self.pontosParaBoost = 0
            self.boost_liberado = True

    def ativar_boost(self, pontuacao):
        if self.boost_liberado:
            self.boost_liberado = False
            self.boost_ativado = True
            pontuacao += 5
        return pontuacao


class Obstáculos:
    def __init__(self, x):
        self.x = x
        self.largura = 100
        self.altura_topo = random.randint(100, 400)
        self.espaco = 180

    def atualizar(self):
        self.x -= velocidade_cano

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 255), (self.x, 0, self.largura, self.altura_topo))
        pygame.draw.rect(tela, (255, 255, 255),
                         (self.x, self.altura_topo + self.espaco, self.largura, altura))

    def colidiu(self, orion: Orion):
        rect = orion.get_rect()
        topo = pygame.Rect(self.x, 0, self.largura, self.altura_topo)
        base = pygame.Rect(self.x, self.altura_topo + self.espaco, self.largura, altura)
        return rect.colliderect(topo) or rect.colliderect(base)

    def passou(self, orion: Orion):
        return self.x + self.largura < orion.x and not hasattr(self, 'pontuado')