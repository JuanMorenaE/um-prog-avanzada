package clasesPrincipales;

import clasesAuxiliares.*;
import utilsConfig.Configuracion;
import utilsConfig.Utils;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.LinkedBlockingQueue;



public class Mozo implements Runnable {

    private final int id;
    public Random random;
    public final LinkedBlockingQueue<Tarea> tareas;
    public Cocina cocina;

    public Mozo(int id, Cocina cocina, LinkedBlockingQueue<Tarea> tareas) {
        this.id = id;
        this.cocina = cocina;
        this.tareas = tareas;
        this.random = new Random();
    }

    public void agregarTarea(Tarea tarea) {
        tareas.add(tarea);
    }

    private void realizarTarea(Tarea tarea) throws InterruptedException {
        
        switch (tarea.getTipo()) {
            case TOMAR_PEDIDO:
                tomarPedido(tarea.getMesa());
                break;

            case ENTREGAR_COMIDA:
                entregarComida(tarea.getPedido());
                break;

            case LIMPIAR_MESA:
                limpiarMesa(tarea.getMesa());
                break;

        }
    }

    private void tomarPedido(Mesa mesa) throws InterruptedException {
        System.out.println("Mozo " + id + " esta tomando el pedido de la mesa " + mesa.numero);
        long time = Utils.RandomBetween(random, Configuracion.TZmin, Configuracion.TZmax);
        Thread.sleep(time);

        List<Menu> menus = new LinkedList<>();

        for (int i = 0; i < mesa.clientes.length; i++) {
            Cliente cliente = mesa.clientes[i];
            menus.add(cliente.menu);

        }

        cocina.agregarPedido(new Pedido(mesa, menus));

        System.out.println("Mozo " + id + " tomo el pedido de la mesa en " + time + "ms");
    }

    private void entregarComida(Pedido pedido) throws InterruptedException {
        if (pedido == null) {
            throw new IllegalArgumentException("La tarea de entrega debe incluir un pedido");
        }
        long time = Utils.RandomBetween(random, Configuracion.TRmin, Configuracion.TRmax);
        Thread.sleep(time);
        pedido.getMesa().comidaLista();
    }

    private void limpiarMesa(Mesa mesa) throws InterruptedException {
        long time = Utils.RandomBetween(random, Configuracion.TLmin, Configuracion.TLmax);

        Thread.sleep(time);
        mesa.ocupada = false;
    }

    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            Tarea tarea = null;
            try {
                tarea = tareas.take();
                realizarTarea(tarea);

            } catch (InterruptedException e) {
                if (tarea != null) {
                    agregarTarea(tarea);
                }
                Thread.currentThread().interrupt();
                return;
            }
        }
    }
}
