import pygame
 
# Initializing Pygame
pygame.init()
width = 500
height = 750

x = 200
y = 250
# Initializing surface
surface = pygame.display.set_mode((width,height))
background = pygame.image.load("assests/water.png")
background = pygame.transform.scale(background,(width,height))
facing_left = False
fisherman_sprite = pygame.image.load("assests/fisherman.png").convert_alpha()
fisherman_sprite = pygame.transform.scale(fisherman_sprite,(150,150))
speed = 2
# Initializing Color
color = (255,0,0)
while True:
    pygame.display.set_caption("Fish Game")
    surface.blit(background,(0,0))
    surface.blit(fisherman_sprite, (x, y))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not facing_left:  # Only flip if not already facing left
            fisherman_sprite = pygame.transform.flip(fisherman_sprite, True, False)
            facing_left = True
        if x - speed > 0:
            x -= speed  # Move left

    if keys[pygame.K_RIGHT]:
        if facing_left:  # Only flip if not already facing right
            fisherman_sprite = pygame.transform.flip(fisherman_sprite, True, False)
            facing_left = False
        if x + speed < width - 150:
            x += speed  # Move right

    if keys[pygame.K_UP]:
        if(y - speed > 0):
            y -= speed  # Move up
    if keys[pygame.K_DOWN]:
        if(y + speed < height - 150):
            y += speed  # Move down

    #Draw sprite
    

    surface.blit(fisherman_sprite, (x, y))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  