import datetime, structs, math, pygame
from collections import deque


def dist(pos1, pos2):
    return math.hypot(pos2[0]-pos1[0], pos2[1]-pos1[1])


def ang(pos1, pos2):
    return math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])


class Palette:
    COLOR_1 = (85, 94, 123)
    COLOR_5 = (253, 228, 127)
    COLOR_8 = (35, 150, 170)
    COLOR_9 = (238, 238, 238)
    COLOR_10 = (38, 50, 56)
    COLOR_11 = (117, 117, 117)
    COLOR_12 = (66, 66, 66)

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


class Timer(Asset):  
    def __init__(
        self, surface, color, rect, start_angle, stop_angle, width, 
        on_finished=lambda:None
        ):
        self.screen = surface
        self.color = color
        self.rect = rect
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.width = width
        self.on_finished = on_finished
        self.seconds = 0

    def draw(self):
        to_timer = 15 - self.seconds
        if to_timer < 0:
            self.on_finished()
        pygame.draw.arc(
            self.screen, self.color, self.rect, self.start_angle,
            self.stop_angle - 0.41866667*self.seconds, self.width
        )


class Truck(Asset):
    default_time = 2
    endmove_time = datetime.datetime.now()

    def __init__(self, screen, position=(100, 160)):    
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
        pass
        #mouse_pos = pygame.mouse.get_pos()
        #if event.type == pygame.MOUSEBUTTONUP:
            #self.move(mouse_pos)

    def get_pos(self):
        time_now = datetime.datetime.now()

        if time_now>self.endmove_time:
            return self.end_position
        
        c_time = (self.endmove_time-time_now).total_seconds()
        theta = ang(self.start_position, self.end_position)
        hp = dist(self.start_position, self.end_position)
        w = (c_time/self.default_time) # w = 2
        x = self.end_position[0]-math.cos(theta)*(hp*w)
        y = self.end_position[1]-math.sin(theta)*(hp*w)
        return (x, y)

    def move(self, position):
        pygame.mixer.music.load('sonds/vrum.mp3')
        pygame.mixer.music.play(0)
        self.start_position = self.end_position
        self.end_position = position
        self.endmove_time = datetime.datetime.now()+datetime.timedelta(
            seconds=self.default_time
        )


class Button(Asset):

    def __init__(
        self, screen, position, on_press=lambda:None, 
        on_focus=lambda:None, text='', font_size=30, width=200, height=50,
        color=Palette.BLUE, font_color=Palette.WHITE, focused_color=Palette.COLOR_8,
        press_color=Palette.COLOR_5, icon=None
    ):
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
        self.text = Text(
            screen=self.screen, text=text, position=self.center, font_size=font_size,
            font_color=font_color
        )

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
            # self.pressed = True
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
    
    def __init__(
        self, screen, position, text='', font_size=30, font_color=Palette.WHITE,
        font_type='freesansbold.ttf', padding=5
    ):
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
        y_pos = self.center[1]-(
            max(0, n//2-1)*self.padding + max(0, n//2-1)*self.font_size
        )
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


class Line(Asset):

    def __init__(
        self, screen, pos1=(0, 0), pos2=(0, 0), line_thickness=7, visible=True,
        color=Palette.COLOR_12, mouse_guide=False
    ):
        self.screen = screen
        self.pos1 = pos1
        self.pos2 = pos2
        self.line_thickness = line_thickness
        self.visible = visible
        self.color = color

    def get_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.pos2 = (mouse_pos[0], mouse_pos[1])

    def draw(self):
        if self.visible:
            pygame.draw.line(
                self.screen, self.color, self.pos1, self.pos2, self.line_thickness
            )


class Node(Asset):
    
    def __init__(
        self, game, circle_radius=25,  position=(100, 100),
        default_color=Palette.COLOR_11, on_press=lambda a:None, on_focus=lambda:None,
        on_unfocus=lambda:None, ID=0
    ):
        self.game = game
        self.circle_radius = circle_radius
        self.on_press = on_press
        self.on_focus = on_focus
        self.on_unfocus = on_unfocus
        self.position = position
        self.mouse_over = False
        self.color = default_color
        self.default_color = default_color
        self.ID = ID

    def draw(self):
        pygame.draw.circle(
            self.game.screen, self.color, self.position, self.circle_radius
        )
        
    def get_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        dist = math.hypot(mouse_pos[0]-self.position[0], mouse_pos[1]-self.position[1])
        if dist<=self.circle_radius:
            if event.type==pygame.MOUSEBUTTONUP:
                self.color = Palette.RED
                print(self.ID)
                self.on_press(self.ID)
            else:
                self.color = Palette.COLOR_12
                self.on_focus()
        else:
            self.color = self.default_color
            self.on_unfocus()


class Edge(Asset):

    def __init__(
        self, game, pos1=(100, 100),  pos2=(500, 500),
        color=Palette.COLOR_12, line_thickness=5, weight=1,
        num_padding=15
    ):
        self.game = game
        self.pos1 = pos1
        self.pos2 = pos2
        self.line_thickness = line_thickness
        self.color = color
        self.xmed = (pos1[0]+pos2[0])//2
        self.ymed = (pos1[1]+pos2[1])//2
        self.weight=Text(
            screen=self.game.screen, position=(self.xmed, self.ymed), 
            text=str(weight), font_size=30, font_color=color
        ) 

    def draw(self):
        pygame.draw.line(
            self.game.screen, self.color, self.pos1, self.pos2, self.line_thickness
        )
        pygame.draw.circle(
            self.game.screen, Palette.COLOR_9, (self.xmed, self.ymed), 15
        )
        self.weight.draw()


class Graph(Asset):

    def __init__(
        self, game, graph=structs.Graph(1), reveal=False, circle_radius=25,
        line_thickness=3, editable=False, truck=None
    ):
        self.game = game
        self.reveal = reveal
        self.circle_radius = circle_radius
        self.line_thickness = line_thickness
        self.editable = editable
        self.truck = truck
        self.set_graph(graph)

    def press_node(self, i):
        if self.truck != None:
            if i in self.graph.adj_list[self.current_node]:
                self.current_node = i
                self.path.add(i+1)
                self.node_list[i].default_color = Palette.BLUE
                self.truck.move(self.positions[i])

    def set_graph(self, graph):
        self.node_list = []
        self.edge_list = []
        self.graph = graph
        self.positions = get_positions(
            self.graph.tam, self.game.WIDTH,
            self.game.HEIGHT
        )
        if self.truck!=None:
            self.truck.start_position = self.positions[0]
            self.truck.end_position = self.positions[0]

        for k in range(self.graph.tam):
            if (k+1) == self.graph.tam:
                node = Node(
                    self.game, circle_radius=self.circle_radius,
                    position=self.positions[k],
                    on_press=self.press_node, ID=k,
                    default_color=Palette.GREEN
                )
            else:
                node = Node(
                    self.game, circle_radius=self.circle_radius, 
                    position=self.positions[k], 
                    on_press=self.press_node, ID=k
                )
            self.node_list.append(node)
        for u, v, w in self.graph.edge_list:
            edge = Edge(
                self.game, pos1=self.positions[u], 
                pos2=self.positions[v], line_thickness=self.line_thickness,
                weight=w
            )
            self.edge_list.append(edge)
        self.current_node = 0
        self.node_list[0].default_color = Palette.BLUE
        self.path = {1}

    def draw(self):
        for edge in self.edge_list:
            edge.draw()
        for node in self.node_list:
            node.draw()

    def get_event(self, event):
        for edge in self.edge_list:
            edge.get_event(event)
        for node in self.node_list:
            node.get_event(event) 


# class Graph(Asset):
#     node_select = -1
#     pressed = False
#     user_answer = deque()

#     def __init__(
#         self, game, graph=structs.Graph(1), reveal=False, circle_radius=25,
#         line_thickness=5, editable=False, ):
#         self.game = game
#         self.graph = graph
#         self.reveal = reveal
#         self.circle_radius = circle_radius
#         self.line_thickness = line_thickness
#         self.editable = editable
#         self.positions = get_positions(
#             self.graph.tam, self.game.WIDTH, self.game.HEIGHT
#         )
#         self.answer_color = None

#     def set_graph(self, graph):
#         self.graph = graph
#         self.positions = get_positions(
#             self.graph.tam, self.game.WIDTH, self.game.HEIGHT
#         )

#     def get_event(self, event):
#         mouse_pos = pygame.mouse.get_pos()
#         if event.type == pygame.MOUSEBUTTONUP:
#             self.on_press()
#             self.pressed = True
#         else:
#             self.pressed = False
        
#         select = -1
#         i = 0
#         for position in self.positions:
#             dist = math.hypot(mouse_pos[0]-position[0], mouse_pos[1]-position[1])
#             if dist<=self.circle_radius:
#                 select = i
#             i+=1
#         self.node_select = select

#     def draw_node(self, i, color=Palette.COLOR_11):
#         pygame.draw.circle(
#             self.game.screen, color, self.positions[i], self.circle_radius
#         )
    
#     def draw_edge(self, u, v, color=Palette.COLOR_12):
#         pos1 = self.positions[u-1]
#         pos2 = self.positions[v-1]
#         a = pos1[1]-pos2[1]
#         b = pos2[0]-pos1[0]
#         theta = math.atan2(a, b)
#         x1 = pos1[0]+math.cos(theta)*self.circle_radius
#         y1 = pos1[1]-math.sin(theta)*self.circle_radius
#         x2 = pos2[0]-math.cos(theta)*self.circle_radius
#         y2 = pos2[1]+math.sin(theta)*self.circle_radius
#         pygame.draw.line(
#             self.game.screen, color, (x1, y1), (x2, y2), self.line_thickness
#         )

#     def on_press(self):
#         pass
#     def draw(self):
#         template = self.graph.path
#         for i in range(self.graph.tam):
#             if self.editable and self.node_select==i and self.pressed:
#                 self.draw_node(i=i, color=Palette.COLOR_8)
#             elif self.editable and self.node_select==i and not self.pressed:
#                 self.draw_node(i=i, color=Palette.COLOR_5)
#             elif self.reveal:
#                 if i+1 in template:
#                     self.draw_node(i=i, color=self.answer_color)
#                 else:
#                     self.draw_node(i=i)
#             elif not self.editable and self.node_select==i and self.pressed:
#                 if i+1 not in self.user_answer:
#                     self.user_answer.append(i+1)
#                 self.draw_node(i=i, color=Palette.BLUE)
#                 if self.graph.path[-1] - 1 == i:
#                     self.game.answer_question(self.user_answer)
#                     self.user_answer = deque()
#                     self.node_select = -1
#             elif (i+1) not in self.user_answer:
#                 if self.graph.path[0] - 1 == i:
#                     self.draw_node(i=i, color=Palette.BLACK)
#                 elif self.graph.path[-1] - 1 == i:
#                     self.draw_node(i=i, color=Palette.GREEN)
#                 else:
#                     self.draw_node(i=i)
#             else:
#                 self.draw_node(i=i, color=Palette.BLUE)

#         if not self.reveal:
#             for u, v, c in self.graph.edge_list:
#                 self.draw_edge(u, v)
#         else:
#             for pos in range(len(template)-1):
#                 self.draw_edge(template[pos], template[pos+1], self.answer_color)
#             self.user_answer = deque()


def get_positions(tam, screen_width, screen_heigth):
    # Posições dos nós de acordo com o tamanho dos grafos
    x_mid = screen_width//2 
    y_mid = screen_heigth//2
    
    if tam==1:
        return [(100, 240)]
    elif tam==2:
        return [(100, 240), (924, 528)]
    elif tam==3:
        return [(100, 240), (360, 640), (620, 440)]
    elif tam==4:
        return [(100, 240), (360, y_mid), (200, y_mid-100), 
                (700, y_mid)]
    elif tam==5:
        return [(100, 240), (x_mid-150, y_mid-50), (x_mid-150, y_mid+150),
                (x_mid+150, y_mid+150), (x_mid+150, y_mid-50)]
    elif tam==6:
        return [(100, 240), (x_mid-200, y_mid), (x_mid-100, y_mid+150), 
                (x_mid+100, y_mid+150), (x_mid+200, y_mid), (x_mid+100, y_mid-150)]
    elif tam==7:
        return [(100, 240), (x_mid-100, y_mid-90), (x_mid-200, y_mid), 
                (x_mid-100, y_mid+120), (x_mid+100, y_mid+120), (x_mid+200, y_mid),
                (x_mid+100, y_mid-90)]
    elif tam==8:
        return [(100, 240), (200, 600), (340, 300), (400, 600), (500, 300),
                (700, 700), (700, 200), (900, 600)]
    elif tam==9:
        return [(100, 240), (190, 700), (280, 400), (370, 700), (460, 400), 
                (550, 700), (640, 400), (730, 700), (820, 400)]
    elif tam==10:
        return [(100, 240), (180, 528), (260, 240), (340, 528), (420, 240),
                (500, 528), (580, 240), (660, 528), (740, 240), (900, 600)]
