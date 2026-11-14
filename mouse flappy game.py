import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Escape!")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)
big_font = pygame.font.SysFont("Arial", 55, bold=True)

# Colors
SKY = (90, 185, 235)
BUILDING = (55, 75, 110)
WINDOW = (255, 220, 100)
BROWN = (145, 85, 45)
DARK = (65, 45, 35)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (210, 45, 55)
GREY = (120, 120, 130)

# Game variables
mouse_x = 170
mouse_y = 280
mouse_velocity = 0
gravity = 0.42
jump_power = -8

score = 0
game_over = False
started = False

obstacles = []
obstacle_speed = 4
spawn_timer = 0

train_x = -500
building_scroll = 0


# Draw mouse
def draw_mouse(x, y):

    x, y = int(x), int(y)

    # Tail
    pygame.draw.line(
        screen, (210, 130, 140),
        (x - 20, y + 5),
        (x - 42, y + 15), 4
    )

    # Ears
    pygame.draw.circle(screen, (130, 90, 85), (x - 8, y - 17), 12)
    pygame.draw.circle(screen, (230, 140, 150), (x - 8, y - 17), 7)

    pygame.draw.circle(screen, (130, 90, 85), (x + 10, y - 17), 12)
    pygame.draw.circle(screen, (230, 140, 150), (x + 10, y - 17), 7)

    # Body
    pygame.draw.ellipse(
        screen, (145, 125, 120),
        (x - 25, y - 10, 48, 30)
    )

    # Head
    pygame.draw.circle(screen, (155, 135, 130), (x + 15, y - 5), 17)

    # Nose
    pygame.draw.circle(screen, (230, 100, 120), (x + 31, y - 5), 5)

    # Eye
    pygame.draw.circle(screen, BLACK, (x + 20, y - 10), 3)
    pygame.draw.circle(screen, WHITE, (x + 21, y - 11), 1)

    # Whiskers
    pygame.draw.line(screen, WHITE, (x + 23, y), (x + 43, y - 6), 1)
    pygame.draw.line(screen, WHITE, (x + 23, y + 2), (x + 43, y + 5), 1)


# Draw mousetrap
def draw_trap(x, y, width, height):

    # Wooden board
    pygame.draw.rect(
        screen, BROWN,
        (x, y, width, height)
    )

    pygame.draw.rect(
        screen, DARK,
        (x, y, width, height), 5
    )

    # Wood details
    for i in range(int(x) + 12, int(x + width), 20):
        pygame.draw.line(
            screen, (185, 120, 65),
            (i, y + 5), (i, y + height - 5), 2
        )

    # Spring
    spring_y = y + height // 2

    pygame.draw.line(
        screen, GREY,
        (x + 15, spring_y),
        (x + width - 15, spring_y), 5
    )

    for i in range(0, 5):
        pygame.draw.circle(
            screen, WHITE,
            (int(x + 20 + i * 12), spring_y), 3
        )

    # Cheese
    cheese_x = int(x + width // 2)
    cheese_y = int(y + height // 2 + 15)

    pygame.draw.circle(
        screen, (255, 190, 30),
        (cheese_x, cheese_y), 15
    )

    pygame.draw.circle(
        screen, (255, 225, 80),
        (cheese_x - 4, cheese_y - 4), 4
    )


# Background buildings
buildings = []

for i in range(12):
    buildings.append({
        "x": i * 100,
        "height": random.randint(100, 220)
    })


def draw_background():

    global building_scroll, train_x

    screen.fill(SKY)

    # Clouds
    for i in range(4):
        cx = (i * 230 - building_scroll // 2) % 1000

        pygame.draw.circle(screen, WHITE, (cx, 100), 20)
        pygame.draw.circle(screen, WHITE, (cx + 20, 90), 25)
        pygame.draw.circle(screen, WHITE, (cx + 45, 105), 20)

    # Buildings
    for b in buildings:

        bx = (b["x"] - building_scroll) % 1200
        by = 420 - b["height"]

        pygame.draw.rect(
            screen, BUILDING,
            (bx, by, 75, b["height"])
        )

        # Windows
        for wx in range(10, 65, 25):
            for wy in range(15, b["height"] - 10, 30):

                pygame.draw.rect(
                    screen, WINDOW,
                    (bx + wx, by + wy, 10, 15)
                )

    building_scroll += 1

    # Railway track
    pygame.draw.rect(screen, (80, 75, 75), (0, 500, WIDTH, 15))
    pygame.draw.rect(screen, (100, 100, 105), (0, 515, WIDTH, 8))

    for i in range(0, WIDTH, 35):
        pygame.draw.rect(
            screen, DARK,
            (i, 500, 8, 23)
        )

    # Moving train
    train_x += 5

    if train_x > WIDTH:
        train_x = -550

    pygame.draw.rect(
        screen, RED,
        (train_x, 440, 550, 60),
        border_radius=8
    )

    pygame.draw.rect(
        screen, WHITE,
        (train_x, 450, 550, 28)
    )

    # Train windows
    for i in range(5):
        pygame.draw.rect(
            screen, (70, 145, 190),
            (train_x + 20 + i * 105, 452, 65, 22),
            border_radius=4
        )

    pygame.draw.rect(
        screen, DARK,
        (train_x, 493, 550, 7)
    )


# Create obstacles
def create_obstacle():

    gap = 180
    gap_y = random.randint(180, 370)

    obstacles.append({
        "x": WIDTH,
        "gap_y": gap_y,
        "gap": gap,
        "passed": False
    })


def reset_game():

    global mouse_y, mouse_velocity
    global score, game_over, started
    global obstacles, obstacle_speed, spawn_timer

    mouse_y = 280
    mouse_velocity = 0

    score = 0
    game_over = False
    started = False

    obstacles = []
    obstacle_speed = 4
    spawn_timer = 0


# Main loop
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse click or touch
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over:
                reset_game()

            else:
                started = True
                mouse_velocity = jump_power

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:

                if game_over:
                    reset_game()

                else:
                    started = True
                    mouse_velocity = jump_power

            if event.key == pygame.K_r and game_over:
                reset_game()

    # Background
    draw_background()

    if started and not game_over:

        # Mouse physics
        mouse_velocity += gravity
        mouse_y += mouse_velocity

        # Spawn traps
        spawn_timer += 1

        if spawn_timer > 100:
            create_obstacle()
            spawn_timer = 0

        # Increase difficulty
        obstacle_speed = min(8, 4 + score // 10)

        # Move traps
        for ob in obstacles:

            ob["x"] -= obstacle_speed

            x = int(ob["x"])
            gap_y = ob["gap_y"]
            gap = ob["gap"]

            # Top trap
            draw_trap(x, 0, 75, gap_y - gap // 2)

            # Bottom trap
            bottom_y = gap_y + gap // 2
            draw_trap(
                x, bottom_y,
                75, HEIGHT - bottom_y
            )

            # Collision rectangles
            mouse_rect = pygame.Rect(
                mouse_x - 22, mouse_y - 20, 55, 35
            )

            top_rect = pygame.Rect(
                x, 0, 75, gap_y - gap // 2
            )

            bottom_rect = pygame.Rect(
                x, bottom_y, 75, HEIGHT - bottom_y
            )

            if mouse_rect.colliderect(top_rect) or \
               mouse_rect.colliderect(bottom_rect):
                game_over = True

            # Score
            if not ob["passed"] and x + 75 < mouse_x:
                score += 1
                ob["passed"] = True

        # Remove old obstacles
        obstacles = [
            ob for ob in obstacles
            if ob["x"] > -100
        ]

        # Screen boundaries
        if mouse_y < 0 or mouse_y > HEIGHT:
            game_over = True

    else:

        # Draw existing obstacles while waiting
        for ob in obstacles:

            x = int(ob["x"])
            gap_y = ob["gap_y"]
            gap = ob["gap"]

            draw_trap(x, 0, 75, gap_y - gap // 2)

            bottom_y = gap_y + gap // 2

            draw_trap(
                x, bottom_y, 75,
                HEIGHT - bottom_y
            )

    # Mouse
    draw_mouse(mouse_x, mouse_y)

    # Score
    score_text = font.render(
        f"SCORE: {score}", True, WHITE
    )
    screen.blit(score_text, (20, 20))

    # Start screen
    if not started and not game_over:

        message = font.render(
            "MOUSE ESCAPE!", True, WHITE
        )

        instruction = font.render(
            "CLICK OR PRESS SPACE", True, WHITE
        )

        screen.blit(
            message,
            (WIDTH // 2 - message.get_width() // 2, 210)
        )

        screen.blit(
            instruction,
            (WIDTH // 2 - instruction.get_width() // 2, 260)
        )

    # Game over
    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        title = big_font.render(
            "GAME OVER", True, RED
        )

        final_score = font.render(
            f"YOUR SCORE: {score}", True, WHITE
        )

        restart = font.render(
            "CLICK OR PRESS R TO RESTART", True, WINDOW
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 200)
        )

        screen.blit(
            final_score,
            (WIDTH // 2 - final_score.get_width() // 2, 280)
        )

        screen.blit(
            restart,
            (WIDTH // 2 - restart.get_width() // 2, 350)
        )

    pygame.display.flip()

pygame.quit()
sys.exit()