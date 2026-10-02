import java.util.Random;

public class Cliente implements Runnable {
    public Random random;
    public Mesa mesa;

    public int lugarEnMesa;
    public boolean mirandoMenu;
    public boolean esperando;
    public boolean comiendo;
    public boolean pagando;

    public Cliente() {
        this.random = new Random();
    }

    public void leerMenu() {
        // System.out.println("Leyendo Menu...");
        this.mirandoMenu = true;

        long time = Utils.RandomBetween(random, Configuracion.TMmin, Configuracion.TMmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }

        // System.out.println("Menu leido - " + time + "ms");
        this.mirandoMenu = false;
    }

    public void comer() {
        // System.out.println("Comiendo...");
        this.comiendo = true;

        long time = Utils.RandomBetween(random, Configuracion.TQmin, Configuracion.TQmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }

        this.comiendo = false;
        // System.out.println("Terminado de comer - " + time + "ms");
    }

    public void sentarse(Mesa mesa) {
    }

    @Override
    public void run() {
        // 1. Se sienta.
        mesa.sentarse(this);

        // 2. Lee menu.
        leerMenu();

        this.esperando = true;

        // Esperamos a que toda la mesa lea el menu antes de avisar al mozo.
        try {
            mesa.barrier.await();
        } catch (Exception ex) {

        }

        // 3. Avisa al mozo.

        // 4. Espera la comida

        this.esperando = false;

        // 5. Come
        comer();

        // 6. Paga

        // 7. Se va
        mesa.levantarse(this);
    }

    @Override
    public String toString() {
        if (this.comiendo)
            return "C";
        else if (this.esperando)
            return "E";
        else if (this.mirandoMenu)
            return "M";
        else if (this.pagando)
            return "P";
        return "S";
    }
}