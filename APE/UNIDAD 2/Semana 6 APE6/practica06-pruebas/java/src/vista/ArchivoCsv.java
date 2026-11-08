package vista;

import modelo.Resultado;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.Locale;

// Guarda el resumen de las pruebas en un CSV (mismo formato que Python)
public class ArchivoCsv {

    // Guarda la secuencia de números (n,u)
    public void guardarSecuencia(String ruta, double[] numeros) throws IOException {
        File archivo = new File(ruta);
        if (archivo.getParentFile() != null) {
            archivo.getParentFile().mkdirs();
        }
        try (PrintWriter escritor = new PrintWriter(archivo, "UTF-8")) {
            escritor.println("n,u");
            for (int i = 0; i < numeros.length; i++) {
                escritor.println((i + 1) + "," + String.format(Locale.US, "%.10f", numeros[i]));
            }
        }
    }

    public void guardarPruebas(String ruta, List<Resultado> resultados) throws IOException {
        File archivo = new File(ruta);
        if (archivo.getParentFile() != null) {
            archivo.getParentFile().mkdirs();   // crea la carpeta si no existe
        }

        try (PrintWriter escritor = new PrintWriter(archivo, "UTF-8")) {
            escritor.println("configuracion,chi2,gl,p_chi,decision_chi,d_ks,p_ks,decision_ks");
            for (Resultado r : resultados) {
                // Locale.US para que el decimal sea punto y no coma
                escritor.println(String.format(Locale.US, "%s,%.10e,%d,%.10e,%s,%.10e,%.10e,%s",
                        r.configuracion.nombre, r.chi.chi2, r.chi.grados, r.chi.p,
                        r.chi.rechaza ? "rechaza" : "no rechaza",
                        r.ks.d, r.ks.p, r.ks.rechaza ? "rechaza" : "no rechaza"));
            }
        }
    }
}
