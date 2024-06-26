import pygame
import math
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.run = 180
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(self.run, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        if display_score() >= 270:
            self.rect.x += 2
        self.apply_gravity()
        self.animation_state()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            enemy_2 = pygame.image.load('graphics/enemy/enemy_2.png').convert_alpha()
            enemy_02 = pygame.image.load('graphics/enemy/enemy_02.png').convert_alpha()
            self.frames = [enemy_2, enemy_02]
            y_pos = 210
        else:
            enemy_1 = pygame.image.load('graphics/enemy/enemy_1.png').convert_alpha()
            enemy_01 = pygame.image.load('graphics/enemy/enemy_01.png').convert_alpha()
            self.frames = [enemy_1, enemy_01]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
        if display_score() >= 300:
            self.kill()


def display_score():
    scores = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = font_1.render(f'Score: {scores}m', False, (200, 200, 200))
    score_rect = score_surf.get_rect(midleft=(600, 40))
    screen.blit(score_surf, score_rect)
    return scores


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        death_sound = pygame.mixer.Sound("audio/death.wav")
        death_sound.play()
        return False
    else:
        return True

pygame.init()
screenW = 800
screenH = 400
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Running Game')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeboy-z8XGD.ttf', 35)
font_1 = pygame.font.Font('font/Pixeboy-z8XGD.ttf', 30)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops=-1)
# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()


# Intro screen
intro = pygame.image.load('graphics/mainMenu/intro.png').convert_alpha()
intro_rect = intro.get_rect(center=(400, 100))
intro_2 = font_1.render("Press space for start game!", False, ("red"))
intro2_rect = intro_2.get_rect(center=(393, 220))
# Background and flag
sky_surface = pygame.image.load('graphics/background/Sky.png').convert()
ground_surface = pygame.image.load('graphics/background/ground.png').convert()
flag_surface = pygame.image.load('graphics/background/flag.png').convert_alpha()
flag_x = 1000
# Win Screen
win = pygame.image.load('graphics/mainMenu/win.png').convert_alpha()
win_rect = win.get_rect(center=(400, 150))
# Lost Screen
lost = pygame.image.load('graphics/mainMenu/lost.png').convert_alpha()
lost_rect = lost.get_rect(center=(400, 150))
# Cloud Screen
cloud = pygame.image.load('graphics/background/cloud1.png')
cloud_2 = pygame.image.load('graphics/background/cloud2.png')
cloud_x = 0
cloud_y = 0
montain = pygame.image.load('graphics/background/tree_1.png')
# Box Screen
box = pygame.image.load('graphics/background/box.png')
box_rect = box.get_rect(center=(670, 40))

obstacle_timer = pygame.USEREVENT + 1

# Ground Animation
BGW = ground_surface.get_width()
scroll = 0
tile = math.ceil(screenW / BGW) + 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)
                player.sprite.rect.x = 180
                pygame.time.set_timer(obstacle_timer, 1400)
                if score >= 240:
                    flag_x = 1000
                    flag_x -= 1
                    screen.blit(flag_surface, (flag_x, 210))
    if game_active:
        screen.blit(sky_surface, (0, 0))
        cloud_x -= 2
        if cloud_x == -150:
            cloud_x = 800
        screen.blit(cloud, (cloud_x, 40))
        screen.blit(cloud_2, (cloud_x + 50, 90))
        cloud_y -= 2
        if cloud_y == -320:
            cloud_y = 800
        screen.blit(box, box_rect)
        screen.blit(montain, (cloud_y+200, 255))
        screen.blit(montain, (cloud_x -50, 255))
        # screen.blit(ground_surface,(0,300))
        score = display_score()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()

        player.draw(screen)
        player.update()
        for i in range(0, tile):
            screen.blit(ground_surface, (i * BGW + scroll, 300))
        scroll -= 3
        # reset scroll
        if abs(scroll) > BGW:
            scroll = 0
    else:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score_message = font_1.render(f'Your score: {score}m', False, ('Gray'))
        score_message_rect = score_message.get_rect(center=(395, 330))
        if score == 0:
            screen.blit(intro, intro_rect)
            screen.blit(intro_2, intro2_rect)
        else:
            screen.blit(lost, lost_rect)
            screen.blit(score_message, (310, 150))
    # When nearly Finish not Enemy
    if score >= 255:
        pygame.time.set_timer(obstacle_timer, 0)
    # Flag come to player
    if score >= 240:
        if game_active:
            flag_x -= 1
            screen.blit(flag_surface, (flag_x, 210))
    # When Player run to 300 score Finished
    if score >= 300:
        game_active = False
        pygame.time.set_timer(obstacle_timer, 1400)
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface,(0,300))
        score_message = font_1.render(f'Your score: {score} m', False, (200, 200, 200))
        if score == 0:
            screen.blit(intro, intro_rect)
        else:
            screen.blit(win, win_rect)
            screen.blit(score_message, (294, 170))
    pygame.display.update()
    clock.tick(60)