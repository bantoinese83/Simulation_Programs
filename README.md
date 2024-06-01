# Simulation Programs

This project is a collection of various simulation programs. Each program simulates a different scenario using different physics properties and rendering techniques.

## Advanced Bouncing Ball Simulation

One of the simulations in this project is an advanced bouncing ball simulation. It uses Pygame for rendering and includes physics properties such as gravity, elasticity, and friction.

### Features

- Ball objects with properties such as position, velocity, radius, color, and hit count.
- Physics properties including gravity, elasticity, and friction.
- Collision detection and response between balls.
- Wall collision detection and response for each ball.
- Ball hit count tracking and display.
- Ball hit count threshold for ball removal.
- Ball removal and respawn after reaching the hit count threshold.
- Ball rendering with Pygame.
- Ball movement and physics simulation.
- Ball collision detection and response.

### How to Run

To run the bouncing ball simulation, execute the `bouncing_ball_sim.py` script with a Python interpreter that has Pygame installed.

```bash
python bouncing_ball_sim.py
```


## Conway's Game of Life

Another simulation in this project is Conway's Game of Life. It's a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input.

### Features

- Grid of cells, each of which is either alive or dead.
- Each cell's future state is determined by its current state and the number of its neighbors that are alive.
- If a cell is alive and has 2 or 3 neighbors, it stays alive, otherwise it dies.
- If a cell is dead and has exactly 3 neighbors, it becomes alive.

### How to Run

To run the Game of Life simulation, execute the `game_of_life.py` script with a Python interpreter that has Pygame installed.

```bash
python game_of_life_sim.py
```