import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

#Топологическая сортировка DAG, по алгоритму Кана
#Исключительно тестовая версия с использованием networkx как родительского класса.
class topoSort(nx.DiGraph):
    def count_verts(self): # считаем входящие и исходящие ребра, количество вершин
        """ Подготовка графа к сортировке, считаем входящие, исходящие веришны и общее количество вершин """
        self.d = {} # словарь в который мы соберем out_degree
        for _ in self.nodes(): # добавляем вершины из которых выходят ребра в словарь
            self.d[_] = []
            
        for l in self.edges: # считаем кол-во out_degree для наших вершин и записываем в формате {(int) FROM : list [(int) TO, *n]}
            if l[0] in self.d: # l[0], l[1] т.к. self.edges хранит кортежы (А, Б), ребро из А в вершину Б
                self.d.setdefault(l[0], []).append(l[1]) # все исходящие ребра из вершины l[0] храняться в словаре с ключом l[0] (наименование веришны), возврат ключа - списко вершин в которые наши ребра направлены.
        
    def topological_sort_r(self, v: int, node_list: list, stack: list)->None:
        """ Рекрусия для сортировки, не вызывать на прямую """
        node_list.remove(v) #отмечаем вершину как пройденную (удаляем ее из общего списка вершин
        for i in self.d[v]: #повторяем для каждой вершины для который мы являлись in_degree ->
            if i in node_list:
                self.topological_sort_r(i, node_list, stack) # рекурсия для нахождения всех "дочерних узлов"
                
        stack.append(v) #добавляем вершину в стак ( по факту лист, просто выведем его с "хвоста"
 
 
    def topological_sort(self):
        """ Используем топологическую сортировку (граф DAG) для получения сортированного графа, исходный граф не изменяеться! """
        node_list = list(self.nodes()) # все вершины для удобства "отметки" храним в списке, пройденные просто удалим из него
        stack = [] 
        for i in range(len(self.nodes())):# родительский метод nodes() возвращает список всех вершин
            if i in node_list:
                self.topological_sort_r(i, node_list, stack)
                
        print(stack[::-1]) #ВНИМАНИЕ! Мы только выводим результат сортировки в консоль, сам исходный граф остаётся не изменным
        
    def find_path(self, start: int, end: int, current_path=[])->list:
        """ Ищем путь из точки А в точку Б """
        current_path.append(start)
        if start == end:
            return current_path
        if start not in self.d:
            return [-1]
        for vert in self.d[start]:
            if vert not in current_path:
                long_path = self.find_path(vert, end, current_path)
                if long_path:
                    return long_path
        return [-1]
                
        
        
directedGraph = topoSort()

#directedGraph.add_edges_from([('E', 'C'), ('E', 'A'), ('D', 'A'), ('E', 'B'), ('C', 'D'), ('D', 'B')])
graph_edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
directedGraph.add_edges_from(graph_edges)

directedGraph.count_verts()
directedGraph.topological_sort()

directedGraphPath = topoSort()


print(directedGraph.find_path(5, 1))


nx.draw(directedGraph, with_labels=True, font_weight='bold')
plt.show()

