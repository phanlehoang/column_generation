import numpy as np
import math

from bucket import Bucket
class TimeConstraintShortestPathSolver :
    def __init__(self, nodes, start_node, end_node, time_constraint,) :
        self.nodes = nodes
        if(nodes[0].id==1):
            #thêm 1 node vào đầu mảng
            self.nodes.insert(0,None)
        self.start_node = start_node
        self.end_node = end_node
        self.time_constraint = time_constraint
    

    def __repr__(self) :
        return "TimeConstraintShortestPathSolver({}, {}, {}, {})".format(self.nodes, self.start_node, self.end_node, self.time_constraint)
    def __str__(self):
        return "TimeConstraintShortestPathSolver({}, {}, {}, {})".format(self.nodes, self.start_node, self.end_node, self.time_constraint)
    def init_solve(self):
        #tạo d(i,j) là mảng 2 chiều i từ 0->6, j từ 0-> time_constraint
        #tạo mảng 2 chiều d[i][j] là mảng 1 chiều j từ 0-> time_constraint
        self.d = np.array( [[math.inf for i in range(self.time_constraint+1)] 
                           for j in range(len(self.nodes))])
        self.d[self.start_node, :] = 0
        #a = infinty trong pytho
        self.prev = np.array( [[Bucket(-1,-1) for i in range(self.time_constraint+1)] 
                           for j in range(len(self.nodes))])
        self.prev[self.start_node, :] = [Bucket(0,0) for i in range(self.time_constraint+1)]

        self.list = [Bucket(self.start_node,0)]
    def list_process(self):
        while len(self.list) > 0 :
            bucket = self.list.pop()
            current_node_id = bucket.node_id
            for arc in self.nodes[current_node_id].arcs:
                if bucket.time + arc.travel_time <= self.time_constraint:
                    if self.d[current_node_id, bucket.time] + arc.cost < self.d[arc.end_point, int(bucket.time + arc.travel_time)]:
                        self.d[arc.end_point,int( bucket.time + arc.travel_time)] = self.d[current_node_id, bucket.time] + arc.cost
                        self.prev[arc.end_point, bucket.time + arc.travel_time] = bucket.copy()
                        self.list.append(Bucket(arc.end_point, bucket.time + arc.travel_time))
    def solve(self):
        self.init_solve()
        self.list_process()

    def get_result(self):
        #B1: tìm time trong d[end_node][time<= time_constrant] sao cho d ở đó là min
        choose_time = self.time_constraint
        for i in range(self.time_constraint-1, -1, -1):
            if self.d[self.end_node, i] < self.d[self.end_node, choose_time]:
                choose_time = i
        #B2: tìm đường đi từ end_node về start_node
        result = []
        current_node_id = self.end_node
        current_time = choose_time
        while current_node_id != self.start_node:
            result.append(current_node_id)
            prev_node_id = self.prev[current_node_id, current_time].node_id
            prev_time = self.prev[current_node_id, current_time].time
            current_node_id = prev_node_id
            current_time = prev_time
        result.append(self.start_node)
        result.reverse()
        return result