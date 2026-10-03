import clasesPrincipales.Restaurante;
import utilsConfig.Configuracion;

public class Main {
    public static void main(String[] args) {
        Restaurante restaurante = new Restaurante();
        
        Thread mainThread = new Thread(restaurante);
        mainThread.start();

        try {
            Thread.sleep(Configuracion.T);
        } catch (Exception ex) {

        }

        restaurante.cerrar();
    }
}