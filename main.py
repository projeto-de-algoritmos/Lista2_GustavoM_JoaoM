from game import Game
from structs import Graph, read_graphs

graphs = read_graphs('graphs.txt')
g = Game()
g.run(graphs)
