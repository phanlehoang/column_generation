
#duty arc
from csp_wizard.node import Node
import arc
def create_odd_node(tasks, position, pi):
    # Tạo node
    id = tasks[position].id
    current_task = tasks[position]
    node = Node(id = id*2-1,
                arcs =[arc.Arc(cost = -pi[position],
                               travel_time = current_task.time_end -current_task.time_start,

                                start_point = id*2-1,
                                  end_point = id*2)])
    return node
#connecting arc
def create_even_node(tasks, position, pi, T_idle, T_drive):
    # Tạo node
    id = tasks[position].id
    current_task = tasks[position]
    #tạo arcs 
    arcs = []
    for next_position in range(position+1,len(tasks)):
        next_id = tasks[next_position].id
        next_task = tasks[next_position]
        if (next_task.time_start >= current_task.time_end
          and next_task.time_start <= current_task.time_end + T_idle):
            arcs.append(arc.Arc(cost = -pi[next_position],
                               travel_time = 0,
                                start_point = id*2,
                                  end_point = next_id*2-1))
    arcs.append(arc.Arc(cost = 0,
                                travel_time = 0,
                                start_point = id*2,
                                  end_point = len(tasks)*2+1,
                                  ))
    node = Node(id = id*2,
                arcs = arcs)
    
    return node
def create_starting_node(tasks, pi, T_idle, T_drive):
    arcs = []
    for position in range(len(tasks)):
        next_task = tasks[position]
        arcs.append(arc.Arc(cost = -pi[position],
                               travel_time = 0,
                                start_point = 0,
                                  end_point = next_task.id*2-1))
    return Node(id = 0, arcs = arcs)
    return arcs
    
def create_graph_min_n_drivers(tasks, pi, T_idle, T_drive):
    nodes = []
    #tạo node đầu tiên
    nodes.append(create_starting_node(tasks, pi, T_idle, T_drive))
    #tạo các node lẻ
    for position in range(len(tasks)):
        nodes.append(create_odd_node(tasks, position, pi))
        nodes.append(create_even_node(tasks, position, pi, T_idle, T_drive))
    #tạo node cuối cùng
    nodes.append(Node(id = len(tasks)*2+1, arcs = []))
    return nodes

def create_idle_nodes_from_min_n_driver_nodes(nodes, tasks):
    for node in nodes:
        #phải là connect arc
        if node.id % 2 == 0 and node.id != 0 and node.id != len(tasks)*2+1:
            for arc in node.arcs:
                position_source = arc.start_point//2-1
                if(arc.end_point == len(tasks)*2+1):
                    continue
                position_destination = arc.end_point//2
                arc.cost += (tasks[position_destination].time_start - 
                             tasks[position_source].time_end)







