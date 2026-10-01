import java.util.List;
import java.util.Objects;

public class Pedido {
    public enum Estado {
        CREADO, EN_COCINA, EN_PREPARACION, LISTO, ENTREGADO
    }

    private final Mesa mesa;
    private final List<Menu> menus;
    private Estado estado = Estado.CREADO;

    public Pedido(Mesa mesa, List<Menu> menus) {
        this.mesa = Objects.requireNonNull(mesa);
        this.menus = List.copyOf(menus);
        if (this.menus.isEmpty()) {
            throw new IllegalArgumentException("El pedido debe tener al menos un menu");
        }
    }

    public Mesa getMesa() {
        return mesa;
    }

    public List<Menu> getMenus() {
        return menus;
    }

    public synchronized Estado getEstado() {
        return estado;
    }

    public synchronized void cambiarEstado(Estado nuevoEstado) {
        Objects.requireNonNull(nuevoEstado);
        if (nuevoEstado.ordinal() != estado.ordinal() + 1) {
            throw new IllegalStateException("Transicion invalida: " + estado + " -> " + nuevoEstado);
        }
        estado = nuevoEstado;
    }
}
