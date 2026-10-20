import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

public class Dijkstra {

    record Arista(int destino, int peso) { }

    static final int INF = Integer.MAX_VALUE;

    private final List<List<Arista>> adj;
    private final int[] dist;
    private final int[] pred;

    public Dijkstra(int n) {
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        dist = new int[n];
        pred = new int[n];
    }

    public void agregarArista(int u, int v, int w) {
        adj.get(u).add(new Arista(v, w));
        adj.get(v).add(new Arista(u, w));
    }

    public void dijkstra(int s) {
        int n = adj.size();
        boolean[] permanente = new boolean[n];
        Arrays.fill(dist, INF);
        Arrays.fill(pred, -1);
        dist[s] = 0;
        // Cada entrada es {distancia, vértice}; la cola entrega primero la menor distancia.
        PriorityQueue<int[]> cola = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        cola.add(new int[] {0, s});
        while (!cola.isEmpty()) {
            int u = cola.remove()[1];
            if (permanente[u]) {
                continue;   // entrada vieja: u ya tiene su distancia definitiva
            }
            permanente[u] = true;
            for (Arista a : adj.get(u)) {
                int v = a.destino();
                if (!permanente[v] && dist[u] + a.peso() < dist[v]) {
                    dist[v] = dist[u] + a.peso();
                    pred[v] = u;
                    cola.add(new int[] {dist[v], v});
                }
            }
        }
    }

    public String camino(String[] nombres, int v) {
        if (pred[v] == -1) {
            return nombres[v];
        }
        return camino(nombres, pred[v]) + " -> " + nombres[v];
    }

    public static void main(String[] args) {
        String[] nombres = {"Bogota", "Lima", "Quito", "La Paz", "Asuncion", "B. Aires"};
        Dijkstra g = new Dijkstra(6);
        int[][] aristas = {{0, 1, 4}, {0, 2, 2}, {1, 2, 1}, {1, 3, 5}, {1, 4, 7},
                           {2, 3, 8}, {2, 4, 10}, {3, 4, 2}, {3, 5, 6}, {4, 5, 3}};
        for (int[] a : aristas) {
            g.agregarArista(a[0], a[1], a[2]);
        }
        g.dijkstra(0);
        for (int v = 0; v < nombres.length; v++) {
            System.out.println(nombres[v] + ": " + g.dist[v] + "  (" + g.camino(nombres, v) + ")");
        }
    }
}
