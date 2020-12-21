import os

import pandas as pd

scriptdir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(scriptdir, '..')
data_dir = os.path.join(project_root, 'data')

def read_tsv(filename):
    """
    Load data in TSV format from the data directory.

    filename -- Relative path to the file from the root of the data directory.
    """
    return pd.read_csv(os.path.join(data_dir, filename), sep='\t')