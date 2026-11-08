package modelo;

// Resultado de la prueba Chi-cuadrado
public class ResultadoChi {
    public final int[] observadas;
    public final double esperada;
    public final double chi2;
    public final int grados;
    public final double p;
    public final double critico;    // chi2 crítico para alfa = 0.05
    public final boolean rechaza;

    public ResultadoChi(int[] observadas, double esperada, double chi2, int grados, double p, double critico) {
        this.observadas = observadas;
        this.esperada = esperada;
        this.chi2 = chi2;
        this.grados = grados;
        this.p = p;
        this.critico = critico;
        this.rechaza = p < Resultado.ALFA;
    }
}
