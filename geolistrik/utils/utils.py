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