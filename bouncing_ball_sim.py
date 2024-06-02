import pygame
import sys
import random
from pygame.math import Vector2
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Bouncing Ball Simulation with Mouse Interaction")

# Colors
background_color = (255, 255, 255)
wall_thickness = 10

# Physics properties
gravity = 0.5
elasticity = 0.95
friction = 0.99

# Track positions of mouse to get movement vector
mouse_trajectory = []

# Font for displaying hit count
font = pygame.font.Font(None, 36)


class Ball:
    def __init__(self, x, y, radius, color, vx, vy, hit_threshold):
        self.position = Vector2(x, y)
        self.velocity = Vector2(vx, vy)
        self.radius = radius
        self.color = color
        self.hit_count = 0
        self.hit_threshold = hit_threshold
        self.selected = False

    def update(self):
        if not self.selected:
            self.position += self.velocity
            self.velocity.y += gravity
            self.velocity.x *= friction
            self.velocity.y *= friction
            self.handle_wall_collisions()
        else:
            self.velocity = Vector2(x_push, y_push)

    def handle_wall_collisions(self):
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x = -self.velocity.x * elasticity
        elif self.position.x + self.radius > WIDTH:
            self.position.x = WIDTH - self.radius
            self.velocity.x = -self.velocity.x * elasticity

        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y = -self.velocity.y * elasticity
        elif self.position.y + self.radius > HEIGHT:
            self.position.y = HEIGHT - self.radius
            if abs(self.velocity.y) < 0.1:
                self.velocity.y = 0
            else:
                self.velocity.y = -self.velocity.y * elasticity

    def draw(self, _screen):
        pygame.draw.circle(_screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        hit_count_text = font.render(str(self.hit_count), True, (0, 0, 0))
        _screen.blit(hit_count_text, (
        self.position.x - hit_count_text.get_width() // 2, self.position.y - hit_count_text.get_height() // 2))

    def check_select(self, pos):
        if pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2,
                       self.radius * 2).collidepoint(pos):
            self.selected = True
        return self.selected


def draw_walls():
    pygame.draw.line(screen, 'white', (0, 0), (0, HEIGHT), wall_thickness)
    pygame.draw.line(screen, 'white', (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
    pygame.draw.line(screen, 'white', (0, 0), (WIDTH, 0), wall_thickness)
    pygame.draw.line(screen, 'white', (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness)


def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed


def create_balls(number_of_balls):
    return [
        Ball(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), random.randint(30, 60),
             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.uniform(-5, 5),
             random.uniform(-5, 5), random.randint(5, 15))
        for _ in range(number_of_balls)
    ]


def handle_collisions(_balls):
    balls_to_remove = []
    balls_to_add = []

    for i in range(len(_balls)):
        ball1 = _balls[i]
        for j in range(i + 1, len(_balls)):
            ball2 = _balls[j]
            dx = ball1.position.x - ball2.position.x
            dy = ball1.position.y - ball2.position.y
            distance = math.hypot(dx, dy)
            if distance < ball1.radius + ball2.radius:
                ball1.hit_count += 1
                ball2.hit_count += 1
                angle = math.atan2(dy, dx)
                speed1 = ball1.velocity.length()
                speed2 = ball2.velocity.length()
                direction1 = ball1.velocity.angle_to(Vector2(1, 0))
                direction2 = ball2.velocity.angle_to(Vector2(1, 0))
                new_velocity1 = Vector2(speed2 * math.cos(direction2 - angle), speed1 * math.sin(direction1 - angle))
                new_velocity2 = Vector2(speed1 * math.cos(direction1 - angle), speed2 * math.sin(direction2 - angle))
                ball1.velocity = new_velocity1.rotate(angle)
                ball2.velocity = new_velocity2.rotate(angle)

                # Separate overlapping balls
                overlap = 0.5 * (ball1.radius + ball2.radius - distance + 1)
                ball1.position += Vector2(dx, dy).normalize() * overlap
                ball2.position -= Vector2(dx, dy).normalize() * overlap

        if ball1.hit_count >= ball1.hit_threshold:
            balls_to_remove.append(ball1)
            balls_to_add.append(create_balls(1)[0])

    for ball in balls_to_remove:
        _balls.remove(ball)
    _balls.extend(balls_to_add)


def main():
    balls = create_balls(10)
    clock = pygame.time.Clock()

    global x_push, y_push
    x_push, y_push = 0, 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for ball in balls:
                        ball.check_select(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for ball in balls:
                        ball.selected = False

        screen.fill(background_color)
        mouse_coords = pygame.mouse.get_pos()
        mouse_trajectory.append(mouse_coords)
        if len(mouse_trajectory) > 20:
            mouse_trajectory.pop(0)
        x_push, y_push = calc_motion_vector()

        draw_walls()
        for ball in balls:
            ball.update()
        handle_collisions(balls)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
