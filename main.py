import pygame


W, H = 720, 480

screen = pygame.display.set_mode((W, H))

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == pygame.KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == pygame.K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == pygame.QUIT:
            running = False


pygame.init()