# Generador que trae Python (random), para compararlo con el que trae Java
import random


class GeneradorNativo:
    def __init__(self, semilla):
        self.azar = random.Random(semilla)

    def siguiente(self):
        # Devuelve el siguiente número entre 0 y 1
        return self.azar.random()
