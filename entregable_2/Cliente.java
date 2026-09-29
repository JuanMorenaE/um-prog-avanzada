import java.util.Random;

public class Cliente implements Runnable {
    public Random random;

    public Cliente() {
        random = new Random();
    }

    public void leerMenu() {
        long time = Utils.RandomBetween(random, Configuracion.TMmin, Configuracion.TMmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }
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
        // 1. Espera mesa.

        // 2. Se sienta.

        // 3. Lee menu.
        leerMenu();

        // 4. Avisa al mozo.

        // 5. Espera la comida

        // 6. Come
        comer();

        // 7. Paga

        // 8. Se va
    }
}