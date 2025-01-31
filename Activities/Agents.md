# Agent description
In this model, an agent represents a robot located in a grid where there are several rewards in different positions. Additionally the robot starts with an energy level that reduces by one in each movement. However, the energy can also increment or decrease if the robot reaches a reward (which can have a negative value).
Each agent is able to move either up, down, left or right from its current position (as long as it doesn't leave grid area).
For this simulation, the efficiency is measured according to the amount of rewards picked before the robot's energy is finished.

## Random
This type of agent will choose a random direction (up, down, left or right) and if possible move accordingly:

```python
move = self.moves[np.random.randint(0,4)]
self.environment.move_by(self.agent, move)
```

## Largest
This agent will set its next target to the largest available reward (according to a priority queue) and move in that direction until it is reached. This requires to setup the priority queue, which will keep the largest value on top.

``` python
elif self.type is AgentType.LARGEST:
    self.pq = PriorityQueue()
    
    for i in range(len(self.grid)): 
        for j in range(len(self.grid[i])):  
            value = self.grid[i][j]
            
            if value != 0:  
                self.pq.put((-1*value, (i, j))) 
                # The negative value is used as the pq sorts increasingly
```

## Closest
In this case, the agent will set the target to the closest available reward from its current position regardless of the reward value. For this, it is necessary to keep a reward list:

```python
elif self.type is AgentType.CLOSEST:
    self.rewards_list = []

    for i in range(len(self.grid)): 
        for j in range(len(self.grid[i])):  
            value = self.grid[i][j]
            
            if value != 0:  
                self.rewards_list.append((value, (i,j)))
```

For choosing the closest reward the Manhattan distance is calculated as follows:

```python
for reward in self.rewards_list:
    value, position = reward

    distance = abs(position[0] - float(self.current_position[0])) + abs(position[1] - float(self.current_position[1]))

    if distance < closest_reward[0]:
        closest_reward = (distance, position)
        r = reward
```

## Testing
All agents were evaluated using different cases from the `assets` folder, counting the total amount of rewards that were picked. This resulted in the `LARGEST` type of agent being the most efficient and the `RANDOM` being the least efficient.