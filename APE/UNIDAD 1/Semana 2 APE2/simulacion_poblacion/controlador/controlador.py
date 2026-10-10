import copy

from modelo.parametros import Parametros, DATOS
from modelo.modelos import Deterministico, Discreto, Estocastico, Continuo
from vista import vista_consola, vista_grafica

VALORES_R = [-0.10, 0.0, 0.05, 0.13, 0.20]
VALORES_SIGMA = [0, 25, 50, 100, 200] # sigma = 0 modelo discreto

class Controlador:
    def __init__(self, datos=DATOS):
        self.params = Parametros(datos)
        self.modelos = [Deterministico(), Discreto(), Estocastico(), Continuo()]

    def _simular(self, modelo, **cambios):
        # Simula un modelo cambiando algunos parámetros como r o sigma
        p = copy.copy(self.params)
        for nombre, valor in cambios.items():
            setattr(p, nombre, valor)
        return modelo.simular(p)

    def ejecutar(self):
        # 1. con los mismos parámetros
        resultados = {}
        for modelo in self.modelos:
            resultados[modelo.nombre] = modelo.simular(self.params)

        vista_consola.mostrar_parametros(self.params)
        vista_consola.mostrar_resumen(resultados, self.params)

        # 2. Influencia de r (determinístico)
        curvas_r = []
        for r in VALORES_R:
            t, poblacion = self._simular(Deterministico(), r=r)
            curvas_r.append((r, t, poblacion))

        # 3. Efecto de la aleatoriedad (estocástico)
        curvas_sigma = []
        for sigma in VALORES_SIGMA:
            t, poblacion = self._simular(Estocastico(), sigma=sigma)
            curvas_sigma.append((sigma, t, poblacion))

        vista_grafica.grafica_comparacion(resultados, self.params)
        vista_grafica.grafica_influencia_r(curvas_r)
        vista_grafica.grafica_efecto_sigma(curvas_sigma)
