import pygame
import sys
from classes import *

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Rescue Flight')
Ticks = pygame.time.Clock()
fonte = pygame.font.Font(None , 50)
fonte_titulo = pygame.font.Font(None, 80)



def desenhar_pontuacao(pontos):
    texto = fonte.render(str(pontos), True, (255, 0, 0))
    tela.blit(texto, (largura // 2, 30))
    
def tela_inicial():
     while True:
        tela.fill((0,0,0))

        titulo = fonte_titulo.render("Rescue Flight", True, (255,255,255))
        instrucao = fonte.render("prescione ESPAÇO para começar o jogo", True, (255,255,255))

        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 2 - 100))
        tela.blit(instrucao, (largura // 2 - instrucao.get_width() // 2, altura // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        Ticks.tick(80)

def Game_over(pontos):
     while True:
        tela.fill((0,0,0))

        titulo = fonte_titulo.render("Game Over", True, (255,255,255))
        pontua = fonte.render(f"Pontuação: {pontos}", True, (255, 255, 255))
        instrucao = fonte.render("prescione R para jogar novamente", True, (255,255,255))

        
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 2 - 100))
        tela.blit(pontua, (largura // 2 - pontua.get_width() // 2, altura // 2 - 30))
        tela.blit(instrucao, (largura // 2 - instrucao.get_width() // 2, altura // 2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

        Ticks.tick(80)