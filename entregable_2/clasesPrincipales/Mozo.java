package clasesPrincipales;

import clasesAuxiliares.*;
import utilsConfig.Configuracion;
import utilsConfig.Utils;
import utilsConfig.Config;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.LinkedBlockingQueue;


import java.util.concurrent.ThreadLocalRandom;

public class Mozo implements Runnable {

    private final int id;
    public Random random;
    public LinkedBlockingQueue<Tarea> tareas;
    public Cocina cocina;

    public Mozo(int id, Cocina cocina) {
        this.id = id;
        this.tareas = new LinkedBlockingQueue<>();
        this.cocina = cocina;
        this.random = new Random();
    }

    public void agregarTarea(Tarea tarea) {
        tareas.add(tarea);
    }

    private void realizarTarea(Tarea tarea) {
        
        switch (tarea.getTipo()) {
            case ATENDER_MESA:
                tomarPedido(tarea.getMesa());
                break;
        
            case ENTREGAR_COMIDA:
                recogerPlatosCocina();
                break;

            case LIMPIAR_MESA:
                limpiarMesa(tarea.getMesa());
                break;

        }

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
            Pedido pedido = cocina.pedidosListos.take();
            Thread.sleep(time);

            Mesa mesa = pedido.getMesa();
            mesa.comidaLista();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
    }

    private void limpiarMesa(Mesa mesa) {
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
                Tarea tarea = tareas.take();

                realizarTarea(tarea);
                

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
