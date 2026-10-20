import java.util.ArrayList;
import java.util.List;

public class ABB<T extends Comparable<T>> {

    private static class Nodo<T> {
        T llave;
        Nodo<T> izq;
        Nodo<T> der;

        Nodo(T llave) {
            this.llave = llave;
        }
    }

    private Nodo<T> raiz;

    public boolean buscar(T k) {
        Nodo<T> x = raiz;
        while (x != null && k.compareTo(x.llave) != 0) {
            x = k.compareTo(x.llave) < 0 ? x.izq : x.der;
        }
        return x != null;
    }

    public T minimo() {
        Nodo<T> x = raiz;
        while (x.izq != null) {
            x = x.izq;
        }
        return x.llave;
    }

    public void insertar(T k) {
        raiz = insertar(raiz, k);
    }

    // Devuelve la raíz del subárbol después de insertar k en él.
    private Nodo<T> insertar(Nodo<T> x, T k) {
        if (x == null) {
            return new Nodo<>(k);
        }
        if (k.compareTo(x.llave) < 0) {
            x.izq = insertar(x.izq, k);
        } else {
            x.der = insertar(x.der, k);
        }
        return x;
    }

    public void eliminar(T k) {
        raiz = eliminar(raiz, k);
    }

    private Nodo<T> eliminar(Nodo<T> x, T k) {
        if (x == null) {
            return null;                      // k no está
        }
        int c = k.compareTo(x.llave);
        if (c < 0) {
            x.izq = eliminar(x.izq, k);
        } else if (c > 0) {
            x.der = eliminar(x.der, k);
        } else if (x.izq == null) {
            return x.der;                     // casos 1 y 2: cero o un hijo
        } else if (x.der == null) {
            return x.izq;
        } else {
            Nodo<T> s = x.der;                // caso 3: dos hijos
            while (s.izq != null) {
                s = s.izq;                    // sucesor = mínimo del subárbol derecho
            }
            x.llave = s.llave;
            x.der = eliminar(x.der, s.llave);
        }
        return x;
    }

    public List<T> inorden() {
        List<T> res = new ArrayList<>();
        inorden(raiz, res);
        return res;
    }

    private void inorden(Nodo<T> x, List<T> res) {
        if (x != null) {
            inorden(x.izq, res);
            res.add(x.llave);
            inorden(x.der, res);
        }
    }

    public static void main(String[] args) {
        ABB<Integer> t = new ABB<>();
        for (int k : new int[] {12, 5, 18, 2, 9, 15, 19, 13, 17}) {
            t.insertar(k);
        }
        System.out.println("inorden: " + t.inorden());
        System.out.println("buscar 13: " + t.buscar(13) + ", buscar 14: " + t.buscar(14));
        System.out.println("minimo: " + t.minimo());
        t.eliminar(9);
        t.eliminar(5);
        t.eliminar(12);
        System.out.println("después de eliminar 9, 5 y 12: " + t.inorden());
    }
}
