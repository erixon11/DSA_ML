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
            if i in node_list: # если вершина не отмечена -
                self.topological_sort_r(i, node_list, stack) # рекурсия для нахождения всех "дочерних узлов"
                
        stack.append(v) #добавляем вершину в стак ( по факту лист, просто выведем его с "хвоста"
 
 
    def topological_sort(self):
        """ Используем топологическую сортировку (граф DAG) для получения сортированного графа, исходный граф не изменяеться! """
        node_list = list(self.nodes()) # все вершины для удобства "отметки" храним в списке, пройденные просто удалим из него
        stack = [] 
        for i in range(len(self.nodes())):# родительский метод nodes() возвращает список всех вершин
            if i in node_list: # для каждой вершины повторяем нашу рекурсию
                self.topological_sort_r(i, node_list, stack) # уходим в рекурсивную функцию
                
        return(stack[::-1]) #ВНИМАНИЕ! Мы только выводим результат сортировки в консоль, сам исходный граф остаётся не изменным
        
    def find_path(self, start: int, end: int, current_path=[])->list:
        """ Ищем путь из точки А в точку Б """
        current_path.append(start) # добавим стартовую точку в наш путь.
        if start == end: #если начальная точка == конечной - вернём список с этой вершиной
            return current_path
        if start not in self.d: # если стартовая точка не является частью нашего графа, вернем -1
            return [-1]
        for vert in self.d[start]: # ищем все возможные пути из нашей стартовой точки
            if vert not in current_path: # если мы сделали "шаг", добавим его в наш "длинный список"
                long_path = self.find_path(vert, end, current_path) # рекурсивно повторяем всё с начала
                if long_path: # если путь есть - вернём его.
                    return long_path
        return [-1]
                
directedGraph = topoSort()

fromto = (5, 1) # кортеж с стартовой точкой поиска пути и конечной

#directedGraph.add_edges_from([('E', 'C'), ('E', 'A'), ('D', 'A'), ('E', 'B'), ('C', 'D'), ('D', 'B')])
graph_edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)] # ребра нашего графа

directedGraph.add_edges_from(graph_edges)
directedGraph.count_verts()
print("Default graph nodes: {} \nDefault graph edges: {}".format(directedGraph.nodes(), directedGraph.edges()))
sorted_graph = directedGraph.topological_sort()
print("Sorted graph: {}".format(sorted_graph))
path = directedGraph.find_path(*fromto)
print("Path {} is: {}".format(fromto, path)) 
color_map = []

#для более приятного восприятия, окрасим вершины на пути из точки Х в У синим цветом, а красными верщинами обозначим те, что мы не пройдём
for node in directedGraph.nodes():
    if node in path:
        color_map.append('blue')
    else: 
        color_map.append('red') 
        
nx.draw(directedGraph, node_color=color_map, edge_color='green', with_labels=True, font_weight='bold')
plt.show()
