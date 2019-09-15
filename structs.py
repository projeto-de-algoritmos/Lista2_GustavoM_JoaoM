from collections import deque, namedtuple

class UnionFind:
    def __init__(self, n):
        self.parent = []
        self.rank = []
        for i in range(n):
            self.rank.append(0)
            self.parent.append(i)
    def find(self, i):
        return i if self.parent[i]==i else self.find(self.parent[i])
    def is_same_set(self, i, j):
        return self.find(i)==self.find(j)
    def union_set(self, i, j):
        x = self.find(i)
        y = self.find(j)
        if self.rank[x]>self.rank[y]:
            self.parent[y]=x
        else:
            self.parent[x]=y
            if(self.rank[x]==self.rank[y]):
                self.rank[y]+=1


# Grafo Direcionado
class Graph:
    def __init__(self, tam):
        self.tam = tam
        self.edge_list = []
        self.mst_adj_list = []
        for _ in range(self.tam):
            self.mst_adj_list.append(set())

    def add_edge(self,u,v,w):
        self.edge_list.append([u-1,v-1,w])

    # Arvore geradora máxima
    def kruskal(self):
        self.edge_list =  sorted(self.edge_list, key=lambda item: item[2], reverse=True) 
        uf = UnionFind(self.tam)
        for edge in self.edge_list:
            if not uf.is_same_set(edge[0], edge[1]):
                self.mst_adj_list[edge[0]].add(edge[1])
                self.mst_adj_list[edge[1]].add(edge[0])
                uf.union_set(edge[0], edge[1])
    
    def get_path(self, source, destination):
        assert source>0 and source<=self.tam, 'Essa origem não existe'
        assert destination>0 and destination<=self.tam, 'Esse destino não existe'
        source-=1
        destination-=1
        q = []
        visited = [False]*(self.tam)
        pred = [-1]*(self.tam)
        q.append(source)
        visited[source]=True
        pred[source] = source     
        while len(q)>0:
            u = q.pop()
            for v in self.mst_adj_list[u]:
                if visited[v]:
                    continue
                visited[v]=True
                pred[v]=u
                if v==destination:
                    q.clear()
                    break
                q.append(v)
        path = []
        path.append(destination+1)
        u = destination
        while pred[u]!=source:
            path.append(pred[u]+1)
            u = pred[u]
        path.append(source+1)
        path.reverse()
        self.path = path
        print(path)

def read_graphs(path):
    file = open(path)
    contents = file.read().split('$')[1:-1]
    graphs = []
    for content in contents:
        lines = content.split('\n')[1:-1]
        tam = int(lines[0])
        source, destination = map(int, lines[1].split())
        graph = Graph(tam)
        for line in lines[2:]:
            u, v, c = map(int, line.split())
            graph.add_edge(u, v, c)   
        graph.kruskal()
        graph.get_path(source, destination)  
        graphs.append(graph)
    return graphs