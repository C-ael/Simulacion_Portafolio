DATOS = [1000, 1100, 1250, 1400, 1600, 1850, 2100] # población en cada período

def tasa_promedio(datos):
    #Promedio de la tasa de crecimiento entre períodos consecutivos
    tasas = []
    for i in range(1, len(datos)):
        tasas.append((datos[i] - datos[i - 1]) / datos[i - 1])
    return sum(tasas) / len(tasas)

class Parametros:
    def __init__(self, datos, sigma=50, dt=0.1, semilla=42):
        self.datos = datos
        self.P0 = datos[0]                # población inicial
        self.tiempo = len(datos) - 1      # número de períodos
        self.r = tasa_promedio(datos)     # tasa de crecimiento
        self.sigma = sigma                # nivel de aleatoriedad (ruido)
        self.dt = dt                      # tamaño del paso para Euler
        self.semilla = semilla            # para repetir los mismos números aleatorios
