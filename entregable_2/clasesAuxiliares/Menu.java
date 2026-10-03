package clasesAuxiliares;

public final class Menu {
    private final String nombre;
    private final long TCmin;
    private final long TCmax;

    public Menu(String nombre, long TCmin, long TCmax) {

        this.nombre = nombre;
        this.TCmin = TCmin;
        this.TCmax = TCmax;
    }

    public String getNombre() {
        return nombre;
    }

    public long getTCmin() {
        return TCmin;
    }

    public long getTCmax() {
        return TCmax;
    }
}
