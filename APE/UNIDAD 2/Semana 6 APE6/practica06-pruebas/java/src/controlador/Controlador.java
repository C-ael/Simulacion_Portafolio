package controlador;

import modelo.Configuracion;
import modelo.GeneradorLCG;
import modelo.PruebaChi;
import modelo.PruebaKS;
import modelo.Resultado;
import modelo.ResultadoChi;
import modelo.ResultadoKS;
import vista.ArchivoCsv;
import vista.Consola;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

// Controlador: sigue los pasos de la guía y le pasa los resultados a la vista
public class Controlador {

    private static final int CANTIDAD = 10000;      // números por configuración
    private static final int INTERVALOS = 10;       // k para Chi-cuadrado (gl = 9)

    // Configuraciones a comparar: la primera es la de la guía
    private static final Configuracion[] CONFIGURACIONES = {
            new Configuracion("Guia semilla 12345", 1664525L, 1013904223L, 1L << 32, 12345L),
            new Configuracion("Guia semilla 54321", 1664525L, 1013904223L, 1L << 32, 54321L),
            new Configuracion("RANDU", 65539L, 0L, 1L << 31, 1L),
            new Configuracion("Parametros malos m=16", 5L, 3L, 16L, 1L),
    };

    private static final String RUTA_CSV = "resultados/pruebas_java.csv";

    public void ejecutar() {
        Consola consola = new Consola();
        consola.mostrarInicio(CANTIDAD, INTERVALOS, Resultado.ALFA);

        PruebaChi pruebaChi = new PruebaChi();
        PruebaKS pruebaKS = new PruebaKS();
        List<Resultado> resultados = new ArrayList<>();

        ArchivoCsv archivoCsv = new ArchivoCsv();
        int numero = 0;
        for (Configuracion c : CONFIGURACIONES) {
            numero++;
            // Actividad 1: generar los números con el LCG
            double[] numeros = new GeneradorLCG(c.a, c.c, c.m, c.semilla).generar(CANTIDAD);
            // Algoritmos 2 y 3: las dos pruebas
            ResultadoChi chi = pruebaChi.aplicar(numeros, INTERVALOS);
            ResultadoKS ks = pruebaKS.aplicar(numeros);
            Resultado resultado = new Resultado(c, numeros, chi, ks);
            resultados.add(resultado);
            consola.mostrarConfiguracion(resultado);
            // Paso 12 del Algoritmo 1: guardar la secuencia para las pruebas
            guardarSecuencia(archivoCsv, consola, numero, numeros);
        }

        consola.mostrarResumen(resultados);

        try {
            archivoCsv.guardarPruebas(RUTA_CSV, resultados);
            consola.mostrarMensaje("Resultados guardados en " + RUTA_CSV
                    + ". Ahora ejecuta el programa Python para compararlos y ver las gráficas.");
        } catch (IOException error) {
            consola.mostrarMensaje("No se pudo guardar el CSV: " + error.getMessage());
        }
    }

    private void guardarSecuencia(ArchivoCsv archivoCsv, Consola consola, int numero, double[] numeros) {
        try {
            archivoCsv.guardarSecuencia("resultados/secuencia_java_" + numero + ".csv", numeros);
        } catch (IOException error) {
            consola.mostrarMensaje("No se pudo guardar la secuencia: " + error.getMessage());
        }
    }
}
