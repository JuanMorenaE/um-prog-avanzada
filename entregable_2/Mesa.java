import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.CyclicBarrier;

public class Mesa {
    public int numero;
    public boolean ocupada;

    public Cliente[] clientes;
    public AtomicInteger lugarLibre;
    public CyclicBarrier barrier;

    public Mesa(int numero) {
        this.numero = numero;
        this.clientes = new Cliente[Configuracion.P];
        this.lugarLibre = new AtomicInteger(0);

        this.barrier = new CyclicBarrier(Configuracion.P);
    }

    public void sentarse(Cliente cliente) {
        int libre = lugarLibre.getAndIncrement();
        clientes[libre] = cliente;
        cliente.lugarEnMesa = libre;

        if (libre == Configuracion.P - 1)
            ocupada = true;
    }

    public void levantarse(Cliente cliente) {
        int libre = lugarLibre.getAndDecrement() - 1;
        clientes[cliente.lugarEnMesa] = null;

        // System.out.println("El cliente de la mesa " + numero + " se levanto, quedan "
        // + libre + " clientes en la mesa.");

        if (libre == 0) {
            ocupada = false;
            // System.out.println("Todos los clientes de la mesa " + numero + " se
            // levantaron, la mesa queda libre.");
        }
    }
}
