package clasesPrincipales;

import clasesAuxiliares.Menu;
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
                Restaurante.cocina.adquirirSartenes();
                try {
                    cocinarMenu(trabajo.getMenu());
                } finally {
                    Restaurante.cocina.liberarSartenes();
                }
                if (trabajo.getPedido().marcarPlatoTerminado()) {
                    Restaurante.cocina.pedidosListos.put(trabajo.getPedido());
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
        Thread.sleep(time);
    }
}
