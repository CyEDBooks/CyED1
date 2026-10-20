import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Queue;
import java.util.Set;

public class Jarras {

    record Estado(int a, int b) { }          // a: litros en la jarra de 4, b: en la de 3

    record Nodo(Estado estado, Nodo padre, String operador, int profundidad) { }

    static final int CAP_A = 4;
    static final int CAP_B = 3;

    static boolean esMeta(Estado e) {
        return e.a() == 2;
    }

    static List<Nodo> sucesores(Nodo n) {
        int a = n.estado().a();
        int b = n.estado().b();
        int de4a3 = Math.min(a, CAP_B - b);
        int de3a4 = Math.min(b, CAP_A - a);
        Object[][] ops = {
            {"Llenar 4", new Estado(CAP_A, b)},
            {"Llenar 3", new Estado(a, CAP_B)},
            {"Vaciar 4", new Estado(0, b)},
            {"Vaciar 3", new Estado(a, 0)},
            {"4->3", new Estado(a - de4a3, b + de4a3)},
            {"3->4", new Estado(a + de3a4, b - de3a4)},
        };
        List<Nodo> hijos = new ArrayList<>();
        for (Object[] op : ops) {
            Estado e = (Estado) op[1];
            if (!e.equals(n.estado())) {
                hijos.add(new Nodo(e, n, (String) op[0], n.profundidad() + 1));
            }
        }
        return hijos;
    }

    // Búsqueda preferente por amplitud sin crear estados repetidos.
    static Nodo buscar(Estado inicial) {
        Queue<Nodo> cola = new ArrayDeque<>();
        Set<Estado> creados = new HashSet<>();
        cola.add(new Nodo(inicial, null, null, 0));
        creados.add(inicial);
        while (!cola.isEmpty()) {
            Nodo n = cola.remove();
            if (esMeta(n.estado())) {
                return n;
            }
            for (Nodo h : sucesores(n)) {
                if (creados.add(h.estado())) {
                    cola.add(h);
                }
            }
        }
        return null;
    }

    static void imprimir(Nodo n) {
        if (n.padre() != null) {
            imprimir(n.padre());
            System.out.print(" --" + n.operador() + "--> ");
        }
        System.out.print("(" + n.estado().a() + "," + n.estado().b() + ")");
    }

    public static void main(String[] args) {
        Nodo meta = buscar(new Estado(0, 0));
        imprimir(meta);
        System.out.println();
        System.out.println("profundidad = " + meta.profundidad());
    }
}
