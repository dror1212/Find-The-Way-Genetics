import pygame
import time
import random
import math
import tkinter as tk
from Population import Population

if __name__ == '__main__':
    population = 1400
    moves = 1800
    mutationRate = 0.01
    survivelRate = 0.2
    population = Population(mutationRate,population,moves,survivelRate)
    while not population.isFinished:
        population.display()
        population.calcFitness()
        population.naturalSelection()
        print(population.getBest())
        if population.isFinished:
            break
        population.generate()
        
    pygame.quit()

