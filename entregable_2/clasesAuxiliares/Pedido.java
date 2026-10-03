package clasesAuxiliares;

import java.util.List;
import java.util.Objects;

public class Pedido {

    private final Mesa mesa;
    private final List<Menu> platos;

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

}
