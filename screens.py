import pygame, math

# from pygame.locals import *
from assets import Button, Text, Palette, Truck


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
        # self.game.screen.fill(Palette.COLOR_1)

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
        super().__init__(game=game, background_color=Palette.COLOR_1)
        
        # Assets
        title = Text(
            screen=self.game.screen, position=((self.x_middle),(100)),
            text=self.game.GAME_NAME, font_size=60
        )
        sub_title = Text(
            screen=self.game.screen, position=((self.x_middle), (180)),
            text=self.game.INTRO_TEXT, font_size=34, font_color=Palette.COLOR_5
        )
        
        info_icon = pygame.image.load('info.png')
        info_button = Button(
            screen=self.game.screen, position=((70), (40)),
            on_press=lambda:game.change_screen(InfoScreen), icon=info_icon,
            text="Info", width=120, color=Palette.COLOR_1
        )

        play_button = Button(
            screen=game.screen, position=((self.x_middle), (game.HEIGHT-200)),
            on_press=self.game.start_game, text='Jogar', width=300
        )

        self.put_asset(title)
        self.put_asset(sub_title)
        self.put_asset(info_button)
        self.put_asset(play_button)


class InfoScreen(Screen):
    ID = 3

    def __init__(self, game):
        super().__init__(game=game, background_color=Palette.COLOR_9)

        # Assets
        back_button = Button(
            screen=self.game.screen, position=((79), (40)),
            on_press=lambda:game.change_screen(Menu), text='Voltar', width=120
        )
        title = Text(
            screen=self.game.screen, position=((self.x_middle), (40)),
            text='A definir', font_size=38, font_color=Palette.BLACK
        )

        definition_text = open('definition.txt').read()
        definition = Text(
            screen=self.game.screen, position=((self.x_middle), (self.y_middle)),
            text=definition_text, font_size=24, font_type='robotoslab',
            font_color=Palette.BLACK
        )

        self.put_asset(back_button)
        self.put_asset(title)
        self.put_asset(definition)


class GameScreen(Screen):
    ID = 2
    
    def __init__(self, game):
        super().__init__(game=game, background_color=Palette.BLUE)
        
        # Assets
        truck = Truck(screen=game.screen)
        self.put_asset(truck)

