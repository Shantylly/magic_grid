from OpenGL.GL import *
from OpenGL.GLU import *

def draw_grid(sphere_pos, grid_distance, grid_color):
    """Draws a grid around the sphere to provide a reference on the ground."""
    max_alpha = 0.6  # Maximum transparency value for the grid lines
    grid_distance_extended = grid_distance * 1.2  # Extend the grid a bit beyond the reach

    # Calculate the range for grid lines based on the sphere's current position
    min_x = int(sphere_pos[0] - grid_distance_extended)
    max_x = int(sphere_pos[0] + grid_distance_extended)
    min_z = int(sphere_pos[2] - grid_distance_extended)
    max_z = int(sphere_pos[2] + grid_distance_extended)

    glBegin(GL_LINES)
    # Draw grid lines parallel to X-axis
    for x in range(min_x, max_x + 1):
        if x % 5 == 0:  # Draw a line every 5 units
            alpha = max_alpha * (1 - abs(x - sphere_pos[0]) / grid_distance_extended)
            glColor4f(grid_color[0], grid_color[1], grid_color[2], alpha)
            glVertex3f(x, -0.5, min_z)
            glVertex3f(x, -0.5, max_z)

    # Draw grid lines parallel to Z-axis
    for z in range(min_z, max_z + 1):
        if z % 5 == 0:  # Draw a line every 5 units
            alpha = max_alpha * (1 - abs(z - sphere_pos[2]) / grid_distance_extended)
            glColor4f(grid_color[0], grid_color[1], grid_color[2], alpha)
            glVertex3f(min_x, -0.5, z)
            glVertex3f(max_x, -0.5, z)
    glEnd()

def setup_scene():
    """Sets up initial lighting and other scene settings if needed."""
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    light_position = [10, 10, 10, 1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHT0)
    glClearColor(0.5, 0.7, 1.0, 1)
