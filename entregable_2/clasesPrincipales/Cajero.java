package clasesPrincipales;

import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.Random;

public class Cajero implements Runnable {
    private final int id;
    private final Random random = new Random();

    public Cajero(int id) {
        this.id = id;
    }

    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            Cliente cliente = null;
            try {
                Utils.log("Cajero " + id, "Esperando clientes para cobrar");
                cliente = Utils.retirar(Restaurante.filaClientesPagar, "Caja", "Cajero " + id + " toma un cliente");
                long tiempo = Utils.RandomBetween(random, Configuracion.TYmin, Configuracion.TYmax);
                Utils.log("Cajero " + id, "Cobra a " + cliente + " el menu '" + cliente.menu.getNombre() + "'");
                Thread.sleep(tiempo);
                Utils.log("Cajero " + id, "Termina de cobrar a " + cliente + " (tardo " + tiempo + "ms)");
                cliente.pagoRealizado();
            } catch (InterruptedException e) {
                if (cliente != null) {
                    Utils.encolar(Restaurante.filaClientesPagar, cliente, "Caja", "Se devuelve un cobro pendiente");
                }
                Utils.log("Cajero " + id, "Termina su turno");
                Thread.currentThread().interrupt();
                return;
            }
        }
    }
}
