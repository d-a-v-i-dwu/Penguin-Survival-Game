import pygame
import os
import sys
import numpy as np
from classes.snowball import Snowball
from classes.snowball_shadow import Snowball_Shadow

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    return os.path.join(base_path, relative_path)

class Penguin(pygame.sprite.Sprite):
    def __init__(self, mouse_has_moved, snowballs):
        super().__init__()

        self.mouse_has_moved = mouse_has_moved
        self.snowballs = snowballs

        snowball_cursor_path = resource_path(os.path.join("resources", "images", "snowball_cursor.png"))
        self.aiming_cursor = pygame.transform.scale(pygame.image.load(snowball_cursor_path).convert_alpha(), (40, 40))

        self.snowball_animations = []
        snowball_folder = resource_path(os.path.join("resources", "images", "snowball_animations"))
        snowball_animation_scale_factor = 0.5

        for folder in os.listdir(snowball_folder):
            directional_snowball_folder = os.path.join(snowball_folder, folder)
            directional_snowball_folder_sorted = sorted(os.listdir(directional_snowball_folder), key=lambda x: int(os.path.splitext(x)[0]))
            directional_snowball_animations = []

            for img in directional_snowball_folder_sorted:
                image = pygame.image.load(os.path.join(directional_snowball_folder, img)).convert_alpha()
                directional_snowball_animations.append(pygame.transform.scale(image, (int(image.get_width() * snowball_animation_scale_factor), int(image.get_height() * snowball_animation_scale_factor))))

            self.snowball_animations.append(directional_snowball_animations)

        self.current_snowball_animation = None
        self.x_shift = 0
        self.y_shift = 0

        self.walking_animations = []
        walking_folder = resource_path(os.path.join("resources", "images", "walking_animations"))

        for folder in os.listdir(walking_folder):
            directional_walking_folder = os.path.join(walking_folder, folder)
            directional_walking_animations = []
            animation_increment = float(folder[2:])

            for img in os.listdir(directional_walking_folder):
                image = pygame.image.load(os.path.join(directional_walking_folder, img)).convert_alpha()
                directional_walking_animations.append(image)

            self.walking_animations.append((directional_walking_animations, animation_increment))

        start_position = (400,200)

        self.current_animation_folder = self.walking_animations[4][0]
        self.image = self.current_animation_folder[0]
        self.rect = self.image.get_rect(midbottom = start_position)
        
        self.click_pos = np.array([start_position[0], start_position[1]])
        self.movement_vector = np.array([0,0])
        self.walking = True

        self.animation_index = 0
        self.animation_increment = 0
        self.flip = False

        self.orientation_vector = np.array([0,1])
        self.mouse_angle = 0

        self.gathering_snowball = False
        self.throwing_snowball = False
        self.mouse_clicked = False
        self.is_aiming = False
        self.rect_correct = False


    def mouse_moved(self):
        self.mouse_has_moved = True


    def orient(self):
        if self.mouse_has_moved:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.orientation_vector[0] = mouse_x - self.rect.center[0]
            self.orientation_vector[1] = mouse_y - self.rect.center[1]
        magnitude = np.linalg.norm(self.orientation_vector)
        cos_theta = np.dot(self.orientation_vector, np.array([0,1])) / (magnitude)
        self.mouse_angle = np.degrees(np.arccos(cos_theta))
        if self.orientation_vector[0] > 0:
            self.flip = True
        else:
            self.flip = False


    def face_mouse(self):
        if self.mouse_angle < 12.5:
            animation_folder_index = 4
        elif self.mouse_angle < 77.5:
            animation_folder_index = 3
        elif self.mouse_angle < 102.5:
            animation_folder_index = 2
        elif self.mouse_angle <= 167.5:
            animation_folder_index = 1
        else:
            animation_folder_index = 0

        self.current_animation_folder = self.walking_animations[animation_folder_index][0]
        self.animation_increment = self.walking_animations[animation_folder_index][1]
        self.image = pygame.transform.flip(self.current_animation_folder[0], self.flip, False)


    def move(self):
        if abs(self.rect.midbottom[0] - self.click_pos[0]) + abs(self.rect.midbottom[1] - self.click_pos[1]) < 5:
             self.rect.midbottom = self.click_pos
             self.walking = False
        else:
            self.movement_vector[0] = self.click_pos[0] - self.rect.midbottom[0]
            self.movement_vector[1] = self.click_pos[1] - self.rect.midbottom[1]
            magnitude = np.linalg.norm(self.movement_vector)
            self.movement_vector = (self.movement_vector / magnitude) * 4.5
            self.rect.midbottom = (self.rect.midbottom[0] + self.movement_vector[0], self.rect.midbottom[1] + self.movement_vector[1])


    def animate_walking(self):
        self.animation_index += self.animation_increment
        if self.animation_index >= len(self.current_animation_folder):
            self.animation_index = 0
        else:
            self.image = pygame.transform.flip(self.current_animation_folder[int(self.animation_index)], self.flip, False)


    def snowball_key_press_check(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_t] or pygame.mouse.get_pressed()[2]:
            self.gathering_snowball = True
            self.walking = False
            self.is_aiming = False
            self.animation_index = 0


    def snowball_orient(self):
        # print("snowball orient")
        if self.mouse_angle <= 85:
            self.current_snowball_animation = self.snowball_animations[0]
            if self.flip:
                self.x_shift = -12
                self.y_shift = -18
            else:
                self.x_shift = -9
                self.y_shift = -18
        else:
            self.current_snowball_animation = self.snowball_animations[1]
            if self.flip:
                self.x_shift = 5
                self.y_shift = -10
            else:
                self.x_shift = -12
                self.y_shift = -10


    def snowball_animation(self):
        # print("snowball_animation")
        if self.current_snowball_animation == None:
            self.snowball_orient()
            self.rect.x += self.x_shift
            self.rect.y += self.y_shift

        if self.animation_index < len(self.current_snowball_animation):
            self.image = pygame.transform.flip(self.current_snowball_animation[int(self.animation_index)], self.flip, False)
            self.animation_index += 0.33
        else:
            self.animation_index = 0
            self.gathering_snowball = False
            self.is_aiming = True
            pygame.mouse.set_cursor((20, 20), self.aiming_cursor)


    def aiming(self):
        # print("aiming")
        self.rect.x -= self.x_shift
        self.rect.y -= self.y_shift
        self.orient()
        self.snowball_orient()
        self.rect.x += self.x_shift
        self.rect.y += self.y_shift
        self.image = pygame.transform.flip(self.current_snowball_animation[-1], self.flip, False)


    def throw_snowball(self):
        if self.animation_index < len(self.current_snowball_animation):
            self.image = pygame.transform.flip(self.current_snowball_animation[int(self.animation_index)], self.flip, False)
            self.animation_index += 0.33
        else:
            self.current_snowball_animation = None
            self.throwing_snowball = False
            self.animation_index = 0
            self.rect_correct = True
            pygame.mouse.set_cursor(pygame.cursors.arrow)

            
    def click_check(self):
        if pygame.mouse.get_pressed()[0] and not self.throwing_snowball and not pygame.mouse.get_pressed()[2]:
            self.mouse_clicked = True
        elif self.mouse_clicked == True:
            if self.gathering_snowball:
                self.gathering_snowball = False
                self.current_snowball_animation = None
                self.rect_correct = True
            self.mouse_clicked = False
            self.click_pos = pygame.mouse.get_pos()
            if self.is_aiming:
                self.throwing_snowball = True
                self.is_aiming = False
                start_x, start_y = self.rect.center
                if self.current_snowball_animation == self.snowball_animations[0]:
                    start_y -= 1
                    if self.flip:
                        start_x -= 16
                    else:
                        start_x += 35
                    self.current_snowball_animation = self.snowball_animations[2]
                else:
                    start_y += 10
                    if self.flip:
                        start_x += 1
                    else:
                        start_x += 2
                    self.current_snowball_animation = self.snowball_animations[3]

                Snowball_Shadow(self.snowballs, (start_x, start_y), self.click_pos, self.mouse_angle, self.flip)
                Snowball(self.snowballs, (start_x, start_y), self.click_pos, self.mouse_angle, self.flip)

            else:
                self.orient()
                self.face_mouse()
                if not self.walking:
                    self.walking = True
                    self.animation_index = 0


    def update(self):
        self.click_check()

        if self.rect_correct:
            self.rect.x -= self.x_shift
            self.rect.y -= self.y_shift
            self.rect_correct = False
        
        if self.throwing_snowball:
            self.throw_snowball()
        else:
            self.snowball_key_press_check()
            if self.is_aiming:
                self.aiming()
            elif self.gathering_snowball:
                self.snowball_animation()
            elif self.walking:
                self.animate_walking()
                self.move()
            else:
                self.orient()
                self.face_mouse()
