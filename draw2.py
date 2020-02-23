from graphviz import Digraph
from itertools import groupby
import json

g = Digraph('G', filename='pathways2.gv')

with open('data/1.json') as f:
    dep_spec = json.load(f)

for qualifications, group in groupby(dep_spec['qualifications'], lambda x: x[1]):
    with g.subgraph() as s:
        s.attr(rank='same')
        for qualification in group:
            s.node(qualification)

for qualification, details in dep_spec['qualifications'].items():
    for dependency in details['dependencies']:
        g.edge(dependency, qualification)

g.view()
