"""Motif Counter definition."""

import pandas as pd
from tqdm import tqdm
import networkx as nx
from networkx.generators.atlas import *

class MotifCounterMachine(object):
    """
    Connected motif orbital role counter.
    """
    def __init__(self, graph, args):
        """
        Creating an orbital role counter machine.
        :param graph: NetworkX graph.
        :param args: Arguments object.
        """
        self.graph = graph
        self.args = args

    def create_edge_subsets(self):
        """
        Enumerating connected subgraphs with size 2 up to the graphlet size.
        """
        print("\nEnumerating subgraphs.\n")
        self.edge_subsets = dict()
        subsets = [[edge[0], edge[1]] for edge in self.graph.edges()]
        self.edge_subsets[2] = subsets
        unique_subsets = dict()
        for i in range(3, self.args.graphlet_size+1):
            print("Enumerating graphlets with size: " +str(i) + ".")
            for subset in tqdm(subsets):
                for node in subset:
                    for neb in self.graph.neighbors(node):
                        new_subset = subset+[neb]
                        if len(set(new_subset)) == i:
                            new_subset.sort()
                            unique_subsets[tuple(new_subset)] = 1
            subsets = [list(k) for k, v in unique_subsets.items()]
            self.edge_subsets[i] = subsets
            unique_subsets = dict()

    def enumerate_graphs(self):
        """
        Creating a hash table of the benchmark motifs.
        """
        graphs = graph_atlas_g()
        self.interesting_graphs = {i: [] for i in range(2, self.args.graphlet_size+1)}
        for graph in graphs:
            if graph.number_of_nodes() > 1 and graph.number_of_nodes() < self.args.graphlet_size+1:
                if nx.is_connected(graph):
                    self.interesting_graphs[graph.number_of_nodes()].append(graph)

    def enumerate_categories(self):
        """
        Creating a hash table of benchmark orbital roles.
        """
        main_index = 0
        self.categories = dict()
        for size, graphs in self.interesting_graphs.items():
            self.categories[size] = dict()
            for index, graph in enumerate(graphs):
                self.categories[size][index] = dict()
                degrees = list(set([graph.degree(node) for node in graph.nodes()]))
                for degree in degrees:
                    self.categories[size][index][degree] = main_index
                    main_index = main_index + 1
        self.unique_motif_count = main_index + 1

    def setup_features(self):
        """
        Counting all the orbital roles.
        """
        print("\nCounting orbital roles.\n")
        self.features = {node: {i:0 for i in range(self.unique_motif_count)}for node in self.graph.nodes()}
        for size, node_lists in self.edge_subsets.items():
            graphs = self.interesting_graphs[size]
            for nodes in tqdm(node_lists):
                sub_gr = self.graph.subgraph(nodes)
                for index, graph in enumerate(graphs):
                    if nx.is_isomorphic(sub_gr, graph):
                        for node in sub_gr.nodes():
                            self.features[node][self.categories[size][index][sub_gr.degree(node)]] += 1
                        break

    def create_tabular_motifs(self):
        """
        Creating a table with the orbital role features.
        """
        print("Saving the dataset.")
        self.binned_features = {node: [] for node in self.graph.nodes()}
        self.motifs = [[n]+[self.features[n][i] for i in  range(self.unique_motif_count)] for n in self.graph.nodes()]
        self.motifs = pd.DataFrame(self.motifs)
        self.motifs.columns = ["id"] + ["role_"+str(index) for index in range(self.unique_motif_count)]
        self.motifs.to_csv(self.args.output, index=None)

    def extract_features(self):
        """
        Executing steps for feature extraction.
        """
        self.create_edge_subsets()
        self.enumerate_graphs()
        self.enumerate_categories()
        self.setup_features()
        self.create_tabular_motifs()
