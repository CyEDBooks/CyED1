import java.util.ArrayList;
import java.util.List;

public class ArbolNArio<T> {

    static class Nodo<T> {
        private final T elem;
        private final List<Nodo<T>> hijos = new ArrayList<>();

        Nodo(T elem) {
            this.elem = elem;
        }

        boolean esHoja() {
            return hijos.isEmpty();
        }

        // Patrón de recorrido total: la raíz cuenta 1 y se suma el peso de cada hijo.
        int darPeso() {
            int peso = 1;
            for (Nodo<T> h : hijos) {
                peso += h.darPeso();
            }
            return peso;
        }

        int darNroHojas() {
            if (esHoja()) {
                return 1;
            }
            int hojas = 0;
            for (Nodo<T> h : hijos) {
                hojas += h.darNroHojas();
            }
            return hojas;
        }

        // Altura = número de nodos de la rama más larga.
        int darAltura() {
            int maxAltura = 0;
            for (Nodo<T> h : hijos) {
                maxAltura = Math.max(maxAltura, h.darAltura());
            }
            return maxAltura + 1;
        }

        // Patrón de descenso recursivo: se detiene apenas encuentra el elemento.
        Nodo<T> buscar(T e) {
            if (elem.equals(e)) {
                return this;
            }
            for (Nodo<T> h : hijos) {
                Nodo<T> r = h.buscar(e);
                if (r != null) {
                    return r;
                }
            }
            return null;
        }
    }

    private Nodo<T> raiz;

    // Primer nivel: trata el árbol vacío y delega en la raíz.
    public int darPeso() {
        return raiz == null ? 0 : raiz.darPeso();
    }

    public int darNroHojas() {
        return raiz == null ? 0 : raiz.darNroHojas();
    }

    public int darAltura() {
        return raiz == null ? 0 : raiz.darAltura();
    }

    public void insertar(T padre, T elem) {
        if (raiz == null) {
            raiz = new Nodo<>(elem);
            return;
        }
        Nodo<T> p = raiz.buscar(padre);
        if (p == null) {
            throw new IllegalArgumentException("El padre " + padre + " no existe");
        }
        p.hijos.add(new Nodo<>(elem));
    }

    public static void main(String[] args) {
        ArbolNArio<String> t = new ArbolNArio<>();
        t.insertar(null, "a");
        String[][] aristas = {{"a", "b"}, {"a", "c"}, {"a", "d"}, {"b", "e"}, {"b", "f"},
                              {"e", "h"}, {"e", "i"}, {"e", "j"}, {"c", "g"}, {"c", "k"},
                              {"g", "l"}, {"g", "m"}, {"m", "n"}, {"m", "o"}, {"d", "p"},
                              {"d", "q"}};
        for (String[] a : aristas) {
            t.insertar(a[0], a[1]);
        }
        System.out.println("peso = " + t.darPeso());
        System.out.println("hojas = " + t.darNroHojas());
        System.out.println("altura = " + t.darAltura());
    }
}
