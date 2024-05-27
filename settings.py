# settings.py
display = (800, 600)

# Global game state
sphere_pos = [0, 0, 0]
sphere_radius = 3
move_speed = 0.3

camera_pos = [0, 50, 30]
camera_offset = [0, 50, 30]

red_dots = []
explored_areas = set()
MAX_RED_DOTS = 100  # Maximum number of red dots on the map

grid_distance = 80
grid_color = [0.3, 0.7, 0.4]  # Color of the grid lines

score = 0

missiles = []  # Centralized missile list
