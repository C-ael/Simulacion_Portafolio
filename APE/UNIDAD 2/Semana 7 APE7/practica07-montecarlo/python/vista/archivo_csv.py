# Guarda los resultados en CSV (mismo formato que Java)
import os


def crear_carpeta(ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)


def guardar_resultados(ruta, resultados):
    crear_carpeta(ruta)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("generador,n,dentro,pi,error,tiempo_ms,chi2,p_chi\n")
        for (generador, n), r in resultados.items():
            archivo.write(f"{generador},{n},{r.dentro},{r.pi:.10f},{r.error:.10e},"
                          f"{r.tiempo_ms:.3f},{r.chi2:.10e},{r.p:.10e}\n")


def guardar_repeticiones(ruta, resumenes):
    crear_carpeta(ruta)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("n,repeticion,pi,error\n")
        for n, resumen in resumenes.items():
            for i, (pi, error) in enumerate(zip(resumen.estimaciones, resumen.errores), start=1):
                archivo.write(f"{n},{i},{pi:.10f},{error:.10e}\n")
