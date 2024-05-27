import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
from numpy.linalg import norm  # Import norm function
from settings import display, sphere_pos, camera_pos, camera_offset, score
import settings  # Import settings module to access and modify the score globally
from objects import Sphere, draw_all_dots
from render import draw_grid, setup_scene
from logics import generate_red_dots, remove_off_grid_dots, check_collisions, launch_missile, update_missiles, create_slash, update_slashes, update_red_dots
from text import draw_text, init_text_rendering

# Initialize key state tracking
key_state = {}

def setup_opengl():
    """Initializes OpenGL context and sets up the 3D scene."""
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1.0, 1)  # Sky blue background color
    glMatrixMode(GL_PROJECTION)
    gluPerspective(65, display[0] / display[1], 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    init_text_rendering()  # Initialize text rendering system
    setup_opengl()  # Set up OpenGL configurations
    setup_scene()  # Setup lighting and other scene-specific properties
    
    clock = pygame.time.Clock()
    sphere = Sphere(sphere_pos)
    red_dots = generate_red_dots(sphere_pos, settings.grid_distance, settings.explored_areas, [])  # Initial generation of red dots
    missiles = []
    slashes = []  # List to keep track of active slashes
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_state[event.key] = True
            elif event.type == pygame.KEYUP:
                key_state[event.key] = False
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        red_dots = handle_input(sphere, red_dots, missiles, slashes)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(*camera_pos, *sphere_pos, 0, 1, 0)
        
        draw_grid(sphere_pos, settings.grid_distance, settings.grid_color)
        sphere.draw()
        draw_all_dots(red_dots)
        draw_text(f"Score: {settings.score}", 24, (10, 10))  # Access score from settings module
        draw_text(f"Life: {sphere.life}", 24, (10, 40))  # Display the sphere's remaining life
        
        red_dots = update_red_dots(sphere, red_dots)  # Move red dots towards the sphere
        red_dots = update_missiles(missiles, red_dots)  # Update missile positions and collisions
        red_dots = update_slashes(slashes, red_dots)  # Update slashes and check for collisions
        for missile in missiles:
            missile.draw()  # Draw all active missiles
        for slash in slashes:
            slash.draw()  # Draw all active slashes
        
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

        if sphere.life <= 0:
            running = False  # Stop the game when life reaches 0

    pygame.quit()

def handle_input(sphere, red_dots, missiles, slashes):
    global score
    move_speed = 0.2

    if key_state.get(K_UP):
        sphere.position[2] -= move_speed
    if key_state.get(K_DOWN):
        sphere.position[2] += move_speed
    if key_state.get(K_LEFT):
        sphere.position[0] -= move_speed
    if key_state.get(K_RIGHT):
        sphere.position[0] += move_speed
    if key_state.get(K_a, False):  # Check for 'A' key press
        sphere.show_circle = True
        sphere.circle_time = time.time()
        key_state[K_a] = False  # Reset key state
    if key_state.get(K_z, False):  # Check for 'Z' key press
        if red_dots:  # Ensure there are red dots to target
            nearest_dot = min(red_dots, key=lambda dot: norm([dot.position[0] - sphere.position[0], dot.position[2] - sphere.position[2]]))
            launch_missile(sphere, nearest_dot, missiles, size=0.2, length=1.0)
            key_state[K_z] = False  # Reset key state
    if key_state.get(K_e, False):  # Check for 'E' key press
        create_slash(sphere, slashes)
        key_state[K_e] = False  # Reset key state

    camera_pos[:] = [sphere.position[i] + camera_offset[i] for i in range(3)]
    red_dots = remove_off_grid_dots(sphere.position, red_dots, settings.grid_distance)
    red_dots = check_collisions(sphere, red_dots)
    red_dots = generate_red_dots(sphere.position, settings.grid_distance, settings.explored_areas, red_dots)

    return red_dots

if __name__ == "__main__":
    main()
