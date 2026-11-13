"""Gera documentacao de revisao e GraphML a partir do unico fonte entregue."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing, Line, Circle, String
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/'grafo.c').read_text()
people = re.findall(r'\{"([^"]+)",\s*(\d+),\s*"([^"]+)",\s*"([^"]+)"\}', source)
edges = [tuple(map(int, e)) for e in re.findall(r'\{(\d+),(\d+)\}', source)]
result = (ROOT/'output/resultado.txt').read_text(encoding='utf-8')
cliques = re.findall(r'^(P\d+) \((\d+) membros\): \{([^}]+)\}', result, re.M)
influential = re.findall(r'^(.+): unico membro comum a (.+)\.$', result, re.M)
influential_names = {n for n,p in influential}
coords = [(120,100),(40,45),(40,155),(170,40),(170,160),(220,100),
          (270,45),(320,100),(370,160),(420,100),(480,40),(530,100),
          (480,220),(530,300),(430,330),(380,260),(330,330),(280,270),
          (280,390),(230,330),(180,270),(130,330),(80,390),(30,330),(30,230)]

graphml = ['<?xml version="1.0" encoding="UTF-8"?>',
 '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:y="http://www.yworks.com/xml/graphml">',
 '<key id="d0" for="node" yfiles.type="nodegraphics"/>',
 '<key id="d1" for="edge" yfiles.type="edgegraphics"/>',
 '<graph id="Rede" edgedefault="undirected">']
for i, ((name,age,course,hobby),(x,y)) in enumerate(zip(people,coords)):
    color = '#F0BD55' if name in influential_names else '#DCE9F2'
    graphml.append(f'<node id="n{i}"><data key="d0"><y:ShapeNode>'
       f'<y:Geometry x="{x*2.2}" y="{y*2.2}" width="145" height="46"/>'
       f'<y:Fill color="{color}" transparent="false"/>'
       '<y:BorderStyle color="#24425B" type="line" width="1.0"/>'
       f'<y:NodeLabel fontSize="12">{i:02d} - {escape(name)}</y:NodeLabel>'
       '<y:Shape type="roundrectangle"/></y:ShapeNode></data></node>')
for i,(u,v) in enumerate(edges):
    graphml.append(f'<edge id="e{i}" source="n{u}" target="n{v}"><data key="d1">'
        '<y:PolyLineEdge><y:LineStyle color="#65788A" type="line" width="1.0"/>'
        '<y:Arrows source="none" target="none"/></y:PolyLineEdge></data></edge>')
graphml.append('</graph></graphml>')
(ROOT/'docs/rede-social.graphml').write_text('\n'.join(graphml),encoding='utf-8')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Texto',fontName='Helvetica',fontSize=10.2,leading=14,spaceAfter=9))
styles.add(ParagraphStyle(name='Titulo',fontName='Helvetica-Bold',fontSize=24,leading=29,textColor=colors.HexColor('#193B55'),spaceAfter=16))
styles.add(ParagraphStyle(name='Subtitulo',fontName='Helvetica-Bold',fontSize=15,leading=20,textColor=colors.HexColor('#193B55'),spaceAfter=12))
styles.add(ParagraphStyle(name='Celula',fontName='Helvetica',fontSize=8.5,leading=11))
styles.add(ParagraphStyle(name='Pequeno',fontName='Helvetica',fontSize=8.5,leading=12,spaceAfter=8))
story=[]
def p(text,style='Texto'): story.append(Paragraph(text,styles[style]))
def title(text): p(text,'Subtitulo')
def table(rows,widths):
    data=[[Paragraph(str(c),styles['Celula']) for c in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCE9F2')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7F9')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#193B55'))]))
    story.append(t);story.append(Spacer(1,12))
def page(): story.append(PageBreak())

p('TEORIA DOS GRAFOS · 2026-2','Pequeno')
p('Panelinhas e influência<br/>em uma rede social','Titulo')
p('Projeto de Programação - Parte 2','Subtitulo')
table([['Integrante','RA'],['Ryan Ledo','10352727'],['Renan Horochk','10438120'],['Alef Sousa','10431891']],[350,145])
p('<b>VERSÃO PARA REVISÃO - 13/11/2026</b><br/>O código e os resultados da rede estão implementados. O desenho desta versão é uma prévia: a elaboração/exportação no yEd ainda está pendente. Os requisitos adicionais da Parte 1 não foram disponibilizados e ainda precisam ser conferidos. Esta versão não deve ser enviada como entrega final.','Texto')
title('1. Objetivo')
p('O projeto identifica panelinhas e pessoas influentes em uma comunidade universitária representada por um grafo. Cada vértice corresponde a um participante e cada aresta representa uma amizade recíproca. A rede contém 25 participantes e 42 amizades.')
p('Uma panelinha é um conjunto maximal de pelo menos três participantes em que todos são amigos entre si. Maximal significa que não é possível acrescentar outro participante ao conjunto mantendo essa condição. Não significa que o conjunto precisa ser o maior da rede.')
p('Uma pessoa é influente quando participa de duas ou mais panelinhas cuja interseção contém somente essa pessoa. A consulta complementar identifica amizades entre participantes pertencentes a panelinhas distintas.')
title('2. Modelagem')
p('Foi adotado um grafo simples, não orientado e sem pesos. Os nomes completos, idades, cursos e interesses são dados fictícios para demonstração; não representam uma coleta de relações pessoais. Os nomes são nomes de pessoas, em vez de rótulos abstratos como A e B.')
p('A representação usada é a lista de adjacência do arquivo grafo.c fornecido pelo professor. As relações são cadastradas em uma tabela constante. O programa cria um único grafo e executa todas as consultas sem solicitar entrada pelo teclado.')
page()

title('3. Participantes e atributos')
p('O identificador corresponde ao índice na tabela PESSOAS e ao número apresentado no desenho. Os campos de texto do programa usam caracteres ASCII para facilitar a exibição no console do Windows.','Pequeno')
table([['ID','Nome','Idade','Curso','Interesse']]+[[f'{i:02d}',*person] for i,person in enumerate(people)],[28,155,38,125,149])
p('As amizades são simétricas. A listagem produzida pelo programa mostra todos os atributos e todos os amigos de cada participante. A participante 24 tem uma amizade e não pertence a nenhuma panelinha.','Pequeno')
page()

title('4. Desenho da rede - prévia de revisão')
p('<b>Pendente:</b> abrir docs/rede-social.graphml no yEd, elaborar/revisar a disposição do grafo e exportar o desenho. Substituir esta prévia pela exportação antes da entrega. O controle automatizado do yEd não foi autorizado nesta sessão.','Texto')
d=Drawing(495,390)
for u,v in edges:
    x1,y1=coords[u];x2,y2=coords[v]
    d.add(Line(x1*.86,370-y1*.85,x2*.86,370-y2*.85,strokeColor=colors.HexColor('#8395A3'),strokeWidth=.85))
for i,((name,*_), (x,y)) in enumerate(zip(people,coords)):
    d.add(Circle(x*.86,370-y*.85,12,fillColor=colors.HexColor('#F0BD55' if name in influential_names else '#DCE9F2'),strokeColor=colors.HexColor('#193B55'),strokeWidth=1))
    d.add(String(x*.86,370-y*.85-3,f'{i:02d}',fontName='Helvetica-Bold',fontSize=8,textAnchor='middle'))
story.append(d)
p('Figura 1. Prévia gerada por código, ainda não elaborada no yEd. Vértices amarelos: pessoas influentes. Vértices azuis: demais participantes. Os números correspondem à tabela da seção 3. As linhas não possuem direção.','Pequeno')
title('Conferência das relações')
p('Cada par abaixo é uma amizade; seus dois sentidos são armazenados pelo código base. A tabela permite conferir a prévia e o GraphML com a constante AMIZADES.')
p('; '.join(f'{u:02d}-{v:02d}' for u,v in edges)+'.','Pequeno')
page()

title('5. Algoritmos implementados')
p('<b>Construção e exibição.</b> main calcula a ordem a partir da tabela constante PESSOAS, chama criarGrafo e preenche os atributos dos vértices. Para cada par de AMIZADES, valida os índices, rejeita laços e repetições na rede social e chama acrescentarAresta. A função exibirRede percorre os vértices e suas listas de amigos. Cada amizade é contada apenas quando o primeiro índice é menor que o segundo.')
p('<b>Busca das panelinhas.</b> encontrarPanelinhas cria um vetor de trabalho e uma lista dinâmica de resultados. buscarPanelinhas faz uma busca recursiva com retrocesso. A cada chamada, o vetor contém uma clique. Um vértice só é acrescentado quando ligadoATodos confirma sua amizade com todos os membros atuais. A busca escolhe índices estritamente crescentes; por isso cada conjunto é visitado uma única vez.')
p('Quando o conjunto tem pelo menos três membros, ehMaximal percorre todos os vértices externos. Se algum deles for amigo de todos os membros, o conjunto ainda pode crescer e não é salvo. Caso contrário, uma cópia é armazenada na lista de panelinhas. Essa verificação inclui vértices de índices menores, evitando registrar como maximal um conjunto que só não pode crescer na ordem atual da busca.')
p('<b>Correção.</b> O conjunto inicial vazio é uma clique. Cada extensão preserva essa propriedade, pois o novo membro é adjacente a todos os anteriores. Toda clique pode ser percorrida pela sequência crescente de seus índices, de modo que nenhuma clique maximal é perdida. Somente conjuntos com tamanho mínimo três e sem extensão externa são salvos; a ordem crescente evita repetições.')
p('<b>Pessoas influentes.</b> Para cada vértice, ehInfluente conta as panelinhas que o contêm. Havendo duas ou mais, verifica se existe outro vértice presente em todas elas. Se existir, a pessoa não é influente; se não existir, a interseção é somente ela. A saída informa as panelinhas que comprovam o resultado.')
p('A verificação considera também famílias de três ou mais panelinhas. Se alguma subfamília tem interseção {v}, a interseção de todas as panelinhas contendo v também é {v}. Reciprocamente, quando essa última interseção é {v}, a própria família completa fornece a comprovação.')
p('<b>Amizades influentes.</b> Para cada aresta u-v, amizadeInfluente procura duas panelinhas distintas, uma contendo u e outra contendo v. A primeira dupla encontrada serve como testemunha. A saída percorre cada aresta apenas uma vez. Foi seguida a definição literal do enunciado: ela não exige panelinhas disjuntas nem proíbe que os participantes compartilhem outra panelinha.')
p('<b>Memória.</b> A lista de panelinhas não tem limite fixo de resultados. Cada registro possui um vetor próprio de membros. destruirPanelinhas libera esses vetores e registros; destruirGrafo libera as listas de adjacência e o vetor de vértices. Falhas de alocação são verificadas.','Texto')
page()

title('6. Resultados obtidos')
table([['Panelinha','Tamanho','Participantes']]+[[a,b,c] for a,b,c in cliques],[65,55,375])
p('Foram encontradas 10 panelinhas: sete com três membros e três com quatro. Por exemplo, {Diego Souza, Elisa Costa, Felipe Almeida} não é maximal, pois Ana Silva pode ser acrescentada. Já o par {Yasmin Freitas, Zelia Mendes} não tem o tamanho mínimo exigido.','Texto')
table([['Pessoa influente','Panelinhas com interseção única']]+[[a,b] for a,b in influential],[245,250])
p('Há 9 pessoas influentes, superando o mínimo de duas exigido no projeto. A influência é calculada a partir das panelinhas; não é atribuída por quantidade de amigos nem cadastrada manualmente.','Pequeno')
page()

title('7. Consulta complementar e custo')
p('O grupo possui três integrantes e, portanto, a consulta de amizades influentes é opcional. Ela foi mantida como complemento. Foram obtidas 36 amizades influentes segundo a interpretação da seção 5. Exemplos: Carla Oliveira (P1) e Gabriela Lima (P3); Lucas Fernandes (P5) e Pedro Araujo (P7). A saída do programa apresenta todas as relações e suas testemunhas.')
p('Uma amizade entre pessoas da mesma panelinha também pode ser listada se houver panelinhas distintas que testemunhem a definição. Por exemplo, Ana pertence a P1 e Diego pertence a P2, embora ambos também estejam em P2. Não foi acrescentada uma restrição de exclusividade que não aparece no enunciado.')
p('<b>Complexidade.</b> Considere n vértices, m arestas e k panelinhas. A lista de adjacência ocupa O(n + m). Consultar uma amizade custa O(n) no pior caso. A busca pode visitar até 2<super>n</super> subconjuntos e tem limite superior conservador O(2<super>n</super> n³), incluindo os testes de extensão e maximalidade. O problema é exponencial no pior caso; a implementação foi escolhida pela simplicidade e adequação à rede pequena do projeto.')
p('A lista de resultados ocupa O(kn), além de O(n) para o vetor de trabalho e a pilha recursiva. A identificação de pessoas influentes tem limite O(kn³). A consulta complementar tem limite O(mk²n). Esses limites consideram as buscas lineares nos vetores de membros e nas listas de adjacência; não há matriz de adjacência auxiliar no programa entregue.')
title('8. Compilação e execução')
p('O arquivo grafo.c contém todo o código do programa. Para compilar com GCC:')
p('<font name="Courier" size="8.8">gcc -std=c90 -pedantic-errors -Wall -Wextra -Werror<br/>grafo.c -o grafo.exe</font><br/>(Usar o comando em uma única linha.)')
p('No Dev-C++ para Windows, abrir grafo.c, selecionar compilação como C, compilar e executar. As tabelas já contêm todos os dados. Não há scanf, getchar, menu, leitura de arquivo nem pausa programada. Ao executar por um terminal já aberto, toda a saída permanece disponível.')
title('9. Verificação realizada')
p('A compilação com GCC em modo C90 estrito foi concluída sem avisos. O programa executou e produziu 25 participantes, 42 amizades, 10 panelinhas, 9 pessoas influentes e 36 amizades influentes. Um verificador independente em Python enumerou combinações de vértices por tamanho e comparou os conjuntos completos com a saída real, incluindo as pessoas e amizades influentes; as comparações passaram.')
p('Foi preparado também um teste C para todos os grafos simples de 1 a 6 vértices, com comparação por máscaras de subconjuntos. Esse teste compilou, mas sua execução foi bloqueada pelo Controle de Aplicativo do Windows. Ele não é apresentado como aprovado. Não foi realizada execução na interface do Dev-C++; a compatibilidade foi verificada pelo compilador em modo ANSI C90.')
page()

title('10. Alterações em relação à base do professor')
p('Foram preservadas as estruturas Aresta e Vertice, o encadeamento das arestas e as funções criarGrafo, destruirGrafo, acrescentarAresta e imprimirGrafo. O campo nome continua sendo o identificador inteiro original. Foram adicionados apenas os atributos nomeReal, idade, curso e interesse ao vértice.')
p('As funções originais receberam verificações de alocação e inicialização dos atributos. destruirGrafo passa a anular o ponteiro liberado. Se a alocação da segunda metade de uma aresta falhar, acrescentarAresta desfaz a primeira inserção. O cabeçalho memory.h foi substituído por string.h, da biblioteca padrão, para memcpy. A função original ainda permite laços e arestas paralelas; somente a montagem desta rede social os rejeita.')
p('O main demonstrativo foi substituído pela inicialização da rede constante e pelas chamadas das consultas. imprimirGrafo permanece disponível; exibirRede acrescenta nomes e atributos à apresentação. As funções de busca e de análise foram adicionadas sem substituir a representação original por outra estrutura de grafo.')
title('11. Como alterar a rede')
p('Editar PESSOAS para modificar nomes e atributos ou acrescentar participantes. Editar AMIZADES para incluir ou excluir pares de índices. O número de participantes e o número de relações são calculados com sizeof. Ao remover uma pessoa do meio da tabela, atualizar os índices das amizades subsequentes. Depois, recompilar, executar e atualizar o GraphML e o relatório. Os resultados não são fixados no algoritmo.')
title('12. Fontes e recursos utilizados')
p('<b>Grafos-Projeto2-2026-2.pdf.</b> Enunciado fornecido pelo usuário: definições de panelinha, pessoa influente e amizade influente, requisitos da rede, da documentação e da entrega.')
p('<b>grafo.c, representação de grafos, versão 2026-2.</b> Código base fornecido pelo professor: estruturas e operações de listas de adjacência. As adaptações estão descritas na seção 10.')
p('<b>Assistência do Codex.</b> Utilizada para desenvolver as funções adicionais, preparar dados demonstrativos, verificações e documentação. Não foram consultados artigos, livros ou páginas externas sobre algoritmos de grafos nesta implementação. Como o conteúdo das aulas não foi fornecido integralmente, não se afirma que todas as técnicas adicionais tenham sido abordadas em aula.')
p('<b>Ferramentas.</b> GCC para compilação; Python para verificação independente; ReportLab para gerar este PDF. GraphML preparado para abertura no yEd. O desenho desta revisão foi produzido por código e ainda precisa da etapa obrigatória no yEd.')
title('13. Pendências para a entrega definitiva')
p('Conferir os requisitos adicionais da Parte 1; confirmar que os nomes informados representam a identificação completa solicitada; elaborar e exportar o desenho no yEd; substituir a prévia e remover os avisos de revisão somente após resolver essas pendências. O ZIP de revisão contém apenas o PDF e o arquivo grafo.c, conforme a composição pedida para a entrega.')

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#C7D3DD'));canvas.line(50,43,545,43)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#536778'))
    canvas.drawString(50,30,'Teoria dos Grafos | Projeto 2 | Versão para revisão')
    canvas.drawRightString(545,30,str(doc.page))

SimpleDocTemplate(str(ROOT/'output/documentacao-revisao.pdf'),pagesize=A4,
    rightMargin=50,leftMargin=50,topMargin=46,bottomMargin=55,
    title='Panelinhas e influencia - Projeto 2 - Revisao',
    author='Ryan Ledo; Renan Horochk; Alef Sousa').build(story,onFirstPage=footer,onLaterPages=footer)
print('PDF de revisao e GraphML gerados.')
