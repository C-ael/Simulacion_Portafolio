package modelo;

import java.util.Random;

// Generador que trae Java (java.util.Random), para compararlo con el que trae Python
public class GeneradorNativo implements Generador {

    private final Random azar;

    public GeneradorNativo(long semilla) {
        this.azar = new Random(semilla);
    }

    // Devuelve el siguiente número entre 0 y 1
    @Override
    public double siguiente() {
        return azar.nextDouble();
    }
}
