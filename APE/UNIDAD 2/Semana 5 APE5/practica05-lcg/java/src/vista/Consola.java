package vista;

import modelo.Valor;

import java.util.List;
import java.util.Locale;

// Todo lo que se imprime en la terminal
public class Consola {

    public void mostrarParametros(long a, long c, long m, long semilla, int cantidad) {
        System.out.println("=== Generador Congruencial Lineal en Java ===");
        System.out.println("a = " + a);
        System.out.println("c = " + c);
        System.out.println("m = 2^32 = " + m);
        System.out.println("semilla = " + semilla);
        System.out.println("valores generados = " + cantidad);
        System.out.println();
    }

    public void mostrarPrimeras20(List<Valor> valores) {
        System.out.println("Primeras 20 observaciones (semilla 12345):");
        System.out.printf("%3s  %11s  %12s%n", "n", "X", "U");
        for (int i = 0; i < 20; i++) {
            Valor v = valores.get(i);
            System.out.println(String.format(Locale.US, "%3d  %11d  %12.10f", v.n, v.x, v.u));
        }
        System.out.println();
    }

    public void mostrarEstadisticas(long semilla, double media, double varianza, int repetidos) {
        System.out.println("Semilla " + semilla + ":");
        System.out.println(String.format(Locale.US, "  media     = %.6f   (esperada 0.500000)", media));
        System.out.println(String.format(Locale.US, "  varianza  = %.6f   (esperada 0.083333)", varianza));
        System.out.println("  X repetidos en la secuencia = " + repetidos);
        System.out.println();
    }

    public void mostrarTituloPeriodo() {
        System.out.println("=== Análisis del período ===");
    }

    public void mostrarEjemplos(long[][] casos, long[] periodos) {
        System.out.println("Ejemplos con m = 16 para ver el efecto de los parámetros:");
        System.out.printf("%3s %3s %3s %8s %8s%n", "a", "c", "m", "semilla", "período");
        for (int i = 0; i < casos.length; i++) {
            System.out.printf("%3d %3d %3d %8d %8d%n", casos[i][0], casos[i][1], casos[i][2], casos[i][3], periodos[i]);
        }
        System.out.println();
    }

    public void mostrarPeriodoReal(long periodo, double segundos) {
        System.out.println("Período medido con los parámetros de la guía: " + periodo
                + " pasos (" + String.format(Locale.US, "%.1f", segundos) + " s)");
        System.out.println();
    }

    public void mostrarMensaje(String mensaje) {
        System.out.println(mensaje);
    }

}
