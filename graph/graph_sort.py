import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

#Топологическая сортировка DAG, по алгоритму Кана
#Исключительно тестовая версия с использованием networkx как родительского класса.
class topoSort(nx.DiGraph):
    def count_verts(self): # считаем входящие и исходящие ребра, количество вершин
        self.V = len(self.nodes()) # родительский метод nodes() возвращает список всех вершин
        self.d = {} # словарь в который мы соберем out_degree
        for _ in self.nodes(): # добавляем вершины из которых выходят ребра в словарь
            self.d[_] = []
            
        for l in self.edges: # считаем кол-во out_degree для наших вершин и записываем в формате {(int) FROM : list [(int) TO, *n]}
            if l[0] in self.d: # l[0], l[1] т.к. self.edges хранит кортежы (А, Б), ребро из А в вершину Б
                self.d.setdefault(l[0], []).append(l[1]) # все исходящие ребра из вершины l[0] храняться в словаре с ключом l[0] (наименование веришны), возврат ключа - списко вершин в которые наши ребра направлены.
        
    def topologicalSortR(self, v, node_list, stack):
        node_list.remove(v)
        for i in self.d[v]:
            if i in node_list:
                self.topologicalSortR(i, node_list, stack) # рекурсия для нахождения всех "дочерних узлов"
                
        stack.append(v)
 
 
    def topologicalSort(self):
        node_list = list(self.nodes())
        stack = []       
        for i in range(self.V):
            if i in node_list:
                self.topologicalSortR(i, node_list, stack)
                
        print(stack[::-1])
        


directedGraph = topoSort()

#directedGraph.add_edges_from([('E', 'C'), ('E', 'A'), ('D', 'A'), ('E', 'B'), ('C', 'D'), ('D', 'B')])
directedGraph.add_edges_from([(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1) ])

directedGraph.count_verts()
directedGraph.topologicalSort()


nx.draw(directedGraph, with_labels=True, font_weight='bold')
plt.show()  
