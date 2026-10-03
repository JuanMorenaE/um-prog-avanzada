package clasesPrincipales;

import clasesAuxiliares.Menu;
import clasesAuxiliares.Tarea;
import clasesAuxiliares.TrabajoCocina;
import utilsConfig.Utils;

import java.util.Random;

public class Cocinero implements Runnable {
    public int id;

    public Random random = new Random();

    public Cocinero(int id) {
        this.id = id;
    }

    @Override
    public void run() {
        while (true) {
            try {
                TrabajoCocina trabajo = Restaurante.cocina.tomarTrabajo();
                int mesa = trabajo.getPedido().getMesa().numero;
                log("Toma '" + trabajo.getMenu().getNombre() + "' del pedido de la mesa " + mesa
                        + ", espera 2 sartenes");

                Restaurante.cocina.adquirirSartenes();
                try {
                    cocinarMenu(trabajo.getMenu());
                } finally {
                    Restaurante.cocina.liberarSartenes();
                }
                log("Termina '" + trabajo.getMenu().getNombre() + "' de la mesa " + mesa + " y libera las sartenes");

                if (trabajo.getPedido().marcarPlatoTerminado()) {
                    log("El pedido de la mesa " + mesa + " esta completo, queda listo para servir");
                    Mozo.tareas.add(new Tarea(Tarea.TipoTarea.ENTREGAR_COMIDA, null, trabajo.getPedido()));
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
    }

    // la coccion ocurre fuera del bloqueo de Cocina para q se pueda trabajar en
    // paralelo.
    public void cocinarMenu(Menu menu) throws InterruptedException {
        long time = Utils.RandomBetween(random, menu.getTCmin(), menu.getTCmax());
        log("Consigue las sartenes y cocina '" + menu.getNombre() + "' (" + time + "ms)");
        Thread.sleep(time);
    }

    private void log(String mensaje) {
        Utils.log("Cocinero " + id, mensaje);
    }
}
