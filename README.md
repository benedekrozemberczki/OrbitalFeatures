OrbitalStrike
============================================
An implementation of "Biological Network Comparison Using Graphlet Degree Distribution" (Bioinformatics 2007).
<div style="text-align:center"><img src ="orbit.png" ,width=500/></div>
<p align="justify">
Analogous to biological sequence comparison, comparing cellular networks is an important problem that could provide insight into biological understanding and therapeutics. For technical reasons, comparing large networks is computationally infeasible, and thus heuristics, such as the degree distribution, clustering coefficient, diameter, and relative graphlet frequency distribution have been sought. It is easy to demonstrate that two networks are different by simply showing a short list of properties in which they differ. It is much harder to show that two networks are similar, as it requires demonstrating their similarity in all of their exponentially many properties. Clearly, it is computationally prohibitive to analyze all network properties, but the larger the number of constraints we impose in determining network similarity, the more likely it is that the networks will truly be similar.</p>

This repository provides an implementation of Graph Wavelet Neural Network as described in the paper:

> Biological network comparison using graphlet degree distribution.
> Natasa Przulj.
> BioInformatics, 2007.
> [[Paper]](https://www.ncbi.nlm.nih.gov/pubmed/17237089)

### Requirements

The codebase is implemented in Python 3.5.2. package versions used for development are just below.
```
networkx          1.11
tqdm              4.28.1
numpy             1.15.4
pandas            0.23.4
texttable         1.5.0
scipy             1.1.0
argparse          1.1.0
torch             0.4.1
torch-scatter     1.0.4
torch-sparse      0.2.2
torchvision       0.2.1
scikit-learn      0.20.0
PyGSP             0.5.1
```
### Datasets

The code takes the **edge list** of the graph in a csv file. Every row indicates an edge between two nodes separated by a comma. The first row is a header. Nodes should be indexed starting with 0. A sample graph for `Cora` is included in the  `input/` directory. In addition to the edgelist there is a JSON file with the sparse features and a csv with the target variable.

The **feature matrix** is a sparse binary one it is stored as a json. Nodes are keys of the json and feature indices are the values. For each node feature column ids are stored as elements of a list. The feature matrix is structured as:

```javascript
{ 0: [0, 1, 38, 1968, 2000, 52727],
  1: [10000, 20, 3],
  2: [],
  ...
  n: [2018, 10000]}
```

The **target vector** is a csv with two columns and headers, the first contains the node identifiers the second the targets. This csv is sorted by node identifiers and the target column contains the class meberships indexed from zero. 

| **NODE ID**| **Target** |
| --- | --- |
| 0 | 3 |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |
| ... | ... |
| n | 3 |

### Options

Training the model is handled by the `src/main.py` script which provides the following command line arguments.

#### Input and output options

```
  --edge-path        STR   Input graph path.   Default is `input/cora_edges.csv`.
  --features-path    STR   Features path.      Default is `input/cora_features.json`.
  --target-path      STR   Target path.        Default is `input/cora_target.csv`.
  --log-path         STR   Log path.           Default is `logs/cora_logs.json`.
```

#### Model options

```
  --epochs                INT       Number of Adam epochs.         Default is 300.
  --learning-rate         FLOAT     Number of training epochs.     Default is 0.001.
  --weight-decay          FLOAT     Weight decay.                  Default is 5*10**-4.
  --filters               INT       Number of filters.             Default is 16.
  --dropout               FLOAT     Dropout probability.           Default is 0.5.
  --test-size             FLOAT     Test set ratio.                Default is 0.2.
  --seed                  INT       Random seeds.                  Default is 42.
  --approximation-order   INT       Chebyshev polynomial order.    Default is 20.
  --tolerance             FLOAT     Wavelet coefficient limit.     Default is 10**-4.
  --scale                 FLOAT     Heat kernel scale.             Default is 1.0.
```

### Examples

The following commands learn  the weights of a graph wavelet neural network and saves the logs. The first example trains a graph wavelet neural network on the default dataset with standard hyperparameter settings. Saving the logs at the default path.

```
python src/main.py
```
<p align="center">
<img style="float: center;" src="gwnn_run.jpg">
</p>

Training a model with more filters in the first layer.

```
python src/main.py --filters 32
```

Approximationg the wavelets with polynomials that have an order of 5.

```
python src/main.py --approximation-order 5
```
