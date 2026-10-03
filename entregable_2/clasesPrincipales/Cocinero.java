package clasesPrincipales;

import clasesAuxiliares.Cocina;
import clasesAuxiliares.Menu;
import clasesAuxiliares.TrabajoCocina;
import utilsConfig.Utils;

import java.util.Random;

public class Cocinero implements Runnable {
    public int id;
    public Cocina cocina;

    public Random random = new Random();

    public Cocinero(int id, Cocina cocina) {
        this.id = id;
        this.cocina = cocina;
    }

    @Override
    public void run() {
        while (true) {
            try {
                TrabajoCocina trabajo = cocina.tomarTrabajo();
                cocina.adquirirSartenes();
                try {
                    cocinarMenu(trabajo.getMenu());
                } finally {
                    cocina.liberarSartenes();
                }
                if (trabajo.getPedido().marcarPlatoTerminado()) {
                    cocina.pedidosListos.put(trabajo.getPedido());
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
    }
    // la coccion ocurre fuera del bloqueo de Cocina para q se pueda trabajar en paralelo.
    public void cocinarMenu(Menu menu) throws InterruptedException {
        long time = Utils.RandomBetween(random, menu.getTCmin(), menu.getTCmax());
        Thread.sleep(time);
    }
}
