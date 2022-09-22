import pygame
from sys import exit
from random import randint

# Mostrar Puntuación
def display_score():
    current_time = int(((pygame.time.get_ticks()) / 1000 - start_time) * 2.5)
    score_surface = text_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    
    return current_time


# Mostrar Inicio/GameOver
def display_gameOver(record):
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)

    # Resetear posición del jugador
    player_rect.midbottom = (80, 300)
    player_grav = 0

    # Limpiar lista de obstáculos
    obstacle_rect_list.clear()
        

    # Show Title
    game_title = text_font.render("SALTA POR TU VIDA", False, (111, 235, 196))
    game_title = pygame.transform.scale2x(game_title)
    game_title_rect = game_title.get_rect(center=(400, 80))
    game_subtitle = text_font.render("Press space to start", False, (111, 235, 196))
    game_subtitle_rect = game_subtitle.get_rect(center=(400, 320))
    screen.blit(game_title, game_title_rect)
    screen.blit(game_subtitle, game_subtitle_rect)
        

    # Show Score
    score_message = text_font.render(f"Your score: {score}", False, "Yellow")
    score_message_rect = score_message.get_rect(center=(400, 350))
    screen.blit(score_message, score_message_rect)

    # Record
    if(score == 0):
        return 0
    elif(score >= record):
        new_record_surf = text_font.render("NEW RECORD", False, "Yellow").convert()
        new_record_rect = new_record_surf.get_rect(center=(400,380))
        screen.blit(new_record_surf,new_record_rect)
        record = score
        return record
    else:
        new_record_surf = text_font.render(f"Record: {record}", False, "Yellow").convert()
        new_record_rect = new_record_surf.get_rect(center=(400,380))
        screen.blit(new_record_surf,new_record_rect)
        return record


# Movimiento obstáculos
def obstacle_movement(obstacle_list):
    if obstacle_list:
        # Spawnear y mover todos los caracoles
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 4 + aceleracion

            # Si tiene altura 300 -> es un caracol
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            # Si no, es un enemigo volador
            else:
                screen.blit(fly_surf, obstacle_rect)

        # Borrar los caracoles que pasen la x = -100
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


# Colisiones
def collisions(player, obstacles):
    if obstacles:
        for rect in obstacles:
            if player.colliderect(rect):
                return False
    return True


# Animacion del jugador
def player_animation():
    global player_surf, player_index

    # Saltando
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        # Walk
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


# Initialitaze
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner xD")
mouse_pos = (0, 0)
record = 0
score = 0
game_active = False

# Clock (controlling the frametime)
clock = pygame.time.Clock()

# Start time
start_time = 0

# <------FONT------->
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# <------SURFACES------>
# Sky surface
sky_surface = pygame.image.load("graphics/Sky.png").convert()

# Ground surface
ground_surface = pygame.image.load("graphics/ground.png").convert()

# <----OBSTACLES---->
# Snail surfaces
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# Fly_surf
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Enemy acceleration
aceleracion = 0

# Lista de obstáculos:
obstacle_rect_list = []

# <----Player---->
# Player surfaces
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

# Indices
player_index = 0

# Lista de superficies
player_surf = player_walk[player_index]
# Player rectangle
player_rect = player_surf.get_rect(midbottom=(80, 300))

# Player Gravity
player_grav = 0

# Player start game
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # Escalar la imagen
player_stand_rect = player_stand.get_rect(center=(400, 200))

# <----Timers---->

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


# Event Loop
while True:
    for event in pygame.event.get():
        # Salir del juego con el botón x
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Controles en Juego activo
        if game_active:
            # Controles de ratón
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                player_grav = -20
            # Controles de teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_grav = -20
            # Crear enemigos
            if event.type == obstacle_timer:
                # Crear caracol (a partir de variable aleatoria)
                if randint(0, 3):
                    obstacle_rect_list.append(
                        snail_surface.get_rect(bottomright=(randint(900, 1100), 300))
                    )
                # Crear enemigo volador
                else:
                    obstacle_rect_list.append(
                        fly_surf.get_rect(bottomright=(randint(900, 1100), 210)) 
                    )
            # Animaciones de los enemigos
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        # Controles en Game Over
        else:
            # Reiniciar
            # Controles de ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
                # Reiniciar tiempo
                start_time = int(pygame.time.get_ticks()) / 1000
            # Controles de teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    # Reiniciar tiempo
                    start_time = int(pygame.time.get_ticks()) / 1000
    # Juego activo
    if game_active:
        # Sky and ground
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Actualizar score y mostrar
        score = display_score()

        # Movimiento del jugador
        player_grav += 1
        player_rect.y += player_grav

        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        # Animaciones
        player_animation()

        # Draw player
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Colisiones
        game_active = collisions(player_rect, obstacle_rect_list)
        
        # Aceleracion
        aceleracion += float(display_score())*0.0001

    # Game Over / Start Game
    else:
        record = display_gameOver(record)
        aceleracion = 0

    # update everything
    pygame.display.update()
    clock.tick(60)  # Frametime
