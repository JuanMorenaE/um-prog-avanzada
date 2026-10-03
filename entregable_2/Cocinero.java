import java.util.Random;

public class Cocinero implements Runnable {
    public int id;
    public Cocina cocina;

    public Random random = new Random();

    public Cocinero(int id, Cocina cocina) {
        this.id = id;
        this.cocina = cocina;
    }

    @Override
    public void run() {
        while (true) {
            try {
                Pedido pedido = cocina.pedidosCocina.take();
                cocinar(pedido);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public void cocinar(Pedido pedido) {
        for (Menu menu : pedido.getMenus()) {
            long time = Utils.RandomBetween(random, menu.getTCmin(), menu.getTCmax());

            try {
                Thread.sleep(time);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}