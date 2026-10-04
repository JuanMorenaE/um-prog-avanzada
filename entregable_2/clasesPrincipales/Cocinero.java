package clasesPrincipales;

import clasesAuxiliares.Menu;
import clasesAuxiliares.Pedido;
import clasesAuxiliares.Tarea;
import clasesAuxiliares.TrabajoCocina;
import utilsConfig.Utils;

import java.util.Random;

public class Cocinero implements Runnable {
    public int id;

    public Random random = new Random();

    public Cocinero(int id) {
        this.id = id;
    }

    @Override
    public void run() {
        while (true) {
            try {
                log("Esperando", "Espera un plato para cocinar");
                TrabajoCocina trabajo = Restaurante.cocina.tomarTrabajo();
                Pedido pedido = trabajo.getPedido();
                String destino = pedido.getTipo() == Pedido.Tipo.MESA
                        ? "la mesa " + pedido.getMesa().numero
                        : pedido.getClienteTakeAway().toString();
                log("Esperando sartenes", "Toma '" + trabajo.getMenu().getNombre() + "' del pedido de " + destino
                        + ", espera 2 sartenes");

                Restaurante.cocina.adquirirSartenes();
                try {
                    cocinarMenu(trabajo.getMenu());
                } finally {
                    Restaurante.cocina.liberarSartenes();
                }
                log("Plato terminado", "Termina '" + trabajo.getMenu().getNombre() + "' de " + destino + " y libera las sartenes");

                if (trabajo.getPedido().marcarPlatoTerminado()) {
                    log("Pedido completo", "El pedido de " + destino + " esta completo, queda listo para entregar");
                    if (pedido.getTipo() == Pedido.Tipo.TAKE_AWAY) {
                        EmpleadoTakeAway.agregarPedidoListo(pedido);
                    } else {
                        Mozo.agregarTarea(new Tarea(Tarea.TipoTarea.ENTREGAR_COMIDA, null, pedido));
                    }
                }
            } catch (InterruptedException e) {
                log("Terminado", "Termina su turno");
                Thread.currentThread().interrupt();
                return;
            }
        }
    }

    // la coccion ocurre fuera del bloqueo de Cocina para q se pueda trabajar en
    // paralelo.
    public void cocinarMenu(Menu menu) throws InterruptedException {
        long time = Utils.RandomBetween(random, menu.getTCmin(), menu.getTCmax());
        log("Cocinando " + menu.getNombre(), "Consigue las sartenes y cocina '" + menu.getNombre() + "' (" + time + "ms)");
        Thread.sleep(time);
    }

    private void log(String estado, String mensaje) {
        Restaurante.estadoDisplay.actualizarActor("Cocinero " + id, estado, mensaje);
    }
}
