import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# OpenGL settings
glOrtho(-40, 40, -30, 30, -1, 1)

# Game variables
snake_position = [(20, 20)]
snake_direction = (1, 0)
food_position = (random.randint(-39, 39), random.randint(-29, 29))
score = 0

def draw_square(position, size=1):
    glBegin(GL_QUADS)
    glVertex2f(position[0] - size, position[1] - size)
    glVertex2f(position[0] + size, position[1] - size)
    glVertex2f(position[0] + size, position[1] + size)
    glVertex2f(position[0] - size, position[1] + size)
    glEnd()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_direction = (-1, 0)
    elif keys[pygame.K_RIGHT]:
        snake_direction = (1, 0)
    elif keys[pygame.K_UP]:
        snake_direction = (0, 1)
    elif keys[pygame.K_DOWN]:
        snake_direction = (0, -1)

    # Update snake position
    new_head = (snake_position[0][0] + snake_direction[0], snake_position[0][1] + snake_direction[1])
    snake_position.insert(0, new_head)
    if new_head == food_position:
        score += 1
        food_position = (random.randint(-39, 39), random.randint(-29, 29))
    else:
        snake_position.pop()

    # Check for collisions
    if new_head in snake_position[1:] or abs(new_head[0]) > 39 or abs(new_head[1]) > 29:
        break

    # Render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1, 0, 0)
    draw_square(food_position)
    glColor3f(0, 1, 0)
    for segment in snake_position:
        draw_square(segment)
    pygame.display.flip()
    pygame.time.wait(100)

print("Game Over! Your score was:", score)
