import clasesAuxiliares.Mesa;
import clasesPrincipales.Cocinero;
import clasesPrincipales.Mozo;
import clasesPrincipales.Restaurante;
import utilsConfig.Configuracion;

public class Main {
    public static void main(String[] args) {
        Restaurante restaurante = new Restaurante();

        // ============================
        // Inicialización

        // Cargamos Mesas
        for (int i = 0; i < Configuracion.M; i++)
            restaurante.mesasLibres.add(new Mesa(i + 1));

        // Cargamos Mozos
        for (int i = 0; i < Configuracion.Z; i++) {
            restaurante.mozos[i] = new Mozo(i + 1);
            new Thread(restaurante.mozos[i]).start();
        }

        // Cargamos Cocineros
        for (int i = 0; i < Configuracion.C; i++) {
            restaurante.cocineros[i] = new Cocinero(i + 1);
            new Thread(restaurante.cocineros[i]).start();
        }

        // ============================

        Thread mainThread = new Thread(restaurante);
        mainThread.start();

        try {
            Thread.sleep(Configuracion.T);
        } catch (InterruptedException _) {
            Thread.currentThread().interrupt();
        }

        mainThread.interrupt();
    }
}
