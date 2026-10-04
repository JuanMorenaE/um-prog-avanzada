package clasesPrincipales;

import clasesAuxiliares.Menu;
import utilsConfig.Configuracion;
import utilsConfig.Utils;
import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
// se separa de Cliente porque no usa mesa ni espera a un grupo

public class ClienteTakeAway implements Runnable {
    public enum Estado {
        ESPERANDO, ACEPTADO, ENTREGADO, CANCELADO
    }

    private Estado estado = Estado.ESPERANDO;
    private static final AtomicInteger contador = new AtomicInteger(0);
    private final Random random = new Random();
    private final CountDownLatch atencionFinalizada = new CountDownLatch(1);
    private Menu menu;
    public final int id;

    public ClienteTakeAway() {
        this.id = contador.incrementAndGet();
    }

    public Menu getMenu() {
        return menu;
    }

    // llamamos el empleado despues de entregar la comida, no al terminar la coccion
    public synchronized Estado getEstado() {
        return estado;
    }

    synchronized boolean aceptarPedido() {
        if (estado != Estado.ESPERANDO) {
            return false;
        }
        estado = Estado.ACEPTADO;
        log("Pedido aceptado, espera el cobro y la entrega");
        return true;
    }

    synchronized void cancelarSinPedido() {
        if (estado == Estado.ESPERANDO) {
            estado = Estado.CANCELADO;
            log("Pedido cancelado, se retira sin pedir");
            atencionFinalizada.countDown();
        }
    }

    public synchronized void recibirPedido() {
        if (estado != Estado.ACEPTADO) {
            throw new IllegalStateException("Solo se puede entregar un pedido aceptado");
        }
        estado = Estado.ENTREGADO;
        log("Pedido entregado");
        atencionFinalizada.countDown();
    }

    @Override
    public void run() {
        try {
            if (!Restaurante.abierto) {
                cancelarSinPedido();
                log("Se retira porque el restaurante esta cerrado");
                return;
            }

            log("Elige un menu para llevar");
            long tiempo = Utils.RandomBetween(random, Configuracion.TMmin, Configuracion.TMmax);
            Thread.sleep(tiempo);
            menu = Configuracion.menus.get(random.nextInt(Configuracion.menus.size()));

            if (!Restaurante.abierto) {
                cancelarSinPedido();
                log("Se retira sin pedir porque cerro el restaurante");
                return;
            }

            log("Elige '" + menu.getNombre() + "' y espera al empleado Take Away");
            EmpleadoTakeAway.agregarCliente(this);
            atencionFinalizada.await();
            if (getEstado() == Estado.ENTREGADO) {
                log("Recibe su pedido y se retira");
            } else {
                log("Se retira sin pedir porque cerro el restaurante");
            }
        } catch (InterruptedException e) {
            EmpleadoTakeAway.retirarCliente(this);
            Thread.currentThread().interrupt();
            log("Se interrumpe la espera del cliente");
        }
    }

    private void log(String mensaje) {
        Utils.log(toString(), mensaje);
    }

    @Override
    public String toString() {
        return "Cliente Take Away " + id;
    }
}
