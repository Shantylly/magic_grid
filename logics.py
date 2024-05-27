import random
from numpy.linalg import norm  # Import norm function
from objects import RedDot, Missile, Slash
import settings  # Import settings module to access and modify the score globally

MAX_RED_DOTS = 20  # Maximum number of red dots on the map

def generate_red_dots(sphere_pos, grid_distance, explored_areas, current_red_dots):
    red_dots = list(current_red_dots)  # Copy current red dots
    min_x, min_y, min_z = [sphere_pos[i] - grid_distance for i in range(3)]
    max_x, max_y, max_z = [sphere_pos[i] + grid_distance for i in range(3)]
    
    new_area = set()
    for x in range(int(min_x), int(max_x) + 1, 5):  # Spacing dots every 5 units
        for z in range(int(min_z), int(max_z) + 1, 5):
            if (x, z) not in explored_areas:
                new_area.add((x, -0.5, z))
    
    explored_areas.update(new_area)
    
    while len(red_dots) < MAX_RED_DOTS and new_area:  # Maintain a maximum of MAX_RED_DOTS
        x, y, z = random.choice(list(new_area))
        red_dots.append(RedDot((x, y, z)))
        new_area.remove((x, y, z))
    
    return red_dots

def remove_off_grid_dots(sphere_pos, red_dots, grid_distance):
    """Removes red dots that are off the grid relative to the sphere's current position."""
    return [dot for dot in red_dots if (sphere_pos[0] - grid_distance <= dot.position[0] <= sphere_pos[0] + grid_distance) and
                                        (sphere_pos[2] - grid_distance <= dot.position[2] <= sphere_pos[2] + grid_distance)]

def check_collisions(sphere, red_dots):
    global score
    swallow_radius = sphere.expanded_radius  # Use the expanded radius for swallowing
    new_red_dots = []
    for dot in red_dots:
        if norm([dot.position[0] - sphere.position[0], dot.position[2] - sphere.position[2]]) <= sphere.radius:
            sphere.reduce_life()  # Reduce life if the red dot touches the sphere directly
        elif norm([dot.position[0] - sphere.position[0], dot.position[2] - sphere.position[2]]) <= swallow_radius:
            settings.score += 10  # Increment score by 10 for each swallowed dot
        else:
            new_red_dots.append(dot)
    return new_red_dots  # Return the updated list of red dots

def launch_missile(sphere, target_dot, missiles, size=0.2, length=1.0):
    missile = Missile(start_pos=sphere.position, target_pos=target_dot.position, size=size, length=length)
    missiles.append(missile)

def update_missiles(missiles, red_dots):
    red_dots_to_remove = []
    for missile in missiles:
        missile.update()
        if not missile.active:
            continue
        for dot in red_dots:
            if norm([dot.position[0] - missile.position[0], dot.position[2] - missile.position[2]]) < 0.5:
                red_dots_to_remove.append(dot)
                settings.score += 10
                missile.active = False  # Deactivate the missile after hitting the dot
                break
    # Remove collided red dots from the list
    red_dots = [dot for dot in red_dots if dot not in red_dots_to_remove]
    missiles[:] = [m for m in missiles if m.active]
    return red_dots  # Return the updated list of red dots

def create_slash(sphere, slashes):
    slash = Slash(sphere.position)
    slashes.append(slash)

def update_slashes(slashes, red_dots):
    red_dots_to_remove = []
    for slash in slashes:
        slash.update()
        if not slash.active:
            continue
        for dot in red_dots:
            if norm([dot.position[0] - slash.position[0], dot.position[2] - slash.position[2]]) < slash.radius:
                red_dots_to_remove.append(dot)
                settings.score += 10
                break
    # Remove collided red dots from the list
    red_dots = [dot for dot in red_dots if dot not in red_dots_to_remove]
    slashes[:] = [s for s in slashes if s.active]
    return red_dots  # Return the updated list of red dots

def update_red_dots(sphere, red_dots):
    for dot in red_dots:
        dot.move_towards(sphere.position)
    return red_dots
