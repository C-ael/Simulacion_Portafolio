package modelo;

// Cualquier generador de números entre 0 y 1 (el LCG propio o el que trae Java)
public interface Generador {
    double siguiente();
}
