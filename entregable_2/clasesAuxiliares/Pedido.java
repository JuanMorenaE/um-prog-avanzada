package clasesAuxiliares;

import java.util.List;
import java.util.Objects;

public class Pedido {
    public enum Estado {
        CREADO, TOMADO, EN_PREPARACION, LISTO, ENTREGADO
    }

    private final Mesa mesa;
    private final List<Menu> platos;
    private Estado estado = Estado.CREADO;

    public Pedido(Mesa mesa, List<Menu> platos) {
        this.mesa = mesa;
        this.platos = platos;
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

    public synchronized Estado getEstado() {
        return estado;
    }

    public synchronized void cambiarEstado(Estado nuevoEstado) {
        Objects.requireNonNull(nuevoEstado);
        estado = nuevoEstado;
    }
}
