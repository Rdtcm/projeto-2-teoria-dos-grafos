/* Teste independente: enumera subconjuntos por mascara e compara resultados.
 * Este arquivo NAO faz parte da entrega de um unico fonte ao professor. */
#define main mainProjeto
#include "../grafo.c"
#undef main
#include <assert.h>

static unsigned long mascara(const Panelinha *p) {
    unsigned long m;
    int i;
    m = 0;
    for (i = 0; i < p->tamanho; i++) m |= 1UL << p->membros[i];
    return m;
}

static int bits(unsigned long m) {
    int n;
    n = 0;
    while (m) { n += (int) (m & 1UL); m >>= 1; }
    return n;
}

static void verificar(int n, unsigned long arestas) {
    int adj[6][6], u, v, k, clique, maximal, quantidade, achou, esperado;
    unsigned long m, conjunto, lista[64], familia, intersecao;
    Vertice *G;
    Panelinha *p, *resultado;
    memset(adj, 0, sizeof(adj));
    criarGrafo(&G, n);
    k = 0;
    for (u = 0; u < n; u++) for (v = u + 1; v < n; v++) {
        if (arestas & (1UL << k)) {
            adj[u][v] = adj[v][u] = 1;
            assert(acrescentarAresta(G, n, u, v));
        }
        k++;
    }
    quantidade = 0;
    for (m = 1; m < (1UL << n); m++) {
        if (bits(m) < 3) continue;
        clique = 1;
        for (u = 0; u < n; u++) for (v = u + 1; v < n; v++)
            if ((m & (1UL << u)) && (m & (1UL << v)) && !adj[u][v]) clique = 0;
        if (!clique) continue;
        maximal = 1;
        for (u = 0; u < n; u++) {
            if (m & (1UL << u)) continue;
            achou = 1;
            for (v = 0; v < n; v++)
                if ((m & (1UL << v)) && !adj[u][v]) achou = 0;
            if (achou) maximal = 0;
        }
        if (maximal) lista[quantidade++] = m;
    }
    resultado = encontrarPanelinhas(G, n);
    k = 0;
    for (p = resultado; p != NULL; p = p->prox) {
        conjunto = mascara(p);
        achou = 0;
        for (u = 0; u < quantidade; u++) if (lista[u] == conjunto) achou++;
        assert(achou == 1);
        { Panelinha *q; for (q = p->prox; q != NULL; q = q->prox) assert(mascara(q) != conjunto); }
        k++;
    }
    assert(k == quantidade);
    for (v = 0; v < n; v++) {
        esperado = 0;
        /* Oraculo: testa cada familia de pelo menos duas panelinhas. */
        for (familia = 1; familia < (1UL << quantidade); familia++) {
            if (bits(familia) < 2) continue;
            intersecao = (1UL << n) - 1;
            for (u = 0; u < quantidade; u++)
                if (familia & (1UL << u)) intersecao &= lista[u];
            if (intersecao == (1UL << v)) esperado = 1;
        }
        assert(ehInfluente(resultado, n, v) == esperado);
    }
    for (u = 0; u < n; u++) for (v = u + 1; v < n; v++) {
        int i, j, a, b;
        esperado = 0;
        for (i = 0; i < quantidade; i++) for (j = 0; j < quantidade; j++)
            if (i != j && (lista[i] & (1UL << u)) && (lista[j] & (1UL << v))) esperado = 1;
        assert(amizadeInfluente(resultado, u, v, &a, &b) == esperado);
    }
    destruirPanelinhas(&resultado);
    destruirGrafo(&G, n);
    assert(resultado == NULL && G == NULL);
}

int main(void) {
    int n, i, total;
    unsigned long m, limite;
    Vertice *G;
    Panelinha *p, *lista;
    const unsigned long esperadas[] = {7UL,57UL,224UL,896UL,7680UL,
        28672UL,114688UL,983040UL,3670016UL,14680064UL};
    total = 0;
    for (n = 1; n <= 6; n++) {
        limite = 1UL << (n * (n - 1) / 2);
        for (m = 0; m < limite; m++) { verificar(n, m); total++; }
    }
    criarGrafo(&G, 25);
    for (i = 0; i < (int)(sizeof(AMIZADES)/sizeof(AMIZADES[0])); i++)
        assert(acrescentarAresta(G,25,AMIZADES[i][0],AMIZADES[i][1]));
    lista = encontrarPanelinhas(G,25);
    i = 0;
    for (p = lista; p; p = p->prox) { assert(i < 10); assert(mascara(p) == esperadas[i]); i++; }
    assert(i == 10);
    n = 0;
    for (i = 0; i < 25; i++) n += ehInfluente(lista,25,i);
    assert(n == 9);
    assert(!acrescentarAresta(G,25,-1,0));
    assert(!acrescentarAresta(G,25,0,25));
    destruirPanelinhas(&lista);
    destruirGrafo(&G,25);
    printf("OK: %d grafos simples (1 a 6 vertices), rede de 25 e indices invalidos.\n",total);
    return 0;
}
