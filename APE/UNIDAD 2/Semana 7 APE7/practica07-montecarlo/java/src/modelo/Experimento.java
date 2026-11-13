package modelo;

// Experimento Monte Carlo: estimar pi con puntos en un cuadrado y un círculo inscrito
//
// Cuadrado de lado 2 (de -1 a 1) y círculo de radio 1 en el centro.
// Área del círculo / área del cuadrado = pi / 4, así que pi ≈ 4 · Nc / N
public class Experimento {

    // Lanza n puntos y cuenta cuántos caen dentro del círculo (x² + y² <= 1)
    private long contarDentro(Generador generador, int n) {
        long dentro = 0;
        for (int i = 0; i < n; i++) {
            double x = 2 * generador.siguiente() - 1;       // número entre -1 y 1
            double y = 2 * generador.siguiente() - 1;
            if (x * x + y * y <= 1) {
                dentro++;
            }
        }
        return dentro;
    }

    public ResultadoPi estimarPi(Generador generador, int n) {
        long inicio = System.nanoTime();
        long dentro = contarDentro(generador, n);
        double tiempoMs = (System.nanoTime() - inicio) / 1e6;
        return new ResultadoPi(n, dentro, tiempoMs);
    }
}
