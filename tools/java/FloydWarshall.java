public class FloydWarshall {

    static final int INF = Integer.MAX_VALUE / 2;   // evita desbordar al sumar dos INF

    private final int n;
    private final int[][] w;
    private final int[][] p;

    public FloydWarshall(int n) {
        this.n = n;
        w = new int[n][n];
        p = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                w[i][j] = (i == j) ? 0 : INF;
                p[i][j] = j;   // P0: ir directo
            }
        }
    }

    public void agregarArco(int u, int v, int peso) {
        w[u][v] = peso;
    }

    public void floydWarshall() {
        for (int k = 0; k < n; k++) {           // pivote
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (w[i][k] + w[k][j] < w[i][j]) {
                        w[i][j] = w[i][k] + w[k][j];
                        p[i][j] = k;            // el recorrido de i a j pasa por k
                    }
                }
            }
        }
    }

    // Inserta pivotes recursivamente, como en las diapositivas.
    public String recorrido(String nombres, int i, int j) {
        int k = p[i][j];
        if (k == j) {
            return nombres.charAt(i) + " -> " + nombres.charAt(j);
        }
        return recorrido(nombres, i, k) + recorrido(nombres, k, j).substring(1);
    }

    public static void main(String[] args) {
        String nombres = "abcd";
        FloydWarshall g = new FloydWarshall(4);
        g.agregarArco(0, 1, 3);
        g.agregarArco(0, 2, 4);
        g.agregarArco(1, 3, 5);
        g.agregarArco(2, 3, 3);
        g.agregarArco(3, 0, 8);
        g.floydWarshall();
        for (int i = 0; i < 4; i++) {
            StringBuilder fila = new StringBuilder();
            for (int j = 0; j < 4; j++) {
                fila.append(String.format("%4d", g.w[i][j]));
            }
            System.out.println(fila);
        }
        System.out.println(g.recorrido(nombres, 0, 3) + "   costo " + g.w[0][3]);
        System.out.println(g.recorrido(nombres, 1, 2) + "   costo " + g.w[1][2]);
    }
}
