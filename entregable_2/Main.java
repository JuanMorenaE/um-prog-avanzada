import clasesAuxiliares.Cocina;
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

        restaurante.mozos = new Mozo[Configuracion.Z];
        restaurante.cocineros = new Cocinero[Configuracion.C];
        restaurante.cocina = new Cocina();

        // Cargamos Mesas
        for (int i = 0; i < Configuracion.M; i++)
            restaurante.mesasLibres.add(new Mesa(i + 1, restaurante.mesasPorAtender));

        // Cargamos Mozos
        for (int i = 0; i < Configuracion.Z; i++) {
            restaurante.mozos[i] = new Mozo(i + 1, restaurante.cocina, restaurante.mesasPorAtender);
            new Thread(restaurante.mozos[i]).start();
        }

        // Cargamos Cocineros
        for (int i = 0; i < Configuracion.C; i++) {
            restaurante.cocineros[i] = new Cocinero(i + 1, restaurante.cocina);
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