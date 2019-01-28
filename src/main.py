from parser import parameter_parser
from motif_count import MotifCounterMachine
from utils import load_graph, tab_printer

def main(args):
    """
    Role2Vec model fitting.
    :param args: Arguments object.
    """
    tab_printer(args)
    graph = load_graph(args.graph_input)
    model = MotifCounterMachine(graph, args)
    model.extract_features()

if __name__ == "__main__":
    args = parameter_parser()
    main(args)
