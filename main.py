from classes.penguin import Penguin
from classes.snowball_obstacle import Snowball_Obstacle
import pygame
from sys import exit

pygame.init()

screen_size = (800,400)
screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen_size)
background.fill('White')

pygame.display.set_caption("Club Penguin")
clock = pygame.time.Clock()

snowballs = pygame.sprite.Group()

mouse_has_moved = False
player = pygame.sprite.GroupSingle()
player.add(Penguin(mouse_has_moved, snowballs))
player_sprite = player.sprite

obstacles = pygame.sprite.Group()

obstacle_timer = 0
timer_increment = 0.01

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION and not mouse_has_moved:
            player_sprite.mouse_moved()
            mouse_has_moved = True

    

    screen.blit(background, (0,0))
    snowballs.update()
    player.update()
    player.draw(screen)
    snowballs.draw(screen)
    pygame.display.update()
    clock.tick(60)