package utilsConfig;

import clasesAuxiliares.Mesa;
import clasesPrincipales.Cliente;
import clasesPrincipales.Restaurante;

import java.util.Random;
import java.util.concurrent.BlockingQueue;

public class Utils {
    // El display imprime la copia del estado asociada a esta notificacion.
    public static void log(String actor, String mensaje) {
        Restaurante.estadoDisplay.actualizarActor(actor, mensaje, mensaje);
    }

    // La operacion de cola y su notificacion comparten el bloqueo del registro.
    public static <T> void encolar(BlockingQueue<T> cola, T elemento, String nombre, String mensaje) {
        synchronized (Restaurante.estadoDisplay) {
            cola.add(elemento);
            Restaurante.estadoDisplay.actualizarCola(nombre, cola.size(), mensaje);
            Restaurante.estadoDisplay.notifyAll();
        }
    }

    public static <T> T retirar(BlockingQueue<T> cola, String nombre, String mensaje)
            throws InterruptedException {
        synchronized (Restaurante.estadoDisplay) {
            T elemento;
            while ((elemento = cola.poll()) == null) {
                Restaurante.estadoDisplay.wait();
            }
            Restaurante.estadoDisplay.actualizarCola(nombre, cola.size(), mensaje);
            return elemento;
        }
    }

    public static long RandomBetween(Random random, long x, long y) {
        return random.nextLong(y - x + 1) + x;
    }
}
