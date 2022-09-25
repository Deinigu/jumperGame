import pygame
from sys import exit
from random import randint, choice

# Clase Jugador
class Player(pygame.sprite.Sprite):
    # Inicializar
    def __init__(self):
        super().__init__()

        # Sprites
        player_walk_1 = pygame.image.load(
            "graphics/Player/player_walk_1.png"
        ).convert_alpha()
        player_walk_2 = pygame.image.load(
            "graphics/Player/player_walk_2.png"
        ).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))

        # Gravedad
        self.gravity = 0

    # Controles del jugador
    def player_input(self):
        keys = pygame.key.get_pressed()
        # Jump
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    # Aplicar gravedad al jugador
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        # Mantenerse en el suelo
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    # Animaciones
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    # Actualizar jugador
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# Clase Obstáculo
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        # Sprites Mosca
        if type == "fly":
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        # Sprites Caracol
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    # Animaciones
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    # Actualizar obstáculo
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    # Destruir obstáculo
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


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
    if score == 0:
        return 0
    elif score >= record:
        new_record_surf = text_font.render("NEW RECORD", False, "Yellow").convert()
        new_record_rect = new_record_surf.get_rect(center=(400, 380))
        screen.blit(new_record_surf, new_record_rect)
        record = score
        return record
    else:
        new_record_surf = text_font.render(
            f"Record: {record}", False, "Yellow"
        ).convert()
        new_record_rect = new_record_surf.get_rect(center=(400, 380))
        screen.blit(new_record_surf, new_record_rect)
        return record


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

# Initialitaze
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner xD")
mouse_pos = (0, 0)
record = 0
score = 0
game_active = False

# <----Groups---->
# Player group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacle group
obstacle_group = pygame.sprite.Group()

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

# Player start game
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # Escalar la imagen
player_stand_rect = player_stand.get_rect(center=(400, 200))

# <----Timers---->
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)


# Event Loop
while True:
    for event in pygame.event.get():
        # Salir del juego con el botón x
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Timer en juego activo
        if game_active:
            if event.type == obstacle_timer:
                # Crear obstáculo
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

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

        # Draw and update Player
        player.draw(screen)
        player.update()

        # Draw and update Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Colisiones
        game_active = collision_sprite()

    # Game Over / Start Game
    else:
        record = display_gameOver(record)

    # update everything
    pygame.display.update()
    clock.tick(60)  # Frametime
