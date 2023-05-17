import numpy as np
import math

from bucket import Bucket
class TimeConstraintShortestPathSolverVer2 :
    def __init__(self, nodes, start_node, end_node, time_constraint,) :
        self.nodes = nodes
        if(nodes[0].id==1):
            #thêm 1 node vào đầu mảng
            self.nodes.insert(0,None)
        self.start_node = start_node
        self.end_node = end_node
        self.time_constraint = time_constraint
        self.new_pattern = None
        self.new_pattern_column = None
    

    def __repr__(self) :
        return "TimeConstraintShortestPathSolver({}, {}, {}, {})".format(self.nodes, self.start_node, self.end_node, self.time_constraint)
    def __str__(self):
        return "TimeConstraintShortestPathSolver({}, {}, {}, {})".format(self.nodes, self.start_node, self.end_node, self.time_constraint)
    def init_solve(self):
        #tạo d(i,j) là mảng 2 chiều i từ 0->6, j từ 0-> time_constraint
        #tạo mảng 2 chiều d[i][j] là mảng 1 chiều j từ 0-> time_constraint
        self.d = {}
        self.d[self.start_node, 0] = 0
        #a = infinty trong pytho
        self.prev = {}
        self.list = [(self.start_node, 0 )]
    def list_process(self):
        while len(self.list) > 0 :
            bucket = self.list.pop()
            current_node_id = bucket[0]
            for arc in self.nodes[current_node_id].arcs:
                if bucket[1] + arc.travel_time <= self.time_constraint:
                    if(current_node_id, bucket[1]) not in self.d:
                            self.d[current_node_id, bucket[1]] = math.inf
                    if(arc.end_point, int(bucket[1] + arc.travel_time)) not in self.d:
                            self.d[arc.end_point, int(bucket[1] + arc.travel_time)] = math.inf
                
                    if (self.d[current_node_id, bucket[1]] + arc.cost <
                            self.d[arc.end_point, int(bucket[1] + arc.travel_time)]):
                            self.d[arc.end_point,int( bucket[1] + arc.travel_time)] = self.d[current_node_id, bucket[1]] + arc.cost
                            self.prev[arc.end_point, bucket[1] + arc.travel_time] = bucket[0], bucket[1]
                            self.list.append((arc.end_point, bucket[1] + arc.travel_time))
                    
                        
                    
                
    def solve(self):
        self.init_solve()
        self.list_process()

    def get_result(self):
        #B1: tìm time trong d[end_node][time<= time_constrant] sao cho d ở đó là min
        choose_time = self.time_constraint
        if(self.end_node, self.time_constraint) not in self.d:
            self.d[self.end_node, self.time_constraint] = math.inf
        for i in range(self.time_constraint-1, -1, -1):
            if (self.end_node, i) in self.d:
                if self.d[self.end_node, i] < self.d[self.end_node, choose_time]:
                    choose_time = i
        #B2: tìm đường đi từ end_node về start_node
        result = []
        current_node_id = self.end_node
        current_time = choose_time
        while current_node_id != self.start_node:
            result.append(current_node_id)
            prev_node_id = self.prev[current_node_id, current_time][0]
            prev_time = self.prev[current_node_id, current_time][1]
            current_node_id = prev_node_id
            current_time = prev_time
        result.append(self.start_node)
        result.reverse()
        return result
    
    def get_new_pattern_from_path(self,ans, tasks):
        self.new_pattern = []
        self.new_pattern_column = np.zeros(len(tasks))
        for i in range(len(ans)-1):
            if ans[i]%2 == 1:
                position = int((ans[i]-1)/2)
                self.new_pattern_column[position] = 1
                self.new_pattern.append(position)