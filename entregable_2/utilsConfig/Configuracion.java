package utilsConfig;

public final class Configuracion {

    // Valores iniciales editables. Todos los tiempos estan en milisegundos.
    public static final long T = 10_000; // Duracion de la simulacion.

    public static final int M = 5; // Cantidad de mesas.
    public static final int P = 4; // Personas por mesa.
    public static final int Z = 3; // Cantidad de mozos.
    public static final int C = 2; // Cantidad de cocineros.
    public static final int Y = 1; // Cantidad de cajas.

    // Intervalo entre llegadas de clientes.
    public static final long TPmin = 500;
    public static final long TPmax = 2_000;

    // Seleccion del menu.
    public static final long TMmin = 1_000;
    public static final long TMmax = 3_000;

    // Tiempo para comer.
    public static final long TQmin = 3_000;
    public static final long TQmax = 6_000;

    // Anotar el pedido y pasarlo a la cocina.
    public static final long TZmin = 500;
    public static final long TZmax = 1_500;

    // Retirar los platos de la cocina y servirlos.
    public static final long TRmin = 500;
    public static final long TRmax = 1_500;

    // Levantar los platos y limpiar la mesa.
    public static final long TLmin = 1_000;
    public static final long TLmax = 2_000;

    // Rango de coccion de referencia; cada menu debe definir su propio rango.
    public static final long TCmin = 2_000;
    public static final long TCmax = 5_000;

    // Cobrar a un cliente.
    public static final long TYmin = 500;
    public static final long TYmax = 1_500;

    // Anexo opcional para grupos de tres integrantes.
    public static final int Q = 4; // Cantidad de sartenes (al menos 2).
    public static final long TWmin = 1_000; // Llegadas de clientes para llevar.
    public static final long TWmax = 3_000;

    public Configuracion() {
    }
}
