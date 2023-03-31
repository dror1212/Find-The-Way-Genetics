import pygame
import time
import random
import math
import tkinter as tk

class Rocket:
    def __init__(self, moves):
        self.moves = randomWays(moves)
        self.fitness = 0
        self.rect = [240, 400, 12, 12]
        self.isAlive = True
        self.startingRect = [240, 400, 12, 12]
        self.win = False
        self.turns = moves

    def move(self, index):
        self.rect[0] += self.moves[index][0]
        self.rect[1] += self.moves[index][1]

    def getDistance(self, target):
        if self.isAlive:
            return math.sqrt((self.rect[0] - target[0])**2 + (self.rect[1] - target[1])**2)
        return 99999

    def calcFitness(self, target,originalDistnace):
        score = 0
        distance = math.sqrt((self.rect[0] - target[0])**2 + (self.rect[1] - target[1])**2)
        if distance < float(originalDistnace) and self.isAlive:
            if self.win:
                self.fitness = 0.6 + ((((len(self.moves) - self.turns) / len(self.moves))) * 0.4)
            else:
                self.fitness = ((((originalDistnace - distance) / originalDistnace)) ** ((((originalDistnace - distance) / originalDistnace) / 0.2)+1) * 0.6)
        else:
            self.fitness = 0
        
        return self.fitness

    def crossOver(self, partner):
        child = Rocket(len(self.moves))
        midPoint = random.randint(0, len(self.moves))
        child.moves = self.moves[:midPoint] + partner.moves[midPoint:]
        
        return child

    def mutation(self, mutationRate):
        for i in range(len(self.moves)):
            if random.random() <= mutationRate:
                self.moves[i] = generatePoint()

def generatePoint():
    return (random.randint(-3,3),random.randint(-3,3))

def randomWays(length):
    moves = []
    for i in range(length):
        moves.append(generatePoint())
    return moves
