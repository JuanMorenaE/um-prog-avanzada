package clasesPrincipales;

import clasesAuxiliares.Cocina;
import clasesAuxiliares.Menu;
import clasesAuxiliares.Pedido;
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
                Pedido pedido = cocina.pedidosCocina.take();
                cocinar(pedido);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public void cocinar(Pedido pedido) {
        int mesa = pedido.getMesa().numero;
        log("Recibe el pedido de la mesa " + mesa + ": " + Mozo.nombres(pedido.getPlatos()));

        for (Menu menu : pedido.getPlatos()) {
            long time = Utils.RandomBetween(random, menu.getTCmin(), menu.getTCmax());
            log("Cocina '" + menu.getNombre() + "' para la mesa " + mesa + " (" + time + "ms)");

            try {
                Thread.sleep(time);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        log("Termina el pedido de la mesa " + mesa);
    }

    private void log(String mensaje) {
        Utils.log("Cocinero " + id, mensaje);
    }
}