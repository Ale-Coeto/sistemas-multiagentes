import socket
import numpy as np
import agentpy as ap
import matplotlib.pyplot as plt
import time
from queue import PriorityQueue

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1101))
from_server = s.recv(4096)
print ("Received from server: ",from_server.decode("ascii"))

SLEEP = 0.2

city = np.load('streets-1.npy')

class CityAgent(ap.Agent):
    
    '''
    Start agent with 4 actions
    '''
    def setup(self):
        self.actions = {'up': (-1,0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        self.env = self.model.env
        self.steps = 0
        self.i = 0

    '''
    Move agent to next step
    '''
    def execute(self):
        if self.i < len(self.path):
            step = self.path[self.i]
            message = f"{step[0]+0.5},1,{step[1]+0.5}"
            print("\n",message)
            s.send(message.encode('utf-8'))
            self.env.move_to(self, self.path[self.i])
            self.steps += city[self.path[self.i]]
            self.i += 1
        time.sleep(SLEEP)

    '''
    Get manhattan distance for heuristic
    '''
    def get_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    '''
    Use A* to find optimal solution
    '''
    def solve(self):
        n,m = city.shape

        pq = PriorityQueue()
        pq.put((0,self.p.init))

        scores = {self.p.init: 0}
        curr_path = {}

        while not pq.empty():
            _, current_pos = pq.get()
            
            if current_pos == self.p.goal:
                # print("Solved")
                self.path = []
                while current_pos in curr_path:
                    self.path.append(current_pos)
                    current_pos = curr_path[current_pos]
                self.path = self.path[::-1]
                # print("Path: ", self.path)
                return
            
            x,y = current_pos
            for _, (dx,dy) in self.actions.items():
                nx,ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and city[nx][ny] != -1 and city[nx][ny] != -10:
                    tentative_g_score = scores[current_pos] + city[nx][ny]

                    if (nx, ny) not in scores or tentative_g_score < scores[(nx, ny)]:
                        scores[(nx, ny)] = tentative_g_score
                        f_score = tentative_g_score + self.get_distance((nx, ny), self.p.goal)
                        pq.put((f_score, (nx, ny)))  
                        curr_path[(nx, ny)] = current_pos

    '''
    Get position of the agent
    '''
    def get_position(self):
        return self.env.positions[self]

class City(ap.Grid):
    '''
    Start city
    '''
    def setup(self):
        self.city = self.p.city

class CityModel(ap.Model):
    
    '''
    Start model
    '''
    def setup(self):
        city[self.p.goal] = 1
        self.env = City(self, shape=city.shape)
        self.agent = CityAgent(self)
        self.env.add_agents([self.agent], positions=[self.p.init])
        self.agent.solve()

    '''
    On each step, agent moves
    '''
    def step(self):
        self.agent.execute()

    '''
    Stop simulation if goal is reached
    '''
    def update(self):
        if self.agent.get_position() == self.model.p.goal:
            self.stop()

'''
Animation
'''
def animation_plot(model, ax):
    n, m = model.p.city.shape
    grid = np.copy(city)
    grid[model.p.goal] = 200

    color_dict = {1: '#ffffff', 2: '#7c4700', 4: '#2a9dfb', 5: '#6e5c56', -1: '#000000', -10: '#4f4f4f', 100: '#0000ff', 200: '#00ff00'}
    ap.gridplot(grid, ax=ax, color_dict=color_dict, convert=True)
    agent = list(model.env.agents)[0]
    grid[model.env.positions[agent]] = 100
    ap.gridplot(grid, ax=ax, color_dict=color_dict, convert=True)
    ax.set_title("City Agent\nTime: {}".format(agent.steps))


parameters = {
    'city': city,
    'init': (5, 3),
    'goal': (16,26),
    'steps': 100
}
print(city.shape
      )
model = CityModel(parameters)
model.run()