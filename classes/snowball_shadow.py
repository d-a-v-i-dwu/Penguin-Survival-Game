import pygame
import os
import sys
import numpy as np

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    return os.path.join(base_path, relative_path)

class Snowball_Shadow(pygame.sprite.Sprite):
    def __init__(self, snowballs, start_pos, end_pos, throw_angle, flip):
        super().__init__(snowballs)

        self.start_pos = start_pos
        self.end_pos = end_pos
        self.throw_angle = np.radians(throw_angle)
        self.flip = flip

        image_path = resource_path(os.path.join("resources", "images", "snowball_shadow.png"))

        self.original_snowball = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (9, 9))

        if self.flip:
            self.original_snowball = pygame.transform.rotozoom(self.original_snowball, np.degrees(self.throw_angle), 1)
        else:
            self.original_snowball = pygame.transform.rotozoom(self.original_snowball, -np.degrees(self.throw_angle), 1)      

        self.image = self.original_snowball
        self.rect = self.image.get_rect(center = start_pos)

        self.current_time = 0
        self.time_increment = 0

        self.time_increment_calculator()
            
    def time_increment_calculator(self):
        movement_vector = np.array([0,0])
        movement_vector[0] = self.end_pos[0] - self.rect.center[0]
        movement_vector[1] = self.end_pos[1] - self.rect.center[1]
        magnitude = np.linalg.norm(movement_vector)

        self.time_increment = 1 / (0.2 * magnitude)

    def horizontal_movement(self):
        x = (1 - self.current_time) * self.start_pos[0] + self.current_time * self.end_pos[0]
        y = (1 - self.current_time) * self.start_pos[1] + self.current_time * self.end_pos[1]
        self.current_time += self.time_increment
        self.rect.center = (x, y)


    def update(self):
        if self.current_time <= 1:
            self.horizontal_movement()
        else:
            self.kill()