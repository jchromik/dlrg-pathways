from graphviz import Digraph
from itertools import groupby, product
import json

for idx in [1, 3, 4, 5, 6, 7, 8, 10]:

    with open(f'data/{idx}.json') as f:
        dep_spec = json.load(f)
        qualifications = dep_spec['qualifications']

    g = Digraph(f'G{idx}', filename=f'pathways{idx}.gv')
    g.attr(label=dep_spec['name'])

    # Group together qualifications with the same second digit.
    # First digit is defined by dep spec number (1 for S/RS, 3 for San, etc.)
    # Second digit groups similar qualifications within a dep spec.
    groups = [list(group) for _, group in groupby(qualifications, lambda x: x[-2])]

    with g.subgraph(name='cluster') as c:

        c.attr(label='')
        
        # For each group:
        # Make a subgraph to put elements of group
        # next to each other (rank='same').
        for group in groups:
            with c.subgraph() as s:
                s.attr(rank='same')
                # Add node for qualification to subgraph.
                for qualification in group:
                    s.node(qualification)
                # Add invisible edges between nodes in subgraph
                # to keep them in the predefined order.
                # (Avoiding repositioning by dot.)
                for q1, q2 in zip(group[0::2], group[1::2]):
                    s.edge(q1, q2, style='invis')

        # Add invisible edges between elements of subsequent groups,
        # in order to force dot to put subgraphs below each other.
        # (And not next to each other.)
        for group1, group2 in zip(groups[0::2], groups[1::2]):
            for n1, n2 in product(group1, group2):
                c.edge(n1, n2, style='invis')

        # Add (visible) edges for all dependency relations.
        for qualification, details in qualifications.items():
            for dependency in details['dependencies']:
                # If dependency is str: Add straight away, because it is a
                # required dependency.
                if isinstance(dependency, str):
                    if dependency in qualifications.keys():
                        c.edge(dependency, qualification)
                    else:
                        g.edge(dependency, qualification)
                # If dependency is list: Add OR-node first, because one element
                # of the list is needed.
                if isinstance(dependency, list):
                    merger_name = f"{qualification}_{dependency}"
                    c.node(merger_name, label="OR", shape="square")
                    g.edge(merger_name, qualification)
                    for dep in dependency:
                        g.edge(dep, merger_name)

    g.render()
