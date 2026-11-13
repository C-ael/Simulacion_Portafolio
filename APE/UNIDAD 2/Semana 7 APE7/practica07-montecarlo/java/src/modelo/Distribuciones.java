package modelo;

// Valor p de la prueba Chi-cuadrado, con fórmulas propias (sin librerías externas)
public class Distribuciones {

    // Coeficientes de la aproximación de Lanczos para calcular log(gamma(x))
    private static final double[] LANCZOS = {0.99999999999980993, 676.5203681218851, -1259.1392167224028,
            771.32342877765313, -176.61502916214059, 12.507343278686905,
            -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7};

    private double logGamma(double x) {
        x -= 1.0;
        double suma = LANCZOS[0];
        for (int i = 1; i < 9; i++) {
            suma += LANCZOS[i] / (x + i);
        }
        double t = x + 7.5;
        return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(suma);
    }

    // Q(a, x): probabilidad de que una Gamma(a) sea mayor que x
    private double gammaIncompletaSuperior(double a, double x) {
        if (x <= 0) {
            return 1.0;
        }
        double prefijo = Math.exp(-x + a * Math.log(x) - logGamma(a));
        if (x < a + 1) {
            // Serie para P(a, x); luego Q = 1 - P
            double termino = 1.0 / a;
            double suma = termino;
            for (int n = 1; n < 1000; n++) {
                termino *= x / (a + n);
                suma += termino;
                if (Math.abs(termino) < Math.abs(suma) * 1e-16) {
                    break;
                }
            }
            return Math.max(0.0, 1.0 - prefijo * suma);
        }
        // Fracción continua para Q(a, x)
        double pequeno = 1e-300;
        double b = x + 1 - a;
        double c = 1 / pequeno;
        double d = 1 / b;
        double h = d;
        for (int i = 1; i < 1000; i++) {
            double an = -i * (i - a);
            b += 2;
            d = an * d + b;
            if (Math.abs(d) < pequeno) {
                d = pequeno;
            }
            c = b + an / c;
            if (Math.abs(c) < pequeno) {
                c = pequeno;
            }
            d = 1 / d;
            double cambio = d * c;
            h *= cambio;
            if (Math.abs(cambio - 1) < 1e-16) {
                break;
            }
        }
        return Math.min(1.0, prefijo * h);
    }

    // P(Chi-cuadrado con 'grados' grados de libertad >= chi2)
    public double pValorChi(double chi2, int grados) {
        return gammaIncompletaSuperior(grados / 2.0, chi2 / 2.0);
    }
}
