import pygame
import sys
import random
from pygame.math import Vector2
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Advanced Bouncing Ball Simulation")

# Colors
background_color = (255, 255, 255)

# Physics properties
gravity = 0.5
elasticity = 0.95
friction = 0.01

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

    def update(self):
        self.position += self.velocity
        self.velocity.y += gravity
        self.velocity *= (1 - friction)
        self.handle_wall_collisions()

    def handle_wall_collisions(self):
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x = -self.velocity.x * elasticity
        elif self.position.x + self.radius > width:
            self.position.x = width - self.radius
            self.velocity.x = -self.velocity.x * elasticity

        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y = -self.velocity.y * elasticity
        elif self.position.y + self.radius > height:
            self.position.y = height - self.radius
            if abs(self.velocity.y) < 0.1:
                self.velocity.y = 0
            else:
                self.velocity.y = -self.velocity.y * elasticity

    def draw(self, _screen):
        pygame.draw.circle(_screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        hit_count_text = font.render(str(self.hit_count), True, (0, 0, 0))
        _screen.blit(hit_count_text, (
        self.position.x - hit_count_text.get_width() // 2, self.position.y - hit_count_text.get_height() // 2))


def create_balls(number_of_balls):
    return [
        Ball(random.randint(50, width - 50), random.randint(50, height - 50), random.randint(5, 15),
             # Marbles are smaller
             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.uniform(-5, 5),
             random.uniform(-5, 5), random.randint(5, 15))  # Random hit threshold between 5 and 15
        for _ in range(number_of_balls)
    ]


def handle_collisions(_balls):
    for i in reversed(range(len(_balls))):
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
                speed1 = math.hypot(ball1.velocity.x, ball1.velocity.y)
                speed2 = math.hypot(ball2.velocity.x, ball2.velocity.y)
                direction1 = math.atan2(ball1.velocity.y, ball1.velocity.x)
                direction2 = math.atan2(ball2.velocity.y, ball2.velocity.x)
                new_speed1 = speed2 * math.cos(direction2 - angle)
                new_speed2 = speed1 * math.cos(direction1 - angle)
                ball1.velocity.x = new_speed1 * math.cos(angle) + speed1 * math.sin(direction1 - angle) * math.cos(
                    angle + math.pi / 2)
                ball1.velocity.y = new_speed1 * math.sin(angle) + speed1 * math.sin(direction1 - angle) * math.sin(
                    angle + math.pi / 2)
                ball2.velocity.x = new_speed2 * math.cos(angle) + speed2 * math.sin(direction2 - angle) * math.cos(
                    angle + math.pi / 2)
                ball2.velocity.y = new_speed2 * math.sin(angle) + speed2 * math.sin(direction2 - angle) * math.sin(
                    angle + math.pi / 2)
        if ball1.hit_count >= ball1.hit_threshold:
            del _balls[i]  # Remove ball
            _balls.append(create_balls(1)[0])  #


def main():
    balls = create_balls(10)
    clock = pygame.time.Clock()  #
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background_color)
        for ball in balls:
            ball.update()
        handle_collisions(balls)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
