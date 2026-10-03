package clasesAuxiliares;

public final class TrabajoCocina {
    private final Pedido pedido;
    private final Menu menu;

    public TrabajoCocina(Pedido pedido, Menu menu) {
        this.pedido = pedido;
        this.menu = menu;
    }

    public Pedido getPedido() {
        return pedido;
    }

    public Menu getMenu() {
        return menu;
    }
}
