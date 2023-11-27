import pygame
import os
import numpy as np
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    return os.path.join(base_path, relative_path)

class Snowball(pygame.sprite.Sprite):
    def __init__(self, snowballs, start_pos, end_pos, throw_angle, flip):
        super().__init__(snowballs)

        self.start_pos = start_pos
        self.end_pos = end_pos
        self.throw_angle = np.radians(throw_angle)
        self.flip = flip

        image_path = resource_path(os.path.join("resources", "images", "snowball.png"))
        self.original_snowball = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (9, 9))

        if self.flip:
            self.rotation_speed = -20
        else:
            self.rotation_speed = 20   

        self.image = self.original_snowball
        self.rect = self.image.get_rect(center=start_pos)
        
        self.rotation = 0

        self.current_time = 0
        self.time_increment = 0
        self.mid_pos = np.array([0, 0])

        self.mid_pos_calculator()

    def mid_pos_calculator(self):
        movement_vector = np.array([0, 0])
        movement_vector[0] = self.end_pos[0] - self.rect.center[0]
        movement_vector[1] = self.end_pos[1] - self.rect.center[1]
        magnitude = np.linalg.norm(movement_vector)

        self.time_increment = 1 / (0.2 * magnitude)
        height_vector = np.array([-movement_vector[1], movement_vector[0]]) / 2 * np.sin(self.throw_angle)
        halfway_point = np.array([self.rect.center[0] + movement_vector[0] / 2, self.rect.center[1] + movement_vector[1] / 2])

        if self.flip:
            self.mid_pos = halfway_point - height_vector
        else:
            self.mid_pos = halfway_point + height_vector

    def rotate(self):
        self.rotation += self.rotation_speed

        rotated_image = pygame.transform.rotozoom(self.original_snowball, self.rotation, 1)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image

    def bezier_movement(self):
        x = (1 - self.current_time) ** 2 * self.start_pos[0] + 2 * (1 - self.current_time) * self.current_time * self.mid_pos[0] + self.current_time ** 2 * self.end_pos[0]
        y = (1 - self.current_time) ** 2 * self.start_pos[1] + 2 * (1 - self.current_time) * self.current_time * self.mid_pos[1] + self.current_time ** 2 * self.end_pos[1]
        self.current_time += self.time_increment
        self.rect.center = (x, y)

    def update(self):
        if self.current_time <= 1:
            self.rotate()
            self.bezier_movement()