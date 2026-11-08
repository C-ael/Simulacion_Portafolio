# Guarda el resumen de las pruebas en un CSV (mismo formato que Java)
import os


def guardar_secuencia(ruta, numeros):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("n,u\n")
        for n, u in enumerate(numeros, start=1):
            archivo.write(f"{n},{u:.10f}\n")


def guardar_pruebas(ruta, resultados):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("configuracion,chi2,gl,p_chi,decision_chi,d_ks,p_ks,decision_ks\n")
        for r in resultados:
            archivo.write(f"{r.configuracion.nombre},{r.chi.chi2:.10e},{r.chi.grados},{r.chi.p:.10e},"
                          f"{'rechaza' if r.chi.rechaza else 'no rechaza'},"
                          f"{r.ks.d:.10e},{r.ks.p:.10e},{'rechaza' if r.ks.rechaza else 'no rechaza'}\n")
