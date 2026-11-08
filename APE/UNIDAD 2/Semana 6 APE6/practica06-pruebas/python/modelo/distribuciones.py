# Valores p de las dos pruebas, calculados con fórmulas propias (sin librerías externas)
import math

# Coeficientes de la aproximación de Lanczos para calcular log(gamma(x))
LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
           771.32342877765313, -176.61502916214059, 12.507343278686905,
           -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]


def log_gamma(x):
    x -= 1.0
    suma = LANCZOS[0]
    for i in range(1, 9):
        suma += LANCZOS[i] / (x + i)
    t = x + 7.5
    return 0.5 * math.log(2 * math.pi) + (x + 0.5) * math.log(t) - t + math.log(suma)


def gamma_incompleta_superior(a, x):
    # Q(a, x): probabilidad de que una Gamma(a) sea mayor que x
    if x <= 0:
        return 1.0
    prefijo = math.exp(-x + a * math.log(x) - log_gamma(a))
    if x < a + 1:
        # Serie para P(a, x); luego Q = 1 - P
        termino = 1.0 / a
        suma = termino
        for n in range(1, 1000):
            termino *= x / (a + n)
            suma += termino
            if abs(termino) < abs(suma) * 1e-16:
                break
        return max(0.0, 1.0 - prefijo * suma)
    # Fracción continua para Q(a, x)
    pequeno = 1e-300
    b = x + 1 - a
    c = 1 / pequeno
    d = 1 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        if abs(d) < pequeno:
            d = pequeno
        c = b + an / c
        if abs(c) < pequeno:
            c = pequeno
        d = 1 / d
        cambio = d * c
        h *= cambio
        if abs(cambio - 1) < 1e-16:
            break
    return min(1.0, prefijo * h)


def p_valor_chi(chi2, grados):
    # P(Chi-cuadrado con 'grados' grados de libertad >= chi2)
    return gamma_incompleta_superior(grados / 2.0, chi2 / 2.0)


def valor_critico_chi(grados, alfa=0.05):
    # Valor de chi2 que deja una probabilidad 'alfa' a su derecha (búsqueda por bisección)
    bajo, alto = 0.0, 1000.0
    for _ in range(200):
        medio = (bajo + alto) / 2
        if p_valor_chi(medio, grados) > alfa:
            bajo = medio
        else:
            alto = medio
    return (bajo + alto) / 2


def densidad_chi(x, grados):
    # Curva de campana (asimétrica) de la distribución Chi-cuadrado
    if x <= 0:
        return 0.0
    k = grados / 2.0
    return math.exp((k - 1) * math.log(x) - x / 2 - k * math.log(2) - log_gamma(k))


def valor_critico_ks(n, alfa=0.05):
    # Valor de D que deja una probabilidad 'alfa' a su derecha (misma aproximación del valor p)
    bajo, alto = 0.0, 1.0
    for _ in range(100):
        medio = (bajo + alto) / 2
        if p_valor_ks(medio, n) > alfa:
            bajo = medio
        else:
            alto = medio
    return (bajo + alto) / 2


def p_valor_ks(d, n):
    # Distribución de Kolmogorov (aproximación para muestras grandes)
    raiz = math.sqrt(n)
    lam = (raiz + 0.12 + 0.11 / raiz) * d
    if lam < 0.2:
        return 1.0
    suma = 0.0
    for j in range(1, 101):
        termino = 2 * (-1) ** (j - 1) * math.exp(-2 * j * j * lam * lam)
        suma += termino
        if abs(termino) < 1e-18:
            break
    return min(1.0, max(0.0, suma))
