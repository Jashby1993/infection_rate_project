import pygame, sys
import numpy as np

BLACK = (0,0,0)
WHITE = (255,255,255)
OFFWHITE = (243,240,186)
BLUE = (19,51,163)
PURPLE = (158,42,103)
GREEN = (35,248,42)
RED = (166,16,18)
ORANGE = (211,81,11)

#dot colors
VULNERABLE = BLUE
INFECTED = ORANGE
RECOVERED = PURPLE

BACKGROUND = OFFWHITE


class Dot(pygame.sprite.Sprite):
    def __init__(
            self,
            x,
            y,
            width,
            height,
            color = BLACK,
            radius = 5,
            velocity = [0,0],
    ):
        super().__init__()
        self.image = pygame.Surface(
            [radius * 2, radius * 2])
        self.image.fill(BACKGROUND)
        pygame.draw.circle(
            self.image, color ,(radius, radius), radius
        )

        self.rect = self.image.get_rect()
        self.pos = np.array([x,y], dtype = np.float64)
        self.vel = np.asarray(velocity, dtype=np.float64)

        self.killswitch_on = False
        self.recovered = False

        self.WIDTH = width
        self.HEIGHT = height
    def update(self):
        self.pos += self.vel
        x,y = self.pos

        if x < 0:
            self.pos[0] = self.WIDTH
            x = self.WIDTH
        if x > self.WIDTH:
            self.pos[0] = 0
            x = 0
        if y < 0:
            self.pos[1] = self.HEIGHT
            y = self.HEIGHT
        if y > self.HEIGHT:
            self.pos[1] = 0
            y = 0
        self.rect.x = x
        self.rect.y = y
        if self.killswitch_on:
            self.cycles_to_fate -= 1
            if self.cycles_to_fate == 0:
                self.killswitch = False
                some_number = np.random.rand()
                if self.mortality_rate >= some_number:
                    #this removes the sprite. may want to "respawn" as a motionless grey dot instead
                    self.kill()
                else:
                    self.recovered = True

    def respawn(self, color, radius = 5):
        return Dot(
            self.rect.x,
            self.rect.y,
            self.WIDTH,
            self.HEIGHT,
            color = color,
            velocity = self.vel,            
        )

    def killswitch(self, cycles_to_fate = 150, mortality_rate = .2):
        self.killswitch_on = True
        self.cycles_to_fate = cycles_to_fate
        self.mortality_rate = mortality_rate

class Simulation:
    def __init__(self, width = 600, height = 400):
        self.WIDTH = width
        self.HEIGHT = height
        self.vulnerable_container = pygame.sprite.Group()
        self.infected_container = pygame.sprite.Group()
        self.recovered_container = pygame.sprite.Group()
        self.dead_container = pygame.sprite.Group()
        self.all_container = pygame.sprite.Group()
#starting dudes
        self.n_vulnerable = 20
        self.n_infected = 1
        #self.n_infected.killswitch()


        self.T = 1000
        self.cycles_to_fate = 20
        self.mortality_rate = .2

    def start(self):
        self.N = self.n_vulnerable + self.n_infected
        pygame.init()
        screen = pygame.display.set_mode(   [ self.WIDTH, self.HEIGHT])
        #adding vulnerable dudes
        for i in range(self.n_vulnerable):
            x = np.random.randint(0,self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1

            dude = Dot(x, y, self.WIDTH, self.HEIGHT, color = VULNERABLE, velocity = vel)
            self.vulnerable_container.add(dude)
            self.all_container.add(dude)
            #adding infected dudes
        for i in range(self.n_infected):
            x = np.random.randint(0,self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1

            dude = Dot(x, y, self.WIDTH, self.HEIGHT, color = INFECTED, velocity = vel)
            self.infected_container.add(dude)
            self.all_container.add(dude)
        clock = pygame.time.Clock()
        for i in range(self.T):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.all_container.update()
            screen.fill(BACKGROUND)

            #new infections ? 
            #problem for another time: new infecteds reverse velocity, original infecteds don't
            collision_group = pygame.sprite.groupcollide(
                self.vulnerable_container,
                self.infected_container,
                True,
                False,
            )
            for dude in collision_group:
                new_dude = dude.respawn(INFECTED)
                new_dude.vel *= -1
                #recover or die
                new_dude.killswitch(
                    self.cycles_to_fate, self.mortality_rate
                )
                self.infected_container.add(new_dude)
                self.all_container.add(new_dude)
                
            
            
            #recoveries?
            recovered = []
            for dude in self.infected_container:
               if dude.recovered:
                   new_dude = dude.respawn(RECOVERED)
                   self.recovered_container.add(new_dude)
                   self.all_container.add(new_dude)
                   recovered.append(dude)
            if len(recovered) > 0:
                self.infected_container.remove(*recovered)
                self.all_container.remove(*recovered)

            self.all_container.draw(screen)
            pygame.display.flip()
            clock.tick(60)
        pygame.QUIT()


#starting simulation
if __name__== "__main__":
    infection = Simulation()
    infection.n_vulnerable = 80

    infection.start()

