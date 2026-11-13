package modelo;

// Chi-cuadrado de bondad de ajuste (1 grado de libertad):
// compara los puntos dentro/fuera observados con los esperados si pi fuera el real
public class PruebaChi {

    public static final double ALFA = 0.05;

    private final Distribuciones distribuciones = new Distribuciones();

    // Guarda el estadístico y el valor p en el resultado
    public void bondadAjuste(ResultadoPi r) {
        double esperadoDentro = r.n * Math.PI / 4;
        double esperadoFuera = r.n - esperadoDentro;
        r.chi2 = Math.pow(r.dentro - esperadoDentro, 2) / esperadoDentro
                + Math.pow((r.n - r.dentro) - esperadoFuera, 2) / esperadoFuera;
        r.p = distribuciones.pValorChi(r.chi2, 1);
    }
}
