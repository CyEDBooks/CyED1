import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Kruskal {

    record Arista(int u, int v, int peso) { }

    private final int n;
    private final List<Arista> aristas = new ArrayList<>();
    private int[] padre;

    public Kruskal(int n) {
        this.n = n;
    }

    public void agregarArista(int u, int v, int w) {
        aristas.add(new Arista(u, v, w));
    }

    // Representante de la componente de v: se sube por 'padre' hasta la raíz.
    private int encontrar(int v) {
        while (padre[v] != v) {
            v = padre[v];
        }
        return v;
    }

    public List<Arista> kruskal() {
        padre = new int[n];
        for (int v = 0; v < n; v++) {
            padre[v] = v;   // cada vértice empieza en su propia componente
        }
        List<Arista> ordenadas = new ArrayList<>(aristas);
        ordenadas.sort(Comparator.comparingInt(Arista::peso));
        List<Arista> arbol = new ArrayList<>();
        for (Arista a : ordenadas) {
            int ru = encontrar(a.u());
            int rv = encontrar(a.v());
            if (ru != rv) {
                padre[rv] = ru;   // unir las dos componentes
                arbol.add(a);
                if (arbol.size() == n - 1) {
                    break;
                }
            }
        }
        return arbol;
    }

    public static void main(String[] args) {
        String nombres = "abcdefg";
        Kruskal g = new Kruskal(7);
        String[] aristas = {"ab1", "bc2", "ad4", "bd6", "be4", "ce5", "cf6", "de3", "ef8", "dg4",
                            "eg7", "fg3"};
        for (String a : aristas) {
            g.agregarArista(nombres.indexOf(a.charAt(0)), nombres.indexOf(a.charAt(1)),
                    a.charAt(2) - '0');
        }
        int total = 0;
        for (Arista a : g.kruskal()) {
            System.out.println("{" + nombres.charAt(a.u()) + "," + nombres.charAt(a.v()) + "} "
                    + a.peso());
            total += a.peso();
        }
        System.out.println("peso total = " + total);
    }
}
