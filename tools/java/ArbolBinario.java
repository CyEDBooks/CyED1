public class ArbolBinario<T> {

    static class NodoBinario<T> {
        T elem;
        NodoBinario<T> izq;
        NodoBinario<T> der;

        NodoBinario(T elem, NodoBinario<T> izq, NodoBinario<T> der) {
            this.elem = elem;
            this.izq = izq;
            this.der = der;
        }

        boolean esHoja() {
            return izq == null && der == null;
        }

        int darPeso() {
            int peso = 1;
            if (izq != null) {
                peso += izq.darPeso();
            }
            if (der != null) {
                peso += der.darPeso();
            }
            return peso;
        }

        int darAltura() {
            int hi = izq == null ? 0 : izq.darAltura();
            int hd = der == null ? 0 : der.darAltura();
            return 1 + Math.max(hi, hd);
        }

        int contarHojas() {
            if (esHoja()) {
                return 1;
            }
            return (izq == null ? 0 : izq.contarHojas()) + (der == null ? 0 : der.contarHojas());
        }

        // Completo: todo elemento no terminal tiene exactamente dos hijos.
        boolean esCompleto() {
            if (esHoja()) {
                return true;
            }
            if (izq == null || der == null) {
                return false;
            }
            return izq.esCompleto() && der.esCompleto();
        }
    }

    private final NodoBinario<T> raiz;

    public ArbolBinario(NodoBinario<T> raiz) {
        this.raiz = raiz;
    }

    public int darPeso() {
        return raiz == null ? 0 : raiz.darPeso();
    }

    public int darAltura() {
        return raiz == null ? 0 : raiz.darAltura();
    }

    public int contarHojas() {
        return raiz == null ? 0 : raiz.contarHojas();
    }

    public boolean esCompleto() {
        return raiz == null || raiz.esCompleto();
    }

    static <T> NodoBinario<T> n(T e, NodoBinario<T> izq, NodoBinario<T> der) {
        return new NodoBinario<>(e, izq, der);
    }

    public static void main(String[] args) {
        ArbolBinario<Integer> t = new ArbolBinario<>(
                n(10, n(15, n(25, n(7, null, null), n(6, null, null)), null),
                      n(-6, null, n(18, null, null))));
        System.out.println("peso = " + t.darPeso());
        System.out.println("altura = " + t.darAltura());
        System.out.println("hojas = " + t.contarHojas());
        System.out.println("completo = " + t.esCompleto());
    }
}
