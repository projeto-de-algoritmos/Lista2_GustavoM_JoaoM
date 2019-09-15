import pygame

from screens import Menu, GameScreen, InfoScreen


class Game:
    # Game constants
    WIDTH = 1024
    HEIGHT = 768
    GAME_NAME = 'Jogo dos Caminhos'
    INTRO_TEXT = 'Identifique o menor caminho'

    # Game states
    running = False
    __screens = {}
    current_screen = Menu.ID

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        pygame.display.set_caption(self.GAME_NAME)
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        
        self.__screens[Menu.ID] = Menu(self)
        self.__screens[InfoScreen.ID] = InfoScreen(self)
        self.__screens[GameScreen.ID] = GameScreen(self)
        
        self.clock = pygame.time.Clock()

    def run(self):
        pygame.init()
        
        self.running = True
        while self.running:
            self.__screens[self.current_screen].run()
    
    def start_game(self):
        self.current_screen = GameScreen.ID
    
    def change_screen(self, screen):
        self.current_screen = screen.ID

    def exit(self):
        self.running = False
