# text_manager.py
import pygame
from OpenGL.GL import *
from settings import display

def init_text_rendering():
    """Initializes font rendering settings."""
    pygame.font.init()  # Ensure the Pygame font module is initialized

def draw_text(text, size, position):
    """Renders text at a specified position on the screen.
    
    Args:
        text (str): The text to be rendered.
        size (int): Font size of the text.
        position (tuple): A tuple (x, y) specifying the position on the screen.
    """
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))  # Render white text
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    # Textures are handled here
    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    # Set orthographic projection for 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable depth test to ensure text is not removed by the depth buffer
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor3f(1.0, 1.0, 1.0)  # Set text color to white
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(position[0], position[1])
    glTexCoord2f(1, 1)
    glVertex2f(position[0] + width, position[1])
    glTexCoord2f(1, 0)
    glVertex2f(position[0] + width, position[1] + height)
    glTexCoord2f(0, 0)
    glVertex2f(position[0], position[1] + height)
    glEnd()

    # Clean up
    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
    glDeleteTextures(1, [texture_id])
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

