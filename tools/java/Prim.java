import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class Prim {

    record Arista(int u, int v, int peso) { }

    private final int n;
    private final List<List<Arista>> adj;

    public Prim(int n) {
        this.n = n;
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
    }

    public void agregarArista(int u, int v, int w) {
        Arista a = new Arista(u, v, w);
        adj.get(u).add(a);
        adj.get(v).add(a);
    }

    public List<Arista> prim(int inicio) {
        boolean[] enArbol = new boolean[n];
        List<Arista> arbol = new ArrayList<>();
        PriorityQueue<Arista> candidatas =
                new PriorityQueue<>((a, b) -> Integer.compare(a.peso(), b.peso()));
        enArbol[inicio] = true;
        candidatas.addAll(adj.get(inicio));
        while (arbol.size() < n - 1 && !candidatas.isEmpty()) {
            Arista a = candidatas.remove();
            if (enArbol[a.u()] && enArbol[a.v()]) {
                continue;   // ya no es candidata: crearía un circuito
            }
            int nuevo = enArbol[a.u()] ? a.v() : a.u();
            enArbol[nuevo] = true;
            arbol.add(a);
            for (Arista b : adj.get(nuevo)) {
                if (!enArbol[b.u()] || !enArbol[b.v()]) {
                    candidatas.add(b);
                }
            }
        }
        return arbol;
    }

    public static void main(String[] args) {
        String nombres = "abcdefg";
        Prim g = new Prim(7);
        String[] aristas = {"ab1", "bc2", "ad4", "bd6", "be4", "ce5", "cf6", "de3", "ef8", "dg4",
                            "eg7", "fg3"};
        for (String a : aristas) {
            g.agregarArista(nombres.indexOf(a.charAt(0)), nombres.indexOf(a.charAt(1)),
                    a.charAt(2) - '0');
        }
        int total = 0;
        for (Arista a : g.prim(0)) {
            System.out.println("{" + nombres.charAt(a.u()) + "," + nombres.charAt(a.v()) + "} "
                    + a.peso());
            total += a.peso();
        }
        System.out.println("peso total = " + total);
    }
}
