import java.util.Random;

public class Cliente implements Runnable {
    public Random random;
    public Mesa mesa;

    public int lugarEnMesa;

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
        
        System.out.println("Menu leido - " + time + "ms");
    }

    public void comer() {
        System.out.println("Comiendo...");
        long time = Utils.RandomBetween(random, Configuracion.TQmin, Configuracion.TQmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }

        System.out.println("Terminado de comer - " + time + "ms");
    }

    public void sentarse(Mesa mesa) {
    }

    @Override
    public void run() {
        // 1. Se sienta.
        mesa.sentarse(this);

        // 2. Lee menu.
        leerMenu();

        // Esperamos a que toda la mesa lea el menu antes de avisar al mozo.
        try {
            mesa.barrier.await();
        }catch (Exception ex) {

        }

        System.out.println("Todos los clientes de la mesa " + mesa.numero + " leyeron el menu, avisando al mozo.");

        // 3. Avisa al mozo.

        // 4. Espera la comida

        // 5. Come
        comer();

        // 6. Paga

        // 7. Se va
        mesa.levantarse(this);
    }
}