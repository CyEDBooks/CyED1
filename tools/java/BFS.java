import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Queue;

public class BFS {

    enum Color { BLANCO, GRIS, NEGRO }

    static final int INF = Integer.MAX_VALUE;

    private final List<List<Integer>> adj;
    private final int[] d;
    private final int[] pi;

    public BFS(int n) {
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        d = new int[n];
        pi = new int[n];
    }

    public void agregarArista(int u, int v) {
        adj.get(u).add(v);
        adj.get(v).add(u);
    }

    public void bfs(int s) {
        int n = adj.size();
        Color[] color = new Color[n];
        Arrays.fill(color, Color.BLANCO);
        Arrays.fill(d, INF);
        Arrays.fill(pi, -1);
        color[s] = Color.GRIS;
        d[s] = 0;
        Queue<Integer> q = new ArrayDeque<>();
        q.add(s);
        while (!q.isEmpty()) {
            int u = q.remove();
            for (int v : adj.get(u)) {
                if (color[v] == Color.BLANCO) {
                    color[v] = Color.GRIS;
                    d[v] = d[u] + 1;
                    pi[v] = u;
                    q.add(v);
                }
            }
            color[u] = Color.NEGRO;
        }
    }

    public String camino(int s, int v) {
        if (v == s) {
            return String.valueOf(s);
        }
        if (pi[v] == -1) {
            return "no hay camino de " + s + " a " + v;
        }
        return camino(s, pi[v]) + " -> " + v;
    }

    public static void main(String[] args) {
        BFS g = new BFS(6);           // vértices 1..5 (el 0 no se usa)
        int[][] aristas = {{1, 2}, {1, 5}, {2, 3}, {2, 4}, {2, 5}, {3, 4}, {4, 5}};
        for (int[] a : aristas) {
            g.agregarArista(a[0], a[1]);
        }
        g.bfs(3);
        for (int v = 1; v <= 5; v++) {
            System.out.println(v + ": d = " + g.d[v] + ", pi = " + (g.pi[v] == -1 ? "NIL" : g.pi[v])
                    + ", camino = " + g.camino(3, v));
        }
    }
}
