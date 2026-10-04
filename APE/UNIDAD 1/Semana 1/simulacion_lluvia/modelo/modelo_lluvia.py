# Modelo matemático: I = a*H + b*N + c*Tf

class ModeloLluvia:
    def __init__(self, nombre, w_h=0.5, w_n=0.3, w_t=0.2, umbrales=(0.40, 0.60, 0.75)):
        self.nombre = nombre
        self.w_h = w_h              # peso humedad
        self.w_n = w_n              # peso nubosidad
        self.w_t = w_t              # peso factor de temperatura
        self.umbrales = umbrales    # límites entre estados

    def factor_temperatura(self, temp):
        # Tf según la tabla: 1.00 (<=10 °C) baja 0.05 por cada °C hasta 0.10 (>= 28 °C).
        # Así también funcionan temperaturas impares como 15 o 17.
        tf = 1 - 0.05 * (temp - 10)
        return max(0.10, min(1.00, tf))

    def indice(self, h, n, tf):
        return self.w_h * h + self.w_n * n + self.w_t * tf

    def estado(self, i):
        u1, u2, u3 = self.umbrales
        if i < u1:
            return "Sin lluvia"
        if i < u2:
            return "Baja posibilidad"
        if i < u3:
            return "Lluvia probable"
        return "Lluvia"

# Devuelve una lista de diccionarios, uno por hora.
    def calcular(self, datos):
        resultados = []
        for hora, humedad, nubosidad, temp in datos:
            h = humedad / 100
            n = nubosidad / 100
            tf = self.factor_temperatura(temp)
            i = round(self.indice(h, n, tf), 4)
            resultados.append({
                "hora": hora, "humedad": humedad, "nubosidad": nubosidad,
                "temp": temp, "H": h, "N": n, "Tf": round(tf, 2),
                "indice": i, "estado": self.estado(i),
            })
        return resultados
