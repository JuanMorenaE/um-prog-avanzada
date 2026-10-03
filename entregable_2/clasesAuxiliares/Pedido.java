package clasesAuxiliares;

import java.util.List;

public class Pedido {

    private final Mesa mesa;
    private final List<Menu> platos;
    private int siguientePlato = 0;
    private int platosTerminados = 0;

    public Pedido(Mesa mesa, List<Menu> platos) {
        this.mesa = mesa;
        this.platos = List.copyOf(platos);
        if (this.platos.isEmpty()) {
            throw new IllegalArgumentException("El pedido debe tener al menos un menu");
        }
    }

    public Mesa getMesa() {
        return mesa;
    }

    public List<Menu> getPlatos() {
        return platos;
    }

    public synchronized boolean hayPlatosPendientes() {
        return siguientePlato < platos.size();
    }

    public synchronized Menu tomarPlatoPendiente() {
        if (!hayPlatosPendientes()) {
            return null;
        }
        return platos.get(siguientePlato++);
    }

    // cada cocinero tien que llamar una sola vez por cada plato que termine
    // solo quien termine el ultimo plato recibe true
    public synchronized boolean marcarPlatoTerminado() {
        if (platosTerminados >= siguientePlato) {
            throw new IllegalStateException("No hay platos asignados pendientes de terminar");
        }
        platosTerminados++;
        return platosTerminados == platos.size();
    }

}
