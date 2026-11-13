package controlador;

import modelo.Experimento;
import modelo.Generador;
import modelo.GeneradorLCG;
import modelo.GeneradorNativo;
import modelo.PruebaChi;
import modelo.ResultadoPi;
import vista.ArchivoCsv;
import vista.Consola;

import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

// Controlador: sigue los pasos de la guía y le pasa los resultados a la vista
public class Controlador {

    private static final int[] TAMANOS = {1000, 10000, 100000, 1000000};   // tamaños de muestra de la guía
    private static final long SEMILLA = 12345L;
    private static final int REPETICIONES = 10;             // repeticiones por tamaño para ver el error promedio
    private static final long A = 1664525L;                 // parámetros del LCG propio
    private static final long C = 1013904223L;
    private static final long M = 1L << 32;
    private static final String[] GENERADORES = {"LCG propio", "Nativo"};   // el LCG propio y el que trae cada lenguaje

    private Generador crearGenerador(String nombre, long semilla) {
        if (nombre.equals("LCG propio")) {
            return new GeneradorLCG(A, C, M, semilla);
        }
        return new GeneradorNativo(semilla);
    }

    public void ejecutar() {
        Consola consola = new Consola();
        consola.mostrarInicio(TAMANOS, SEMILLA, REPETICIONES);

        Experimento experimento = new Experimento();
        PruebaChi pruebaChi = new PruebaChi();

        // Calentamiento: la primera vez que Java ejecuta un bucle es más lento, y eso falsearía el tiempo
        experimento.estimarPi(crearGenerador("LCG propio", SEMILLA), 200000);
        experimento.estimarPi(crearGenerador("Nativo", SEMILLA), 200000);

        // Experimento principal: una ejecución por generador y tamaño (tabla de la guía)
        Map<String, List<ResultadoPi>> resultados = new LinkedHashMap<>();
        for (String generador : GENERADORES) {
            List<ResultadoPi> lista = new ArrayList<>();
            for (int n : TAMANOS) {
                ResultadoPi r = experimento.estimarPi(crearGenerador(generador, SEMILLA), n);
                pruebaChi.bondadAjuste(r);
                lista.add(r);
            }
            resultados.put(generador, lista);
            consola.mostrarResultados(generador, lista);
        }
        for (String generador : GENERADORES) {
            consola.mostrarBondad(generador, resultados.get(generador));
        }

        // Varias repeticiones con distintas semillas para ver cómo baja el error
        Map<Integer, double[]> repeticiones = new LinkedHashMap<>();
        for (int n : TAMANOS) {
            double[] estimaciones = new double[REPETICIONES];
            for (int i = 0; i < REPETICIONES; i++) {
                estimaciones[i] = experimento.estimarPi(crearGenerador("LCG propio", SEMILLA + i), n).pi;
            }
            repeticiones.put(n, estimaciones);
        }
        consola.mostrarRepeticiones(repeticiones);

        try {
            ArchivoCsv archivoCsv = new ArchivoCsv();
            archivoCsv.guardarResultados("resultados/resultados_java.csv", resultados);
            archivoCsv.guardarRepeticiones("resultados/repeticiones_java.csv", repeticiones);
            consola.mostrarMensaje("Resultados guardados en la carpeta resultados/. "
                    + "Ahora ejecuta el programa Python para compararlos y ver las gráficas.");
        } catch (IOException error) {
            consola.mostrarMensaje("No se pudieron guardar los CSV: " + error.getMessage());
        }
    }
}
