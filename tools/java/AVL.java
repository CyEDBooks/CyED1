import java.util.ArrayList;
import java.util.List;

public class AVL<T extends Comparable<T>> {

    private static class Nodo<T> {
        T llave;
        Nodo<T> izq;
        Nodo<T> der;
        int altura = 1;                 // altura en nodos del subárbol

        Nodo(T llave) {
            this.llave = llave;
        }
    }

    private Nodo<T> raiz;

    private int altura(Nodo<T> n) {
        return n == null ? 0 : n.altura;
    }

    private void actualizar(Nodo<T> n) {
        n.altura = 1 + Math.max(altura(n.izq), altura(n.der));
    }

    // fb(v) = altura del subárbol derecho - altura del subárbol izquierdo
    private int fb(Nodo<T> n) {
        return altura(n.der) - altura(n.izq);
    }

    private Nodo<T> rotarIzquierda(Nodo<T> x) {
        Nodo<T> y = x.der;
        x.der = y.izq;
        y.izq = x;
        actualizar(x);
        actualizar(y);
        return y;
    }

    private Nodo<T> rotarDerecha(Nodo<T> y) {
        Nodo<T> x = y.izq;
        y.izq = x.der;
        x.der = y;
        actualizar(y);
        actualizar(x);
        return x;
    }

    private Nodo<T> rebalancear(Nodo<T> p) {
        actualizar(p);
        if (fb(p) == 2) {
            if (fb(p.der) < 0) {
                p.der = rotarDerecha(p.der);    // caso C: rotación doble
            }
            return rotarIzquierda(p);           // casos A y B
        }
        if (fb(p) == -2) {
            if (fb(p.izq) > 0) {
                p.izq = rotarIzquierda(p.izq);  // caso F: rotación doble
            }
            return rotarDerecha(p);             // casos D y E
        }
        return p;
    }

    public void insertar(T k) {
        raiz = insertar(raiz, k);
    }

    private Nodo<T> insertar(Nodo<T> x, T k) {
        if (x == null) {
            return new Nodo<>(k);
        }
        if (k.compareTo(x.llave) < 0) {
            x.izq = insertar(x.izq, k);
        } else {
            x.der = insertar(x.der, k);
        }
        return rebalancear(x);        // de abajo hacia arriba, por el camino de la inserción
    }

    public List<T> preorden() {
        List<T> res = new ArrayList<>();
        preorden(raiz, res);
        return res;
    }

    private void preorden(Nodo<T> x, List<T> res) {
        if (x != null) {
            res.add(x.llave);
            preorden(x.izq, res);
            preorden(x.der, res);
        }
    }

    public int altura() {
        return altura(raiz);
    }

    public static void main(String[] args) {
        AVL<Integer> t = new AVL<>();
        for (int k = 1; k <= 7; k++) {
            t.insertar(k);
        }
        System.out.println("1..7 -> preorden " + t.preorden() + ", altura " + t.altura());
        AVL<Integer> u = new AVL<>();
        for (int k : new int[] {50, 20, 70, 10, 30, 25}) {
            u.insertar(k);
        }
        System.out.println("50 20 70 10 30 25 -> preorden " + u.preorden() + ", altura " + u.altura());
    }
}
