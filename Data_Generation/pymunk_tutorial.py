import pygame
import pymunk
from moviepy.editor import ImageSequenceClip

# Initialize Pygame and Pymunk
pygame.init()
display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -1000)  # Gravity in Pymunk is in the negative y direction
FPS = 50

def convert_corrdinates(point): 
    """Convert Pymunk coordinates to Pygame coordinates."""
    return int(point.x), int(800 - point.y)


# body and shape
body = pymunk.Body()
# body.position = (200, 400)
body.position = (0, 300)
shape = pymunk.Circle(body, 10)
shape.density = 1
space.add(body, shape)

segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0, 300), (800, 0), 5)
space.add(segment_body, segment_shape)
flat_segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
flat_segment_shape = pymunk.Segment(flat_segment_body, (0, 150), (800, 150), 5)

space.add(flat_segment_body, flat_segment_shape)

def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        display.fill((255, 255, 255))
        x, y = convert_corrdinates(body.position)
        pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), 10)
        pygame.draw.line(display, (0, 0, 0), (0, 500), (400, 650), 5)
        pygame.draw.line(display, (0, 0, 0), (400, 650), (800, 650), 5)
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()
pygame.quit()