from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from random import randint

# Game settings
window_width = 800
window_height = 600
snake_size = 20
snake_speed = 10
score = 0
boundary_offset = 80

#snake respawn
snake = [[window_width // 2, window_height // 2]]

#food random respawn 
max_x = (window_width - 2 * boundary_offset - snake_size) // snake_size
max_y = (window_height - 2 * boundary_offset - snake_size) // snake_size
food = [randint(0, max_x) * snake_size + boundary_offset, 
        randint(0, max_y) * snake_size + boundary_offset]
direction = [snake_speed, 0]

# obstacle position and size
obstacles = [
    # Small obstacles
    {'pos': (150, 150), 'size': (50, 100)},
    {'pos': (600, 400), 'size': (50, 100)},

    # Larger obstacles
    {'pos': (200, 300), 'size': (150, 50)},
    {'pos': (450, 150), 'size': (150, 50)}
]

def draw_line(x0, y0, x1, y1):
    """ Draw a line using the Midpoint Line Algorithm """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    glBegin(GL_POINTS)
    while True:
        glVertex2f(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    glEnd()

def draw_circle(cx, cy, r):
    """ Draw a circle using the Midpoint Circle Algorithm """
    x = 0
    y = r
    d = 1 - r
    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(cx + x, cy + y)
        glVertex2f(cx + y, cy + x)
        glVertex2f(cx - y, cy + x)
        glVertex2f(cx - x, cy + y)
        glVertex2f(cx - x, cy - y)
        glVertex2f(cx - y, cy - x)
        glVertex2f(cx + y, cy - x)
        glVertex2f(cx + x, cy - y)
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()

def draw_rect(x, y, width, height):
    """ Draw a filled rectangle using horizontal lines """
    for i in range(y, y + height):
        draw_line(x, i, x + width, i)

def draw_obstacles():
    """ Draw obstacles within the game window """
    glColor3f(0.6, 0.3, 1.0)  # Orange color for obstacles
    for obstacle in obstacles:
        draw_rect(*obstacle['pos'], *obstacle['size'])

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw boundary lines with an offset inside the window
    glColor3f(1.0, 1.0, 1.0)
    draw_line(boundary_offset, boundary_offset, window_width - boundary_offset, boundary_offset)
    draw_line(boundary_offset, window_height - boundary_offset, window_width - boundary_offset, window_height - boundary_offset)
    draw_line(boundary_offset, boundary_offset, boundary_offset, window_height - boundary_offset)
    draw_line(window_width - boundary_offset, boundary_offset, window_width - boundary_offset, window_height - boundary_offset)

    # Draw snake
    glColor3f(0.0, 1.0, 0.0)
    for segment in snake:
        draw_rect(segment[0], segment[1], snake_size, snake_size)

    # Draw food
    glColor3f(1.0, 0.0, 0.0)
    draw_circle(food[0] + snake_size // 2, food[1] + snake_size // 2, snake_size // 2)

    # Draw obstacles
    draw_obstacles()

    # Display score
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10, window_height - 30)
    for char in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    glutSwapBuffers()

def respawn_food():
    global food
    max_x = (window_width - 2 * boundary_offset - snake_size) // snake_size
    max_y = (window_height - 2 * boundary_offset - snake_size) // snake_size
    food = [randint(0, max_x) * snake_size + boundary_offset, 
            randint(0, max_y) * snake_size + boundary_offset]

def update(value):
    global snake, food, direction, score

    # Move the snake with Wrap-around logic
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
    if new_head[0] >= window_width - boundary_offset:
        new_head[0] = boundary_offset
    elif new_head[0] < boundary_offset:
        new_head[0] = window_width - boundary_offset - snake_size

    if new_head[1] >= window_height - boundary_offset:
        new_head[1] = boundary_offset
    elif new_head[1] < boundary_offset:
        new_head[1] = window_height - boundary_offset - snake_size

    snake.insert(0, new_head)
    snake.pop()

    # Check for collision with food
    if snake[0][0] == food[0] and snake[0][1] == food[1]:
        score += 1
        respawn_food()  
        snake.append(snake[-1]) 

    glutPostRedisplay()
    glutTimerFunc(100, update, 0)


def keyboard(key, x, y):
    global direction
    if key == GLUT_KEY_LEFT and direction[0] != snake_speed:
        direction = [-snake_speed, 0]
    elif  key == GLUT_KEY_RIGHT and direction[0] != -snake_speed:
        direction = [snake_speed, 0]
    elif key == GLUT_KEY_DOWN and direction[1] != snake_speed:
        direction = [0, -snake_speed]
    elif key == GLUT_KEY_UP and direction[1] != -snake_speed:
        direction = [0, snake_speed]

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Snake Game")
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(keyboard)
glutTimerFunc(100, update, 0)
glClearColor(0.0, 0.0, 0.0, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, window_width, 0, window_height)
glMatrixMode(GL_MODELVIEW)
glutMainLoop()