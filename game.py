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
pygame.display.set_caption("EXIT_404")

clock = pygame.time.Clock()

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
# COLORS
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (60, 60, 60)
DARK = (20, 20, 20)
YELLOW = (255, 255, 120)
CYAN = (0, 255, 255)

# =========================
# FONT
# =========================
font = pygame.font.SysFont("consolas", 28)

# =========================
# PLAYER
# =========================
player_size = 40
player_x = 120
player_y = 120
speed = 4

battery = 100

# =========================
# MAP WALLS
# =========================
walls = [
    pygame.Rect(0, 0, 1000, 20),
    pygame.Rect(0, 0, 20, 700),
    pygame.Rect(980, 0, 20, 700),
    pygame.Rect(0, 680, 1000, 20),
    pygame.Rect(200, 100, 20, 500),
    pygame.Rect(400, 0, 20, 400),
    pygame.Rect(600, 200, 20, 500),
]

# =========================
# DOOR
# =========================
door = pygame.Rect(920, 300, 40, 100)

# =========================
# NPC
# =========================
npc_x = 700
npc_y = 500

show_dialog = False

dialogues = [
    "WHY ARE YOU HERE?",
    "YOU SHOULD LEAVE.",
    "IT KNOWS YOU.",
]

current_dialog = ""

# =========================
# ENEMY
# =========================
enemy_x = 850
enemy_y = 100
enemy_speed = 1.2

enemy_active = False

# =========================
# GLITCH
# =========================
glitch_timer = 0
show_glitch = False

# =========================
# JUMPSCARE
# =========================
show_jumpscare = False

# =========================
# SAVE CORRUPTION
# =========================
save_corrupted = False

# =========================
# FOOTSTEP TIMER
# =========================
step_timer = 0

# =========================
# ENDING
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
    # EVENTS
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

                npc_rect = pygame.Rect(npc_x, npc_y, 40, 40)

                if player_rect.colliderect(npc_rect):
                    show_dialog = True
                    current_dialog = random.choice(dialogues)

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
    # GLITCH ACTIVATION
    # =========================
    glitch_timer += 1

    if glitch_timer > 400:
        show_glitch = True

    # =========================
    # ENEMY ACTIVATION
    # =========================
    if glitch_timer > 700:
        enemy_active = True

# =========================
# ENEMY AI
# =========================

if enemy_active == True:

    dx = player_x - enemy_x
    dy = player_y - enemy_y

    distance = math.sqrt(dx**2 + dy**2)

    if distance != 0:

        enemy_x += (dx / distance) * enemy_speed
        enemy_y += (dy / distance) * enemy_speed

    # enemy chase sound
    distance_enemy = math.sqrt((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2)

    if distance_enemy < 200:

        if enemy_sound.get_num_channels() == 0:
            enemy_sound.play()

    else:

        enemy_sound.stop()

# =========================
# JUMPSCARE
# =========================

if enemy_active == True:

    if abs(player_x - enemy_x) < 50 and abs(player_y - enemy_y) < 50:

        show_jumpscare = True
    # =========================
    # GOOD / BAD ENDING
    # =========================
    if player_rect.colliderect(door):

        if battery > 20:
            game_ended = True
            ending_type = "GOOD"

        else:
            game_ended = True
            ending_type = "BAD"

    # =========================
    # SECRET ENDING
    # =========================
    if (
        glitch_timer > 1500
        and abs(player_x - npc_x) < 60
        and abs(player_y - npc_y) < 60
    ):

        game_ended = True
        ending_type = "SECRET"

    # =========================
    # BACKGROUND
    # =========================
    screen.fill(DARK)

    # =========================
    # WALLS
    # =========================
    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)

    # =========================
    # DOOR
    # =========================
    pygame.draw.rect(screen, YELLOW, door)

    # =========================
    # PLAYER
    # =========================
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))

    # =========================
    # NPC
    # =========================
    pygame.draw.rect(screen, (0, 150, 255), (npc_x, npc_y, 40, 40))

    # =========================
    # ENEMY
    # =========================
    if enemy_active:
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, 50, 50))

    # =========================
    # FLASHLIGHT
    # =========================
    darkness = pygame.Surface((WIDTH, HEIGHT))
    darkness.fill(BLACK)

    if battery > 0:

        pygame.draw.circle(
            darkness, (120, 120, 120), (player_x + 20, player_y + 20), 120
        )

        battery -= 0.01

    darkness.set_alpha(220)

    screen.blit(darkness, (0, 0))

    # =========================
    # UI
    # =========================
    draw_text(f"BATTERY: {int(battery)}%", WHITE, 20, 20)

    # =========================
    # DIALOG
    # =========================
    if show_dialog:

        pygame.draw.rect(screen, BLACK, (100, 550, 800, 100))
        pygame.draw.rect(screen, WHITE, (100, 550, 800, 100), 3)

        draw_text(current_dialog, RED, 130, 590)

    # =========================
    # GLITCH EFFECT
    # =========================
    if show_glitch:

        glitch_words = [
            "RUN",
            "DON'T TRUST IT",
            "SYSTEM ERROR",
            "WAKE UP",
        ]

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
    # FAKE POPUP
    # =========================
    if glitch_timer > 1200:

        pygame.draw.rect(screen, WHITE, (300, 200, 400, 200))

        draw_text("WINDOWS ERROR", BLACK, 360, 240)
        draw_text("UNKNOWN ENTITY DETECTED", RED, 320, 320)

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

    # =========================
    # ENDING SCREEN
    # =========================
    if game_ended:

        screen.fill(BLACK)

        if ending_type == "GOOD":

            draw_text("GOOD ENDING", WHITE, 350, 220)

            draw_text("YOU ESCAPED THE SCHOOL.", WHITE, 250, 320)

        elif ending_type == "BAD":

            draw_text("BAD ENDING", RED, 350, 220)

            draw_text("THE DARKNESS FOLLOWED YOU.", RED, 190, 320)

        elif ending_type == "SECRET":

            draw_text("SECRET ENDING", CYAN, 320, 220)

            draw_text("YOU WERE THE ENTITY ALL ALONG.", CYAN, 120, 320)

        pygame.display.update()

        pygame.time.delay(5000)

        pygame.quit()
        sys.exit()

    pygame.display.update()

pygame.quit()
