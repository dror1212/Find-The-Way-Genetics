import pygame
import random
import math
import tkinter as tk
from Rocket import Rocket

class Population:
    def __init__(self, mutationRate, popmax,moves, survivelRate, target):
        self.target = target
        self.survivelRate = survivelRate
        self.mutationRate = mutationRate
        self.popmax = popmax
        self.amount = popmax
        self.matingPool = []
        self.population = [Rocket(moves) for rand in range(popmax)]
        self.geneartion = 1
        self.isFinished = False
        self.fitnessSum = 0
        self.originalDistance = math.sqrt((self.population[0].rect[0] - self.target[0])**2 + (self.population[0].rect[1] - self.target[1])**2)
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.deathZone = pygame.draw.rect(self.screen, (255,0,0), [150, 200, 200, 25])
        self.endPoint = pygame.draw.circle(self.screen, (0,0,255), self.target, 10)
        self.font = pygame.font.Font('freesansbold.ttf', 26)
        
        self.master = tk.Tk()
        tk.Label(self.master, text="Amount to see").grid(row=0)
        self.e1 = tk.Entry(self.master)
        self.e1.grid(row=0, column=1)
        tk.Button(self.master, 
          text='Show', command=self.setAmount).grid(row=3, 
                                                column=1, 
                                                sticky=tk.W, 
                                                pady=4)
        
    def setAmount(self):
        try:
            self.amount = int(self.e1.get())
        except:
            print("Number only")

        
    def display(self):
        self.master.update_idletasks()
        self.master.update()
        for i in range(len(self.population[0].moves)):
            self.population.sort(key = lambda rocket : rocket.getDistance(self.target))
            for event in pygame.event.get():
                pass
            for rocket in self.population:
                if rocket.isAlive and not rocket.win:
                    rocket.move(i)

            self.screen.fill((255, 255, 255))
            counter = self.popmax - 1
            for rocket in self.population[::-1]:
                color = (0,0,0)
                if counter == 0:
                    color = (0,255,0)
                if counter > self.amount:
                    color = (255,255,255)
                currRect = pygame.draw.rect(self.screen, color, rocket.rect)
                    
                if currRect.colliderect(self.deathZone):
                    rocket.isAlive = False
                if currRect.colliderect(self.endPoint) and not rocket.win:
                    rocket.win = True
                    rocket.turns = i
                counter -=1
                    
            pygame.draw.rect(self.screen, (255,0,0), [150, 200, 200, 25])
            self.endPoint = pygame.draw.circle(self.screen, (0,0,255), self.target, 10)
            text = self.font.render('Generation: ' + str(self.geneartion), True, (255,255,255), (0,0,0)) 
            textRect = text.get_rect()  
            self.screen.blit(text, textRect) 

            pygame.display.flip()
            pygame.display.update()
            self.master.update_idletasks()
            self.master.update()

    def calcFitness(self):
        self.fitnessSum = 0
        for pop in self.population:
            if pop.isAlive:
                self.fitnessSum += pop.calcFitness(self.target,self.originalDistance)
            else:
                pop.fitness = 0

    def naturalSelection(self):
        self.matingPool = []

        for pop in self.population:
            if pop.fitness > 0:
                n = int((self.popmax - self.fitnessSum / pop.fitness))
                for a in range(n):
                    self.matingPool.append(pop)

    def generate(self):
        self.population.sort(key = lambda rocket : rocket.fitness, reverse=True)
        newPopulation = self.population[:int(self.survivelRate * len(self.population))]

        for i in range(int(len(self.population) * (1 - self.survivelRate))):
            first = random.choice(self.matingPool)
            second = random.choice(self.matingPool)
            child = first.crossOver(second)
            child.mutation(self.mutationRate)
            newPopulation.append(child)
            
        for i in range(int(len(self.population) * (self.survivelRate))):
            newPopulation[i].rect = [240, 400, 12, 12]
            newPopulation[i].turns = len(newPopulation[i].moves)
            newPopulation[i].win = False

        self.population = newPopulation
        self.geneartion = self.geneartion + 1

    def getBest(self):
        record = 0
        best = self.population[0]

        for pop in self.population:
            if pop.fitness > record:
                record = pop.fitness
                best = pop
                
        bestRect = pygame.draw.rect(self.screen, (0,0,0), best.rect)
            
        return (str(best.fitness) + " " + str(best.turns))

def forSort(rocket):
    return rocket.fitness
    
