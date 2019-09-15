import pygame 
import math
# from pygame.locals import *
from assets import Button
from assets import Text
from assets import Palette
from assets import Truck

class Screen:
    # Screen codes
    ID = 0
    def __init__(self, game, background_color):
        self.game = game
        self.background_color = background_color
        self.x_middle = self.game.WIDTH/2
        self.y_middle = self.game.HEIGHT/2
        self.assets = []
    def build_function(self):
        pass
    def update_function(self):
        pass
    def put_asset(self, asset):
        self.assets.append(asset)

    def draw(self):
        self.game.screen.fill(self.background_color)
        self.update_function()
        for asset in self.assets:
            asset.draw()
    def run(self):
        self.build_function()
        while self.game.running and self.game.current_screen==self.ID:
            for event in pygame.event.get():
                for asset in self.assets:
                    asset.get_event(event)
                if event.type == pygame.QUIT:
                    self.game.exit()
            self.draw()
            pygame.display.update()

class Menu(Screen):
    ID = 1
    def __init__(self, game):
        super().__init__(game=game, background_color=Palette.BLUE)
        #Assets
        truck = Truck(screen=game.screen)
        self.put_asset(truck)