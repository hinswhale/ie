import pandas as pd
from root_path import data_root


def run(path):
    df = pd.read_csv(path)


run(data_root)
