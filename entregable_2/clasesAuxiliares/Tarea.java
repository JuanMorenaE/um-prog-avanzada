package clasesAuxiliares;

public class Tarea {

    public enum TipoTarea {
        TOMAR_PEDIDO,
        ENTREGAR_COMIDA,
        LIMPIAR_MESA
    }

    private Mesa mesa;
    private TipoTarea tipo;
    private Pedido pedido;

    public Tarea(TipoTarea tipo, Mesa mesa, Pedido pedido) {

        this.tipo = tipo;
        this.mesa = mesa;
        this.pedido = pedido;
    }

    public TipoTarea getTipo() {
        return tipo;
    }

    public Pedido getPedido() {
        return pedido;
    }

    public Mesa getMesa() {
        return mesa;
    }
}
