package modelo;

import java.util.Arrays;

// Algoritmo 3: prueba Kolmogorov-Smirnov contra la uniforme (0,1)
public class PruebaKS {

    private final Distribuciones distribuciones = new Distribuciones();

    public ResultadoKS aplicar(double[] numeros) {
        double[] ordenados = numeros.clone();
        Arrays.sort(ordenados);
        int n = ordenados.length;

        double dPositiva = 0.0;
        double dNegativa = 0.0;
        for (int i = 1; i <= n; i++) {
            double u = ordenados[i - 1];
            // F(u) = u para la uniforme (0,1); la empírica vale i/n
            dPositiva = Math.max(dPositiva, (double) i / n - u);
            dNegativa = Math.max(dNegativa, u - (double) (i - 1) / n);
        }
        double p = distribuciones.pValorKS(Math.max(dPositiva, dNegativa), n);
        double critico = distribuciones.valorCriticoKS(n, Resultado.ALFA);
        return new ResultadoKS(dPositiva, dNegativa, p, critico);
    }
}
