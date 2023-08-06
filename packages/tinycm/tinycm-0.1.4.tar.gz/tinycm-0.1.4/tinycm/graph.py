import networkx as nx


class CMGraph(object):
    def __init__(self, configuration):
        self.graph = nx.DiGraph()

        # Add the nodes in the graph
        for identifier in configuration.definitions:
            self.graph.add_node(configuration.definitions[identifier])

        # Add the edges in the graph
        for identifier in configuration.definitions:
            if len(configuration.definitions[identifier].after) > 0:
                for edge in configuration.definitions[identifier].after:
                    edge_from = configuration.definitions[identifier]
                    edge_to = configuration.definitions[edge]
                    self.graph.add_edge(edge_from, edge_to)

    def get_sorted_jobs(self):
        return nx.topological_sort(self.graph, reverse=True)
