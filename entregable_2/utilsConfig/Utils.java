package utilsConfig;
import clasesPrincipales.*;

import clasesAuxiliares.Mesa;
import clasesPrincipales.Cliente;

import java.util.Random;

public class Utils {
    private static final long INICIO = System.currentTimeMillis();

    // Imprime: [segundos desde el inicio] Actor        Mensaje
    public static void log(String actor, String mensaje) {
        double segundos = (System.currentTimeMillis() - INICIO) / 1000.0;
        System.out.printf("[%6.2fs] %-12s %s%n", segundos, actor, mensaje);
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