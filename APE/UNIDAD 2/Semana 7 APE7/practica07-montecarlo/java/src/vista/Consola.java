package vista;

import modelo.PruebaChi;
import modelo.ResultadoPi;

import java.util.List;
import java.util.Locale;
import java.util.Map;

// Todo lo que se imprime en la terminal
public class Consola {

    public void mostrarInicio(int[] tamanos, long semilla, int repeticiones) {
        System.out.println("=== Estimación de pi con el método de Monte Carlo (Java) ===");
        System.out.println("Cuadrado de lado 2 con un círculo de radio 1 inscrito.  pi ≈ 4 · Nc / N");
        StringBuilder lista = new StringBuilder();
        for (int i = 0; i < tamanos.length; i++) {
            lista.append(i > 0 ? ", " : "").append(tamanos[i]);
        }
        System.out.println("Tamaños de muestra: " + lista);
        System.out.println("Semilla: " + semilla + "   Repeticiones por tamaño: " + repeticiones);
        System.out.printf(Locale.US, "Valor real de pi = %.10f%n%n", Math.PI);
    }

    public void mostrarResultados(String generador, List<ResultadoPi> resultados) {
        System.out.println("--- Generador: " + generador + " ---");
        System.out.printf(Locale.US, "%9s%9s%12s%12s%15s%n", "N", "Nc", "pi Java", "Error Java", "t Java (ms)");
        for (ResultadoPi r : resultados) {
            System.out.printf(Locale.US, "%9d%9d%12.6f%12.6f%15.2f%n", r.n, r.dentro, r.pi, r.error, r.tiempoMs);
        }
        System.out.println();
    }

    public void mostrarBondad(String generador, List<ResultadoPi> resultados) {
        System.out.println("Chi-cuadrado de bondad de ajuste, Java, " + generador
                + " (gl = 1, alfa = " + PruebaChi.ALFA + ", crítico = 3.8415)");
        System.out.printf(Locale.US, "%9s%9s%11s%10s%10s  %s%n", "N", "Nc obs", "Nc esp", "chi2", "p", "Decisión");
        for (ResultadoPi r : resultados) {
            String decision = r.p < PruebaChi.ALFA ? "Se rechaza H0" : "No se rechaza H0";
            System.out.printf(Locale.US, "%9d%9d%11.1f%10.4f%10.4f  %s%n",
                    r.n, r.dentro, r.n * Math.PI / 4, r.chi2, r.p, decision);
        }
        System.out.println();
    }

    public void mostrarRepeticiones(Map<Integer, double[]> repeticiones) {
        System.out.println("=== Error según el tamaño de muestra (varias repeticiones, LCG propio) ===");
        System.out.printf(Locale.US, "%9s%13s%10s%10s%n", "N", "Error medio", "Mínimo", "Máximo");
        for (Map.Entry<Integer, double[]> fila : repeticiones.entrySet()) {
            double suma = 0, minimo = Double.MAX_VALUE, maximo = 0;
            for (double pi : fila.getValue()) {
                double error = Math.abs(pi - Math.PI);
                suma += error;
                minimo = Math.min(minimo, error);
                maximo = Math.max(maximo, error);
            }
            System.out.printf(Locale.US, "%9d%13.5f%10.5f%10.5f%n",
                    fila.getKey(), suma / fila.getValue().length, minimo, maximo);
        }
        System.out.println();
    }

    public void mostrarMensaje(String texto) {
        System.out.println(texto);
    }
}
