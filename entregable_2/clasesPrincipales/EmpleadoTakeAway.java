package clasesPrincipales;

import clasesAuxiliares.Pedido;
import utilsConfig.Configuracion;
import utilsConfig.Utils;
import java.util.ArrayDeque;
import java.util.Objects;
import java.util.Queue;
import java.util.Random;

public class EmpleadoTakeAway implements Runnable {
    private static final Object monitor = new Object();
    private static final Queue<Pedido> pedidosListos = new ArrayDeque<>();
    private static boolean cerrado = false;
    private static int pedidosPendientes = 0;
    private final Random random = new Random();

    public static void agregarCliente(ClienteTakeAway cliente) {
        synchronized (monitor) {
            Objects.requireNonNull(cliente);
            if (cerrado || !Restaurante.abierto) {
                cliente.cancelarSinPedido();
                return;
            }
            Restaurante.filaClientesTakeAway.add(cliente);
            monitor.notifyAll();
        }
    }

    public static void retirarCliente(ClienteTakeAway cliente) {
        synchronized (monitor) {
            Restaurante.filaClientesTakeAway.remove(cliente);
            cliente.cancelarSinPedido();
        }
    }

    public static void cerrar() {
        synchronized (monitor) {
            // wl cierre y la aceptacion usan el mismo monitor
            Restaurante.abierto = false;
            cerrado = true;
            ClienteTakeAway cliente;
            while ((cliente = Restaurante.filaClientesTakeAway.poll()) != null) {
                cliente.cancelarSinPedido();
            }
            monitor.notifyAll();
        }
    }

    public static void agregarPedidoListo(Pedido pedido) {
        Objects.requireNonNull(pedido);
        if (pedido.getTipo() != Pedido.Tipo.TAKE_AWAY) {
            throw new IllegalArgumentException("El empleado solo entrega pedidos Take Away");
        }
        synchronized (monitor) {
            pedidosListos.add(pedido);
            monitor.notifyAll();
        }
    }

    @Override
    public void run() {
        try {
            while (!Thread.currentThread().isInterrupted()) {
                Pedido listo;
                ClienteTakeAway cliente = null;
                synchronized (monitor) {
                    while (pedidosListos.isEmpty() && Restaurante.filaClientesTakeAway.isEmpty()) {
                        if (cerrado && pedidosPendientes == 0) {
                            log("Finaliza: todos los pedidos aceptados fueron entregados");
                            return;
                        }
                        monitor.wait();
                    }
                    //la entrega tiene prioridad al seleccionar el siguiente trabajo
                    listo = pedidosListos.poll();
                    if (listo == null) {
                        cliente = Restaurante.filaClientesTakeAway.poll();
                        // Se acepta cuando el empleado comienza a tomar el pedido.
                        if (cliente != null && cliente.aceptarPedido()) {
                            pedidosPendientes++;
                        } else {
                            cliente = null;
                        }
                    }
                }
                
                if (listo != null) {
                    entregarPedido(listo);
                } else if (cliente != null) {
                    atenderCliente(cliente);
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void atenderCliente(ClienteTakeAway cliente) throws InterruptedException {
        log("Toma el pedido de " + cliente);
        Thread.sleep(Utils.RandomBetween(random, Configuracion.TZmin, Configuracion.TZmax));
        log("Cobra a " + cliente);
        Thread.sleep(Utils.RandomBetween(random, Configuracion.TYmin, Configuracion.TYmax));
        Restaurante.cocina.agregarPedido(new Pedido(cliente, cliente.getMenu()));
        log("Envia a cocina el pedido de " + cliente);
    }

    private void entregarPedido(Pedido pedido) throws InterruptedException {
        log("Retira de cocina el pedido de " + pedido.getClienteTakeAway());
        Thread.sleep(Utils.RandomBetween(random, Configuracion.TRmin, Configuracion.TRmax));
        log("Entrega el pedido a " + pedido.getClienteTakeAway());
        pedido.getClienteTakeAway().recibirPedido();
        synchronized (monitor) {
            pedidosPendientes--;
            monitor.notifyAll();
        }
    }

    private void log(String mensaje) {
        Utils.log("Empleado Take Away", mensaje);
    }
}
