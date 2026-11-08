# Resultado de las dos pruebas para una configuración
ALFA = 0.05

class ResultadoChi:
    def __init__(self, observadas, esperada, chi2, grados, p, critico):
        self.observadas = observadas
        self.esperada = esperada
        self.chi2 = chi2
        self.grados = grados
        self.p = p
        self.critico = critico          # chi2 crítico para alfa = 0.05
        self.rechaza = p < ALFA


class ResultadoKS:
    def __init__(self, d_positiva, d_negativa, p, critico):
        self.d_positiva = d_positiva
        self.d_negativa = d_negativa
        self.d = max(d_positiva, d_negativa)
        self.p = p
        self.critico = critico          # D crítico para alfa = 0.05
        self.rechaza = p < ALFA


class Resultado:
    def __init__(self, configuracion, numeros, chi, ks):
        self.configuracion = configuracion
        self.numeros = numeros
        self.chi = chi
        self.ks = ks
