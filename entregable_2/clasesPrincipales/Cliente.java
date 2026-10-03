<<<<<<< HEAD:entregable_2/clasesPrincipales/Cliente.java
package clasesPrincipales;

import clasesAuxiliares.Mesa;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

=======
import java.util.LinkedList;
import java.util.List;
>>>>>>> 65cfd3bd7f6f0cb21f4f708acaca63aa97693861:entregable_2/Cliente.java
import java.util.Random;

public class Cliente implements Runnable {
    public Random random;
    public Mesa mesa;

    public Menu menu;

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

        menu = getRandomMenu();
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
        // 1. Lee menu.
        leerMenu();

        // 2. Espera a que todos hayan pedido.
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

    public Menu getRandomMenu() {
        // TODO: Devolver un menu aleatorio entre una lista de menus predefinidos.
        return new Menu("Ejemplo", Configuracion.TCmin, Configuracion.TCmax);
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