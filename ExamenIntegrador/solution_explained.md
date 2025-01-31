# Finding a good route

## Proposal
To solve this problem, the A* algorithm was selected because the grid is static and already has predefined values for time as well as starting and finishing coordinates. Additionally, this allows to find the optimal route using a heuristic which in this case was the manhattan distance. This way, searching for the shortest route can be faster as the distance to the goal can be calculated and the agent can choose the one with the best estimated cost (distance + time value of the next cell).

## Agent
This was a utility based agent, that made decisions according to the best possible utility/estimated cost according to the goal. 

## Environment
The environment was a grid with predefined values. It was accessible as the agent could know all values in the grid, static as it didn't change with agent actions and discrete because it has finite states.

## Results
Using this implementation, the time taken by the agent to reach its goal was 86 units.