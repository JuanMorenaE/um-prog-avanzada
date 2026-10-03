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

    public ConcurrentLinkedQueue<Cliente> filaClientes = new ConcurrentLinkedQueue<>();
    public ArrayBlockingQueue<Mesa> mesasLibres = new ArrayBlockingQueue<>(Configuracion.M);
    public static LinkedBlockingQueue<Mesa> mesasPorAtender = new LinkedBlockingQueue<>(Configuracion.M);

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
                Utils.log("Restaurante", "Llega el " + cliente + " (en la fila: " + filaClientes.size() + ")");

                semaphore.release();
            }
        });

        Thread asignacionDeClietesThread = new Thread(() -> {
            while (true) {
                try {
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
