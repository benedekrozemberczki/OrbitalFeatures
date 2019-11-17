""" Utilities for printing and data reading."""

import pandas as pd
import networkx as nx
from texttable import Texttable

def tab_printer(args):
    """
    Function to print the logs in a nice tabular format.
    :param args: Parameters used for the model.
    """
    args = vars(args)
    keys = sorted(args.keys())
    t = Texttable()
    t.add_rows([["Parameter", "Value"]]+[[k.replace("_", " ").capitalize(), args[k]] for k in keys])
    print(t.draw())

def load_graph(graph_path):
    """
    Reading an egde list csv as an NX graph object.
    :param graph_path: Path to the edgelist.
    :return graph: Networkx Object.
    """
    graph = nx.from_edgelist(pd.read_csv(graph_path).values.tolist())
    graph.remove_edges_from(graph.selfloop_edges())
    return graph
