import java.util.concurrent.atomic.AtomicInteger;

public class Mesa {
    public int numero;
    public Cliente[] clientes;
    public AtomicInteger lugarLibre;

    public Mesa(int numero) {
        this.numero = numero;
        this.clientes = new Cliente[Configuracion.P];
        this.lugarLibre.set(0);
    }

    public void sentarse(Cliente cliente) {
        int libre = lugarLibre.getAndIncrement();
        clientes[libre] = cliente;
    }
}
