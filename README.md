# Projeto 2 - Teoria dos Grafos (2026-2)

Implementação em ANSI C90 a partir do `grafo.c` do professor, com listas de
adjacência preservadas. Rede demonstrativa com nomes de pessoas e atributos
fictícios, inicializada por constantes, sem entrada interativa.

Integrantes: Ryan Ledo (10352727), Renan Horochk (10438120) e Alef Sousa (10431891).

## Compilar e executar

```sh
gcc -std=c90 -pedantic-errors -Wall -Wextra -Werror grafo.c -o grafo.exe
./grafo.exe
```

No Windows, execute `grafo.exe` em um terminal aberto. No Dev-C++, abra
`grafo.c` como C, compile e execute. O programa usa somente a biblioteca
padrão de C. A interface do Dev-C++ ainda não foi testada; a compilação GCC
em C90 estrito passou sem avisos.

Resultados conferidos: **25 participantes, 42 amizades, 10 panelinhas,
9 pessoas influentes e 36 amizades influentes**. A consulta complementar
de amizades é opcional para o grupo de três integrantes.

## Arquivos

- `grafo.c`: único fonte necessário para o programa entregue.
- `output/resultado.txt`: saída completa da execução verificada.
- `output/documentacao-revisao.pdf`: documentação de sete páginas, com pendências explícitas.
- `output/projeto2-revisao.zip`: contém somente `grafo.c` e o PDF.
- `docs/rede-social.graphml`: grafo com 25 nós e 42 arestas para abrir no yEd.
- `testes/verificar_saida.py`: oráculo independente da rede entregue; executado com sucesso.
- `testes/testar.c`: bateria exaustiva de todos os grafos simples de 1 a 6 vértices;
  compilou, mas o Controle de Aplicativo do Windows bloqueou sua execução.
- `ferramentas/gerar_documentacao.py`: reproduz o PDF de revisão e o GraphML;
  requer Python e ReportLab. A representação gráfica é uma prévia gerada por código.

## Pendências antes de enviar ao professor

1. Obter a Parte 1 e conferir os requisitos de documentação a que o enunciado remete.
2. Abrir `docs/rede-social.graphml` no **yEd**, elaborar/revisar o desenho e exportá-lo.
   A automação do yEd não foi autorizada nesta sessão. O GraphML e a prévia do
   PDF não comprovam a elaboração obrigatória no software.
3. Inserir a exportação do yEd no relatório e atualizar o ZIP; retirar o rótulo
   de revisão apenas após resolver as pendências.
4. Conferir se os nomes fornecidos estão completos como exige o enunciado.

O ZIP atual é uma versão para revisão, **não uma entrega final integralmente conforme**.

## Alterar a rede

Edite apenas `PESSOAS` e `AMIZADES` em `grafo.c`. Os índices das amizades
correspondem às posições das pessoas. Ao remover uma posição intermediária,
atualize os índices posteriores. O tamanho da rede é calculado automaticamente.
Recompile e atualize os resultados e a documentação depois da alteração.

## Definições adotadas

- Panelinhas são cliques **maximais**, com pelo menos três membros; não são
  somente as cliques de maior tamanho.
- Pessoa influente é a única pessoa comum a uma família de duas ou mais panelinhas.
  O código considera a interseção da família inteira, inclusive três ou mais grupos.
- Amizade influente tem uma aresta entre pessoas que pertencem a panelinhas
  distintas. Não se exige exclusividade nem disjunção, restrições ausentes no PDF.

## Verificações reproduzíveis

```sh
python testes/verificar_saida.py
gcc -std=c90 -pedantic-errors -Wall -Wextra -Werror testes/testar.c -o output/testar.exe
./output/testar.exe
python ferramentas/gerar_documentacao.py
```

O primeiro teste espera o executável em `output/grafo.exe`; compile com
`-o output/grafo.exe` antes de executá-lo. O teste exaustivo verifica panelinhas,
influência e pertencimento a panelinhas distintas contra enumerações independentes.
