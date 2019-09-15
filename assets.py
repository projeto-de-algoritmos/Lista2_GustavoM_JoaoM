import pygame
import datetime
import math

def dist(pos1, pos2):
    return math.hypot(pos2[0]-pos1[0], pos2[1]-pos1[1])

def ang(pos1, pos2):
    return math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])

class Palette:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (224, 70, 68)
    BLUE = (67, 91, 198)
    GREEN = (104, 188, 39)

class Asset:
    def get_event(self, event):
        pass
    def draw(self):
        pass

class Truck(Asset):
    default_time = 2.5
    endmove_time = datetime.datetime.now()
    def __init__(self, screen, position=(100, 100)):
        
        self.surface = pygame.image.load('assets/truck.png')
        self.rect = self.surface.get_rect()
        self.start_position = position
        self.end_position = position
        self.screen = screen
        self.endmove_time = datetime.datetime.now()

    def draw(self):
        position = self.get_pos()
        rect = self.surface.get_rect()
        rect.center = position
        self.screen.blit(self.surface, rect)

    def get_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            self.move(mouse_pos)

    def get_pos(self):
        time_now = datetime.datetime.now()
        if time_now>self.endmove_time:
            return self.end_position
        c_time = (self.endmove_time-time_now).total_seconds()
        theta = ang(self.start_position, self.end_position)
        hp = dist(self.start_position, self.end_position)
        w = (c_time/self.default_time)
        #w = 2
        x = self.end_position[0]-math.cos(theta)*(hp*w)
        y = self.end_position[1]-math.sin(theta)*(hp*w)
        return (x, y)

    def move(self, position):
        pygame.mixer.music.load('sonds/vrum.mp3')
        pygame.mixer.music.play(0)
        self.start_position = self.end_position
        self.end_position = position
        self.endmove_time = datetime.datetime.now()+datetime.timedelta(seconds=self.default_time)

class Button(Asset):
    def __init__(self, screen, position, on_press=lambda:None, 
        on_focus=lambda:None, text='', font_size=30, 
        width=200, height=50, color=Palette.BLUE, font_color=Palette.WHITE, 
        focused_color=Palette.GREEN, press_color=Palette.BLACK,
        icon=None):
        self.icon = icon
        self.screen = screen
        self.center = position
        self.on_press = on_press
        self.on_focus = on_focus
        self.width = width
        self.height = height
        self.color = color
        self.focused_color = focused_color
        self.press_color = press_color
        self.pressed = False
        self.focused = False
        self.text = Text(screen=self.screen, text=text, position=self.center, font_size=font_size, font_color=font_color)

    def get_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        x1 = self.center[0]-self.width/2
        y1 = self.center[1]-self.height/2
        x2 = self.center[0]+self.width/2
        y2 = self.center[1]+self.height/2
        if mouse_pos[0]>=x1 and mouse_pos[0]<=x2 and mouse_pos[1]>=y1 and mouse_pos[1]<=y2:
            self.focused = True
        else:
            self.focused = False
            return    
        if self.focused and event.type == pygame.MOUSEBUTTONUP:
            #self.pressed = True
            self.on_press()
        else:
            self.pressed = False
            if self.focused:
                self.on_focus()

    def draw(self, event=None):
        b_color = self.color
        if self.focused and self.pressed:
            b_color = self.press_color
        elif self.focused:
            b_color = self.focused_color            
        x1 = self.center[0]-self.width/2
        y1 = self.center[1]-self.height/2
        pygame.draw.rect(self.screen, b_color, (x1,y1, self.width, self.height))
        if self.icon:
            self.icon = pygame.transform.scale(self.icon, (30, 30))
            rect = self.icon.get_rect()
            rect.center = (x1+20, self.center[1])
            self.screen.blit(self.icon, rect)
            self.text.center = (self.center[0]+20, self.center[1])
        self.text.draw()

class Text(Asset):
    def __init__(self, screen, position, text='', font_size=30, font_color=Palette.WHITE, font_type='freesansbold.ttf', padding=5):
        self.screen = screen
        self.text = text
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.padding = padding
        self.center = (position)

    def draw(self):
        lines = self.text.split('\n')
        n = len(lines)
        y_pos = self.center[1]-( max(0, n//2-1)*self.padding + max(0, n//2-1)*self.font_size )
        if n!=1 and n%2==1:
            y_pos -= int(self.padding/2+self.font_size/2)
        x_pos = self.center[0]
        self.style = pygame.font.SysFont(self.font_type, self.font_size)
        for line in lines:
            text_surf = self.style.render(line, True, self.font_color)
            text_rect = text_surf.get_rect()
            text_rect.center = (x_pos, y_pos)
            self.screen.blit(text_surf, text_rect)
            y_pos+=self.font_size+self.padding
    