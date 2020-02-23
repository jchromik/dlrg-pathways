from graphviz import Digraph
from itertools import groupby, product
import json

for idx in [1, 3, 4, 5, 6, 7, 8, 10]:

    g = Digraph(f'G{idx}', filename=f'pathways{idx}.gv')

    with open(f'data/{idx}.json') as f:
        dep_spec = json.load(f)
        qualifications = dep_spec['qualifications']

    groups = [list(group) for _, group in groupby(qualifications, lambda x: x[1])]

    for group in groups:
        with g.subgraph() as s:
            s.attr(rank='same')
            for qualification in group:
                s.node(qualification)
            for q1, q2 in zip(group[0::2], group[1::2]):
                s.edge(q1, q2, style='invis')

    for group1, group2 in zip(groups[0::2], groups[1::2]):
        for n1, n2 in product(group1, group2):
            g.edge(n1, n2, style='invis')

    for qualification, details in dep_spec['qualifications'].items():
        for dependency in details['dependencies']:
            if isinstance(dependency, str):
                g.edge(dependency, qualification)
            if isinstance(dependency, list):
                for dep in dependency:
                    g.edge(dep, qualification)

    g.render()
