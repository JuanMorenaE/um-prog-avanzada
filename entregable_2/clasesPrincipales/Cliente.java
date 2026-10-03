package clasesPrincipales;

import clasesAuxiliares.Mesa;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.Random;

public class Cliente implements Runnable {
    public Random random;
    public Mesa mesa;

    public Cliente() {
        this.random = new Random();
    }

    public void leerMenu() {
        System.out.println("Leyendo Menu...");
        long time = Utils.RandomBetween(random, Configuracion.TMmin, Configuracion.TMmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }

        System.out.println("Menu leido.");
    }

    public void comer() {
        long time = Utils.RandomBetween(random, Configuracion.TQmin, Configuracion.TQmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }
    }

    public void sentarse(Mesa mesa) {
    }

    @Override
    public void run() {
        // 1. Se sienta.
        mesa.sentarse(this);

        // 2. Lee menu.
        leerMenu();

        // 3. Avisa al mozo.

        // 4. Espera la comida

        // 5. Come
        comer();

        // 6. Paga

        // 7. Se va
    }
}