import pygame
import sys
from classes import *
from telas import *

pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Rescue Flight")
fonte = pygame.font.Font(None, 50)
fonte_menor = pygame.font.Font(None, 36)
Ticks = pygame.time.Clock()


def Fase1():
    orion = Orion()
    obstaculos = [Obstáculos(largura + i * 300) for i in range(3)]
    pontos = 0

    def desenhar_pontuacao(pontos):
        texto = fonte.render(str(pontos), True, (255, 0, 0))
        tela.blit(texto, (largura // 2 - 20, 30))

    def desenhar_mensagem_boost():
        if orion.boost_liberado:
            texto = fonte_menor.render("BOOST DISPONÍVEL! (aperte B)", True, (255, 255, 0))
            tela.blit(texto, (20, 20))

    rodando = True
    while rodando:
        tela.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    orion.pular()

                if event.key == pygame.K_b:
                    pontos_antes = pontos
                    pontos = orion.ativar_boost(pontos)
                    if pontos > pontos_antes:
                        obstaculos = [Obstáculos(largura + i * 300) for i in range(3)]

        orion.atualizar()

        for obs in obstaculos:
            obs.atualizar()
            obs.desenhar(tela)

            if obs.colidiu(orion):
                rodando = False

            if obs.passou(orion):
                pontos += 1
                orion.adicionar_ponto()
                setattr(obs, 'pontuado', True)

        if obstaculos[0].x + obstaculos[0].largura < 0:
            obstaculos.pop(0)
            obstaculos.append(Obstáculos(obstaculos[-1].x + 300))

        if orion.y > altura or orion.y < 0:
            rodando = False

        orion.desenhar(tela)
        desenhar_pontuacao(pontos)
        desenhar_mensagem_boost()

        pygame.display.flip()
        Ticks.tick(80)

    return pontos