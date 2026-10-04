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

    public static void printMesas(Mesa[] mesas) {
        clearConsole();
        System.out.println();
        System.out.println();
        System.out.println();
        System.out.println();
        System.out.println();

        for (Mesa mesa : mesas) {
            System.out.print("Mesa " + mesa.numero + ": ");
            System.out.print(String.join(" | ", getClientesString(mesa)));
            System.out.println("");
        }
    }

    public static String[] getClientesString(Mesa mesa) {
        String[] clientes = new String[Configuracion.P];

        for (int i = 0; i < Configuracion.P; i++) {
            Cliente cliente = mesa.clientes[i];

            if (cliente == null)
                clientes[i] = "-";
            else
                clientes[i] = cliente.toString();
        }

        return clientes;
    }

    public final static void clearConsole() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
}
