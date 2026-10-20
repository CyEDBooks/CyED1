import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public class Recorridos {

    static class Nodo<T> {
        T elem;
        Nodo<T> izq;
        Nodo<T> der;

        Nodo(T elem, Nodo<T> izq, Nodo<T> der) {
            this.elem = elem;
            this.izq = izq;
            this.der = der;
        }
    }

    static <T> void preorden(Nodo<T> n, List<T> res) {
        if (n == null) {
            return;
        }
        res.add(n.elem);           // raíz
        preorden(n.izq, res);      // subárbol izquierdo
        preorden(n.der, res);      // subárbol derecho
    }

    static <T> void inorden(Nodo<T> n, List<T> res) {
        if (n == null) {
            return;
        }
        inorden(n.izq, res);
        res.add(n.elem);
        inorden(n.der, res);
    }

    static <T> void postorden(Nodo<T> n, List<T> res) {
        if (n == null) {
            return;
        }
        postorden(n.izq, res);
        postorden(n.der, res);
        res.add(n.elem);
    }

    // Por niveles: es BFS sobre el árbol, con una cola.
    static <T> List<T> porNiveles(Nodo<T> raiz) {
        List<T> res = new ArrayList<>();
        Queue<Nodo<T>> cola = new ArrayDeque<>();
        if (raiz != null) {
            cola.add(raiz);
        }
        while (!cola.isEmpty()) {
            Nodo<T> n = cola.remove();
            res.add(n.elem);
            if (n.izq != null) {
                cola.add(n.izq);
            }
            if (n.der != null) {
                cola.add(n.der);
            }
        }
        return res;
    }

    static <T> Nodo<T> n(T e, Nodo<T> izq, Nodo<T> der) {
        return new Nodo<>(e, izq, der);
    }

    public static void main(String[] args) {
        Nodo<Character> raiz =
                n('A', n('C', n('D', n('F', null, null), null),
                              n('G', n('E', null, null), n('J', null, null))),
                       n('B', n('H', n('I', null, null), null), null));
        List<Character> pre = new ArrayList<>();
        List<Character> in = new ArrayList<>();
        List<Character> post = new ArrayList<>();
        preorden(raiz, pre);
        inorden(raiz, in);
        postorden(raiz, post);
        System.out.println("preorden:    " + pre);
        System.out.println("inorden:     " + in);
        System.out.println("postorden:   " + post);
        System.out.println("por niveles: " + porNiveles(raiz));
    }
}
