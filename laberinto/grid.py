import networkx as nx

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.graph = nx.grid_2d_graph(rows, columns)

    def show_nodes(self):
        return list(self.graph.nodes)
    
    def show_neighbors(self, node):
        if node in self.graph:
            return list(self.graph.neighbors(node))
        else:
            return []

    def lock_cell(self, node):
        if node in self.graph:
            neighbors = list(self.graph.neighbors(node))
            for neighbor in neighbors:
                self.graph.remove_edge(node, neighbor)

    def delete_connection(self, node1, node2):
        if self.graph.has_edge(node1, node2):
            self.graph.remove_edge(node1, node2)

    def add_connection(self, node1, node2):
        if node1 in self.graph and node2 in self.graph:
            self.graph.add_edge(node1, node2)

