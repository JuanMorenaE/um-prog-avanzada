import java.util.concurrent.ThreadLocalRandom;

public class Mozo implements Runnable {

    private final String nombre;

    public Mozo (String nombre) {

        this.nombre = nombre;

    }

    public String getNombre(){
        return nombre;
    }

    private void tomarPedido() {
        try {
            long tiempo = ThreadLocalRandom.current()
                    .nextLong(Config.TZmin, Config.TZmax + 1);

            Thread.sleep(tiempo);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void recogerPlatosCocina(){


    }

    private void limpiarMesa(){

    }

    @Override 
    public void run() {
    }
}
