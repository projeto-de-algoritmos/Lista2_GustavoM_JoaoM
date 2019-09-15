from game import Game
from graph import Graph, read_graphs

graphs = read_graphs('graphs.txt')
g = Game()
g.run(graphs)
