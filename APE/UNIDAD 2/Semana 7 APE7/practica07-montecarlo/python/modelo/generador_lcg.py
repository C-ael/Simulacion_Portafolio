# Generador Congruencial Lineal (LCG): X(n+1) = (a * X(n) + c) mod m
# Es el mismo de las prácticas anteriores: con la misma semilla da siempre la misma secuencia.


class GeneradorLCG:
    def __init__(self, a, c, m, semilla):
        self.a = a
        self.c = c
        self.m = m
        self.x = semilla        # valor actual: al inicio es la semilla

    def siguiente(self):
        # Devuelve el siguiente número entre 0 y 1
        self.x = (self.a * self.x + self.c) % self.m
        return self.x / self.m
