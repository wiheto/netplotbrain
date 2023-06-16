import pandas as pd
from netplotbrain import plot as npbplot
import pytest


# Example node and edges dataframes included with package
nodes = pd.read_csv('./examples/example_nodes.tsv', sep='\t', index_col=0)
edges = pd.read_csv('./examples/example_edges.tsv', sep='\t', index_col=0)

@pytest.mark.mpl_image_compare
def test_preset3():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='surface',
                      view='preset-3',
                      nodes=nodes,
                      edges=edges)
    return fig

@pytest.mark.mpl_image_compare
def test_preset4():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='surface',
                      view='preset-4',
                      nodes=nodes,
                      edges=edges)
    return fig

@pytest.mark.mpl_image_compare
def test_preset4s():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='surface',
                      view='preset-4s',
                      nodes=nodes,
                      edges=edges)
    return fig

@pytest.mark.mpl_image_compare
def test_preset9():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='surface',
                      view='preset-9',
                      nodes=nodes,
                      edges=edges)
    return fig

@pytest.mark.mpl_image_compare
def test_preset6():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='surface',
                      view='preset-6',
                      nodes=nodes,
                      edges=edges)
    return fig

@pytest.mark.mpl_image_compare
def test_preset6s():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='surface',
                      view='preset-6spring',
                      nodes=nodes,
                      edges=edges)
    return fig

