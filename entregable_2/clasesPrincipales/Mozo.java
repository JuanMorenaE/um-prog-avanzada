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
    public static final LinkedBlockingQueue<Tarea> tareas = new LinkedBlockingQueue<Tarea>();

    public Mozo(int id) {
        this.id = id;
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

    private void tomarPedido(Mesa mesa) {
        log("Va a tomar el pedido de la mesa " + mesa.numero);
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

        log("Envia a cocina el pedido de la mesa " + mesa.numero + ": " + nombres(menus)
                + " (tardo " + time + "ms)");

        Restaurante.cocina.agregarPedido(new Pedido(mesa, menus));
    }

    private void entregarComida(Pedido pedido) throws InterruptedException {
        if (pedido == null)
            throw new IllegalArgumentException("La tarea de entrega debe incluir un pedido");

        long time = Utils.RandomBetween(random, Configuracion.TRmin, Configuracion.TRmax);

        try {
            Thread.sleep(time);
        } catch (InterruptedException _) {
            Thread.currentThread().interrupt();
        }

        log("Entrega la comida a la mesa " + pedido.getMesa().numero);

        pedido.getMesa().comidaLista();
    }

    private void limpiarMesa(Mesa mesa) {
        log("Limpia la mesa " + mesa.numero);
        long time = Utils.RandomBetween(random, Configuracion.TLmin, Configuracion.TLmax);

        try {
            Thread.sleep(time);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        log("Termina de limpiar la mesa " + mesa.numero + " (tardo " + time + "ms)");

        mesa.ocupada = false;
    }

    private void log(String mensaje) {
        Utils.log("Mozo " + id, mensaje);
    }

    static String nombres(List<Menu> menus) {
        List<String> nombres = new LinkedList<>();
        for (Menu menu : menus)
            nombres.add(menu.getNombre());

        return String.join(", ", nombres);
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
