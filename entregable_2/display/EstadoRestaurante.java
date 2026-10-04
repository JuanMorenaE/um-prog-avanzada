package display;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

public final class EstadoRestaurante {
    private final Display display;
    private final long inicio = System.nanoTime();
    private final Map<String, String> actores = new LinkedHashMap<>();
    private final Map<Integer, String> mesas = new LinkedHashMap<>();
    private final Map<String, Integer> colas = new LinkedHashMap<>();
    private long numeroEvento = 0;
    private boolean abierto = true;
    private boolean finalizado = false;

    public EstadoRestaurante(Display display) {
        this.display = Objects.requireNonNull(display);
    }

    public synchronized void actualizarActor(String actor, String estado, String mensaje) {
        registrarCambio(actor, estado, Map.of(), Map.of(), mensaje);
    }

    // Permite informar varios datos del mismo cambio en un unico evento.
    public synchronized void registrarCambio(String actor, String estado,
            Map<Integer, String> cambiosMesas, Map<String, Integer> cambiosColas, String mensaje) {
        comprobarActivo();
        Objects.requireNonNull(actor);
        Objects.requireNonNull(estado);
        Objects.requireNonNull(mensaje);
        Map<Integer, String> nuevasMesas = Map.copyOf(cambiosMesas);
        Map<String, Integer> nuevasColas = Map.copyOf(cambiosColas);
        if (nuevasColas.values().stream().anyMatch(cantidad -> cantidad < 0)) {
            throw new IllegalArgumentException("El tamano de una cola no puede ser negativo");
        }
        actores.put(actor, estado);
        mesas.putAll(nuevasMesas);
        colas.putAll(nuevasColas);
        publicar(actor + ": " + mensaje);
    }

    public synchronized void cambiarApertura(boolean abierto, String mensaje) {
        comprobarActivo();
        Objects.requireNonNull(mensaje);
        this.abierto = abierto;
        publicar(mensaje);
    }

    public synchronized void actualizarMesa(int numero, String estado, String mensaje) {
        comprobarActivo();
        Objects.requireNonNull(estado);
        Objects.requireNonNull(mensaje);
        mesas.put(numero, estado);
        publicar("Mesa " + numero + ": " + mensaje);
    }

    public synchronized void actualizarCola(String nombre, int cantidad, String mensaje) {
        comprobarActivo();
        Objects.requireNonNull(nombre);
        Objects.requireNonNull(mensaje);
        if (cantidad < 0) {
            throw new IllegalArgumentException("El tamano de una cola no puede ser negativo");
        }
        colas.put(nombre, cantidad);
        publicar(mensaje);
    }

    private void publicar(String mensaje) {
        long tiempo = (System.nanoTime() - inicio) / 1_000_000;
        // Actualizar, copiar y encolar ocurren bajo el mismo bloqueo.
        display.publicar(new EventoDisplay(++numeroEvento, tiempo, mensaje, abierto, actores, mesas, colas));
    }

    // Llamar despues de terminar todos los productores de eventos.
    public synchronized void finalizar() {
        if (!finalizado) {
            display.finalizar();
            finalizado = true;
        }
    }

    private void comprobarActivo() {
        if (finalizado) {
            throw new IllegalStateException("El registro del display ya finalizo");
        }
    }
}
