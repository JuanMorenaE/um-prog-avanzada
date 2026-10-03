package clasesAuxiliares;

import utilsConfig.Configuracion;

import java.util.ArrayDeque;
import java.util.Objects;
import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;

public class Cocina {
    private final Queue<Pedido> pedidosCocina = new ArrayDeque<>();
    public final LinkedBlockingQueue<Pedido> pedidosListos = new LinkedBlockingQueue<>(Configuracion.M);

    public Cocina() {
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
