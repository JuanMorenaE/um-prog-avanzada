package display;

import java.io.PrintStream;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public final class Display implements Runnable {
    private static final EventoDisplay FIN = new EventoDisplay(-1, 0, "", false,
            Map.of(), Map.of(), Map.of());
    private final BlockingQueue<EventoDisplay> eventos = new LinkedBlockingQueue<>();
    private final PrintStream salida;
    private final Path archivoLog;
    private volatile IOException errorLog;

    public Display() {
        this(System.out, Path.of("logs", "restaurante.log"));
    }

    public Display(PrintStream salida) {
        this(salida, null);
    }

    public Display(PrintStream salida, Path archivoLog) {
        this.salida = Objects.requireNonNull(salida);
        this.archivoLog = archivoLog;
    }

    public void verificarLog() {
        if (errorLog != null) {
            throw new UncheckedIOException("No se pudo escribir el log del display", errorLog);
        }
    }

    void publicar(EventoDisplay evento) {
        eventos.add(evento);
    }

    void finalizar() {
        // La senal se procesa despues de todos los eventos ya encolados.
        eventos.add(FIN);
    }

    @Override
    public void run() {
        try (BufferedWriter log = abrirLog()) {
            while (true) {
                EventoDisplay evento = eventos.take();
                if (evento == FIN) {
                    return;
                }
                String texto = formatear(evento);
                salida.print(texto);
                if (log != null) {
                    log.write(texto);
                    log.flush();
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } catch (IOException e) {
            errorLog = e;
            salida.println("Error al escribir el log: " + e.getMessage());
        }
    }

    private BufferedWriter abrirLog() throws IOException {
        if (archivoLog == null) {
            return null;
        }
        Path padre = archivoLog.toAbsolutePath().getParent();
        Files.createDirectories(padre);
        return Files.newBufferedWriter(archivoLog, StandardCharsets.UTF_8);
    }

    private String formatear(EventoDisplay evento) {
        StringBuilder texto = new StringBuilder(String.format("%n=== Evento %d | %.2fs | %s ===%n",
                evento.numero(), evento.milisegundos() / 1000.0, evento.abierto() ? "ABIERTO" : "CERRADO"));
        texto.append(evento.mensaje()).append('\n').append("Actores:\n");
        evento.actores().forEach((actor, estado) -> texto.append("  ").append(actor).append(": ").append(estado).append('\n'));
        texto.append("Mesas:\n");
        evento.mesas().forEach((numero, estado) -> texto.append("  Mesa ").append(numero).append(": ").append(estado).append('\n'));
        texto.append("Colas:\n");
        evento.colas().forEach((nombre, cantidad) -> texto.append("  ").append(nombre).append(": ").append(cantidad).append('\n'));
        return texto.toString();
    }
}
