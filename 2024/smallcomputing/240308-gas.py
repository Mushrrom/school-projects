import sys, pygame
import random
# If two particles ever do randomly stick together thats simulating covalent bonding


# Boring is whether or not to fix the funny combined particles bug (feature)
# If you want to see a non janky experience set this to true
# If you want to see what it looks like set to true and restart the program
# until you see two particles stuck together 
BORING = True


pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WALL_WIDTH = 10

#Colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#canvas declaration
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bouncing particle')

class Particle:
    def __init__(self, color: tuple = None):
        self.size = random.randint(10, 30)
        self.x = random.randint(WALL_WIDTH+self.size, SCREEN_WIDTH - WALL_WIDTH-self.size)
        self.y = random.randint(WALL_WIDTH+self.size, SCREEN_HEIGHT - WALL_WIDTH-self.size)

        self.vx = random.randint(3, 5)
        self.vy = random.randint(3, 5)

        # Set the initial direction of the particle in radians
        self.velocity = random.randint(5, 15)
        self.color = random.choice([BLUE, WHITE, RED, GREEN, BLUE, YELLOW]) if not color else color

    def move(self, particles: list):
        self.x += self.vx
        self.y += self.vy

        if self.x <  WALL_WIDTH + self.size:
            self.x = WALL_WIDTH + self.size
            self.vx = -self.vx

        elif self.x > SCREEN_WIDTH - WALL_WIDTH - self.size:
            self.x = SCREEN_WIDTH - WALL_WIDTH - self.size
            self.vx = -self.vx

        if self.y < WALL_WIDTH + self.size:
            self.y = WALL_WIDTH + self.size
            self.vy = -self.vy

        elif self.y > SCREEN_HEIGHT - WALL_WIDTH - self.size:
            self.y = SCREEN_HEIGHT - WALL_WIDTH - self.size
            self.vy = -self.vy
        
        selfVector = pygame.math.Vector2(self.x, self.y)
        for p in particles:
            pVector = pygame.math.Vector2(p.x, p.y)
            # This uses the vector of the other particle to find the distance to the 
            # particle from the centre of the self particle. This is done by checking 
            # whether the location of the p vector is less than the size of self plus the
            # size of the other particle. (the pVector returns a location in this example)
            # print(pVector)
            # print(pVector.magnitude())
            if pVector.distance_squared_to(selfVector) < (self.size + p.size)**2:
                # print("hit")
                netVector = selfVector - pVector
                # This part just reverses both of the vectors based on the directon they were collided
                # with from - a colission from the bottom will make the particle move up and one from 
                # the side will cause it to move sideways
                selfVelVector = pygame.math.Vector2(self.vx, self.vy).reflect(netVector)
                pVelVector = pygame.math.Vector2(p.vx, p.vy).reflect(netVector)
                # print(selfVelVector.x)
                self.vx, self.vy = float(selfVelVector.x), float(selfVelVector.y)
                p.vx, p.vy = pVelVector.x, pVelVector.y



    def draw(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.size, 0)


def drawWalls():
    pygame.draw.line(screen, GREEN, [0, 0], [SCREEN_WIDTH, 0], WALL_WIDTH)
    pygame.draw.line(screen, GREEN, [0, 0], [0, SCREEN_HEIGHT], WALL_WIDTH)
    pygame.draw.line(screen, GREEN, [SCREEN_WIDTH, 0], [SCREEN_WIDTH, SCREEN_HEIGHT], WALL_WIDTH)
    pygame.draw.line(screen, GREEN, [0, SCREEN_HEIGHT], [SCREEN_WIDTH, SCREEN_HEIGHT], WALL_WIDTH)



amnt = 10 # amount of particles
particles = [Particle() for _ in range(amnt)]




# Fix funny glitch :(
if BORING:
    c1 = 0
    while c1 < amnt-1:
        c1 += 1
        for c2 in range(amnt):
            if c1 == c2: continue
            p1Vector = pygame.math.Vector2(particles[c1].x, particles[c1].y)
            p2Vector = pygame.math.Vector2(particles[c2].x, particles[c2].y)
            if p1Vector.distance_squared_to(p2Vector) < (particles[c1].size + particles[c2].size)**2:
                print("a")
                particles[c2].x = random.randint(WALL_WIDTH+particles[c2].size, SCREEN_WIDTH - WALL_WIDTH-particles[c2].size)
                particles[c2].y = random.randint(WALL_WIDTH+particles[c2].size, SCREEN_HEIGHT - WALL_WIDTH-particles[c2].size)
                c1 = -1

        




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    drawWalls()

    particles2 = particles[:]
    for particle in particles:
        particles2.pop(0)
        particle.move(particles2)
        particle.draw()
    
    pygame.display.update()
    fpsClock.tick(FPS)


# 798c6429b633eac7b01cdc69e32d6cca7ccedf5129d490c184de3c5ea1b21712
# 798c64e507a34eb868233ba043d58e8352c8ef7be54e54ac0f800c9d87b21712