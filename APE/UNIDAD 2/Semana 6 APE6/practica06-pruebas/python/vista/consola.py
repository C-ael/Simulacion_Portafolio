# Todo lo que se imprime en la terminal

def decision(rechaza):
    return "Se rechaza H0" if rechaza else "No se rechaza H0"


class Consola:

    def mostrar_inicio(self, cantidad, k, alfa):
        print("=== Validación estadística de números pseudoaleatorios (Python) ===")
        print(f"Números por configuración: {cantidad}")
        print(f"Intervalos Chi-cuadrado: {k}  (grados de libertad = {k - 1})")
        print(f"Nivel de significancia: {alfa}")
        print("H0: X ~ U(0,1)   H1: X no sigue U(0,1)")
        print()

    def mostrar_configuracion(self, r):
        c = r.configuracion
        print(f"--- {c.nombre} ---")
        print(f"a = {c.a}, c = {c.c}, m = {c.m}, semilla = {c.semilla}")
        print(f"Primeros 10 valores: {', '.join(f'{u:.6f}' for u in r.numeros[:10])}")
        print()
        print("Chi-cuadrado:")
        print(f"  {'Intervalo':<12}{'Observada':>10}{'Esperada':>10}")
        for i, o in enumerate(r.chi.observadas):
            limite = f"[{i / len(r.chi.observadas):.1f}, {(i + 1) / len(r.chi.observadas):.1f})"
            print(f"  {limite:<12}{o:>10}{r.chi.esperada:>10.1f}")
        print(f"  chi2 = {r.chi.chi2:.4f}   gl = {r.chi.grados}   p = {r.chi.p:.6f}")
        print(f"  chi2 crítico (alfa 0.05, gl {r.chi.grados}) = {r.chi.critico:.4f}")
        print(f"  Decisión: {decision(r.chi.rechaza)}")
        print()
        print("Kolmogorov-Smirnov:")
        print(f"  D+ = {r.ks.d_positiva:.6f}   D- = {r.ks.d_negativa:.6f}   D = {r.ks.d:.6f}")
        print(f"  p = {r.ks.p:.6f}")
        print(f"  D crítico (alfa 0.05) = {r.ks.critico:.6f}")
        print(f"  Decisión: {decision(r.ks.rechaza)}")
        print()

    def mostrar_resumen(self, resultados):
        print("=== Resumen de las configuraciones ===")
        print(f"{'Configuración':<28}{'chi2':>12}{'p chi':>10}{'D (KS)':>10}{'p KS':>10}  Decisión")
        for r in resultados:
            conclusion = "uniforme" if not (r.chi.rechaza or r.ks.rechaza) else "NO uniforme"
            print(f"{r.configuracion.nombre:<28}{r.chi.chi2:>12.3f}{r.chi.p:>10.4f}"
                  f"{r.ks.d:>10.5f}{r.ks.p:>10.4f}  {conclusion}")
        print()

    def mostrar_comparacion(self, comparacion):
        print("=== Comparación con Java ===")
        print(f"{'Configuración':<28}{'Valores iguales':>16}{'chi2':>6}{'p chi':>7}{'D':>5}{'p KS':>7}")
        for nombre, iguales, total, a, b, c, d in comparacion:
            print(f"{nombre:<28}{f'{iguales}/{total}':>16}{'sí' if a else 'NO':>6}{'sí' if b else 'NO':>7}"
                  f"{'sí' if c else 'NO':>5}{'sí' if d else 'NO':>7}")
        print()

    def mostrar_sin_java(self):
        print("No se encontró 'resultados/pruebas_java.csv'.")
        print("Ejecuta primero el programa Java para poder compararlo.")
        print()

    def mostrar_mensaje(self, texto):
        print(texto)
