package clasesAuxiliares;

import clasesPrincipales.Cliente;
import clasesPrincipales.Mozo;
import clasesPrincipales.Restaurante;
import utilsConfig.Configuracion;
import utilsConfig.Utils;

import java.util.concurrent.Phaser;

public class Mesa {
    public int numero;
    public boolean ocupada;
    public boolean comidaLista;

    public Cliente[] clientes;
    public int lugarLibre;
    public Phaser phaser;

    public Mesa(int numero) {
        this.numero = numero;
        this.clientes = new Cliente[Configuracion.P];
        this.lugarLibre = 0;

        this.phaser = crearPhaser();
    }

    public synchronized void sentarse(Cliente cliente) {

        clientes[lugarLibre] = cliente;
        cliente.lugarEnMesa = lugarLibre;
        cliente.mesa = this;
        lugarLibre++;

        if (lugarLibre == Configuracion.P)
            ocupada = true;

        Restaurante.clienteEsperaComida();
        new Thread(cliente).start();
    }

    public synchronized void levantarse(Cliente cliente) {
        clientes[cliente.lugarEnMesa] = null;
        lugarLibre--;

        if (lugarLibre == 0) {
            log("Se fueron todos los clientes, se pide un mozo para limpiar");
            Mozo.tareas.add(new Tarea(Tarea.TipoTarea.LIMPIAR_MESA, this, null));
        }
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

    private void log(String mensaje) {
        Utils.log("Mesa " + numero, mensaje);
    }

    private Phaser crearPhaser() {
        Mesa mesa = this;

        return new Phaser(Configuracion.P) {
            @Override
            protected boolean onAdvance(int phase, int registeredParties) {
                if (phase == 0) {
                    if (!Restaurante.abierto) {
                        mesa.log("El restaurante cerro antes de pedir, los clientes se van");
                        return true;
                    }

                    mesa.log("Todos eligieron, se pide un mozo para tomar el pedido");
                    Mozo.tareas.add(new Tarea(Tarea.TipoTarea.TOMAR_PEDIDO, mesa, null));
                } else if (phase == 1) {
                    mesa.log("Todos estan servidos, empiezan a comer");
                }
                return false;
            }
        };
    }
}
