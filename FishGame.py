import pygame
import random
import math

# Initializing Pygame
pygame.init()
width = 500
height = 750

# Start fisherman at the bottom center
x = width // 2 - 75
y = height - 150

# Initializing surface
surface = pygame.display.set_mode((width, height))
background = pygame.image.load("assests/water.png")
background = pygame.transform.scale(background, (width, height))

facing_left = False
fisherman_sprite = pygame.image.load("assests/fisherman.png").convert_alpha()
fisherman_sprite = pygame.transform.scale(fisherman_sprite, (150, 150))

fish_sprite = pygame.image.load("assests/fish.png").convert_alpha()
fish_sprite = pygame.transform.scale(fish_sprite, (100, 100))

shark_sprite = pygame.image.load("assests/shark.png").convert_alpha()
shark_sprite = pygame.transform.scale(shark_sprite, (100, 100))

speed = 4
fall_speed = 3  # Speed of falling objects
score = 0  # Score counter
high_score = 0  # High score tracker
lives = 3  # Number of lives
font = pygame.font.Font(None, 36)

def start_screen():
    button_rect = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 50)
    while True:
        surface.blit(background, (0, 0))
        pygame.draw.rect(surface, (0, 0, 128), button_rect, border_radius=10)
        title_text = font.render("Fish Game", True, (255, 255, 255))
        instruction_text = font.render("Start", True, (255, 255, 255))
        surface.blit(title_text, (width // 2 - 50, height // 2 - 100))
        surface.blit(instruction_text, (width // 2 - 30, height // 2 - 40))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                return

def restart_screen():
    global high_score
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
    
    # Update high score if current score is higher
    if score > high_score:
        high_score = score
    
    while True:
        surface.blit(background, (0, 0))
        pygame.draw.rect(surface, (0, 0, 128), button_rect, border_radius=10)
        
        # Create text surfaces
        title_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        instruction_text = font.render("Restart", True, (255, 255, 255))
        
        # Get text dimensions for centering
        title_width = title_text.get_width()
        score_width = score_text.get_width()
        high_score_width = high_score_text.get_width()
        
        # Draw centered text
        surface.blit(title_text, (width // 2 - title_width // 2, height // 2 - 150))
        surface.blit(score_text, (width // 2 - score_width // 2, height // 2 - 100))
        surface.blit(high_score_text, (width // 2 - high_score_width // 2, height // 2 - 50))
        surface.blit(instruction_text, (width // 2 - 30, height // 2 + 60))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                return True
            if event.type == pygame.QUIT:
                return False

def move_shark_towards_fisherman(shark_x, shark_y, fisherman_x, fisherman_y, speed):
    dx = fisherman_x - shark_x
    dy = fisherman_y - shark_y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance != 0:
        dx /= distance
        dy /= distance
    
    shark_x += dx * speed
    shark_y += dy * speed
    
    return shark_x, shark_y

def reset_game():
    global x, y, score, lives, fish_x, fish_y, shark_x, shark_y, shark_off_screen
    x = width // 2 - 75
    y = height - 150
    score = 0
    lives = 3
    fish_x = random.randint(0, width - 100)
    fish_y = -100
    shark_x = random.randint(0, width - 150)
    shark_y = -200
    shark_off_screen = False

start_screen()

# Initial positions of fish and shark
fish_x = random.randint(0, width - 100)
fish_y = -100
shark_x = random.randint(0, width - 150)
shark_y = -200
shark_off_screen = False

running = True
while running:
    surface.blit(background, (0, 0))
    surface.blit(fisherman_sprite, (x, y))
    surface.blit(fish_sprite, (fish_x, fish_y))
    surface.blit(shark_sprite, (shark_x, shark_y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not facing_left:
            fisherman_sprite = pygame.transform.flip(fisherman_sprite, True, False)
            facing_left = True
        if x - speed > 0:
            x -= speed

    if keys[pygame.K_RIGHT]:
        if facing_left:
            fisherman_sprite = pygame.transform.flip(fisherman_sprite, True, False)
            facing_left = False
        if x + speed < width - 150:
            x += speed

    if keys[pygame.K_UP]:
        if y - speed > 0:
            y -= speed
    if keys[pygame.K_DOWN]:
        if y + speed < height - 150:
            y += speed

    # Update falling objects
    fish_y += fall_speed
    shark_y += fall_speed

    # Check if shark goes off the screen
    if shark_y > height:
        shark_x = random.randint(0, width - 150)
        shark_y = -150
        shark_off_screen = True

    # Move the shark toward the fisherman
    shark_x, shark_y = move_shark_towards_fisherman(shark_x, shark_y, x, y, 0.5)

    # Check for shark collision
    if (x < shark_x + 150 and x + 150 > shark_x and 
        y < shark_y + 150 and y + 150 > shark_y):
        lives -= 1
        # Reset shark position after collision
        shark_x = random.randint(0, width - 150)
        shark_y = -150
        shark_off_screen = True
        
        if lives <= 0:
            if restart_screen():
                reset_game()
            else:
                running = False
                break

    # Check for fish collision
    if fish_y > height or (x < fish_x + 100 and x + 150 > fish_x and 
                          y < fish_y + 100 and y + 150 > fish_y):
        if y < fish_y + 100 and y + 150 > fish_y:
            score += 1
        fish_x = random.randint(0, width - 100)
        fish_y = -100

    # Render score and lives
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    surface.blit(score_text, (10, 10))
    surface.blit(lives_text, (10, 50))
    surface.blit(high_score_text, (width - 150, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()