import pygame
import random
import math
import sys
import tkinter as tk
from Rocket import Rocket

class Population:
    def __init__(self, mutationRate, popmax, moves, survivelRate, target=(250,50), screen=(500, 500), charecter=[240, 400, 12, 12], deathZones=[[150, 200, 200, 25]]):
        self.target = target
        self.survivelRate = survivelRate
        self.mutationRate = mutationRate
        self.popmax = popmax
        self.amount = popmax
        self.matingPool = []
        self.charecter = charecter
        self.population = [Rocket(moves, self.charecter) for rand in range(popmax)]
        self.geneartion = 1
        self.isFinished = False
        self.fitnessSum = 0
        self.originalDistance = math.sqrt((self.population[0].rect[0] - self.target[0])**2 + (self.population[0].rect[1] - self.target[1])**2)
        pygame.init()
        self.screen = pygame.display.set_mode(screen)
        self.deathZoneColor=(255,0,0)
        self.deathZones = []
        for deathZone in deathZones:
            self.deathZones.append(pygame.draw.rect(self.screen, self.deathZoneColor, deathZone))
        self.targetColor=(0,0,255)
        self.endPoint = pygame.draw.circle(self.screen, self.targetColor, self.target, 10)
        self.charecterColor=(255,255,255)
        self.bestColor=(0,255,0)
        
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.population.sort(key = lambda rocket : rocket.getDistance(self.target))
            for rocket in self.population:
                if rocket.isAlive and not rocket.win:
                    rocket.move(i)

            self.screen.fill((255, 255, 255))
            counter = self.popmax - 1
            for rocket in self.population[::-1]:
                color = (0,0,0)
                if counter == 0:
                    color = self.bestColor
                if counter > self.amount:
                    color = self.charecterColor
                currRect = pygame.draw.rect(self.screen, color, rocket.rect)
                for deathZone in self.deathZones:
                    if currRect.colliderect(deathZone):
                        rocket.isAlive = False
                if currRect.colliderect(self.endPoint) and not rocket.win:
                    rocket.win = True
                    rocket.turns = i
                counter -=1
            
            for deathZone in self.deathZones:
                pygame.draw.rect(self.screen, self.deathZoneColor, deathZone)
            self.endPoint = pygame.draw.circle(self.screen, self.targetColor, self.target, 10)
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

        for i in range(len(newPopulation)):
            newPopulation[i].reset(self.charecter)

        for i in range(int(len(self.population) * (1 - self.survivelRate))):
            first = random.choice(self.matingPool)
            second = random.choice(self.matingPool)
            child = first.crossOver(second)
            child.mutation(self.mutationRate)
            newPopulation.append(child)

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
            
        return ("score: " + str(best.fitness) + " movements: " + str(best.turns))
