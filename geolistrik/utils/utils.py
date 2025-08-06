import numpy as np
import pandas as pd

def save_to_excel_by_sheet(filename, dfs, sheet_names):
    with pd.ExcelWriter(filename) as writer:
        for df, sheet in zip(dfs, sheet_names):
            df.to_excel(writer, sheet_name=sheet, index=False)

def mapping_by_index(conf_elctrode, elektrode):
    elektroda_index_map = {value: idx for idx, value in enumerate(elektrode)}
    indeks = [elektroda_index_map[ce] for ce in conf_elctrode]
    return np.array(indeks)

# Fungsi mapping untuk secondary x-axis

def make_position_to_index(a):
    def position_to_index(x): return x / a
    return position_to_index

def make_index_to_position(a):
    def index_to_position(x): return x * a
    return index_to_position