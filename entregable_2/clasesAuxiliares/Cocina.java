package clasesAuxiliares;

import utilsConfig.Configuracion;

import java.util.ArrayDeque;
import java.util.Objects;
import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.Semaphore;

public class Cocina {
    private final Queue<Pedido> pedidosCocina = new ArrayDeque<>();
    public final LinkedBlockingQueue<Pedido> pedidosListos = new LinkedBlockingQueue<>(Configuracion.M);
    private final Semaphore sartenes;
    private final Semaphore adquisicionSartenes = new Semaphore(1, true);

    public Cocina() {
        if (Configuracion.Q < 2) { // se marca como Dead code xq el Q es una constante, esta x si se cambia el Q
            throw new IllegalArgumentException("La cocina necesita al menos dos sartenes");
        }
        sartenes = new Semaphore(Configuracion.Q, true);
    }

    public void adquirirSartenes() throws InterruptedException {
        // solo un cocinero puede adquirir el par a la vez, evitando deadlock
        adquisicionSartenes.acquire();
        int adquiridas = 0;
        try {
            sartenes.acquire();
            adquiridas++;
            sartenes.acquire();
            adquiridas++;
        } catch (InterruptedException e) {
            sartenes.release(adquiridas);
            throw e;
        } finally {
            adquisicionSartenes.release();
        }
    }

    // llamar solo despues de adquirir ambas sartenes, desde un finally
    public void liberarSartenes() {
        sartenes.release();
        sartenes.release();
    }

    public synchronized void agregarPedido(Pedido pedido) {
        pedidosCocina.add(Objects.requireNonNull(pedido));
        notifyAll();
    }

    public synchronized TrabajoCocina tomarTrabajo() throws InterruptedException {
        while (true) {
            while (pedidosCocina.isEmpty()) {
                wait();
            }

            Pedido pedido = pedidosCocina.peek();
            Menu menu = pedido.tomarPlatoPendiente();
            if (!pedido.hayPlatosPendientes()) {
                pedidosCocina.remove();
            }
            if (menu != null) {
                return new TrabajoCocina(pedido, menu);
            }
        }
    }
}
