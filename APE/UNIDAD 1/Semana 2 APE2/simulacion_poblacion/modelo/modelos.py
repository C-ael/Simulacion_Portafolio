"""Los cuatro modelos de crecimiento poblacional"""

import numpy as np

class Modelo:
    nombre = ""
    def simular(self, p):
        raise NotImplementedError


class Deterministico(Modelo):
    #sin aleatoriedad
    nombre = "Determinístico"

    def simular(self, p):
        t = np.linspace(0, p.tiempo, 100)
        poblacion = []
        for instante in t:
            poblacion.append(p.P0 * np.exp(p.r * instante))
        return t, np.array(poblacion)


class Discreto(Modelo):
    #cambia por intervalos de tiempo definidos
    nombre = "Discreto"

    def simular(self, p):
        poblacion = [p.P0]
        for periodo in range(1, p.tiempo + 1):
            actual = poblacion[-1]
            incremento = p.r * actual
            poblacion.append(actual + incremento)
        t = np.arange(0, p.tiempo + 1)
        return t, np.array(poblacion)


class Estocastico(Modelo):
    # P(t+1) = P(t) + r*P(t) + ruido,  ruido ~ N(0, sigma)
    nombre = "Estocástico"

    def simular(self, p):
        rng = np.random.default_rng(p.semilla)
        poblacion = [p.P0]
        for periodo in range(1, p.tiempo + 1):
            ruido = rng.normal(0, p.sigma)
            actual = poblacion[-1]
            nueva = actual + p.r * actual + ruido
            if nueva < 0: nueva = 0 #la población no puede ser negativa
            poblacion.append(nueva)
        t = np.arange(0, p.tiempo + 1)
        return t, np.array(poblacion)


class Continuo(Modelo):
    #dP/dt = r*P resuelto con Euler: P(t+dt) = P(t) + dt*(r*P(t))
    nombre = "Continuo (Euler)"

    def simular(self, p):
        pasos = round(p.tiempo / p.dt)
        t = np.linspace(0, p.tiempo, pasos + 1)
        poblacion = [p.P0]
        for paso in range(pasos):
            actual = poblacion[-1]
            cambio = p.r * actual
            poblacion.append(actual + p.dt * cambio)
        return t, np.array(poblacion)
