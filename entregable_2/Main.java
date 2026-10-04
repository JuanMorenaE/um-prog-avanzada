import clasesAuxiliares.Mesa;
import clasesPrincipales.Cocinero;
import clasesPrincipales.Cajero;
import clasesPrincipales.EmpleadoTakeAway;
import clasesPrincipales.Mozo;
import clasesPrincipales.Restaurante;
import utilsConfig.Configuracion;

public class Main {
    public static void main(String[] args) {
        Restaurante restaurante = new Restaurante();
        Thread displayThread = new Thread(Restaurante.display, "Display");
        displayThread.start();

        // Registrar todos los cocineros antes de que alguno comience a trabajar.
        for (int i = 0; i < Configuracion.C; i++) {
            Restaurante.estadoDisplay.actualizarActor("Cocinero " + (i + 1), "Esperando", "Inicia su turno");
        }

        // ============================
        // Inicialización

        // Cargamos Mesas
        for (int i = 0; i < Configuracion.M; i++) {
            Restaurante.mesasLibres.add(new Mesa(i + 1));
            Restaurante.estadoDisplay.actualizarMesa(i + 1, "Libre", "Inicio de la simulacion");
        }
        for (int i = 0; i < Configuracion.Z; i++) {
            Restaurante.estadoDisplay.actualizarActor("Mozo " + (i + 1), "Esperando", "Inicia su turno");
        }
        for (int i = 0; i < Configuracion.Y; i++) {
            Restaurante.estadoDisplay.actualizarActor("Cajero " + (i + 1), "Esperando", "Inicia su turno");
        }
        Restaurante.estadoDisplay.actualizarActor("Empleado Take Away", "Esperando", "Inicia su turno");
        for (String cola : new String[] { "Clientes afuera", "Caja", "Atencion Take Away", "Entregas Take Away",
                "Tareas de mozos", "Pedidos de mesas", "Pedidos Take Away" }) {
            Restaurante.estadoDisplay.actualizarCola(cola, 0, "Inicializa " + cola);
        }

        // Cargamos Mozos
        for (int i = 0; i < Configuracion.Z; i++) {
            restaurante.mozos[i] = new Mozo(i + 1);
            restaurante.hilosMozos[i] = new Thread(restaurante.mozos[i], "Mozo " + (i + 1));
            restaurante.hilosMozos[i].start();
        }

        // Cargamos Cocineros
        for (int i = 0; i < Configuracion.C; i++) {
            restaurante.cocineros[i] = new Cocinero(i + 1);
            restaurante.hilosCocineros[i] = new Thread(restaurante.cocineros[i], "Cocinero " + (i + 1));
            restaurante.hilosCocineros[i].start();
        }

        // Cargamos Cajeros
        for (int i = 0; i < Configuracion.Y; i++) {
            restaurante.cajeros[i] = new Cajero(i + 1);
            restaurante.hilosCajeros[i] = new Thread(restaurante.cajeros[i], "Cajero " + (i + 1));
            restaurante.hilosCajeros[i].start();
        }

        // Cargamos el empleado dedicado a Take Away
        EmpleadoTakeAway empleadoTakeAway = new EmpleadoTakeAway();
        Thread empleadoTakeAwayThread = new Thread(empleadoTakeAway, "EmpleadoTakeAway");
        empleadoTakeAwayThread.start();

        // ============================

        Thread mainThread = new Thread(restaurante);
        mainThread.start();

        boolean interrumpido = esperarFin(mainThread);
        interrumpido |= esperarFin(empleadoTakeAwayThread);
        Restaurante.estadoDisplay.finalizar();
        interrumpido |= esperarFin(displayThread);
        Restaurante.display.verificarLog();
        if (interrumpido) {
            Thread.currentThread().interrupt();
        }
    }

    private static boolean esperarFin(Thread hilo) {
        boolean interrumpido = false;
        while (true) {
            try {
                hilo.join();
                return interrumpido;
            } catch (InterruptedException e) {
                interrumpido = true;
            }
        }
    }
}
