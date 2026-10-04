package clasesPrincipales;

import clasesAuxiliares.Cocina;
import clasesAuxiliares.Mesa;
import display.Display;
import display.EstadoRestaurante;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;

public class Restaurante implements Runnable {
    public static final Display display = new Display();
    public static final EstadoRestaurante estadoDisplay = new EstadoRestaurante(display);
    private final ExecutorService poolTakeAway = Executors.newCachedThreadPool();
    public Random random = new Random();

    public static Cocina cocina = new Cocina();
    public Cocinero[] cocineros = new Cocinero[Configuracion.C];
    public Thread[] hilosCocineros = new Thread[Configuracion.C];
    public Mozo[] mozos = new Mozo[Configuracion.Z];
    public Thread[] hilosMozos = new Thread[Configuracion.Z];
    public Cajero[] cajeros = new Cajero[Configuracion.Y];
    public Thread[] hilosCajeros = new Thread[Configuracion.Y];

    public ConcurrentLinkedQueue<Cliente> filaClientes = new ConcurrentLinkedQueue<>();
    public static final LinkedBlockingQueue<Cliente> filaClientesPagar = new LinkedBlockingQueue<>();
    public static final LinkedBlockingQueue<ClienteTakeAway> filaClientesTakeAway = new LinkedBlockingQueue<>();
    public static ArrayBlockingQueue<Mesa> mesasLibres = new ArrayBlockingQueue<>(Configuracion.M);
    public static LinkedBlockingQueue<Mesa> mesasPorAtender = new LinkedBlockingQueue<>(Configuracion.M);

    public static volatile boolean abierto = true;

    private static final Object monitorComida = new Object();
    private static int clientesEsperandoComida = 0;

    public Semaphore semaphore = new Semaphore(0);

    public Restaurante() {

    }

    @Override
    public void run() {
        Thread llegadaClientesThread = new Thread(() -> {
            try {
                while (true) {
                    long time = Utils.RandomBetween(random, Configuracion.TPmin, Configuracion.TPmax);
                    Thread.sleep(time);

                    Cliente cliente = new Cliente();
                    Utils.log(cliente.toString(), "Esperando afuera para formar un grupo");

                    synchronized (estadoDisplay) {
                        filaClientes.add(cliente);
                        estadoDisplay.actualizarCola("Clientes afuera", filaClientes.size(), "Llega " + cliente);
                    }
                    Utils.log("Restaurante", "Llega el " + cliente + " (en la fila: " + filaClientes.size() + ")");

                    semaphore.release();
                }
            } catch (InterruptedException ex) {
                return;
            }

        });

        Thread llegadaTakeAwayThread = new Thread(() -> {
            Random randomTakeAway = new Random();
            try {
                while (abierto) {
                    long tiempo = Utils.RandomBetween(randomTakeAway, Configuracion.TWmin, Configuracion.TWmax);
                    Thread.sleep(tiempo);
                    if (!abierto) {
                        return;
                    }

                    // los clientes para llevar entran sin esperar una mesa ni formar un grupo
                    ClienteTakeAway cliente = new ClienteTakeAway();
                    Utils.log(cliente.toString(), "Llega para pedir comida para llevar");
                    Utils.log("Restaurante", "Llega el " + cliente + " para llevar");
                    poolTakeAway.execute(cliente);
                }
            } catch (InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
        }, "LlegadaTakeAway");

        Thread asignacionDeClietesThread = new Thread(() -> {
            try {
                while (true) {
                    semaphore.acquire(Configuracion.P);
                    Utils.log("Restaurante", "Hay un grupo de " + Configuracion.P + " clientes, busca una mesa libre");

                    Mesa mesa = esperarMesaLibre();

                    if (mesa == null)
                        break;

                    List<Cliente> grupo = new LinkedList<>();
                    synchronized (estadoDisplay) {
                        for (int i = 0; i < Configuracion.P; i++)
                            grupo.add(filaClientes.poll());
                        estadoDisplay.actualizarCola("Clientes afuera", filaClientes.size(), "Se forma un grupo para una mesa");
                    }

                    Utils.log("Restaurante", "Asigna la mesa " + mesa.numero + " a: " + grupo);

                    for (Cliente cliente : grupo)
                        mesa.sentarse(cliente);
                }
            } catch (InterruptedException ex) {
                return;
            }

        });

        llegadaClientesThread.start();
        llegadaTakeAwayThread.start();
        asignacionDeClietesThread.start();

        boolean interrumpido = false;
        try {
            Thread.sleep(Configuracion.T);
        } catch (InterruptedException ex) {
            interrumpido = true;
        }

        Utils.log("Restaurante", "Cierra el restaurante");
        EmpleadoTakeAway.cerrar();
        estadoDisplay.cambiarApertura(false, "Cierra el restaurante; continua la atencion pendiente");

        llegadaClientesThread.interrupt();
        llegadaTakeAwayThread.interrupt();
        asignacionDeClietesThread.interrupt();

        // esperar a los generadores antes de cerrar el pool evita nuevos envios
        if (esperarFin(new Thread[] { llegadaClientesThread, llegadaTakeAwayThread, asignacionDeClietesThread }))
            interrumpido = true;

        Cliente sinMesa;
        while ((sinMesa = filaClientes.poll()) != null) {
            Utils.log(sinMesa.toString(), "Se retira sin mesa porque cerro el restaurante");
        }
        estadoDisplay.actualizarCola("Clientes afuera", 0, "Se retiran los clientes sin mesa");

        poolTakeAway.shutdown();
        boolean poolTerminado = false;
        while (!poolTerminado) {
            try {
                poolTerminado = poolTakeAway.awaitTermination(1, TimeUnit.SECONDS);
            } catch (InterruptedException ex) {
                // mantener el cierre ordenado para terminar los pedidos aceptados
                interrumpido = true;
            }
        }
        Utils.log("Restaurante", "Finalizaron todos los clientes Take Away del pool");

        Utils.log("Restaurante", "Espera a que todas las mesas reciban su comida");
        synchronized (monitorComida) {
            while (clientesEsperandoComida > 0) {
                try {
                    monitorComida.wait();
                } catch (InterruptedException ex) {
                    interrumpido = true;
                }
            }
        }

        Utils.log("Restaurante", "No quedan pedidos por cocinar, los cocineros terminan su turno");
        for (Thread hilo : hilosCocineros)
            hilo.interrupt();
        if (esperarFin(hilosCocineros))
            interrumpido = true;

        Utils.log("Restaurante", "Espera a que se desocupen y limpien todas las mesas");
        int mesasDevueltas = 0;
        while (mesasDevueltas < Configuracion.M) {
            try {
                mesasLibres.take();
                mesasDevueltas++;
            } catch (InterruptedException ex) {
                interrumpido = true;
            }
        }

        Utils.log("Restaurante", "Todas las mesas estan libres, los mozos y cajeros terminan su turno");
        for (Thread hilo : hilosMozos)
            hilo.interrupt();
        for (Thread hilo : hilosCajeros)
            hilo.interrupt();
        if (esperarFin(hilosMozos))
            interrumpido = true;
        if (esperarFin(hilosCajeros))
            interrumpido = true;

        Utils.log("Restaurante", "Fin de la jornada, todo el personal termino su turno");

        if (interrumpido) {
            Thread.currentThread().interrupt();
        }
    }

    public static void clienteEsperaComida() {
        synchronized (monitorComida) {
            clientesEsperandoComida++;
        }
    }

    public static void clienteDejaDeEsperarComida() {
        synchronized (monitorComida) {
            clientesEsperandoComida--;
            monitorComida.notifyAll();
        }
    }

    private boolean esperarFin(Thread[] hilos) {
        boolean interrumpido = false;
        for (Thread hilo : hilos) {
            boolean terminado = false;
            while (!terminado) {
                try {
                    hilo.join();
                    terminado = true;
                } catch (InterruptedException ex) {
                    interrumpido = true;
                }
            }
        }
        return interrumpido;
    }

    private synchronized Mesa esperarMesaLibre() {
        try {
            Mesa selectedMesa = mesasLibres.take();
            return selectedMesa;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return null;
        }
    }
}
