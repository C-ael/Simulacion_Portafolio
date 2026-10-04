# MUestra la tabla por consola.

def mostrar_tabla(nombre, resultados):
    print(f"\n=== {nombre} ===")
    print(f"{'Hora':<6}{'Hum':>5}{'Nub':>5}{'Temp':>6}"
          f"{'H':>7}{'N':>7}{'Tf':>7}{'Índice':>9}  Estado")
    for r in resultados:
        print(f"{r['hora']:<6}{r['humedad']:>5}{r['nubosidad']:>5}{r['temp']:>6}"
              f"{r['H']:>7.2f}{r['N']:>7.2f}{r['Tf']:>7.2f}{r['indice']:>9.3f}"
              f"  {r['estado']}")
