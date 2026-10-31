package controlador;

import modelo.Analisis;
import modelo.GeneradorLCG;
import modelo.Valor;
import vista.ArchivoCsv;
import vista.Consola;

import java.io.IOException;
import java.util.List;

// Controlador: sigue los pasos de la guía y le pasa los resultados a la vista
public class Controlador {

    // Parámetros de la guía
    private static final long A = 1664525L;
    private static final long C = 1013904223L;
    private static final long M = 4294967296L;      // 2^32
    private static final long SEMILLA = 12345L;
    private static final long SEMILLA_2 = 54321L;   // segunda semilla para el paso "cambiar la semilla"
    private static final int CANTIDAD = 10000;

    // Se ejecuta desde la raíz del proyecto (por eso la carpeta es resultados/)
    private static final String CARPETA_RESULTADOS = "resultados/";

    public void ejecutar(boolean medirPeriodoCompleto) {
        Consola consola = new Consola();
        Analisis analisis = new Analisis();
        ArchivoCsv archivo = new ArchivoCsv();

        consola.mostrarParametros(A, C, M, SEMILLA, CANTIDAD);

        // Pasos 1 y 3: generar 10 000 valores con la semilla de la guía
        List<Valor> valores1 = new GeneradorLCG(A, C, M, SEMILLA).generar(CANTIDAD);
        // Paso 7: cambiar la semilla
        List<Valor> valores2 = new GeneradorLCG(A, C, M, SEMILLA_2).generar(CANTIDAD);

        try {
            archivo.guardar(ruta(SEMILLA), valores1);
            archivo.guardar(ruta(SEMILLA_2), valores2);
        } catch (IOException e) {
            consola.mostrarMensaje("No se pudo guardar el CSV: " + e.getMessage());
        }

        // Paso 4: primeras 20 observaciones
        consola.mostrarPrimeras20(valores1);

        consola.mostrarEstadisticas(SEMILLA, analisis.media(valores1), analisis.varianza(valores1),
                analisis.valoresRepetidos(valores1));
        consola.mostrarEstadisticas(SEMILLA_2, analisis.media(valores2), analisis.varianza(valores2),
                analisis.valoresRepetidos(valores2));

        // Paso 6: período
        consola.mostrarTituloPeriodo();
        mostrarEjemplosPeriodo(consola, analisis);
        if (medirPeriodoCompleto) {
            medirPeriodoReal(consola, analisis);
        } else {
            consola.mostrarMensaje("Para medir el período completo con m = 2^32 (tarda unos 30 segundos) "
                    + "ejecuta con el argumento: periodo");
            consola.mostrarMensaje("");
        }

        consola.mostrarMensaje("Resultados guardados en la carpeta resultados/. "
                + "Ahora ejecuta el programa Python para compararlos y ver las gráficas.");
    }

    private String ruta(long semilla) {
        return CARPETA_RESULTADOS + "lcg_java_" + semilla + ".csv";
    }

    private void mostrarEjemplosPeriodo(Consola consola, Analisis analisis) {
        // Con m = 16 el período se puede contar completo. Cada fila es {a, c, m, semilla}
        long[][] casos = {
                {5, 3, 16, 1},      // parámetros buenos: período completo
                {5, 0, 16, 1},      // c = 0: el período se acorta
                {1, 0, 16, 3},      // a = 1 y c = 0: el valor nunca cambia
        };
        long[] periodos = new long[casos.length];
        for (int i = 0; i < casos.length; i++) {
            periodos[i] = analisis.periodo(casos[i][0], casos[i][1], casos[i][2], casos[i][3]);
        }
        consola.mostrarEjemplos(casos, periodos);
    }

    private void medirPeriodoReal(Consola consola, Analisis analisis) {
        // Con m = 2^32 son más de 4 mil millones de pasos: en Java tarda medio minuto aproximadamente
        consola.mostrarMensaje("Midiendo el período con m = 2^32 (puede tardar unos 30 segundos)...");
        long inicio = System.nanoTime();
        long periodo = analisis.periodo(A, C, M, SEMILLA);
        double segundos = (System.nanoTime() - inicio) / 1e9;
        consola.mostrarPeriodoReal(periodo, segundos);
    }
}
