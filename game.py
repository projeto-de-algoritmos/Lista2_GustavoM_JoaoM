import pygame
from screens import AnswerScreen, FinishScreen, InfoScreen, MenuScreen, QuestionScreen


class Game:
    # Game constants
    WIDTH = 1024
    HEIGHT = 768
    GAME_NAME = 'Jogo dos Caminhos'
    INTRO_TEXT = 'Identifique o melhor caminho segundo as regras'

    # Game states
    running = True

    __screens = {}
    current_screen = MenuScreen.ID
    
    CORRECT_ANSWER = 1
    WRONG_ANSWER = 2
    TIMES_UP = 3
    state_question = CORRECT_ANSWER

    graphs = []
    standard_graphs = []
    current_graph = None
    current_question = 0
    max_questions = 0
    correct_ans = 0
    wrong_ans = 0

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        pygame.display.set_caption(self.GAME_NAME)
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        
        self.__screens[MenuScreen.ID] = MenuScreen(self)
        self.__screens[InfoScreen.ID] = InfoScreen(self)
        self.__screens[QuestionScreen.ID] = QuestionScreen(self)
        self.__screens[AnswerScreen.ID] = AnswerScreen(self)
        self.__screens[FinishScreen.ID] = FinishScreen(self)
        
        self.clock = pygame.time.Clock()

    def run(self, graphs=[]):
        pygame.init()
        
        self.standard_graphs = graphs
        self.max_questions = len(graphs)

        while self.running:
            self.__screens[self.current_screen].run()
    
    def exit(self):
        self.running = False

    def start_game(self):
        self.current_question = 0
        self.wrong_ans = 0
        self.correct_ans = 0
        
        self.graphs = self.standard_graphs
        self.max_questions = len(self.graphs)
        
        self.change_screen(QuestionScreen)
    
    def change_screen(self, screen):
        self.current_screen = screen.ID
    
    def no_answer_question(self):
        print('path', self.current_graph.path)
        self.current_graph.path
        self.state_question = self.TIMES_UP
        self.change_screen(AnswerScreen)

    def answer_question(self, user_answer):
        print('path', self.current_graph.path)
        if self.current_graph.path == user_answer:
            self.correct_ans+=1
            self.state_question = self.CORRECT_ANSWER
        else:
            self.wrong_ans+=1
            self.state_question = self.WRONG_ANSWER
        self.change_screen(AnswerScreen)

    def next_question(self):
        self.current_question = self.current_question+1 
        if self.current_question>=self.max_questions:
            self.current_question = 0
            self.change_screen(FinishScreen)
        else:
            self.change_screen(QuestionScreen)
