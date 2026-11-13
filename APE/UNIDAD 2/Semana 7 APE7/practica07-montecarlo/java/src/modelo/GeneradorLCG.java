package modelo;

// Generador Congruencial Lineal (LCG): X(n+1) = (a * X(n) + c) mod m
// Es el mismo de las prácticas anteriores: con la misma semilla da siempre la misma secuencia.
public class GeneradorLCG implements Generador {

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

    // Devuelve el siguiente número entre 0 y 1
    @Override
    public double siguiente() {
        x = (a * x + c) % m;
        return (double) x / m;
    }
}
