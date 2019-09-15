from collections import deque, namedtuple


# Grafo Direcionado
class Graph:
    inf = float('inf')
    Edge = namedtuple('Edge', 'start, end, cost')

    def __init__(self, tam=0, source="", destination="", edges=[]):
        self.tam = tam
        self.source = source
        self.destination = destination
        self.edges = ([self.make_edge(*edge) for edge in edges])

    @property
    def vertices(self):
        return set(sum( ([edge.start, edge.end] for edge in self.edges), []) )

    @property
    def neighbours(self):
        neighbours = { vertex: set() for vertex in self.vertices }
        for edge in self.edges:
            neighbours[edge.start].add( (edge.end, edge.cost) )
        return neighbours
    
    def make_edge(self, start, end, cost=1):
        return self.Edge(start, end, cost)

    def dijkstra(self):
        assert self.source in self.vertices, 'Essa origem não existe'
        assert self.destination in self.vertices, 'Esse destino não existe'

        distances = { vertex: self.inf for vertex in self.vertices }
        previous_vertices = { vertex: None for vertex in self.vertices }
        distances[self.source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == self.inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), self.destination
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)        

        return path


def read_graphs(path):
    file = open(path)
    contents = file.read().split('$')[1:-1]
    graphs = []
    
    for content in contents:
        lines = content.split('\n')[1:-1]
        tam = int(lines[0])
        source, destination = map(int, lines[1].split())
        
        edges = []
        for line in lines[2:]:
            u, v, c = map(int, line.split())
            edges.append((u, v, int(c)))
        
        graph = Graph(tam, source, destination, edges)
        graphs.append(graph)
    return graphs
