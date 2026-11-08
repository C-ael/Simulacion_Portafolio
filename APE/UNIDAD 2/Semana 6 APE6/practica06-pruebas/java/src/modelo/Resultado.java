package modelo;

// Resultado de las dos pruebas para una configuración
public class Resultado {
    public static final double ALFA = 0.05;     // nivel de significancia

    public final Configuracion configuracion;
    public final double[] numeros;
    public final ResultadoChi chi;
    public final ResultadoKS ks;

    public Resultado(Configuracion configuracion, double[] numeros, ResultadoChi chi, ResultadoKS ks) {
        this.configuracion = configuracion;
        this.numeros = numeros;
        this.chi = chi;
        this.ks = ks;
    }
}
