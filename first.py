import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the fonts
font = pygame.font.Font(None, 36)

# Set up the player
player_pos = [WIDTH // 2, HEIGHT - 50]
player_size = [100, 20]
player_speed = 10

# Set up the ball
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_size = [20, 20]
ball_speed = [random.randint(-5, 5), -random.randint(1, 5)]

# Function to draw the player
def draw_player():
    pygame.draw.rect(screen, WHITE, (*player_pos, *player_size))

# Function to draw the ball
def draw_ball():
    pygame.draw.ellipse(screen, WHITE, (*ball_pos, *ball_size))

# Function to move the player
def move_player():
    global player_pos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if player_pos[0] < 0:
        player_pos[0] = 0
    if player_pos[0] + player_size[0] > WIDTH:
        player_pos[0] = WIDTH - player_size[0]

# Function to move the ball
def move_ball():
    global ball_pos, ball_speed
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]
    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball_pos[0] <= 0 or ball_pos[0] + ball_size[0] >= WIDTH:
        ball_speed[0] = -ball_speed[0]

# Function to detect collisions
def detect_collision():
    ball_rect = pygame.Rect(*ball_pos, *ball_size)
    player_rect = pygame.Rect(*player_pos, *player_size)
    if ball_rect.colliderect(player_rect):
        ball_speed[0] = -ball_speed[0]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the screen
    screen.fill(BLACK)
    draw_player()
    draw_ball()

    # Move the player and ball
    move_player()
    move_ball()

    # Detect and handle collisions
    detect_collision()

    # Update the display
    pygame.display.flip()
