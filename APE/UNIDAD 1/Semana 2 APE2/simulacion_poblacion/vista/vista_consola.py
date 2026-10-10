"""resultados por consola"""

def mostrar_parametros(p):
    print("=== Parámetros de la simulación ===")
    print(f"Datos de entrada : {p.datos}")
    print(f"P0 (inicial)     : {p.P0}")
    print(f"r (tasa)         : {p.r:.4f}")
    print(f"tiempo (períodos): {p.tiempo}")
    print(f"sigma (ruido)    : {p.sigma}")
    print(f"dt (paso Euler)  : {p.dt}")
    

def mostrar_resumen(resultados, p):
    real = p.datos[-1]
    print(f"\n=== Población final de cada modelo (dato real: {real}) ===")
    print(f"{'Modelo':<20}{'P final':>10}{'Diferencia':>12}")
    for nombre, (t, poblacion) in resultados.items():
        final = poblacion[-1]
        print(f"{nombre:<20}{final:>10.1f}{final - real:>12.1f}")
