package clasesPrincipales;

import clasesAuxiliares.Cocina;
import clasesAuxiliares.Mesa;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.Semaphore;

public class Restaurante implements Runnable {
    public Random random = new Random();

    public static Cocina cocina = new Cocina();
    public Cocinero[] cocineros = new Cocinero[Configuracion.C];
    public Mozo[] mozos = new Mozo[Configuracion.Z];
    public Cajero[] cajeros = new Cajero[Configuracion.Y];

    public ConcurrentLinkedQueue<Cliente> filaClientes = new ConcurrentLinkedQueue<>();
    public static final LinkedBlockingQueue<Cliente> filaClientesPagar = new LinkedBlockingQueue<>();
    public static ArrayBlockingQueue<Mesa> mesasLibres = new ArrayBlockingQueue<>(Configuracion.M);
    public static LinkedBlockingQueue<Mesa> mesasPorAtender = new LinkedBlockingQueue<>(Configuracion.M);

    public static volatile boolean abierto = true;

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

                    filaClientes.add(cliente);
                    Utils.log("Restaurante", "Llega el " + cliente + " (en la fila: " + filaClientes.size() + ")");

                    semaphore.release();
                }
            } catch (InterruptedException ex) {
                return;
            }

        });

        Thread asignacionDeClietesThread = new Thread(() -> {
            try {
                while (true) {
                    semaphore.acquire(Configuracion.P);
                    Utils.log("Restaurante", "Hay un grupo de " + Configuracion.P + " clientes, busca una mesa libre");

                    Mesa mesa = esperarMesaLibre();

                    if (mesa == null)
                        break;

                    List<Cliente> grupo = new LinkedList<>();
                    for (int i = 0; i < Configuracion.P; i++)
                        grupo.add(filaClientes.poll());

                    Utils.log("Restaurante", "Asigna la mesa " + mesa.numero + " a: " + grupo);

                    for (Cliente cliente : grupo)
                        mesa.sentarse(cliente);
                }
            } catch (InterruptedException ex) {
                return;
            }

        });

        llegadaClientesThread.start();
        asignacionDeClietesThread.start();

        try {
            Thread.sleep(Configuracion.T);
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
        }

        Utils.log("Restaurante", "Cierra el restaurante");
        abierto = false;

        llegadaClientesThread.interrupt();
        asignacionDeClietesThread.interrupt();

        try {
            llegadaClientesThread.join();
            asignacionDeClietesThread.join();
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
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
