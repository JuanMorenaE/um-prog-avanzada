import java.util.Random;
import java.util.concurrent.LinkedBlockingQueue;

public class Restaurante implements Runnable {
    public Random random;
    public boolean open;

    public Mesa[] mesas;
    public LinkedBlockingQueue<Cliente> filaClientes = new LinkedBlockingQueue<Cliente>();

    public Restaurante() {
        this.random = new Random();
        this.open = false;

        this.mesas = new Mesa[Configuracion.M];
    }

    @Override
    public void run() {
        open = true;

        for (int i = 0; i < Configuracion.M; i++)
            mesas[i] = new Mesa(i + 1);

        Thread asignacionDeClietesThread = new Thread(() -> {
            while (true) {
                try {
                    Cliente[] grupo = new Cliente[Configuracion.P];

                    for (int i = 0; i < Configuracion.P; i++)
                        grupo[i] = filaClientes.take();

                    // TODO: Esperar por una mesa libre, en vez de simplemente consultar.

                    Mesa mesa = getMesaLibre();

                    for (Cliente cliente : grupo)
                        mesa.sentarse(cliente);

                } catch (InterruptedException _) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        Thread llegadaClientesThread = new Thread(() -> {
            while (open) {
                long time = Utils.RandomBetween(random, Configuracion.TPmin, Configuracion.TPmax);

                try {
                    Thread.sleep(time);
                } catch (InterruptedException _) {
                    System.out.println("El restaurante cerro, no se aceptan mas clientes.");
                    Thread.currentThread().interrupt();
                }

                Cliente cliente = new Cliente();
                filaClientes.add(cliente);

                System.out.println(
                        "Llego un nuevo cliente al restaurante, la cola es de " + filaClientes.size() + " clientes");
            }
        });

        asignacionDeClietesThread.start();
        llegadaClientesThread.start();

        try {
            Thread.sleep(Configuracion.T);
        } catch (InterruptedException _) {
            Thread.currentThread().interrupt();
        }

        llegadaClientesThread.interrupt();
    }

    public synchronized Mesa getMesaLibre() {
        Mesa selectedMesa = null;

        for (Mesa mesa : mesas)
            if (mesa.lugarLibre.get() != Configuracion.P && !mesa.ocupada
                    && (selectedMesa == null || mesa.lugarLibre.get() > selectedMesa.lugarLibre.get()))
                selectedMesa = mesa;

        return selectedMesa;
    }

    public void cerrar() {
        open = false;
    }
}
