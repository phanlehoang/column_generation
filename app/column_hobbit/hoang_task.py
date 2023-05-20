from bus_wizard.task import Task
#import random import randint
import random
import numpy as np
def hoang_task(time_first, time_last, step_time=15, task_duration=120) :
    step_time_function = lambda x: 7 if x < 18*60 else 15
    current_time_first = time_first
    current_time_last = time_first + task_duration
    tasks = []
    counter =1
    while(current_time_last <= time_last):
        tasks.append(Task(counter,current_time_first, current_time_last))
        current_time_first += step_time_function(current_time_first)
        current_time_last += step_time_function(current_time_last)
       
        counter +=1
    return tasks

#từ 4h chiều đến 6h chiều
#16*60 -> 18*60
#1 số ngẫu nhiên từ 1->15
#từ 6h chiều đến 9h tối
#18*60 -> 21*60
#1 số ngẫu nhiên từ 1->15