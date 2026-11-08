package modelo;

// Resultado de la prueba Kolmogorov-Smirnov
public class ResultadoKS {
    public final double dPositiva;
    public final double dNegativa;
    public final double d;
    public final double p;
    public final double critico;    // D crítico para alfa = 0.05
    public final boolean rechaza;

    public ResultadoKS(double dPositiva, double dNegativa, double p, double critico) {
        this.dPositiva = dPositiva;
        this.dNegativa = dNegativa;
        this.d = Math.max(dPositiva, dNegativa);
        this.p = p;
        this.critico = critico;
        this.rechaza = p < Resultado.ALFA;
    }
}
