import gurobipy as gp
from gurobipy import GRB
import numpy as np
import arc

from csp_wizard.node import Node
from idle_time_calculation import idle_time_calculation

from time_constraint_shortest_path_solver_ver2 import TimeConstraintShortestPathSolverVer2

from create_graph_min_n_drivers import create_graph_min_n_drivers
from create_graph_min_n_drivers import create_idle_nodes_from_min_n_driver_nodes

from min_n_drivers_solver import MinNDriverSolver
class IdleTimeSolver(MinNDriverSolver):
    def bonus_init(self):
        self.fix_n_drivers = self.final_n_drivers
        self.pi_fix_n_drivers = 0
        self.idle_times = np.array( [
            idle_time_calculation(pattern= self.patterns[i], tasks= self.tasks)
              for i in range(len(self.patterns))
        ])

    def restricted_master_solver_idle(self):
        # Set objective
        self.restricted_model.setObjective(self.x @ self.idle_times
                                               , GRB.MINIMIZE)
        #remove all constraints
        self.restricted_model.remove(self.restricted_model.getConstrs())
        # Add constraints
        A = self.patterns_columns
        self.restricted_model.addConstr(sum(self.x) <= self.fix_n_drivers,
                                            name=f"constr_fix_n_driver")
        for i in range(self.n):
            self.restricted_model.addConstr(A[i] @ (self.x) == 1,
                                            name=f"constr_{i}")
        # Optimize model
        self.restricted_model.optimize()
        #giá trị đối ngẫu của các ràng buộc
        self.pi=None
        self.pi = np.array([self.restricted_model.getConstrByName(f"constr_{i}").Pi 
                            for i in range(self.n)])
        self.pi_fix_n_drivers = self.restricted_model.getConstrByName(f"constr_fix_n_driver").Pi
    
    def solve_sub_problem_idle(self):
        #create sub problem
        nodes = create_graph_min_n_drivers(self.tasks, self.pi, self.T_idle, self.T_drive)
        create_idle_nodes_from_min_n_driver_nodes(nodes, self.tasks)
        self.nodes = nodes
        csp = TimeConstraintShortestPathSolverVer2(
            nodes = nodes,
            start_node = 0,
            end_node = len(self.tasks)*2+1,
            time_constraint = self.T_drive, 
            )
        csp.solve()
        ans = csp.get_result()
        csp.get_new_pattern_from_path(ans=ans,tasks=self.tasks)
        self.new_pattern = csp.new_pattern
        self.new_pattern_column = csp.new_pattern_column
    def solve_final_master_problem_idle(self):
        p = len(self.patterns)
        self.final_idle_model = gp.Model("final_idle_model")
        #set variables
        self.x_final_idle = self.final_idle_model.addMVar(shape=(p), vtype=GRB.BINARY,
                                              name="x_final_idle")
        # Set objective
        self.final_idle_model.setObjective(self.x_final_idle @
                                            self.idle_times, GRB.MINIMIZE)
        #remove all constraints
        # Add constraints
        #constr fix n driver
        self.final_idle_model.addConstr(sum(self.x_final_idle) <= self.fix_n_drivers)
        A = self.patterns_columns
        for i in range(self.n):
            self.final_idle_model.addConstr(A[i] @ (self.x_final_idle) == 1)

        # Optimize model
        self.final_idle_model.optimize()
    def solve_idle(self):
        #self.fix_n_drivers = self.final_n_drivers
        for i in range(self.max_iterations):
            self.restricted_master_solver_idle()
            self.solve_sub_problem_idle()
            idle_time = idle_time_calculation(self.new_pattern, 
                                              self.tasks)
            if  idle_time - self.pi_fix_n_drivers - self.pi.dot(self.new_pattern_column) > 0.0001:
                break
            self.idle_times = np.append(self.idle_times, idle_time)
            self.patterns.append(self.new_pattern.copy())
            self.patterns_columns = np.c_[self.patterns_columns,
                                           self.new_pattern_column.copy()]
            self.b = np.append(self.b, 1)
            #add thêm vào x một biến mới
            self.x.append(self.restricted_model.addVar( vtype=GRB.CONTINUOUS,
                                             lb = 0,
                                                ub = 1,
            ))

        self.solve_final_master_problem_idle()
        #giá trị của hàm mục tiêu của final_idle_model
        self.ans_idle = self.final_idle_model.objVal
    