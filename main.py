import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
gravity = 0.25
bird_movement = 0
bird_jump = -6
pipe_speed = 3
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe_time = pygame.time.get_ticks()

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Load background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load bird image
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (32, 32))
bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT // 2))

# Load pipe images
pipe_surface = pygame.image.load("pipe.png")
pipe_surface = pygame.transform.scale(pipe_surface, (50, 400))
flipped_pipe_surface = pygame.transform.flip(pipe_surface, False, True)

# Pipes list
pipes = []

# Functions
def create_pipe():
    """Creates a new set of pipes (top and bottom)."""
    pipe_height = random.randint(150, SCREEN_HEIGHT - 150 - pipe_gap)
    bottom_pipe = pipe_surface.get_rect(midtop=(SCREEN_WIDTH + 50, pipe_height))
    top_pipe = flipped_pipe_surface.get_rect(midbottom=(SCREEN_WIDTH + 50, pipe_height - pipe_gap))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    """Moves the pipes to the left."""
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    # Remove pipes that are off the screen
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    """Draws the pipes."""
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:  # Bottom pipe
            screen.blit(pipe_surface, pipe)
        else:  # Top pipe
            screen.blit(flipped_pipe_surface, pipe)

def check_collision(pipes):
    """Checks for collisions between the bird and pipes or ground."""
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def display_score(score):
    """Displays the score on the screen."""
    score_surface = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

def reset_game():
    """Resets the game state for a restart."""
    global bird_rect, bird_movement, pipes, score, last_pipe_time, game_active
    bird_rect.center = (100, SCREEN_HEIGHT // 2)
    bird_movement = 0
    pipes.clear()
    score = 0
    last_pipe_time = pygame.time.get_ticks()
    game_active = True

# Game loop
running = True
game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = bird_jump
        if not game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()  # Restart the game

    # Draw background
    screen.blit(background, (0, 0))

    if game_active:
        # Bird mechanics
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_img, bird_rect)

        # Pipes mechanics
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > pipe_frequency:
            pipes.extend(create_pipe())
            last_pipe_time = current_time

        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Collision check
        if check_collision(pipes):
            game_active = False

        # Score update
        for pipe in pipes:
            if pipe.centerx == bird_rect.centerx:
                score += 1

        display_score(int(score))

    else:
        # Display game over screen
        game_over_surface = font.render("Game Over! Press R to Restart", True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
