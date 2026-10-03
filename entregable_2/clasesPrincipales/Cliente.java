package clasesPrincipales;

import clasesAuxiliares.Menu;
import clasesAuxiliares.Mesa;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;

public class Cliente implements Runnable {
    private static final AtomicInteger contador = new AtomicInteger(0);

    public final int id;
    public Random random;
    public Mesa mesa;

    public Menu menu;

    public int lugarEnMesa;
    public boolean mirandoMenu;
    public boolean esperando;
    public boolean comiendo;
    public boolean pagando;

    public Cliente() {
        this.id = contador.incrementAndGet();
        this.random = new Random();
    }

    public void leerMenu() {
        this.mirandoMenu = true;
        log("Lee el menu");

        long time = Utils.RandomBetween(random, Configuracion.TMmin, Configuracion.TMmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }

        menu = getRandomMenu();
        this.mirandoMenu = false;
        log("Elige '" + menu.getNombre() + "' (tardo " + time + "ms)");
    }

    public void comer() {
        this.comiendo = true;
        log("Empieza a comer");

        long time = Utils.RandomBetween(random, Configuracion.TQmin, Configuracion.TQmax);

        try {
            Thread.sleep(time);
        } catch (Exception ex) {

        }

        this.comiendo = false;
        log("Termina de comer (tardo " + time + "ms)");
    }

    public void sentarse(Mesa mesa) {
    }

    @Override
    public void run() {
        log("Se sienta en la mesa " + mesa.numero + " (lugar " + (lugarEnMesa + 1) + ")");

        // 1. Lee menu.
        leerMenu();

        // 2. Espera a que todos elijan y que el mozo tome el pedido.
        this.esperando = true;
        log("Espera a que el resto de la mesa elija");
        try {
            mesa.phaser.arriveAndAwaitAdvance();
        } catch (Exception ex) {

        }

        // 3. Espera la comida
        this.esperando = false;
        log("Espera la comida");
        mesa.esperarComida();
        log("Recibe la comida");

        // 4. Esperar a que todos esten servidos para comer.
        mesa.phaser.arriveAndAwaitAdvance();

        // 4. Comer
        comer();

        // 5. Pagar
        // TODO: Ir a pagar.

        // 6. Irse
        log("Se levanta de la mesa " + mesa.numero);
        mesa.levantarse(this);
    }

    private void log(String mensaje) {
        Utils.log(toString(), mensaje);
    }

    @Override
    public String toString() {
        return "Cliente " + id;
    }

    public Menu getRandomMenu() {
        return Configuracion.menus.get(random.nextInt(Configuracion.menus.size()));
    }
}