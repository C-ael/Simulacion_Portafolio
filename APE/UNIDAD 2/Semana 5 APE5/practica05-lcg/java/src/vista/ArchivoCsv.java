package vista;

import modelo.Valor;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.Locale;

// Guarda la secuencia en un CSV (el mismo formato que usa el programa Python)
public class ArchivoCsv {

    public void guardar(String ruta, List<Valor> valores) throws IOException {
        File archivo = new File(ruta);
        if (archivo.getParentFile() != null) {
            archivo.getParentFile().mkdirs();   // crea la carpeta si no existe
        }

        try (PrintWriter escritor = new PrintWriter(archivo, "UTF-8")) {
            escritor.println("n,x,u");
            for (Valor v : valores) {
                // Locale.US para que el decimal sea punto y no coma
                escritor.println(v.n + "," + v.x + "," + String.format(Locale.US, "%.10f", v.u));
            }
        }
    }
}
