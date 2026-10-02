import java.util.Random;

public class Restaurante implements Runnable {
    public Random random;
    public boolean open;

    public Mesa[] mesas;

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

        while (open) {
            long time = Utils.RandomBetween(random, Configuracion.TPmin, Configuracion.TPmax);

            try {
                Thread.sleep(time);
            } catch (Exception ex) {

            }

            Utils.printMesas(this.mesas);

            Cliente cliente = new Cliente();

            // System.out.println("Llego un nuevo cliente - " + time + "ms");

            Mesa mesa = getMesaLibre();

            if (mesa != null) {
                cliente.mesa = mesa;

                // System.out.println("Se sento en la mesa: " + mesa.numero);

                Thread clienteThread = new Thread(cliente);
                clienteThread.start();
            } else {
                // System.out.println("[!] No hay mesas disponibles.");
            }
        }
    }

    public synchronized Mesa getMesaLibre() {
        Mesa selectedMesa = null;

        for (Mesa mesa : mesas)
            if (mesa.lugarLibre.get() != Configuracion.P && !mesa.ocupada) {
                if (selectedMesa == null || mesa.lugarLibre.get() > selectedMesa.lugarLibre.get())
                    selectedMesa = mesa;
            }

        return selectedMesa;
    }

    public void cerrar() {
        open = false;
    }
}
