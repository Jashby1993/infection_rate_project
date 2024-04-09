import pygame, sys
import numpy as np
import tkinter as tk
from tkinter import messagebox

#temp user input
vulnerable = int(input("Pick a starting population betweent 100 and 800: "))
starting_infected = int(input("Pick a number of infected to start with between 1 and 20: "))
infection_rate = float(input("What is the infection rate? Please use a decimal between .60 and .99: "))
mortality_rate = float(input("What is the mortality rate? Please use a decimal between .00 and .25: "))

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
OFFWHITE = (243,240,186)
BLUE = (19,51,163)
PURPLE = (158,42,103)
GREEN = (35,248,42)
RED = (166,16,18)
ORANGE = (211,81,11)
GREY = (178, 190, 181)
HORRIBLE_YELLOW = (190,175,50)

#Setting colors
BACKGROUND = OFFWHITE
VULNERABLE = BLUE
INFECTED = RED
RECOVERED = PURPLE

#CONSTANTS
FPS = 30
clock = pygame.time.Clock()
WIDTH , HEIGHT = 1000,600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))

#population lists
vulnerable_pop = []
infected_pop = []
recovered_pop = []
dead_pop = []

class CircleSprite(pygame.sprite.Sprite):
    def __init__(
            self,
            x,
            y,
            width,
            height,
            color = BLACK,
            radius = 5,
            velocity = [0,0],
            randomize = False
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
        self.randomize = randomize

        self.WIDTH = width
        self.HEIGHT = height
    def update(self):
        self.pos += self.vel
        x, y = self.pos

        if x < 0 or x > self.WIDTH:
            self.vel[0] *= -1  # Reflect horizontally when hitting left or right wall
        if y < 0 or y > self.HEIGHT:
            self.vel[1] *= -1  # Reflect vertically when hitting top or bottom wall

        self.rect.x = x
        self.rect.y = y

        vel_norm = np.linalg.norm(self.vel)
        if  vel_norm > 4:
            self.vel /= vel_norm

        if self.randomize:
            self.vel += np.random.rand(2) * 2 - 1

        if self.killswitch_on:
            self.cycles_to_fate -= 1
            if self.cycles_to_fate == 0:
                self.killswitch = False
                some_number = np.random.rand()
                if self.mortality_rate >= some_number:
                    infected_pop.pop()
                    dead_pop.append(dude)
                    dude.respawn(GREY)
                    self.infected_container.remove(dude)
                    self.dead_container.add(dude)
                    self.all_container.remove(dude)
                    self.all_container.add(dude)
                    self.vel = [0, 0]
                else:
                    self.recovered = True

    def respawn(self, color, radius = 5):
        return CircleSprite(
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
        self.n_vulnerable = vulnerable
        self.n_infected = starting_infected
        self.infection_rate = infection_rate
        self.mortality_rate = mortality_rate

    def start(self, randomize = False):
        self.N = self.n_vulnerable + self.n_infected
        pygame.init()
        self.screen = pygame.display.set_mode(   [ self.WIDTH, self.HEIGHT])
        #adding vulnerable dudes
        for i in range(self.n_vulnerable):
            x = np.random.randint(0,self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1
            dude = dude(x, y, self.WIDTH, self.HEIGHT, color = VULNERABLE, velocity = vel, randomize = randomize)
            self.vulnerable_container.add(dude)
            vulnerable_pop.append(dude)
            self.all_container.add(dude)

            #adding infected dudes
        for i in range(self.n_infected):
            x = np.random.randint(0,self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1

            dude = CircleSprite(x, y, self.WIDTH, self.HEIGHT, color = INFECTED, velocity = vel, randomize = randomize)
            self.infected_container.add(dude)
            infected_pop.append(dude)
            self.all_container.add(dude)
        
        #new infections ? 
            #problem for another time: new infecteds reverse velocity, original infecteds don't
            vulnerable_infected_collision = pygame.sprite.groupcollide(
                self.vulnerable_container,
                self.infected_container,
                True,
                False,
            )
            for dude in vulnerable_infected_collision:
                just_a_number = np.random.rand()
                if just_a_number <= self.infection_rate:
                    new_dude = dude.respawn(INFECTED)
                    new_dude.vel *= -1
                    #recover or die
                    new_dude.killswitch(
                        self.cycles_to_fate, self.mortality_rate
                    )
                    vulnerable_pop.pop()
                    infected_pop.append(dude)
                    self.infected_container.add(new_dude)
                    self.all_container.add(new_dude)
                else:
                    self.vel *= -1
            #handling all other collisions
            vulnerable_vulnerable_collision = pygame.sprite.groupcollide(
                self.vulnerable_container,
                self.vulnerable_container,
                False,
                False,
            )
            for dude in vulnerable_vulnerable_collision:
                self.vel *= 1
            recovered_vulnerable_collision = pygame.sprite.groupcollide(
                self.vulnerable_container,
                self.recovered_container,
                False,
                False,
            )
            for dude in recovered_vulnerable_collision:
                self.vel *= 1
            infected_infected_collision = pygame.sprite.groupcollide(
                self.infected_container,
                self.infected_container,
                False,
                False,
            )
            for dude in infected_infected_collision:
                self.vel *= 1
            recovered_infected_collision = pygame.sprite.groupcollide(
                self.recovered_container,
                self.infected_container,
                False,
                False,
            )
            for dude in recovered_infected_collision:
                self.vel *= 1
            recovered_recovered_collision = pygame.sprite.groupcollide(
                self.recovered_container,
                self.recovered_container,
                False,
                False,
            )
            for dude in recovered_recovered_collision:
                self.vel *= 1
            for dude in self.infected_container:
               if dude.recovered:
                   new_dude = dude.respawn(RECOVERED)
                   self.recovered_container.add(new_dude)
                   self.all_container.add(new_dude)
                   recovered_pop.append(dude)
            if len(recovered_pop) > 0:
                self.infected_container.remove(*recovered_pop)
                self.all_container.remove(*recovered_pop)
            




def create_gui(root):
    
    disease_label = tk.Label(root, text="Disease Name:")
    disease_label.grid(row=0, column=0, padx=5, pady=5)
    disease_entry = tk.Entry(root)
    disease_entry.grid(row=0, column=1, padx=5, pady=5)
    disease_name_info = tk.Label(root, text="(Must contain 5-20 characters)", fg="gray")
    disease_name_info.grid(row=1, column=1, padx=5, sticky='w')

    population_label = tk.Label(root, text="Total Population:")
    population_label.grid(row=2, column=0, padx=5, pady=5)
    population_entry = tk.Entry(root)
    population_entry.grid(row=2, column=1, padx=5, pady=5)
    population_info = tk.Label(root, text="(Must be an integer between 100 and 800)", fg="gray")
    population_info.grid(row=3, column=1, padx=5, sticky='w')

    starting_infected_label = tk.Label(root, text="Starting Infected:")
    starting_infected_label.grid(row=4, column=0, padx=5, pady=5)
    starting_infected_entry = tk.Entry(root)  # Entry field for starting infected
    starting_infected_entry.grid(row=4, column=1, padx=5, pady=5)
    starting_infected_info = tk.Label(root, text="(Must be an integer between 1 and 20)", fg="gray")
    starting_infected_info.grid(row=5, column=1, padx=5, sticky='w')

    infection_rate_label = tk.Label(root, text="Infection Rate:")
    infection_rate_label.grid(row=6, column=0, padx=5, pady=5)
    infection_rate_entry = tk.Entry(root)
    infection_rate_entry.grid(row=6, column=1, padx=5, pady=5)
    infection_rate_info = tk.Label(root, text="(Must be a decimal between 0.50 and 0.9969)", fg="gray")
    infection_rate_info.grid(row=7, column=1, padx=5, sticky='w')

    mortality_rate_label = tk.Label(root, text="Mortality Rate:")
    mortality_rate_label.grid(row=8, column=0, padx=5, pady=5)
    mortality_rate_entry = tk.Entry(root)
    mortality_rate_entry.grid(row=8, column=1, padx=5, pady=5)
    mortality_rate_info = tk.Label(root, text="(Must be a float between 0.00 and 0.25)", fg="gray")
    mortality_rate_info.grid(row=9, column=1, padx=5, sticky='w')

# Create a button to submit the input

    submit_button = tk.Button(root, text="Start Simulation", command=submit)
    submit_button.grid(row=10, column=0, columnspan=2, padx=5, pady=10)
    # Retrieve values entered by the user and add them to the dictionary
    def submit():
        disease_info = {}
        disease_info['disease_name'] = disease_entry.get()
        disease_info['total_population'] = population_entry.get()
        disease_info['starting_infected'] = starting_infected_entry.get()
        disease_info['infection_rate'] = infection_rate_entry.get()
        disease_info['mortality_rate'] = mortality_rate_entry.get()

        # Validate the input values
        try:
            total_population = int(disease_info['total_population'])
            if not (100 <= total_population <= 800):
                raise ValueError("Total population must be between 100 and 800")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

        try:
            starting_infected = int(disease_info['starting_infected'])
            if not (1 <= starting_infected <= 20):
                raise ValueError("Starting infected must be between 1 and 20")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

        try:
            infection_rate = float(disease_info['infection_rate'])
            if not (0.50 <= infection_rate <= 0.9969):
                raise ValueError("Infection rate must be a float between 0.50 and 0.9969")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

        try:
            mortality_rate = float(disease_info['mortality_rate'])
            if not (0.00 <= mortality_rate <= 0.25):
                raise ValueError("Mortality rate must be a float between 0.00 and 0.25")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

        # Return the dictionary
        print(disease_info)
        return disease_info

def main():
    '''root = tk.Tk()
    root.title("Disease Information")
    create_gui(root)
    user_input = create_gui(root)
    print(user_input)
    
    root.mainloop()'''

    



# Run the application
if __name__ == "__main":
    
    main()


