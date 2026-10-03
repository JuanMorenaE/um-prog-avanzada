package clasesAuxiliares;

import clasesPrincipales.Cliente;
import utilsConfig.Configuracion;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.LinkedBlockingQueue;

public class Mesa {
    public int numero;
    public boolean ocupada;
    public boolean comidaLista;

    public Cliente[] clientes;
    public AtomicInteger lugarLibre;
    public CyclicBarrier barrier;

    public Mesa(int numero, LinkedBlockingQueue<Mesa> mesasPorAtender) {
        this.numero = numero;
        this.clientes = new Cliente[Configuracion.P];
        this.lugarLibre = new AtomicInteger(0);

        this.barrier = new CyclicBarrier(Configuracion.P, () -> {
            mesasPorAtender.add(this);
        });
    }

    public void sentarse(Cliente cliente) {
        int libre = lugarLibre.getAndIncrement();

        clientes[libre] = cliente;
        cliente.lugarEnMesa = libre;
        cliente.mesa = this;

        if (libre == Configuracion.P - 1)
            ocupada = true;

        new Thread(cliente).start();
    }

    public void levantarse(Cliente cliente) {
        int libre = lugarLibre.getAndDecrement() - 1;
        clientes[cliente.lugarEnMesa] = null;

        if (libre == 0) {
            ocupada = false;
            // TODO: Enviar a los mozos que la mesa esta libre y hay que limpiarla.
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
}
