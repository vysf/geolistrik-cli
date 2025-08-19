import os
import numpy as np
import pandas as pd

from rich.console import Console
from rich.progress import track

from geolistrik.plotter.make_plot import make_plot
from geolistrik.plotter.save_image_plot import save_image_plot
from geolistrik.utils.send_acquisition_profiling import send_acquisition_profiling
from geolistrik.utils.utils import (
    save_to_excel_by_sheet,
    mapping_by_index
)

console = Console()

def dipole_dipole(x1, x2, a):
    electrode_pos = np.arange(x1, x2 + 1, a)
    A, B, M, N, X, Y = [], [], [], [], [], []
    max_n = len(electrode_pos)  # estimasi max level n

    for n in track(range(1, max_n), description="Processing levels"):
        for i in range(len(electrode_pos)):
            num = i + (2 + n)
            if num >= len(electrode_pos):
                break
            A.append(electrode_pos[i])
            B.append(electrode_pos[i + 1])
            M.append(electrode_pos[i + (1 + n)])
            N.append(electrode_pos[i + (2 + n)])
            X.append(B[-1] + (M[-1] - B[-1]) / 2)
            Y.append(n)
        if n == 1 and len(A) == 0:
            break

    return np.array(A), np.array(B), np.array(M), np.array(N), np.array(X), np.array(Y), electrode_pos

def run(x1, x2, a, output_dir=".", plot=True):
    console.print("[bold cyan]⏳ Generating Dipole-Dipole configuration...[/]")

    A, B, M, N, X, Y, electrode_pos = dipole_dipole(x1, x2, a)

    measurement_points = list(range(1, len(A)+1))
    geometry_factor = np.pi * Y * (Y + 1) * (Y + 2) * a

    df_by_distance = pd.DataFrame({
        'Measurement Points': measurement_points,
        'Levels n': Y,
        'X-location': X,
        'A': A,
        'B': B,
        'M': M,
        'N': N,
        'V': [None] *  len(A),
        'I': [None] * len(A),
        'k': geometry_factor
    })

    df_by_elctrode_num = df_by_distance.copy()
    df_by_elctrode_num['A'] = mapping_by_index(A, electrode_pos)
    df_by_elctrode_num['B'] = mapping_by_index(B, electrode_pos)
    df_by_elctrode_num['M'] = mapping_by_index(M, electrode_pos)
    df_by_elctrode_num['N'] = mapping_by_index(N, electrode_pos)

    excel_name = f"dipole_dipole_{x1}_{x2}_a{a}.xlsx"
    excel_path = os.path.join(output_dir, excel_name)
    current_excel_path = os.path.realpath(excel_path)

    save_to_excel_by_sheet(
        filename=excel_path,
        dfs=[df_by_distance, df_by_elctrode_num],
        sheet_names=["By Distance", "By Electrode Numbers"]
    )

    # Send data acquisition profiling message
    send_acquisition_profiling(x1, x2, a, Y, electrode_pos, "Dipole-Dipole")

    if plot:
        image_name = f"dipole_dipole_{x1}_{x2}_a{a}.png"
        image_path = os.path.join(output_dir, image_name)
        current_image_path = os.path.realpath(image_path)

        # Penomoran titik ukur
        df_plot = pd.DataFrame({
            'X': X,
            'Y': Y
        })

        # Siapkan data first dan last
        first = df_plot[df_by_distance['A'] == x1]
        last = df_plot[df_by_distance['N'] == x2]

        # buat plot
        fig = make_plot(first, last, X, Y, a, electrode_pos, 'Stacking Chart of Dipole-Dipole Configuration')
        
        # simpan gambar plot
        save_image_plot(fig, image_path)

        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{current_excel_path}[/]")
        console.print(f"🖼  Chart: [bold]{current_image_path}[/]")
    else:
        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{current_excel_path}[/]")
        console.print(f"🖼  Chart: [yellow]Skipped (--no-plot)[/]")
