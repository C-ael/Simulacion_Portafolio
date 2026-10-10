from modelo.datos import DATOS
from modelo.modelo_lluvia import ModeloLluvia
from vista import vista_tabla, vista_grafica

class Controlador:
    def __init__(self):
        self.original = ModeloLluvia("Modelo original")
        # Modelo ajustado: cada coeficiente baja 0.1
        # 0.5 -> 0.4, 0.3 -> 0.2, 0.2 -> 0.1 (no cambian los umbrales)
        self.ajustado = ModeloLluvia("Modelo ajustado", w_h=0.4, w_n=0.2, w_t=0.1)

    def ejecutar(self):
        res_original = self.original.calcular(DATOS)
        res_ajustado = self.ajustado.calcular(DATOS)

        vista_tabla.mostrar_tabla(self.original.nombre, res_original)
        vista_grafica.grafica_indice(self.original, res_original, "indice_original.png")

        vista_tabla.mostrar_tabla(self.ajustado.nombre, res_ajustado)
        vista_grafica.grafica_indice(self.ajustado, res_ajustado, "indice_ajustado.png")

        vista_grafica.grafica_comparacion(res_original, res_ajustado, "comparacion.png")