import pygame 
pygame.init()

display = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
FPS = 50
ACCELERATION = 1

class Ball(): 
    def __init__(self): 
        self.y = 200
        self.velocity = 10
    
    def draw(self): 
        pygame.draw.circle(display, (255, 0, 0), (500, self.y), 20)
    
    def move(self): 
        self.velocity += ACCELERATION
        self.y += self.velocity
        if self.y > 400: 
            self.y = 400
            self.velocity = -self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = -self.velocity

def game():

    # crerate a ball object
    ball = Ball()
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        pygame.draw.line(display, (0, 0, 0), (0, 400), (1000, 400), 10) # draw a line
        # pygame.draw.circle(display, (255, 0, 0), (500, 300), 20) # draw a circle
        ball.move()
        ball.draw()
        pygame.display.update()
        clock.tick(FPS)

game()
pygame.quit()