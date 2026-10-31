package modelo;

import java.util.ArrayList;
import java.util.List;

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

    // Devuelve n valores. La semilla es X(0), por eso el primero es X(1)
    public List<Valor> generar(int cantidad) {
        List<Valor> valores = new ArrayList<>();
        for (int n = 1; n <= cantidad; n++) {
            long valorX = siguiente();
            double u = (double) valorX / m;     // U(n) = X(n) / m, entre 0 y 1
            valores.add(new Valor(n, valorX, u));
        }
        return valores;
    }
}
