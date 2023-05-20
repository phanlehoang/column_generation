
from bus_wizard.task import Task
def idle_time_calculation(pattern, tasks):
    #tính thời gian rảnh
    idle_time = 0
    for i in range(1, len(pattern)):
            position = pattern[i]
            previous_position = pattern[i-1]
            # print(tasks[position].time_start )
            # print(       tasks[previous_position].time_end)
            idle_time += tasks[position].time_start - tasks[previous_position].time_end
    return idle_time