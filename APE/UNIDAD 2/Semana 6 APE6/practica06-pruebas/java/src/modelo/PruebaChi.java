package modelo;

// Algoritmo 2: prueba Chi-cuadrado de uniformidad
public class PruebaChi {

    private final Distribuciones distribuciones = new Distribuciones();

    public ResultadoChi aplicar(double[] numeros, int k) {
        double esperada = (double) numeros.length / k;      // frecuencia esperada de cada intervalo
        int[] observadas = new int[k];
        for (double u : numeros) {
            int intervalo = Math.min((int) (u * k), k - 1); // a qué intervalo [i/k, (i+1)/k) pertenece
            observadas[intervalo]++;
        }

        double chi2 = 0.0;
        for (int o : observadas) {
            chi2 += (o - esperada) * (o - esperada) / esperada;
        }

        int grados = k - 1;
        double p = distribuciones.pValorChi(chi2, grados);
        double critico = distribuciones.valorCriticoChi(grados, Resultado.ALFA);
        return new ResultadoChi(observadas, esperada, chi2, grados, p, critico);
    }
}
