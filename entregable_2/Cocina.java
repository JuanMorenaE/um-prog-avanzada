import java.util.Random;
import java.util.concurrent.LinkedBlockingQueue;

public class Cocina {
    public Random random = new Random();

    public LinkedBlockingQueue<Pedido> pedidosCocina = new LinkedBlockingQueue<Pedido>(Configuracion.M);
    public LinkedBlockingQueue<Pedido> pedidosListos = new LinkedBlockingQueue<Pedido>(Configuracion.M);

    public Cocina() {
    }
}
