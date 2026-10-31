import controlador.Controlador;

public class Main {
    public static void main(String[] args) {
        // Con el argumento "periodo" también se mide el período completo (tarda unos 30 segundos)
        boolean medirPeriodo = args.length > 0 && args[0].equals("periodo");
        new Controlador().ejecutar(medirPeriodo);
    }
}
