package vista;

import modelo.ResultadoPi;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.Locale;
import java.util.Map;

// Guarda los resultados en CSV (mismo formato que Python)
public class ArchivoCsv {

    private PrintWriter abrir(String ruta) throws IOException {
        File archivo = new File(ruta);
        if (archivo.getParentFile() != null) {
            archivo.getParentFile().mkdirs();   // crea la carpeta si no existe
        }
        return new PrintWriter(archivo, "UTF-8");
    }

    // Una fila por generador y tamaño. Locale.US para que el decimal sea punto y no coma
    public void guardarResultados(String ruta, Map<String, List<ResultadoPi>> resultados) throws IOException {
        try (PrintWriter escritor = abrir(ruta)) {
            escritor.println("generador,n,dentro,pi,error,tiempo_ms,chi2,p_chi");
            for (Map.Entry<String, List<ResultadoPi>> grupo : resultados.entrySet()) {
                for (ResultadoPi r : grupo.getValue()) {
                    escritor.println(String.format(Locale.US, "%s,%d,%d,%.10f,%.10e,%.3f,%.10e,%.10e",
                            grupo.getKey(), r.n, r.dentro, r.pi, r.error, r.tiempoMs, r.chi2, r.p));
                }
            }
        }
    }

    public void guardarRepeticiones(String ruta, Map<Integer, double[]> repeticiones) throws IOException {
        try (PrintWriter escritor = abrir(ruta)) {
            escritor.println("n,repeticion,pi,error");
            for (Map.Entry<Integer, double[]> fila : repeticiones.entrySet()) {
                double[] estimaciones = fila.getValue();
                for (int i = 0; i < estimaciones.length; i++) {
                    escritor.println(String.format(Locale.US, "%d,%d,%.10f,%.10e",
                            fila.getKey(), i + 1, estimaciones[i], Math.abs(estimaciones[i] - Math.PI)));
                }
            }
        }
    }
}
