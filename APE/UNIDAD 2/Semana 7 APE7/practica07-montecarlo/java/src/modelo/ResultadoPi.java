package modelo;

// Resultado de un experimento Monte Carlo con N puntos
public class ResultadoPi {
    public final int n;
    public final long dentro;           // Nc: puntos dentro del círculo
    public final double pi;             // pi ≈ 4 · Nc / N
    public final double error;          // error absoluto
    public final double tiempoMs;
    public double chi2 = 0.0;           // se llenan al aplicar la prueba Chi-cuadrado
    public double p = 1.0;

    public ResultadoPi(int n, long dentro, double tiempoMs) {
        this.n = n;
        this.dentro = dentro;
        this.pi = 4.0 * dentro / n;
        this.error = Math.abs(pi - Math.PI);
        this.tiempoMs = tiempoMs;
    }
}
