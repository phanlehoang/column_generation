import gurobipy as gp
from gurobipy import GRB
import numpy as np
import arc

from csp_wizard.node import Node
from initial_patterns import InitialPatternsGenerator

from time_constraint_shortest_path_solver import TimeConstraintShortestPathSolver
from time_constraint_shortest_path_solver_ver2 import TimeConstraintShortestPathSolverVer2

from create_graph_min_n_drivers import create_graph_min_n_drivers

class MinNDriverSolver:
    def __init__(self, T_idle, T_all,T_drive ,tasks, max_iterations=100):
        self.T_idle = T_idle
        self.T_all = T_all
        self.tasks = tasks
        self.n = len(tasks)
        self.T_drive = T_drive
        # initial_pattern_generator = InitialPatternsGenerator(tasks, T_idle, T_drive)
        # initial_pattern_generator.solve()
        # initial_pattern_generator.pattern_column_generator()
        # self.patterns_columns = initial_pattern_generator.patterns_columns
        # self.patterns = initial_pattern_generator.patterns
        self.patterns = [[i] for i in range(self.n)]
        self.patterns_columns = np.eye(self.n)
       
        self.restricted_model = gp.Model("restricted_master_solver")
        self.final_model = gp.Model("final_master_solver")
        # Create variables
        self.x =  [self.restricted_model.addVar( vtype=GRB.CONTINUOUS,
                                           lb = 0,
                                           ub = 1,
                                           
                                            name=f"x_{i} ") 
                   for i in range(len(self.patterns))]
        
        
        self.x_final = None 
        self.b = np.ones(self.n)
        self.pi = None
        self.new_pattern = None
        self.new_pattern_column = None
        self.max_iterations = max_iterations
    
    def restricted_master_solver(self):
        # Set objective
        self.restricted_model.setObjective(sum(self.x), GRB.MINIMIZE)
        #remove all constraints
        self.restricted_model.remove(self.restricted_model.getConstrs())
        # Add constraints
        A = self.patterns_columns
        for i in range(self.n):
            self.restricted_model.addConstr(A[i] @ (self.x) == 1,
                                            name=f"constr_{i}")
        # Optimize model
        self.restricted_model.optimize()
        #giá trị đối ngẫu của các ràng buộc
        self.pi=None
        self.pi = np.array([self.restricted_model.getConstrByName(f"constr_{i}").Pi 
                            for i in range(self.n)])
        
    
    def solve_sub_problem(self):
        #create sub problem
        nodes = create_graph_min_n_drivers(self.tasks, self.pi, self.T_idle, self.T_drive)
        csp = TimeConstraintShortestPathSolverVer2(
            nodes = nodes,
            start_node = 0,
            end_node = len(self.tasks)*2+1,
            time_constraint = self.T_drive, 
            )
        self.nodes = nodes
        csp.solve()
        ans = csp.get_result()
        csp.get_new_pattern_from_path(ans=ans,tasks=self.tasks)
        self.new_pattern = csp.new_pattern
        self.new_pattern_column = csp.new_pattern_column
    def solve_final_master_problem(self):
        p = len(self.patterns)
        #set variables
        self.x_final = self.final_model.addMVar(shape=(p), vtype=GRB.BINARY,
                                              name="x_final")
        # Set objective
        self.final_model.setObjective(self.x_final.sum(), GRB.MINIMIZE)
        #remove all constraints
        # Add constraints
        A = self.patterns_columns
        for i in range(self.n):
            self.final_model.addConstr(A[i] @ (self.x_final) == 1)

        # Optimize model
        self.final_model.optimize()
        self.ans = self.final_model.getAttr(GRB.Attr.X)

    def solve(self):
        for i in range(self.max_iterations):
            self.restricted_master_solver()
            self.solve_sub_problem()
            if 1 - self.pi.dot(self.new_pattern_column) > 0.0001:
                break
            self.patterns.append(self.new_pattern.copy())
            self.patterns_columns = np.c_[self.patterns_columns, self.new_pattern_column.copy()]
            self.b = np.append(self.b, 1)
            #add thêm vào x một biến mới
            self.x.append(self.restricted_model.addVar( vtype=GRB.CONTINUOUS,
                                             lb = 0,
                                            ub = 1,
            ))

        self.solve_final_master_problem()
        self.final_n_drivers = int(sum(self.x_final.X))





        
        