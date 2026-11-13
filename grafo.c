/*
 * PROJETO 2 - TEORIA DOS GRAFOS - 2026-2
 * Ryan Ledo     - RA 10352727
 * Renan Horochk - RA 10438120
 * Alef Sousa    - RA 10431891
 * Base: grafo.c fornecido pelo professor (representacao 2026-2).
 * Compativel com ANSI C / C90. Dados demonstrativos ficticios.
 */

/* 
 * REPRESENTACAO DE GRAFOS - Versao 2026-2
 */

#include<stdio.h>
#include<stdlib.h>
#include<limits.h>
#include<string.h>


/* 
 * Estrutura de dados para representar grafos
 */
typedef struct aresta{ /* Celula de uma lista de arestas */
	int    outroExtremo;
	struct aresta *prox;
}Aresta;

typedef struct vertice{  /* Cada vertice tem um ponteiro para uma lista de arestas incidentes nele */
	int nome; /* Indice original do professor */
	const char *nomeReal;
	int idade;
	const char *curso;
	const char *interesse;
	Aresta *a;
}Vertice;

/*
 * Declaracoes das funcoes para manipulacao de grafos 
 */
void criarGrafo(Vertice **G, int ordem);
void destruirGrafo(Vertice **G, int ordem);
int  acrescentarAresta(Vertice G[], int ordem, int v1, int v2);
void imprimirGrafo(Vertice G[], int ordem);

 
/*
 * Criacao de um grafo com ordem predefinida (passada como argumento),
 *   e, inicilamente, sem nenhuma aresta 
 */
void criarGrafo(Vertice **G, int ordem){
	int i;
	*G= (Vertice*) malloc(sizeof(Vertice)*ordem); /* Alcacao dinamica de um vetor de vertices */
	
	if (*G == NULL) { fprintf(stderr, "Sem memoria.\n"); exit(EXIT_FAILURE); }
	for(i=0; i<ordem; i++){
		(*G)[i].nome= i;
		(*G)[i].nomeReal = "";
		(*G)[i].idade = 0;
		(*G)[i].curso = "";
		(*G)[i].interesse = "";
		(*G)[i].a= NULL;    /* Cada vertice sem nenhuma aresta incidente */
	}
}

/*
 * Deasaloca a memoria dinamica usada para armazenar um grafo.
 */
void destruirGrafo(Vertice **G, int ordem){
	int i;
    Aresta *p, *n;
    
	for(i=0; i<ordem; i++){ /* Remove lista de adjacencia de cada vertice */
	    p= (*G)[i].a;
        while (p!= NULL){
              n= p->prox;
              free(p);
              p= n;
        }
	}
    free(*G);
    *G = NULL;  /* Remove o vetor de vertices */
}

/*  
 * Acrescenta uma nova aresta em um grafo previamente criado. 
 *   Devem ser passados os extremos v1 e v2 da aresta a ser acrescentada 
 * Como o grafo nao e orientado, para uma aresta com extremos i e j, quando
 *   i != j, serao criadas, na estrutura de dados, arestas (i,j) e (j,i) .
 */
int acrescentarAresta(Vertice G[], int ordem, int v1, int v2){
    Aresta * A1, *A2;
    
	if (v1<0 || v1 >= ordem) /* Testo se vertices sao validos */
	   return 0;
	if (v2<0 || v2 >= ordem)
	   return 0;
	
	/* Acrescento aresta na lista do vertice v1 */
	A1= (Aresta *) malloc(sizeof(Aresta));
	if (A1 == NULL) return 0;
	A1->outroExtremo= v2;
	A1->prox= G[v1].a;
	G[v1].a= A1;

	if (v1 == v2) return 1; /* Aresta e um laco */

	/* Acrescento aresta na lista do vertice v2 se v2 != v1 */	
	A2= (Aresta *) malloc(sizeof(Aresta));
	if (A2 == NULL) { G[v1].a = A1->prox; free(A1); return 0; }
	A2->outroExtremo= v1;
	A2->prox= G[v2].a;
	G[v2].a= A2;
	
	return 1;
}


/*  
 * Imprime um grafo com uma notacao similar a uma lista de adjacencia.
 */
void imprimirGrafo(Vertice G[], int ordem){
	int i;
	Aresta *aux;

	printf("\nOrdem:   %d",ordem);
	printf("\nLista de Adjacencia:\n");

	for (i=0; i<ordem; i++){
		printf("\n    v%d: ", i);
		aux= G[i].a;
		for( ; aux != NULL; aux= aux->prox)
			printf("  v%d", aux->outroExtremo);
	}
	printf("\n\n");

}

/* Dados da rede: os indices correspondem a posicao nesta tabela.
 * Para alterar a rede, edite apenas PESSOAS e AMIZADES. */
typedef struct pessoa {
    const char *nome;
    int idade;
    const char *curso;
    const char *interesse;
} Pessoa;

static const Pessoa PESSOAS[] = {
    {"Ana Silva", 20, "Computacao", "Programacao"},
    {"Bruno Santos", 21, "Computacao", "Jogos"},
    {"Carla Oliveira", 20, "Matematica", "Xadrez"},
    {"Diego Souza", 22, "Engenharia", "Robotica"},
    {"Elisa Costa", 19, "Design", "Fotografia"},
    {"Felipe Almeida", 21, "Computacao", "Musica"},
    {"Gabriela Lima", 20, "Design", "Cinema"},
    {"Henrique Rocha", 23, "Engenharia", "Ciclismo"},
    {"Isabela Martins", 21, "Matematica", "Leitura"},
    {"Joao Pereira", 20, "Computacao", "Robotica"},
    {"Karen Ribeiro", 22, "Design", "Desenho"},
    {"Lucas Fernandes", 21, "Engenharia", "Futebol"},
    {"Mariana Gomes", 19, "Computacao", "Xadrez"},
    {"Nicolas Barbosa", 20, "Matematica", "Musica"},
    {"Olivia Carvalho", 22, "Design", "Teatro"},
    {"Pedro Araujo", 23, "Engenharia", "Corrida"},
    {"Quezia Melo", 21, "Computacao", "Cinema"},
    {"Rafael Dias", 20, "Matematica", "Jogos"},
    {"Sofia Nunes", 19, "Design", "Leitura"},
    {"Tiago Vieira", 22, "Engenharia", "Fotografia"},
    {"Ursula Teixeira", 21, "Computacao", "Teatro"},
    {"Vitor Moreira", 20, "Matematica", "Ciclismo"},
    {"Wesley Castro", 23, "Engenharia", "Futebol"},
    {"Yasmin Freitas", 19, "Design", "Desenho"},
    {"Zelia Mendes", 22, "Computacao", "Leitura"}
};

static const int AMIZADES[][2] = {
    {0,1}, {0,2}, {1,2},
    {0,3}, {0,4}, {0,5}, {3,4}, {3,5}, {4,5},
    {5,6}, {5,7}, {6,7},
    {7,8}, {7,9}, {8,9},
    {9,10}, {9,11}, {9,12}, {10,11}, {10,12}, {11,12},
    {12,13}, {12,14}, {13,14},
    {14,15}, {14,16}, {15,16},
    {16,17}, {16,18}, {16,19}, {17,18}, {17,19}, {18,19},
    {19,20}, {19,21}, {20,21},
    {21,22}, {21,23}, {22,23},
    {23,24}, /* Zelia tem uma amizade, mas nao participa de panelinhas. */
    {2,6}, {11,15} /* Ligacoes entre grupos sem criar triangulos. */
};

/* Lista dinamica: nao ha limite fixo para o numero de panelinhas. */
typedef struct panelinha {
    int *membros;
    int tamanho;
    struct panelinha *prox;
} Panelinha;

static void *alocar(size_t bytes) {
    void *p;
    p = malloc(bytes);
    if (p == NULL) {
        fprintf(stderr, "Erro: memoria insuficiente.\n");
        exit(EXIT_FAILURE);
    }
    return p;
}

static int saoAmigos(Vertice G[], int u, int v) {
    Aresta *a;
    for (a = G[u].a; a != NULL; a = a->prox)
        if (a->outroExtremo == v) return 1;
    return 0;
}

static int contem(const int membros[], int tamanho, int v) {
    int i;
    for (i = 0; i < tamanho; i++)
        if (membros[i] == v) return 1;
    return 0;
}

static int ligadoATodos(Vertice G[], const int membros[], int tamanho, int v) {
    int i;
    for (i = 0; i < tamanho; i++)
        if (!saoAmigos(G, membros[i], v)) return 0;
    return 1;
}

/* Maximal significa que NENHUM vertice externo pode ampliar a clique.
 * E necessario verificar tambem vertices menores que o ultimo escolhido. */
static int ehMaximal(Vertice G[], int ordem, const int membros[], int tamanho) {
    int v;
    for (v = 0; v < ordem; v++)
        if (!contem(membros, tamanho, v) &&
            ligadoATodos(G, membros, tamanho, v)) return 0;
    return 1;
}

/* Backtracking: gera cliques em ordem crescente, evitando duplicatas.
 * Um ramo so continua quando o novo vertice e amigo de todos os atuais.
 * A representacao consultada continua sendo a lista do professor. */
static void buscarPanelinhas(Vertice G[], int ordem, int membros[],
                            int tamanho, int inicio, Panelinha ***fim) {
    int v;
    Panelinha *nova;
    if (tamanho >= 3 && ehMaximal(G, ordem, membros, tamanho)) {
        nova = (Panelinha *) alocar(sizeof(Panelinha));
        nova->membros = (int *) alocar(sizeof(int) * tamanho);
        memcpy(nova->membros, membros, sizeof(int) * tamanho);
        nova->tamanho = tamanho;
        nova->prox = NULL;
        **fim = nova;
        *fim = &nova->prox;
        return; /* Uma clique maximal nao admite extensoes. */
    }
    for (v = inicio; v < ordem; v++) {
        if (ligadoATodos(G, membros, tamanho, v)) {
            membros[tamanho] = v;
            buscarPanelinhas(G, ordem, membros, tamanho + 1, v + 1, fim);
        }
    }
}

static Panelinha *encontrarPanelinhas(Vertice G[], int ordem) {
    Panelinha *lista, **fim;
    int *membros;
    lista = NULL;
    fim = &lista;
    membros = (int *) alocar(sizeof(int) * (ordem > 0 ? ordem : 1));
    buscarPanelinhas(G, ordem, membros, 0, 0, &fim);
    free(membros);
    return lista;
}

static void destruirPanelinhas(Panelinha **lista) {
    Panelinha *p;
    while (*lista != NULL) {
        p = *lista;
        *lista = p->prox;
        free(p->membros);
        free(p);
    }
}

static void exibirRede(Vertice G[], int ordem) {
    int v, total;
    Aresta *a;
    total = 0;
    printf("REDE SOCIAL - COMUNIDADE UNIVERSITARIA\n");
    printf("Dados demonstrativos; nomes completos, idades, cursos e interesses.\n");
    for (v = 0; v < ordem; v++) {
        printf("\n[%02d] %s | %d anos | %s | %s\n", v, G[v].nomeReal,
               G[v].idade, G[v].curso, G[v].interesse);
        printf("     Amigos: ");
        if (G[v].a == NULL) printf("nenhum");
        for (a = G[v].a; a != NULL; a = a->prox) {
            printf("%s%s", G[a->outroExtremo].nomeReal,
                   a->prox != NULL ? ", " : "");
            if (v < a->outroExtremo) total++;
        }
        printf("\n");
    }
    printf("\nTotal: %d participantes e %d amizades.\n", ordem, total);
}

static void exibirPanelinhas(Vertice G[], const Panelinha *lista) {
    const Panelinha *p;
    int numero, i;
    numero = 0;
    printf("\nPANELINHAS MAXIMAIS (pelo menos 3 participantes)\n");
    for (p = lista; p != NULL; p = p->prox) {
        printf("P%d (%d membros): {", ++numero, p->tamanho);
        for (i = 0; i < p->tamanho; i++)
            printf("%s%s", i ? ", " : "", G[p->membros[i]].nomeReal);
        printf("}\n");
    }
    printf("Total de panelinhas: %d\n", numero);
}

/* Intersecao de TODAS as panelinhas que contem v. Ha uma familia de
 * duas ou mais com intersecao {v} se, e somente se, esta intersecao e {v}.
 * Isso cobre tambem familias de tres ou mais sem um par de intersecao unica. */
static int ehInfluente(const Panelinha *lista, int ordem, int v) {
    const Panelinha *p;
    int u, quantidade, comum;
    quantidade = 0;
    for (p = lista; p != NULL; p = p->prox)
        if (contem(p->membros, p->tamanho, v)) quantidade++;
    if (quantidade < 2) return 0;
    for (u = 0; u < ordem; u++) {
        if (u == v) continue;
        comum = 1;
        for (p = lista; p != NULL; p = p->prox)
            if (contem(p->membros, p->tamanho, v) &&
                !contem(p->membros, p->tamanho, u)) { comum = 0; break; }
        if (comum) return 0;
    }
    return 1;
}

static void exibirInfluentes(Vertice G[], int ordem, const Panelinha *lista) {
    const Panelinha *p;
    int v, numero, total;
    total = 0;
    printf("\nPESSOAS INFLUENTES\n");
    for (v = 0; v < ordem; v++) {
        if (!ehInfluente(lista, ordem, v)) continue;
        total++;
        printf("%s: unico membro comum a", G[v].nomeReal);
        numero = 0;
        for (p = lista; p != NULL; p = p->prox) {
            numero++;
            if (contem(p->membros, p->tamanho, v)) printf(" P%d", numero);
        }
        printf(".\n");
    }
    printf("Total de pessoas influentes: %d\n", total);
}

/* Definicao literal: existem panelinhas distintas P e Q com u em P e
 * v em Q, e a aresta u-v. O enunciado nao exige exclusividade de membros
 * nem que P e Q sejam disjuntas. Retorna um par de testemunhas. */
static int amizadeInfluente(const Panelinha *lista, int u, int v,
                            int *primeira, int *segunda) {
    const Panelinha *p, *q;
    int i, j;
    i = 0;
    for (p = lista; p != NULL; p = p->prox) {
        i++;
        if (!contem(p->membros, p->tamanho, u)) continue;
        j = 0;
        for (q = lista; q != NULL; q = q->prox) {
            j++;
            if (p != q && contem(q->membros, q->tamanho, v)) {
                *primeira = i; *segunda = j;
                return 1;
            }
        }
    }
    return 0;
}

static void exibirAmizadesInfluentes(Vertice G[], int ordem,
                                    const Panelinha *lista) {
    int u, p, q, total;
    Aresta *a;
    total = 0;
    printf("\nAMIZADES INFLUENTES (consulta complementar)\n");
    for (u = 0; u < ordem; u++)
        for (a = G[u].a; a != NULL; a = a->prox)
            if (u < a->outroExtremo &&
                amizadeInfluente(lista, u, a->outroExtremo, &p, &q)) {
                printf("%s (P%d) -- %s (P%d)\n", G[u].nomeReal, p,
                       G[a->outroExtremo].nomeReal, q);
                total++;
            }
    printf("Total de amizades influentes: %d\n", total);
}

int main(void) {
    Vertice *G;
    Panelinha *panelinhas;
    int ordemG, i, u, v;
    ordemG = (int) (sizeof(PESSOAS) / sizeof(PESSOAS[0]));
    criarGrafo(&G, ordemG);
    for (i = 0; i < ordemG; i++) {
        G[i].nomeReal = PESSOAS[i].nome;
        G[i].idade = PESSOAS[i].idade;
        G[i].curso = PESSOAS[i].curso;
        G[i].interesse = PESSOAS[i].interesse;
    }
    for (i = 0; i < (int) (sizeof(AMIZADES) / sizeof(AMIZADES[0])); i++) {
        u = AMIZADES[i][0]; v = AMIZADES[i][1];
        /* A rede social e simples: rejeita indices invalidos, lacos e repeticoes.
         * A funcao original de insercao continua aceitando multigrafos. */
        if (u < 0 || u >= ordemG || v < 0 || v >= ordemG || u == v ||
            saoAmigos(G, u, v) || !acrescentarAresta(G, ordemG, u, v)) {
            fprintf(stderr, "Erro na amizade %d: (%d, %d).\n", i, u, v);
            destruirGrafo(&G, ordemG);
            return EXIT_FAILURE;
        }
    }
    exibirRede(G, ordemG);
    panelinhas = encontrarPanelinhas(G, ordemG);
    exibirPanelinhas(G, panelinhas);
    exibirInfluentes(G, ordemG, panelinhas);
    exibirAmizadesInfluentes(G, ordemG, panelinhas);
    destruirPanelinhas(&panelinhas);
    destruirGrafo(&G, ordemG);
    return EXIT_SUCCESS;
}
