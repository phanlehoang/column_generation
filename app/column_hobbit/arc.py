## Pseudo code of the CSP algorithm
class Arc:
    def __init__(self, cost=0, travel_time=0, start_point=0, end_point=0):
        self.cost = cost
        self.travel_time = travel_time
        self.start_point = start_point
        self.end_point = end_point
        pass
    def __str__(self):
        return "Cost: {}, Travel Time: {}".format(self.cost, self.travel_time,)
    def __repr__(self):
        return "({},{})".format(self.cost, self.travel_time,)
    
    # N=7
    # Node =[1,N]
