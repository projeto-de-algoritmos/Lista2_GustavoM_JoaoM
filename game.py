import pygame
from screens import Menu
from screens import GameScreen

class Game:
    # Game constants
    WIDTH = 1024
    HEIGHT = 768
    GAME_NAME = 'Caminhãozinho'
    running = False
    __screens = {}
    current_screen = Menu.ID
    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        self.__screens[Menu.ID] = Menu(self)
        self.__screens[GameScreen.ID] = GameScreen(self)
        self.clock = pygame.time.Clock()

    def run(self):
        pygame.init()
        self.running = True
        while self.running:
                self.__screens[self.current_screen].run()
    def start_game(self):
        self.current_screen = GameScreen.ID

    def exit(self):
        self.running = False
