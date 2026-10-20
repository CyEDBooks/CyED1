import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DFS {

    enum Color { BLANCO, GRIS, NEGRO }

    private final List<List<Integer>> adj;
    private final Color[] color;
    private final int[] d;
    private final int[] f;
    private final int[] pi;
    private int tiempo;

    public DFS(int n) {
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        color = new Color[n];
        d = new int[n];
        f = new int[n];
        pi = new int[n];
    }

    public void agregarArco(int u, int v) {
        adj.get(u).add(v);
    }

    public void dfs() {
        Arrays.fill(color, Color.BLANCO);
        Arrays.fill(pi, -1);
        tiempo = 0;
        for (int u = 0; u < adj.size(); u++) {
            if (color[u] == Color.BLANCO) {
                dfsVisit(u);
            }
        }
    }

    private void dfsVisit(int u) {
        tiempo++;
        d[u] = tiempo;
        color[u] = Color.GRIS;
        for (int v : adj.get(u)) {
            if (color[v] == Color.BLANCO) {
                pi[v] = u;
                dfsVisit(v);
            }
        }
        color[u] = Color.NEGRO;
        tiempo++;
        f[u] = tiempo;
    }

    public static void main(String[] args) {
        String nombres = "uvwxyz";
        DFS g = new DFS(6);
        String[] arcos = {"uv", "ux", "vy", "wy", "wz", "xv", "yx", "zz"};
        for (String a : arcos) {
            g.agregarArco(nombres.indexOf(a.charAt(0)), nombres.indexOf(a.charAt(1)));
        }
        g.dfs();
        for (int u = 0; u < 6; u++) {
            System.out.println(nombres.charAt(u) + ": " + g.d[u] + "/" + g.f[u]);
        }
    }
}
