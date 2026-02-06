import pygame

WIDTH, HEIGHT = 800, 600
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (235, 235, 235)

class TypedMessage:
    def __init__(self, text, hold_time, typing_speed=0.08):
        self.text = text
        self.hold_time = hold_time
        self.typing_speed = typing_speed
        self.timer = 0
        self.hold_timer = 0
        self.char_index = 0
        self.finished_typing = False

    def update(self, dt):
        if not self.finished_typing:
            self.timer += dt
            if self.timer >= self.typing_speed:
                self.timer = 0
                self.char_index += 1
                if self.char_index >= len(self.text):
                    self.char_index = len(self.text)
                    self.finished_typing = True
        else:
            self.hold_timer += dt

    def finished(self):
        return self.finished_typing and self.hold_timer >= self.hold_time

    def draw(self, screen, font):
        surf = font.render(self.text[:self.char_index], True, COLOR_WHITE)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(surf, rect)


class BootCutscene:
    def __init__(self, game):
        self.game = game

    def enter(self):
        self.font = pygame.font.SysFont("consolas", 44)

        self.messages = [
            TypedMessage("Sistema: restaurando...", 3.5),
            TypedMessage("Unidade: E.C.H.O", 3.0),
            TypedMessage("Status: ativo", 3.0),
            TypedMessage("Protocolo Mãe: ERRO", 4.5),
        ]

        self.index = 0
        self.fade_in = 255

    def handle_event(self, event):
        pass

    def update(self, dt):
        if self.fade_in > 0:
            self.fade_in -= 180 * dt
            return

        if self.index < len(self.messages):
            msg = self.messages[self.index]
            msg.update(dt)
            if msg.finished():
                self.index += 1
        else:
            # 👇 IMPORT LOCAL → quebra o loop circular
            from fase1_state import Fase1State
            self.game.states.change(Fase1State(self.game))

    def draw(self, screen):
        screen.fill(COLOR_BLACK)

        if self.index < len(self.messages) and self.fade_in <= 0:
            self.messages[self.index].draw(screen, self.font)

        if self.fade_in > 0:
            fade = pygame.Surface((WIDTH, HEIGHT))
            fade.fill(COLOR_BLACK)
            fade.set_alpha(int(self.fade_in))
            screen.blit(fade, (0, 0))