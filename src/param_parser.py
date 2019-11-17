"""Parameter parser tool."""

import argparse

def parameter_parser():
    """
    Calculating counts of orbital roles in connected graphlets.
    Representations are sorted by ID.
    """
    parser = argparse.ArgumentParser(description="Extracting the features.")

    parser.add_argument('--graph-input',
                        nargs='?',
                        default="./input/cora_edges.csv",
	                help='Edge list csv path.')

    parser.add_argument('--output',
                        nargs='?',
                        default='./output/cora_orbital_features.csv',
	                help='Feature output path.')

    parser.add_argument('--graphlet-size',
                        type=int,
                        default=4,
	                help='Maximal graphlet size. Default is 4.')

    return parser.parse_args()
