import pygame
import random
import sys
import math

pygame.init()
pygame.mixer.init()

# =========================
# WINDOW
# =========================
WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 180)

# =========================
# GAME STATE
# =========================
game_state = "menu"

# =========================
# FONT
# =========================
font = pygame.font.SysFont("consolas", 28)
big_font = pygame.font.SysFont("consolas", 70)

# =========================
# BUTTONS
# =========================
start_button = pygame.Rect(350, 280, 300, 80)
quit_button = pygame.Rect(350, 400, 300, 80)

# =========================
# SOUND
# =========================
footstep_sound = pygame.mixer.Sound("footsteps.mp3")
enemy_sound = pygame.mixer.Sound("chase.mp3")

footstep_sound.set_volume(0.3)
enemy_sound.set_volume(0.6)

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# =========================
# TILE SIZE
# =========================
tile_size = 64
wall_size = 64

# =========================
# IMAGES
# =========================
player_img = pygame.image.load("player.png").convert_alpha()
enemy_img = pygame.image.load("enemy.png").convert_alpha()
npc_img = pygame.image.load("npc.png").convert_alpha()
door_img = pygame.image.load("door.png").convert_alpha()
wall_img = pygame.image.load("wall.png").convert_alpha()
floor_img = pygame.image.load("floor.png").convert_alpha()

# =========================
# RESIZE
# =========================
player_size = 48

player_img = pygame.transform.scale(player_img, (80, 80))
enemy_img = pygame.transform.scale(enemy_img, (120, 120))
npc_img = pygame.transform.scale(npc_img, (80, 80))
door_img = pygame.transform.scale(door_img, (64, 128))

wall_img = pygame.transform.scale(wall_img, (wall_size, wall_size))

floor_img = pygame.transform.scale(floor_img, (tile_size, tile_size))

# =========================
# PLAYER
# =========================
player_x = 120
player_y = 120
speed = 4

battery = 100

# =========================
# WALLS
# =========================
walls = [
    pygame.Rect(0, 0, 1000, 32),
    pygame.Rect(0, 0, 32, 700),
    pygame.Rect(968, 0, 32, 700),
    pygame.Rect(0, 668, 1000, 32),
    pygame.Rect(250, 100, 32, 500),
    pygame.Rect(500, 0, 32, 450),
    pygame.Rect(750, 200, 32, 500),
]

# =========================
# DOOR
# =========================
door = pygame.Rect(900, 250, 64, 128)

# =========================
# NPC
# =========================
npc_x = 820
npc_y = 560

show_dialog = False
current_dialog = ""

# =========================
# ENEMY
# =========================
enemy_x = 850
enemy_y = 100

enemy_speed = 1.4
enemy_active = False

# =========================
# EFFECTS
# =========================
glitch_timer = 0
show_glitch = False
show_jumpscare = False
save_corrupted = False
fake_crash_done = False

# =========================
# FOOTSTEP TIMER
# =========================
step_timer = 0

# =========================
# ENDINGS
# =========================
game_ended = False
ending_type = ""


# =========================
# FUNCTIONS
# =========================
def draw_text(text, color, x, y):

    render = font.render(text, True, color)
    screen.blit(render, (x, y))


def collision(rect, walls):

    for wall in walls:

        if rect.colliderect(wall):
            return True

    return False


# =========================
# GAME LOOP
# =========================
running = True

while running:

    clock.tick(60)

    # =========================
    # WINDOW TITLE
    # =========================
    if ending_type == "BAD":

        pygame.display.set_caption("NO_EXIT")

    else:

        pygame.display.set_caption("EXIT_404")

    # =========================
    # MENU
    # =========================
    if game_state == "menu":

        if ending_type == "BAD":

            screen.fill((40, 0, 0))

        else:

            screen.fill(BLACK)

        # TITLE
        if ending_type == "BAD":

            title_text = "NO_EXIT"

        else:

            title_text = "EXIT_404"

        title = big_font.render(title_text, True, RED)

        screen.blit(title, (300, 120))

        draw_text("Psychological Horror", WHITE, 340, 210)

        mouse_pos = pygame.mouse.get_pos()

        # START BUTTON
        if start_button.collidepoint(mouse_pos):

            pygame.draw.rect(screen, (255, 0, 0), start_button)

        else:

            pygame.draw.rect(screen, (120, 0, 0), start_button)

        draw_text("START", WHITE, 445, 305)

        # QUIT BUTTON
        pygame.draw.rect(screen, WHITE, quit_button)

        draw_text("QUIT", BLACK, 460, 425)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_button.collidepoint(mouse_pos):

                    game_state = "game"

                if quit_button.collidepoint(mouse_pos):

                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        continue

    # =========================
    # EVENTS
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

                npc_rect = pygame.Rect(npc_x, npc_y, 48, 48)

                if player_rect.colliderect(npc_rect):

                    show_dialog = True

                    if glitch_timer < 400:

                        current_dialog = "WHY ARE YOU HERE?"

                    elif glitch_timer < 900:

                        current_dialog = "YOU SHOULD LEAVE."

                    elif glitch_timer < 1300:

                        current_dialog = "IT KNOWS YOU."

                    else:

                        creepy_dialogs = [
                            "YOU LEFT US HERE",
                            "IT IS INSIDE YOU",
                            "YOU WERE NEVER HUMAN",
                            "STOP LOOKING AT ME",
                        ]

                        current_dialog = random.choice(creepy_dialogs)

    # =========================
    # MOVEMENT
    # =========================
    old_x = player_x
    old_y = player_y

    keys = pygame.key.get_pressed()

    moving = False

    if keys[pygame.K_w]:
        player_y -= speed
        moving = True

    if keys[pygame.K_s]:
        player_y += speed
        moving = True

    if keys[pygame.K_a]:
        player_x -= speed
        moving = True

    if keys[pygame.K_d]:
        player_x += speed
        moving = True

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    if collision(player_rect, walls):

        player_x = old_x
        player_y = old_y

    # =========================
    # FOOTSTEP SOUND
    # =========================
    if moving:

        step_timer += 1

        if step_timer > 20:

            footstep_sound.play()
            step_timer = 0

    # =========================
    # GLITCH TIMER
    # =========================
    glitch_timer += 1

    if glitch_timer > 400:
        show_glitch = True

    if glitch_timer > 700:
        enemy_active = True

    # =========================
    # ENEMY AI
    # =========================
    if enemy_active:

        dx = player_x - enemy_x
        dy = player_y - enemy_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:

            enemy_x += (dx / distance) * enemy_speed
            enemy_y += (dy / distance) * enemy_speed

        distance_enemy = math.sqrt(
            (player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2
        )

        if distance_enemy < 220:

            if enemy_sound.get_num_channels() == 0:
                enemy_sound.play()

        else:

            enemy_sound.stop()

    # =========================
    # JUMPSCARE
    # =========================
    if enemy_active:

        if abs(player_x - enemy_x) < 70 and abs(player_y - enemy_y) < 70:

            show_jumpscare = True

    # =========================
    # GOOD / BAD ENDING
    # =========================
    if player_rect.colliderect(door) and glitch_timer > 300:

        if battery > 20:

            game_ended = True
            ending_type = "GOOD"

        else:

            game_ended = True
            ending_type = "BAD"

        game_state = "menu"

    # =========================
    # SECRET ENDING
    # =========================
    if (
        glitch_timer > 1500
        and abs(player_x - npc_x) < 70
        and abs(player_y - npc_y) < 70
    ):

        game_ended = True
        ending_type = "SECRET"

    # =========================
    # FLOOR
    # =========================
    for x in range(0, WIDTH, tile_size):

        for y in range(0, HEIGHT, tile_size):

            screen.blit(floor_img, (x, y))

    # =========================
    # WALLS
    # =========================
    for wall in walls:

        for x in range(wall.x, wall.x + wall.width, wall_size):

            for y in range(wall.y, wall.y + wall.height, wall_size):

                screen.blit(wall_img, (x, y))

    # =========================
    # DOOR
    # =========================
    screen.blit(door_img, (door.x, door.y))

    # =========================
    # PLAYER
    # =========================
    screen.blit(player_img, (player_x, player_y))

    # =========================
    # NPC
    # =========================
    screen.blit(npc_img, (npc_x, npc_y))

    # =========================
    # ENEMY
    # =========================
    if enemy_active:

        screen.blit(enemy_img, (enemy_x, enemy_y))

    # =========================
    # FLASHLIGHT
    # =========================
    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    darkness.fill((0, 0, 0, 220))

    pygame.draw.circle(darkness, (0, 0, 0, 0), (player_x + 24, player_y + 24), 140)

    screen.blit(darkness, (0, 0))

    # =========================
    # EYE IN DARKNESS
    # =========================
    if random.randint(1, 250) == 1:

        eye_x = random.randint(0, WIDTH)
        eye_y = random.randint(0, HEIGHT)

        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 8)

        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)

    # =========================
    # BATTERY
    # =========================
    if battery > 0:
        battery -= 0.01

    draw_text(f"BATTERY: {int(battery)}%", WHITE, 20, 20)

    # =========================
    # DIALOG
    # =========================
    if show_dialog:

        pygame.draw.rect(screen, BLACK, (100, 540, 800, 120))

        pygame.draw.rect(screen, WHITE, (100, 540, 800, 120), 3)

        draw_text(current_dialog, RED, 130, 590)

    # =========================
    # GLITCH TEXT
    # =========================
    if show_glitch:

        glitch_words = ["RUN", "DON'T TRUST IT", "SYSTEM ERROR", "WAKE UP"]

        text = random.choice(glitch_words)

        shake_x = random.randint(-15, 15)
        shake_y = random.randint(-15, 15)

        draw_text(text, RED, 400 + shake_x, 80 + shake_y)

    # =========================
    # SAVE CORRUPTION
    # =========================
    if glitch_timer > 1000 and not save_corrupted:

        print("SAVE FILE CORRUPTED")
        save_corrupted = True

    # =========================
    # FAKE CRASH
    # =========================
    if glitch_timer > 1700 and not fake_crash_done:

        screen.fill(BLUE)

        crash_font = pygame.font.SysFont("consolas", 35)

        text1 = crash_font.render("A problem has been detected", True, WHITE)

        text2 = crash_font.render("and Windows has been shut down.", True, WHITE)

        screen.blit(text1, (120, 250))
        screen.blit(text2, (120, 320))

        pygame.display.update()

        pygame.time.delay(3000)

        fake_crash_done = True

    # =========================
    # JUMPSCARE
    # =========================
    if show_jumpscare:

        screen.fill(RED)

        draw_text("YOU SHOULD NOT BE HERE", BLACK, 220, 300)

        pygame.display.update()

        pygame.time.delay(2000)

        pygame.quit()
        sys.exit()

    pygame.display.update()

pygame.quit()
