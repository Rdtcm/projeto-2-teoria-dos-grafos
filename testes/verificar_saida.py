"""Oraculo independente para a rede entregue; nao requer pacotes externos."""
import itertools
import pathlib
import re
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
source = (root / 'grafo.c').read_text()
people = re.findall(r'\{"([^"]+)",\s*\d+,', source)
edges = {frozenset(map(int, e)) for e in re.findall(r'\{(\d+),(\d+)\}', source)}
cliques = []
# Enumera todas as combinacoes por tamanho. Ausencia de K_r implica ausencia
# de cliques maiores, pois qualquer clique maior conteria um K_r.
for size in range(3, len(people) + 1):
    level = [frozenset(c) for c in itertools.combinations(range(len(people)), size)
             if all(frozenset(e) in edges for e in itertools.combinations(c, 2))]
    if not level:
        break
    cliques.extend(level)
maximal = {c for c in cliques if not any(c < other for other in cliques)}
influential = {v for v in range(len(people))
               if len(family := [c for c in maximal if v in c]) >= 2
               and set.intersection(*(set(c) for c in family)) == {v}}
friendships = {e for e in edges if any(u in p and v in q
               for u, v in [tuple(e)] for p in maximal for q in maximal if p != q)}
result = subprocess.run([str(root / 'output/grafo.exe')], capture_output=True,
                        text=True, check=True, timeout=20).stdout
found = {frozenset(people.index(name) for name in names.split(', '))
         for names in re.findall(r'^P\d+ \(\d+ membros\): \{([^}]+)\}', result, re.M)}
assert found == maximal
assert len(re.findall(r'^P\d+ \(', result, re.M)) == len(maximal)
found_people = {people.index(name) for name in re.findall(r'^(.+): unico membro comum', result, re.M)}
assert found_people == influential
found_edges = {frozenset((people.index(a), people.index(b))) for a, b in
               re.findall(r'^(.+) \(P\d+\) -- (.+) \(P\d+\)', result, re.M)}
assert found_edges == friendships
assert (len(people), len(edges), len(maximal), len(influential), len(friendships)) == (25,42,10,9,36)
(root / 'output/resultado.txt').write_text(result, encoding='utf-8')
print('OK: saida real conferida por enumeracao independente de combinacoes.')
print('25 participantes; 42 amizades; 10 panelinhas; 9 pessoas e 36 amizades influentes.')
