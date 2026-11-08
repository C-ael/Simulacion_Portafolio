# Generador Congruencial Lineal (LCG)
# Fórmula de la guía: X(n+1) = (a * X(n) + c) mod m

class GeneradorLCG:
    def __init__(self, a, c, m, semilla):
        self.a = a
        self.c = c
        self.m = m
        self.x = semilla        # valor actual: al inicio es la semilla

    def siguiente(self):
        # Calcula el siguiente valor con la fórmula del LCG
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def generar(self, cantidad):
        # Devuelve una lista con los U(n) = X(n) / m, números entre 0 y 1
        # La semilla es X(0), por eso el primer valor generado es X(1)
        numeros = []
        for _ in range(cantidad):
            numeros.append(self.siguiente() / self.m)
        return numeros
