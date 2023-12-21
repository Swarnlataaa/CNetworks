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
pygame.display.set_caption("Routing Algorithm Visualizer")

# Define router properties
router_radius = 20
router_color = RED

# Define link properties
link_color = WHITE
link_thickness = 2

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    screen.fill(BLACK)

    # Draw routers
    router_a = (width // 4, height // 2)
    router_b = (width // 2, height // 4)
    router_c = (3 * width // 4, height // 2)
    pygame.draw.circle(screen, router_color, router_a, router_radius)
    pygame.draw.circle(screen, router_color, router_b, router_radius)
    pygame.draw.circle(screen, router_color, router_c, router_radius)

    # Draw links
    pygame.draw.line(screen, link_color, router_a, router_b, link_thickness)
    pygame.draw.line(screen, link_color, router_b, router_c, link_thickness)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
