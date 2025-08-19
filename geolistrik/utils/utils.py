import numpy as np
import pandas as pd

def save_to_excel_by_sheet(filename, dfs, sheet_names):
    with pd.ExcelWriter(filename) as writer:
        for df, sheet in zip(dfs, sheet_names):
            df.to_excel(writer, sheet_name=sheet, index=False)

def mapping_by_index(conf_elctrode, elektrode):
    elektroda_index_map = {value: idx for idx, value in enumerate(elektrode)}
    indeks = [elektroda_index_map[ce] for ce in conf_elctrode]
    return np.array(indeks) + 1

# Fungsi mapping untuk secondary x-axis
def make_position_to_index(electrode_pos):
    def position_to_index(val):
        val = np.atleast_1d(val)
        # Anggap electrode_pos terdistribusi merata
        index_vals = (val - electrode_pos[0]) / (electrode_pos[1] - electrode_pos[0]) + 1
        return index_vals if val.size > 1 else index_vals[0]
    return position_to_index

def make_index_to_position(electrode_pos):
    def index_to_position(i):
        i = np.asarray(i, dtype=int)
        i = np.clip(i - 1, 0, len(electrode_pos) - 1)
        return electrode_pos[i]
    return index_to_position