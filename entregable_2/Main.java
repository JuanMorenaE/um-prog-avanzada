import clasesAuxiliares.Mesa;
import clasesPrincipales.Cocinero;
import clasesPrincipales.Cajero;
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
            Restaurante.mesasLibres.add(new Mesa(i + 1));

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

        // Cargamos Cajeros
        for (int i = 0; i < Configuracion.Y; i++) {
            restaurante.cajeros[i] = new Cajero(i + 1);
            new Thread(restaurante.cajeros[i]).start();
        }

        // ============================

        Thread mainThread = new Thread(restaurante);
        mainThread.start();
    }
}
