from graphviz import Digraph
import json

g = Digraph('G', filename='pathways.gv')

dep_specs = []

for dep_spec_index in [1, 3, 4, 5, 6, 7, 8, 10]:
    with open(f"data/{dep_spec_index}.json") as dep_spec_file:
        dep_specs.append(json.load(dep_spec_file))

for dep_spec in dep_specs:
    with g.subgraph(name=f"luster_{dep_spec['name']}") as c:
        c.attr(label=dep_spec['name'])
        for qualification, details in dep_spec['qualifications'].items():
            c.node(qualification, fillcolor=dep_spec['color'], style='filled')
            for dependency in details['dependencies']:
                if isinstance(dependency, str):
                    g.edge(dependency, qualification)
                if isinstance(dependency, list):
                    merger_name = f"{qualification}_{dependency}"
                    c.node(merger_name, label="OR", shape="square")
                    g.edge(merger_name, qualification)
                    for dep in dependency:
                        g.edge(dep, merger_name)

g.view()