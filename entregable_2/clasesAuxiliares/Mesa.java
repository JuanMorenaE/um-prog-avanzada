package clasesAuxiliares;

import clasesPrincipales.Cliente;
import utilsConfig.Configuracion;

import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.Phaser;

public class Mesa {
    public int numero;
    public boolean ocupada;
    public boolean comidaLista;

    public Cliente[] clientes;
    public int lugarLibre;
    public Phaser phaser;
    public LinkedBlockingQueue<Tarea> tareas;

    public Mesa(int numero, LinkedBlockingQueue<Mesa> mesasPorAtender, LinkedBlockingQueue<Tarea> tareas) {
        this.numero = numero;
        this.clientes = new Cliente[Configuracion.P];
        this.lugarLibre = 0;
        this.tareas = tareas;

        this.phaser = crearPhaser();
    }

    public synchronized void sentarse(Cliente cliente) {

        clientes[lugarLibre] = cliente;
        cliente.lugarEnMesa = lugarLibre;
        cliente.mesa = this;
        lugarLibre++;

        if (lugarLibre == Configuracion.P)
            ocupada = true;

        new Thread(cliente).start();
    }

    public synchronized void levantarse(Cliente cliente) {
        clientes[cliente.lugarEnMesa] = null;
        lugarLibre--;

        if (lugarLibre == 0)
            tareas.add(new Tarea(Tarea.TipoTarea.LIMPIAR_MESA, this, null));
    }

    public synchronized void esperarComida() {
        while (!comidaLista) {
            try {
                wait();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public synchronized void comidaLista() {
        comidaLista = true;
        notifyAll();
    }

    private Phaser crearPhaser() {
        Mesa mesa = this;

        return new Phaser(Configuracion.P) {
            @Override
            protected boolean onAdvance(int phase, int registeredParties) {
                if (phase == 0) {
                    tareas.add(new Tarea(Tarea.TipoTarea.TOMAR_PEDIDO, mesa, null));
                }
                return false;
            }
        };
    }
}
