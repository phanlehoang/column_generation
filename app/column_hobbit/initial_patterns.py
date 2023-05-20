from csp_wizard.node import Node
import numpy as np
from arc import Arc
class InitialPatternsGenerator:
    def __init__(self, tasks, T_idle, T_drive) :
        self.tasks = tasks
        self.T_idle = T_idle
        self.T_drive = T_drive
        self.n = len(tasks)
        self.patterns = []
        self.current_pattern=[]
        self.visited = {}
        self.current_driving_duration = 0
    def create_nodes(self):
        self.nodes = [Node(id = i,
                           arcs=[]
                           ) for i in range(self.n+1)]
        for i in range(1, len(self.tasks)+1):
            for j in range(i,len(self.tasks)+1):
                if(self.tasks[j-1].time_start >= self.tasks[i-1].time_end
                   and self.tasks[j-1].time_start - self.tasks[i-1].time_end <= self.T_idle):
                    self.nodes[i].arcs.append(Arc(
                        start_point=i,
                        end_point=j,
                    ))
    def checkT_drive(self, next_position):
        return (self.current_driving_duration + self.tasks[next_position].time_end 
                - self.tasks[next_position].time_start <= self.T_drive)
    
    def dfs_search(self, node ):
        if node.id not in self.visited:
            self.visited[node.id] = True
            self.current_pattern.append(node.id-1)
            self.current_driving_duration += self.tasks[node.id-1].time_end - self.tasks[node.id-1].time_start
            isEnd = True
            for arc in node.arcs:
                if(arc.end_point not in self.visited):
                    if(self.checkT_drive(arc.end_point-1)):
                        isEnd = False
                        self.dfs_search(self.nodes[arc.end_point])
                        break
            if(isEnd and len(self.current_pattern) >= 1):
                self.patterns.append(self.current_pattern)
                self.current_pattern=[]
                self.current_driving_duration = 0
    def solve(self):
        self.create_nodes()
        for i in range(1, len(self.tasks)+1):
            self.current_pattern = []
            self.dfs_search(self.nodes[i])
    def pattern_column_generator(self):
        self.patterns_columns = np.zeros((self.n, len(self.patterns)))
        for i in range(len(self.patterns)):
            for j in range(len(self.patterns[i])):
                self.patterns_columns[self.patterns[i][j]][i] = 1
        return None