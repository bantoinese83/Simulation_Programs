import sys
import pygame
import numpy as np

# Screen dimensions
width, height = 800, 800

# Colors
alive_color = (255, 255, 255)
dead_color = (0, 0, 0)
grid_color = (40, 40, 40)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Cell dimensions
cell_size = 10
num_cells_width = width // cell_size
num_cells_height = height // cell_size
cells = np.random.choice([0, 1], num_cells_width * num_cells_height, p=[0.9, 0.1]).reshape(num_cells_width,
                                                                                           num_cells_height)

# Simulation control
running = True
paused = False


def draw_grid():
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, grid_color, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, grid_color, (0, y), (width, y))


def draw_cells():
    for x in range(num_cells_width):
        for y in range(num_cells_height):
            color = alive_color if cells[x][y] == 1 else dead_color
            pygame.draw.rect(screen, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))


def update_cells():
    global cells
    new_cells = cells.copy()
    for x in range(num_cells_width):
        for y in range(num_cells_height):
            num_alive_neighbors = int((cells[max(x - 1, 0):min(x + 2, num_cells_width),
                                       max(y - 1, 0):min(y + 2, num_cells_height)].sum() - cells[x][y]))
            if cells[x][y] == 1 and (num_alive_neighbors < 2 or num_alive_neighbors > 3):
                new_cells[x][y] = 0
            elif cells[x][y] == 0 and num_alive_neighbors == 3:
                new_cells[x][y] = 1
    cells = new_cells


def handle_input():
    global cells, paused
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Left mouse button
        pos = pygame.mouse.get_pos()
        x, y = pos[0] // cell_size, pos[1] // cell_size
        cells[x][y] = 1
    elif mouse_pressed[2]:  # Right mouse button
        pos = pygame.mouse.get_pos()
        x, y = pos[0] // cell_size, pos[1] // cell_size
        cells[x][y] = 0


def main():
    global running, paused
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_s and paused:
                    update_cells()

        screen.fill(dead_color)
        handle_input()
        if not paused:
            update_cells()
        draw_cells()
        draw_grid()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
