import pygame
from cutscene1 import BootCutscene

WIDTH, HEIGHT = 800, 600

class State:
    def __init__(self, game):
        self.game = game

    def enter(self): pass
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self, screen): pass


class StateMachine:
    def __init__(self, initial_state):
        self.state = initial_state
        self.state.enter()

    def change(self, new_state):
        self.state = new_state
        self.state.enter()

    def handle_event(self, event):
        self.state.handle_event(event)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)


class Fade:
    def __init__(self, speed=220):
        self.alpha = 0
        self.speed = speed
        self.active = False
        self.finished = False

    def start(self):
        self.alpha = 0
        self.active = True
        self.finished = False

    def update(self, dt):
        if self.active:
            self.alpha += self.speed * dt
            if self.alpha >= 255:
                self.alpha = 255
                self.active = False
                self.finished = True

    def draw(self, screen):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        fade.set_alpha(int(self.alpha))
        screen.blit(fade, (0, 0))


class TransitionToBoot(State):
    def enter(self):
        self.fade = Fade()
        self.fade.start()
        self.snapshot = self.game.menu_surface.copy()

    def update(self, dt):
        self.fade.update(dt)
        if self.fade.finished:
            self.game.states.change(BootCutscene(self.game))

    def draw(self, screen):
        screen.blit(self.snapshot, (0, 0))
        self.fade.draw(screen)