package modelo;

// Generador Congruencial Lineal (LCG)
// Fórmula de la guía: X(n+1) = (a * X(n) + c) mod m
public class GeneradorLCG {

    private final long a;
    private final long c;
    private final long m;
    private long x;             // valor actual: al inicio es la semilla

    public GeneradorLCG(long a, long c, long m, long semilla) {
        this.a = a;
        this.c = c;
        this.m = m;
        this.x = semilla;
    }

    public long siguiente() {
        // Calcula el siguiente valor con la fórmula del LCG
        x = (a * x + c) % m;
        return x;
    }

    // Devuelve los U(n) = X(n) / m, números entre 0 y 1
    // La semilla es X(0), por eso el primer valor generado es X(1)
    public double[] generar(int cantidad) {
        double[] numeros = new double[cantidad];
        for (int i = 0; i < cantidad; i++) {
            numeros[i] = (double) siguiente() / m;
        }
        return numeros;
    }
}
