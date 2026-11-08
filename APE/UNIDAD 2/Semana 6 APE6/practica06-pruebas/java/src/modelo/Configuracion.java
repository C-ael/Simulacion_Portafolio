package modelo;

// Una configuración del generador: nombre y parámetros del LCG
public class Configuracion {
    public final String nombre;
    public final long a;
    public final long c;
    public final long m;
    public final long semilla;

    public Configuracion(String nombre, long a, long c, long m, long semilla) {
        this.nombre = nombre;
        this.a = a;
        this.c = c;
        this.m = m;
        this.semilla = semilla;
    }
}
