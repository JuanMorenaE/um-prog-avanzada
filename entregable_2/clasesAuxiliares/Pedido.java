package clasesAuxiliares;

import clasesPrincipales.ClienteTakeAway;
import java.util.List;
import java.util.Objects;

public class Pedido {
    public enum Tipo {
        MESA, TAKE_AWAY
    }

    private final Tipo tipo;
    private final Mesa mesa;
    private final ClienteTakeAway clienteTakeAway;
    private final List<Menu> platos;
    private int siguientePlato = 0;
    private int platosTerminados = 0;

    public Pedido(Mesa mesa, List<Menu> platos) {
        this.tipo = Tipo.MESA;
        this.mesa = Objects.requireNonNull(mesa, "El pedido de mesa necesita una mesa");
        this.clienteTakeAway = null;
        this.platos = List.copyOf(platos);
        if (this.platos.isEmpty()) {
            throw new IllegalArgumentException("El pedido debe tener al menos un menu");
        }
    }

    public Pedido(ClienteTakeAway cliente, Menu menu) {
        this.tipo = Tipo.TAKE_AWAY;
        this.mesa = null;
        this.clienteTakeAway = Objects.requireNonNull(cliente, "El pedido para llevar necesita un cliente");
        this.platos = List.of(Objects.requireNonNull(menu, "El pedido para llevar necesita un menu"));
    }

    public Tipo getTipo() {
        return tipo;
    }

    public ClienteTakeAway getClienteTakeAway() {
        return clienteTakeAway;
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
