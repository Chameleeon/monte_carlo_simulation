import random
import time
import threading
try:
    import pygame
except ImportError:
    print("Pygame is not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "pygame"])
    import pygame
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("MatPlotLib is not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
try:
    import numpy as np
except ImportError:
    print("NumPy is not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "numpy"])
    import numpy as np
try:
    import sympy as sp
except ImportError:
    print("SymPy is not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "sympy"])
    import sympy as sp

class MonteCarlo:

    def __init__(self, window, sim_type: str, circle_radius: int):
        pygame.init()
        self.screen = pygame.display.set_mode((window[0], window[1]), pygame.FULLSCREEN)
        self.screen.fill("Grey10")
        pygame.display.set_caption("Monte Carlo Pi Calculation")
        pygame.time.Clock().tick(1)
        pygame.display.flip()
        self.font_small = pygame.font.Font(None, 40)
        self.points = 0
        self.width = circle_radius*2
        self.height = circle_radius*2
        self.points_in_circle = 0
        self.total_points = 0
        self.pi = 0.0
        self.actual_pi = 0.0
        self.sim_type = sim_type
        self.precision = 0
        self.window = window
        self.fast_mode = False
        self.display_title()
        self.display_square(100)
        self.draw_line()
        self.display_multiplication()
        self.display_number_of_red()
        self.display_total_number()
        pygame.display.update()

    def display_title(self):
        self.font = pygame.font.SysFont("arial", 45)
        self.title_surface = self.font.render("Monte Carlo Pi Calculation", True, "White")
        text_rect = self.title_surface.get_rect(center=(self.window[0]/2, 50))
        self.screen.blit(self.title_surface, text_rect)

    def display_number_of_red(self):
        subtitle = self.font_small.render(f"100000000", True, (224, 72, 52))
        subtitle_rect = subtitle.get_rect(center = (930, 830))
        subtitle.fill("Grey10")
        self.screen.blit(subtitle, subtitle_rect)
        subtitle = self.font_small.render(str(self.points_in_circle), True, (224, 72, 52))
        self.screen.blit(subtitle, subtitle_rect)
        
    def display_total_number(self):
        subtitle = self.font_small.render(f"100000000", True, "Green")
        subtitle_rect = subtitle.get_rect(center = (930, 870))
        subtitle.fill("Grey10")
        self.screen.blit(subtitle,subtitle_rect)
        subtitle = self.font_small.render(str(self.total_points), True, "Green")
        self.screen.blit(subtitle,subtitle_rect)

    def display_square(self, circle_radius):
        pygame.draw.rect(self.screen, "White", (((self.window[0]-self.width)/2)-2, 98, ((circle_radius)*6+4),(circle_radius)*6+4), 2)

    def display_multiplication(self):
        mult = self.font_small.render( "4 *", True, "White")
        mult_rect = mult.get_rect(center = (770, 850))
        self.screen.blit(mult,mult_rect)

    def draw_line(self):
        line = pygame.draw.line(self.screen, "White", (800,850), (1000,850), 2)

    def display_pi(self):
        subtitle = self.font_small.render(f" = 3.0000000000000000  ", True, "Grey10")
        subtitle_rect = subtitle.get_rect(center = (1140, 850))
        subtitle.fill("Grey10")
        self.screen.blit(subtitle,subtitle_rect)
        subtitle = self.font_small.render(f" = {self.pi}  ", True, "White")
        self.screen.blit(subtitle,subtitle_rect)
        
    def display_pi_real(self):
        subtitle = self.font_small.render(f" = 3.0000000000000000  ", True, "Grey10")
        subtitle_rect = subtitle.get_rect(center = (920, 950))
        subtitle.fill("Grey10")
        self.screen.blit(subtitle,subtitle_rect)
        subtitle = self.font_small.render(f"Actual Value of PI: {self.actual_pi}  ", True, "White")
        self.screen.blit(subtitle,subtitle_rect)

    def loop(self):
        sim_thread = None
       
        if self.sim_type == "count":
            sim_thread = threading.Thread(target=self.calculate_pi, args=(self.points,))
            sim_thread.start()
        elif self.sim_type == "precise":
            sim_thread = threading.Thread(target=self.calculate_pi_precise, args=(self.precision,))
            sim_thread.start()
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            self.display_total_number()
            self.display_number_of_red()
            self.display_pi()
            pygame.display.update()

    def generate_point(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        return (x,y)

    def is_point_in_circle(self,point):
        x = point[0] - self.width/2
        y = point[1] - self.width/2
        if x * x + y * y <= (self.width/2) * (self.height/2):
            return True
        else:
            return False

    def calculate_pi(self, points: int):
        self.points_in_circle = 0
        for i in range(1,points+1):
            self.total_points = i
            x = random.uniform(-1,1)
            y = random.uniform(-1,1)
            self.draw(((x + 1) * self.width/2,(y + 1) * self.width/2))
            if (x**2 + y**2) < 1:
                self.points_in_circle += 1
            self.pi = self.points_in_circle*4/self.total_points
            if not self.fast_mode:
                time.sleep(0.0005)

        
    def draw(self,point):
        circle_surface= pygame.Surface((2,2))
        if self.is_point_in_circle(point):
            circle_surface.fill((224,72,52))
        else:
            circle_surface.fill("Green")
        self.screen.blit(circle_surface,(((self.window[0]-self.width)/2)+point[0],100+point[1]) )

    def calculate_pi_precise(self, precision_places: int):
        pi_value = sp.N(sp.pi, )
        self.actual_pi = pi_value
        self.display_pi_real()
        self.points_in_circle = 0
        self.total_points = 0
        while True:
            x = random.uniform(-1,1)
            y = random.uniform(-1,1)
            self.draw(((x + 1) * self.width/2,(y + 1) * self.width/2))
            self.total_points += 1
            if (x**2 + y**2) < 1:
                self.points_in_circle += 1
            self.pi = 4 * self.points_in_circle / self.total_points
            
            decimal_part1 = str(pi_value)[2:] 
            decimal_part2 = str(self.pi)[2:] 

            count = 0
            for d1, d2 in zip(decimal_part1, decimal_part2):
                if d1 != d2:
                    break
                count +=1
                if count == precision_places:
                    break

            if count == precision_places:
                print(f"random_values: {self.total_points}")
                break
        
            if not self.fast_mode:
                time.sleep(0.0005)
        print(f"Real value: {pi_value}\nCalculated value: {self.pi}")

