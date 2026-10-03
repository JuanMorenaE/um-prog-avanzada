package clasesPrincipales;

import clasesAuxiliares.Cocina;
import clasesAuxiliares.Menu;
import clasesAuxiliares.Mesa;
import clasesAuxiliares.Pedido;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.LinkedBlockingQueue;

public class Mozo implements Runnable {

    private final int id;
    public Random random;

    public LinkedBlockingQueue<Mesa> mesasPorAtender;
    public Cocina cocina;

    public Mozo(int id, Cocina cocina, LinkedBlockingQueue<Mesa> mesasPorAtender) {
        this.id = id;
        this.mesasPorAtender = mesasPorAtender;
        this.cocina = cocina;
        this.random = new Random();
    }

    private void tomarPedido(Mesa mesa) {
        System.out.println("Mozo " + id + " esta tomando el pedido de la mesa " + mesa.numero);
        long time = Utils.RandomBetween(random, Configuracion.TPmin, Configuracion.TPmax);

        try {
            Thread.sleep(time);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        List<Menu> menus = new LinkedList<>();

        for (int i = 0; i < mesa.clientes.length; i++) {
            Cliente cliente = mesa.clientes[i];
            menus.add(cliente.menu);

        }

        cocina.pedidosCocina.add(new Pedido(mesa, menus));

        System.out.println("Mozo " + id + " tomo el pedido de la mesa en " + time + "ms");
    }

    private void recogerPlatosCocina() {
        long time = Utils.RandomBetween(random, Configuracion.TRmin, Configuracion.TRmax);

        try {
            Thread.sleep(time);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void limpiarMesa() {
        long time = Utils.RandomBetween(random, Configuracion.TLmin, Configuracion.TLmax);

        try {
            Thread.sleep(time);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void run() {
        while (true) {
            try {
                Mesa mesa = mesasPorAtender.take();

                tomarPedido(mesa);

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
