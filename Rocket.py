import pygame
import time
import random
import math
import tkinter as tk

class Rocket:
    def __init__(self, moves, rect, winFitness=0.6, movementRange=(-3,3)):
        self.fitness = 0
        self.rect = rect.copy()
        self.isAlive = True
        self.startingRect = rect.copy()
        self.win = False
        self.turns = moves
        self.winFitness = winFitness
        self.movementRange = movementRange
        self.moves = []
        self.randomWays(moves)

    def reset(self, rect):
        self.fitness = 0
        self.rect = rect.copy()
        self.isAlive = True
        self.startingRect = rect.copy()
        self.win = False
        self.turns = len(self.moves)

    def move(self, index):
        self.rect[0] += self.moves[index][0]
        self.rect[1] += self.moves[index][1]

    def getDistance(self, target):
        if self.isAlive:
            return math.sqrt((self.rect[0] - target[0])**2 + (self.rect[1] - target[1])**2)
        return 99999

    def calcFitness(self, target, originalDistnace):
        score = 0
        distance = math.sqrt((self.rect[0] - target[0])**2 + (self.rect[1] - target[1])**2)
        if distance < float(originalDistnace) and self.isAlive:
            if self.win:
                self.fitness = self.winFitness + ((((len(self.moves) - self.turns) / len(self.moves))) * (1 - self.winFitness))
            else:
                self.fitness = ((((originalDistnace - distance) / originalDistnace) ** 2) * self.winFitness)
        else:
            self.fitness = 0
        
        return self.fitness

    def crossOver(self, partner):
        child = Rocket(len(self.moves), self.startingRect, self.winFitness, self.movementRange)
        midPoint = random.randint(0, len(self.moves))
        child.moves = self.moves[:midPoint] + partner.moves[midPoint:]
        
        return child

    def mutation(self, mutationRate):
        for i in range(len(self.moves)):
            if random.random() <= mutationRate:
                self.moves[i] = self.generatePoint()

    def generatePoint(self):
        return (random.randint(self.movementRange[0], self.movementRange[1]),random.randint(self.movementRange[0], self.movementRange[1]))

    def randomWays(self, length):
        self.moves = []
        for i in range(length):
            self.moves.append(self.generatePoint())