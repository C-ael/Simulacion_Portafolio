package vista;

import modelo.Resultado;

import java.util.List;
import java.util.Locale;

// Todo lo que se imprime en la terminal
public class Consola {

    private String decision(boolean rechaza) {
        return rechaza ? "Se rechaza H0" : "No se rechaza H0";
    }

    public void mostrarInicio(int cantidad, int k, double alfa) {
        System.out.println("=== Validación estadística de números pseudoaleatorios (Java) ===");
        System.out.println("Números por configuración: " + cantidad);
        System.out.println("Intervalos Chi-cuadrado: " + k + "  (grados de libertad = " + (k - 1) + ")");
        System.out.println("Nivel de significancia: " + alfa);
        System.out.println("H0: X ~ U(0,1)   H1: X no sigue U(0,1)");
        System.out.println();
    }

    public void mostrarConfiguracion(Resultado r) {
        System.out.println("--- " + r.configuracion.nombre + " ---");
        System.out.println("a = " + r.configuracion.a + ", c = " + r.configuracion.c
                + ", m = " + r.configuracion.m + ", semilla = " + r.configuracion.semilla);
        StringBuilder primeros = new StringBuilder();
        for (int i = 0; i < 10; i++) {
            primeros.append(i > 0 ? ", " : "").append(String.format(Locale.US, "%.6f", r.numeros[i]));
        }
        System.out.println("Primeros 10 valores: " + primeros);
        System.out.println();

        int k = r.chi.observadas.length;
        System.out.println("Chi-cuadrado:");
        System.out.printf(Locale.US, "  %-12s%10s%10s%n", "Intervalo", "Observada", "Esperada");
        for (int i = 0; i < k; i++) {
            String limite = String.format(Locale.US, "[%.1f, %.1f)", (double) i / k, (double) (i + 1) / k);
            System.out.printf(Locale.US, "  %-12s%10d%10.1f%n", limite, r.chi.observadas[i], r.chi.esperada);
        }
        System.out.printf(Locale.US, "  chi2 = %.4f   gl = %d   p = %.6f%n", r.chi.chi2, r.chi.grados, r.chi.p);
        System.out.printf(Locale.US, "  chi2 crítico (alfa 0.05, gl %d) = %.4f%n", r.chi.grados, r.chi.critico);
        System.out.println("  Decisión: " + decision(r.chi.rechaza));
        System.out.println();

        System.out.println("Kolmogorov-Smirnov:");
        System.out.printf(Locale.US, "  D+ = %.6f   D- = %.6f   D = %.6f%n", r.ks.dPositiva, r.ks.dNegativa, r.ks.d);
        System.out.printf(Locale.US, "  p = %.6f%n", r.ks.p);
        System.out.printf(Locale.US, "  D crítico (alfa 0.05) = %.6f%n", r.ks.critico);
        System.out.println("  Decisión: " + decision(r.ks.rechaza));
        System.out.println();
    }

    public void mostrarResumen(List<Resultado> resultados) {
        System.out.println("=== Resumen de las configuraciones ===");
        System.out.printf(Locale.US, "%-28s%12s%10s%10s%10s  %s%n", "Configuración", "chi2", "p chi", "D (KS)", "p KS", "Decisión");
        for (Resultado r : resultados) {
            String conclusion = (r.chi.rechaza || r.ks.rechaza) ? "NO uniforme" : "uniforme";
            System.out.printf(Locale.US, "%-28s%12.3f%10.4f%10.5f%10.4f  %s%n",
                    r.configuracion.nombre, r.chi.chi2, r.chi.p, r.ks.d, r.ks.p, conclusion);
        }
        System.out.println();
    }

    public void mostrarMensaje(String texto) {
        System.out.println(texto);
    }
}
