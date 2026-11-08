# Una configuración del generador: nombre y parámetros del LCG

class Configuracion:
    def __init__(self, nombre, a, c, m, semilla):
        self.nombre = nombre
        self.a = a
        self.c = c
        self.m = m
        self.semilla = semilla
