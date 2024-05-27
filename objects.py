import math
from OpenGL.GL import *
from OpenGL.GLU import *
from settings import sphere_pos
import time
import random

class Sphere:
    def __init__(self, position, color=(0.0, 0.0, 1.0), radius=1.0, life=3):
        self.position = position
        self.color = color
        self.radius = radius
        self.life = life  # Add life attribute
        self.show_circle = False
        self.circle_color = (0.67, 0.85, 1.0)  # Light blue
        self.circle_time = 0
        self.expanded_radius = radius  # Current effective radius
        self.default_radius = radius  # Store the default radius
        self.expansion_duration = 5  # Duration for which the radius is expanded

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glColor3fv(self.color)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.radius, 32, 32)
        gluDeleteQuadric(quadric)  # Delete the quadric object to avoid memory leaks
        glPopMatrix()

        if self.show_circle and (time.time() - self.circle_time) < self.expansion_duration:
            self.draw_circle()
            self.expanded_radius = self.default_radius * 5  # Double the radius during expansion
        else:
            self.expanded_radius = self.default_radius  # Reset to default radius

    def draw_circle(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(*self.circle_color, 0.5)  # Semi-transparent
        glBegin(GL_LINE_LOOP)
        for i in range(360):
            angle = math.radians(i)
            x = self.radius * 4 * math.cos(angle) + self.position[0]
            y = self.radius * 4 * math.sin(angle) + self.position[1]
            glVertex3f(x, y, self.position[2])
        glEnd()
        glDisable(GL_BLEND)

    def reduce_life(self):
        self.life -= 1
        print(f"Sphere hit! Life remaining: {self.life}")
        if self.life <= 0:
            print("Game Over!")  # Handle game over logic as needed

class RedDot:
    def __init__(self, position, color=(1.0, 0, 0), size=8, speed=0.08):
        self.position = position
        self.color = color
        self.size = size
        self.speed = speed  # Speed of the red dot
    
    def draw(self):
        glDisable(GL_LIGHTING)  # Disable lighting for drawing dots
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glColor3fv(self.color)
        glVertex3f(*self.position)
        glEnd()
        glEnable(GL_LIGHTING)  # Re-enable lighting if needed elsewhere

    def move_towards(self, target_pos):
        direction = [target_pos[i] - self.position[i] for i in range(3)]
        distance = math.sqrt(sum(d ** 2 for d in direction))
        if distance > 0:
            direction = [d / distance for d in direction]
            self.position = [self.position[i] + self.speed * direction[i] for i in range(3)]

class Missile:
    def __init__(self, start_pos, target_pos, size=0.2, length=1.0):
        self.position = list(start_pos)
        self.target = target_pos
        self.size = size
        self.length = length
        self.speed = 0.2
        self.active = True

    def update(self):
        if not self.active:
            return
        direction = [self.target[i] - self.position[i] for i in range(3)]
        distance = math.sqrt(sum(d ** 2 for d in direction))
        if distance < self.speed:
            self.position = list(self.target)
            self.active = False
        else:
            direction = [d / distance for d in direction]
            self.position = [self.position[i] + self.speed * direction[i] for i in range(3)]

    def draw(self):
        if not self.active:
            return
        
        # Calculate the direction vector
        direction = [self.target[i] - self.position[i] for i in range(3)]
        distance = math.sqrt(sum(d ** 2 for d in direction))
        if distance == 0:
            return
        direction = [d / distance for d in direction]

        # Calculate the rotation axis and angle
        up_vector = [0, 0, 1]  # Assuming the missile points up by default
        axis = [up_vector[1] * direction[2] - up_vector[2] * direction[1],
                up_vector[2] * direction[0] - up_vector[0] * direction[2],
                up_vector[0] * direction[1] - up_vector[1] * direction[0]]
        angle = math.degrees(math.acos(sum(up_vector[i] * direction[i] for i in range(3))))
        
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(angle, *axis)
        glColor3f(1.0, 1.0, 0.0)  # Yellow missile
        quadric = gluNewQuadric()
        gluCylinder(quadric, self.size, self.size, self.length, 16, 16)
        gluDeleteQuadric(quadric)  # Delete the quadric object to avoid memory leaks
        glPopMatrix()

class Slash:
    def __init__(self, sphere_pos, radius=5.0, duration=3.0, speed=0.3):
        self.start_time = time.time()
        self.position = list(sphere_pos)
        self.radius = radius
        self.duration = duration
        self.speed = speed
        self.active = True
        self.angle = random.uniform(0, 360)  # Random direction
        self.direction = [math.cos(math.radians(self.angle)), 0, math.sin(math.radians(self.angle))]  # Direction vector

    def update(self):
        if time.time() - self.start_time > self.duration:
            self.active = False
        else:
            # Move the slash forward
            self.position[0] += self.speed * self.direction[0]
            self.position[2] += self.speed * self.direction[2]

    def draw(self):
        if not self.active:
            return

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.angle, 0, 1, 0)  # Rotate to face the direction
        glColor4f(0.0, 0.0, 1.0, 0.5)  # Semi-transparent blue
        glBegin(GL_POLYGON)
        for i in range(181):  # Draw a semi-circle
            angle = math.radians(i - 90)  # Offset to make the semi-circle face the correct direction
            x = self.radius * math.cos(angle)
            z = self.radius * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()
        glPopMatrix()


def draw_all_dots(red_dots):
    """Utility function to draw all red dots in the provided list."""
    for dot in red_dots:
        dot.draw()

# Optional: To initialize game objects directly within this module for convenience
def initialize_game_objects():
    global sphere, red_dots_instances
    sphere = Sphere(sphere_pos)
    red_dots_instances = [RedDot((x, -0.5, z)) for x in range(-20, 21, 4) for z in range(-20, 21, 4)]

    return sphere, red_dots_instances
