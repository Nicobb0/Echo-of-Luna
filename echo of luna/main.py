import pygame
import sys
from state_machine import StateMachine
from tela_inicial import TelaInicial

WIDTH, HEIGHT = 800, 600
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Echo of Luna")
        self.clock = pygame.time.Clock()

        self.menu_surface = pygame.Surface((WIDTH, HEIGHT))

        self.initial_menu = TelaInicial(self)
        self.states = StateMachine(self.initial_menu)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.states.handle_event(event)

            self.states.update(dt)
            self.states.draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    Game().run()