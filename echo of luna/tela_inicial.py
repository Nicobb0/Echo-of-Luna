import pygame
import os
import random
from state_machine import TransitionToBoot

WIDTH, HEIGHT = 800, 600

class TelaInicial:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.opcoes_renderizadas = []
        self.palette = {
            "background": (10, 15, 31),    # #0A0F1F (Fonte 49)
            "active": (47, 128, 255),      # #2F80FF (Fonte 49)
            "inactive": (43, 47, 58),      # #2B2F3A (Fonte 49)
            "outline": (20, 40, 80)
        }

    def _render_text_outline(self, texto, cor_texto, cor_contorno, espessura=2):
        """Versão otimizada para ser chamada apenas no carregamento"""
        base = self.font.render(texto, True, cor_texto)
        w, h = base.get_size()
        surf = pygame.Surface((w + espessura * 2, h + espessura * 2), pygame.SRCALPHA)
        
        # Desenha o contorno
        outline = self.font.render(texto, True, cor_contorno)
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            surf.blit(outline, (dx * espessura + espessura, dy * espessura + espessura))
        
        surf.blit(base, (espessura, espessura))
        return surf

    def enter(self):
        # Gerenciamento de caminhos robusto (Fonte 19)
        path_img = "Imagens jogo max"
        self.bg = pygame.image.load(os.path.join(path_img, "fundo.png")).convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        titulo_original = pygame.image.load(os.path.join(path_img, "titulo.png")).convert_alpha()
        
        # Redimensionamento mantendo proporção
        largura_desejada = 700
        proporcao = largura_desejada / titulo_original.get_width()
        self.titulo = pygame.transform.scale(
            titulo_original, 
            (largura_desejada, int(titulo_original.get_height() * proporcao))
        )

        self.titulo_y = -self.titulo.get_height()
        self.titulo_y_final = 150
        self.titulo_alpha = 0
        self.glitch_timer = 0

        self.font = pygame.font.Font(os.path.join("fontes", "PressStart2P.ttf"), 22)
        
        self.opcoes = ["SEGUIR A LUZ", "CARREGAR MEMORIA", "CONFIGURACOES"]
        self.opcao_atual = 0
        self._pre_render_menu()

    def _pre_render_menu(self):
        """Otimização: Renderiza as opções uma única vez"""
        self.opcoes_renderizadas = []
        for i, texto in enumerate(self.opcoes):
            if i == self.opcao_atual:
                surf = self._render_text_outline(f"> {texto}", self.palette["active"], self.palette["outline"])
            else:
                surf = self.font.render(f"  {texto}", True, self.palette["inactive"])
            self.opcoes_renderizadas.append(surf)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            old_selection = self.opcao_atual
            if event.key == pygame.K_DOWN:
                self.opcao_atual = (self.opcao_atual + 1) % len(self.opcoes)
            elif event.key == pygame.K_UP:
                self.opcao_atual = (self.opcao_atual - 1) % len(self.opcoes)
            
            # Se mudou a seleção, re-renderiza para atualizar cores
            if old_selection != self.opcao_atual:
                self._pre_render_menu()

            if event.key == pygame.K_RETURN:
                if self.opcoes[self.opcao_atual] == "SEGUIR A LUZ":
                    # Transição para a inicialização do Echo (Fonte 34)
                    self.game.states.change(TransitionToBoot(self.game))

    def update(self, dt):
        # Descida suave com Delta Time (Fonte 18)
        if self.titulo_y < self.titulo_y_final:
            self.titulo_y += 300 * dt
        
        # Fade-in com limite de 255
        self.titulo_alpha = min(255, self.titulo_alpha + 200 * dt)
        
        # Efeito de Glitch Visual (Baseado na instabilidade do Echo - Fonte 38)
        self.glitch_timer += dt
        if self.glitch_timer > 2.0:
            if random.random() > 0.95: # 5% de chance de flicker por frame após 2s
                self.titulo_alpha = random.randint(150, 255)
            else:
                self.titulo_alpha = 255

    def draw(self, screen):
        # Usa a superfície de menu do jogo
        surf = self.game.menu_surface
        surf.blit(self.bg, (0, 0))

        # Desenha Título com Alpha e leve tremor se houver "glitch"
        temp_titulo = self.titulo.copy()
        temp_titulo.set_alpha(int(self.titulo_alpha))
        
        pos_x = WIDTH // 2
        if self.titulo_alpha < 255: # Tremor durante o fade
            pos_x += random.randint(-1, 1)

        titulo_rect = temp_titulo.get_rect(center=(pos_x, int(self.titulo_y)))
        surf.blit(temp_titulo, titulo_rect)

        # Desenha Menu Pré-renderizado
        menu_x = 100
        menu_y = HEIGHT - 280
        for opcao_surf in self.opcoes_renderizadas:
            surf.blit(opcao_surf, (menu_x, menu_y))
            menu_y += 60

        # Aplica o resultado final na tela principal (Fonte 17)
        screen.blit(surf, (0, 0))