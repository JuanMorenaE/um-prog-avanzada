package utilsConfig;

import clasesAuxiliares.Mesa;
import clasesPrincipales.Cliente;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.Random;

public class Utils {
    private static final long INICIO = System.currentTimeMillis();
    private static final PrintWriter archivoLog = abrirArchivoLog("simulacion.txt");

    // Imprime en consola y en simulacion.txt: [segundos desde el inicio] Actor
    // Mensaje
    // synchronized para que las lineas salgan en el mismo orden en los dos lados.
    public static synchronized void log(String actor, String mensaje) {
        double segundos = (System.currentTimeMillis() - INICIO) / 1000.0;
        String linea = String.format("[%6.2fs] %-12s %s", segundos, actor, mensaje);

        System.out.println(linea);
        if (archivoLog != null)
            archivoLog.println(linea);
    }

    private static PrintWriter abrirArchivoLog(String ruta) {
        try {
            // autoFlush = true: cada println se escribe en disco aunque el programa se
            // corte.
            return new PrintWriter(new FileWriter(ruta, StandardCharsets.UTF_8), true);
        } catch (IOException e) {
            System.err.println("No se pudo abrir " + ruta + ", el log solo se muestra en consola");
            return null;
        }
    }

    public static long RandomBetween(Random random, long x, long y) {
        return random.nextLong(y - x + 1) + x;
    }
}