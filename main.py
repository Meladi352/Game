#import library 
import pygame

#timer for game
clock = pygame.time.Clock()

#game window
pygame.init()
screen = pygame.display.set_mode((648, 259))
icon = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(icon)
bg = pygame.image.load("images/bg.png").convert_alpha()

#player images
walk_right = [
    pygame.image.load("images/player_right/right1.png").convert_alpha(),
    pygame.image.load("images/player_right/right2.png").convert_alpha(),
    pygame.image.load("images/player_right/right3.png").convert_alpha(),
    pygame.image.load("images/player_right/right4.png").convert_alpha()
]
walk_left = [
    pygame.image.load("images/player_left/left1.png").convert_alpha(),
    pygame.image.load("images/player_left/left2.png").convert_alpha(),
    pygame.image.load("images/player_left/left3.png").convert_alpha(),
    pygame.image.load("images/player_left/left4.png").convert_alpha()
]
#monster image
ghost = pygame.image.load("images/ogre.png").convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_spead = 5
player_x = 150
player_y = 140

is_jump = False
jump_count = 8

#bg music
#bg_sound = pygame.mixer.Sound('sounds/Iceland Theme.mp3')
#bg_sound.play()

#monster timer
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 4500)

#box timer
box_timer = pygame.USEREVENT + 2
pygame.time.set_timer(box_timer, 25500)

label = pygame.font.Font("Fonts/RubikPuddles-Regular.ttf", 40)
lose_label = label.render("Sinä häviät!", False, (37, 56, 34))
restart_label = label.render("Pelaa uudestaan!", False, (235, 54, 26))
restart_label_rect = restart_label.get_rect(topleft=(145, 150))

bullets_box = pygame.image.load("images/case.png").convert_alpha()
box_list_in_game = []

bullets_left = 5
bullet = pygame.image.load("images/bullet.png").convert_alpha()
bullets = []
gameplay = True

running = True

while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x+648, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if box_list_in_game:
            for el in box_list_in_game:
                screen.blit(bullets_box, el)
                el.x -= 10
                if player_rect.colliderect(el):
                    bullets_left += 1

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_spead
        elif keys[pygame.K_RIGHT] and player_x < 250:
            player_x += player_spead

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -648:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((204, 240, 236))
        screen.blit(lose_label, (195, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 140)))

        if event.type == box_timer:
            box_list_in_game.append(bullets_box.get_rect(topleft=(750, 160)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1

    clock.tick(12)
