# Todo lo que se imprime en la terminal


class Consola:

    def mostrar_parametros(self, a, c, m, semilla, cantidad):
        print("=== Generador Congruencial Lineal en Python ===")
        print(f"a = {a}")
        print(f"c = {c}")
        print(f"m = 2^32 = {m}")
        print(f"semilla = {semilla}")
        print(f"valores generados = {cantidad}")
        print()

    def mostrar_estadisticas(self, semilla, media, varianza, repetidos):
        print(f"Semilla {semilla}:")
        print(f"  media     = {media:.6f}   (esperada 0.500000)")
        print(f"  varianza  = {varianza:.6f}   (esperada 0.083333)")
        print(f"  X repetidos en la secuencia = {repetidos}")
        print()

    def mostrar_comparacion_20(self, valores_python, valores_java):
        # Tabla con las primeras 20 observaciones de Python y de Java
        print("Primeras 20 observaciones (semilla 12345):")
        print(f"{'n':>3}  {'X Python':>11}  {'X Java':>11}  {'U Python':>12}  {'U Java':>12}  Igual")
        for i in range(20):
            n, x1, u1 = valores_python[i]
            _, x2, u2 = valores_java[i]
            igual = "sí" if x1 == x2 and abs(u1 - u2) < 1e-9 else "NO"
            print(f"{n:>3}  {x1:>11}  {x2:>11}  {u1:>12.10f}  {u2:>12.10f}  {igual}")
        print()

    def mostrar_primeras_20(self, valores):
        # Se usa cuando todavía no existe el archivo de Java
        print("Primeras 20 observaciones (semilla 12345):")
        print(f"{'n':>3}  {'X':>11}  {'U':>12}")
        for n, x, u in valores[:20]:
            print(f"{n:>3}  {x:>11}  {u:>12.10f}")
        print()

    def mostrar_resultado_comparacion(self, semilla, iguales, total):
        print(f"Semilla {semilla}: Python y Java coinciden en {iguales} de {total} valores.")

    def mostrar_sin_java(self):
        print("No se encontraron los archivos de Java en 'resultados/'.")
        print("Ejecuta primero el programa Java para poder compararlos.")
        print()

    def mostrar_periodo(self, ejemplos):
        print()
        print("=== Análisis del período ===")
        print("Ejemplos con m = 16 para ver el efecto de los parámetros:")
        print(f"{'a':>3} {'c':>3} {'m':>3} {'semilla':>8} {'período':>8}")
        for ejemplo_a, ejemplo_c, ejemplo_m, semilla, periodo in ejemplos:
            print(f"{ejemplo_a:>3} {ejemplo_c:>3} {ejemplo_m:>3} {semilla:>8} {periodo:>8}")
        print()
        print("Contar el período completo con m = 2^32 en Python tardaría horas;")
        print("ese conteo se hace en el programa Java (ejecutarlo con el argumento: periodo).")
        print()
