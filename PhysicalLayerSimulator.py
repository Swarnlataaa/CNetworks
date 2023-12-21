import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physical Layer Simulator")

# Set up devices
device_radius = 20
device_x = width // 4
device_y = height // 2
device_color = RED

# Set up cables
cable_color = WHITE
cable_thickness = 5

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    screen.fill(BLACK)

    # Draw device
    pygame.draw.circle(screen, device_color, (device_x, device_y), device_radius)

    # Draw cable
    pygame.draw.line(screen, cable_color, (device_x + device_radius, device_y), (width - device_x - device_radius, device_y), cable_thickness)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
