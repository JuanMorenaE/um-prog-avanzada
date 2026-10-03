package clasesPrincipales;

import clasesAuxiliares.Cocina;
import clasesAuxiliares.Mesa;
import clasesAuxiliares.Tarea;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.Random;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.Semaphore;

public class Restaurante implements Runnable {
    public Random random = new Random();

    public Mozo[] mozos;
    public Cocinero[] cocineros;
    public Cocina cocina;

    public ConcurrentLinkedQueue<Cliente> filaClientes = new ConcurrentLinkedQueue<>();
    public ArrayBlockingQueue<Mesa> mesasLibres = new ArrayBlockingQueue<>(Configuracion.M);
    public LinkedBlockingQueue<Mesa> mesasPorAtender = new LinkedBlockingQueue<>(Configuracion.M);

    public LinkedBlockingQueue<Tarea> tareas = new LinkedBlockingQueue<>();

    public Semaphore semaphore = new Semaphore(0);

    public Restaurante() {

    }

    @Override
    public void run() {
        Thread llegadaClientesThread = new Thread(() -> {
            while (true) {
                long time = Utils.RandomBetween(random, Configuracion.TPmin, Configuracion.TPmax);

                try {
                    Thread.sleep(time);
                } catch (InterruptedException _) {
                    Thread.currentThread().interrupt();
                }

                Cliente cliente = new Cliente();

                filaClientes.add(cliente);
                semaphore.release();

                System.out.println(
                        "Llego un nuevo cliente al restaurante, la cola es de " + filaClientes.size()
                                + " clientes");
            }
        });

        Thread asignacionDeClietesThread = new Thread(() -> {
            while (true) {
                try {
                    semaphore.acquire(Configuracion.P);

                    Mesa mesa = esperarMesaLibre();

                    if (mesa == null)
                        break;

                    for (int i = 0; i < Configuracion.P; i++) {
                        Cliente cliente = filaClientes.poll();
                        mesa.sentarse(cliente);
                    }

                    System.out.println("Se asigno la mesa " + mesa.numero + " a " + Configuracion.P + " clientes");

                } catch (InterruptedException _) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        llegadaClientesThread.start();
        asignacionDeClietesThread.start();
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
