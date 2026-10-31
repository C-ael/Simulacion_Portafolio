package modelo;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

// Análisis de la secuencia: estadísticas, valores repetidos y período
public class Analisis {

    // Media de los U. Para una uniforme (0,1) se espera 0.5
    public double media(List<Valor> valores) {
        double suma = 0;
        for (Valor v : valores) {
            suma += v.u;
        }
        return suma / valores.size();
    }

    // Varianza de los U. Para una uniforme (0,1) se espera 1/12 = 0.0833
    public double varianza(List<Valor> valores) {
        double media = media(valores);
        double suma = 0;
        for (Valor v : valores) {
            suma += (v.u - media) * (v.u - media);
        }
        return suma / valores.size();
    }

    // Cuántos X se repiten dentro de la secuencia
    public int valoresRepetidos(List<Valor> valores) {
        Set<Long> vistos = new HashSet<>();
        for (Valor v : valores) {
            vistos.add(v.x);
        }
        return valores.size() - vistos.size();
    }

    // Cuenta cuántos pasos pasan hasta volver a la semilla.
    // Devuelve -1 si nunca vuelve a la semilla.
    public long periodo(long a, long c, long m, long semilla) {
        long x = semilla;
        for (long paso = 1; paso <= m; paso++) {
            x = (a * x + c) % m;
            if (x == semilla) {
                return paso;
            }
        }
        return -1;
    }
}
