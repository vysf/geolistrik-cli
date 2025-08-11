import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rich.console import Console
from rich.progress import track

from geolistrik.utils.utils import (
    save_to_excel_by_sheet,
    mapping_by_index,
    make_position_to_index,
    make_index_to_position
)

console = Console()

def pole_pole(x1, x2, a):
    electrode_pos = np.arange(x1, x2 + 1, a)
    A, M = [], []
    X, Y = [], []
    max_n = len(electrode_pos)  # Estimasi maksimum level n

    for n in track(range(1, max_n), description="Processing levels"):
        for i in range(len(electrode_pos)):
            num = i + n
            if num >= len(electrode_pos):
                break
            A.append(electrode_pos[i])
            M.append(electrode_pos[i + n])
            X.append(A[-1] + (M[-1] - A[-1]) / 2)
            Y.append(n)
        # Jika tidak ada data di level pertama, hentikan
        if n == 1 and len(A) == 0:
            break

    return np.array(A), np.array(M), np.array(X), np.array(Y), electrode_pos

def run(x1, x2, a, output_dir=".", plot=True):
    console.print("[bold cyan]⏳ Generating Pole-Pole configuration...[/]")

    A, M, X, Y, electrode_pos = pole_pole(x1, x2, a)

    measurement_points = list(range(1, len(A)+1))
    spacing = a * Y
    geometry_factor = 2 * np.pi * spacing

    df_by_distance = pd.DataFrame({
        'Measurement Points': measurement_points,
        'Levels n': Y,
        'a': spacing,
        'A': A,
        'M': M,
        'V': [None] *  len(A),
        'I': [None] * len(A),
        'k': geometry_factor
    })

    df_by_elctrode_num = df_by_distance.copy()
    df_by_elctrode_num['A'] = mapping_by_index(A, electrode_pos)
    df_by_elctrode_num['M'] = mapping_by_index(M, electrode_pos)

    excel_name = f"pole_pole_{x1}_{x2}_a{a}.xlsx"
    image_name = f"pole_pole_{x1}_{x2}_a{a}.png"
    excel_path = os.path.join(output_dir, excel_name)
    image_path = os.path.join(output_dir, image_name)

    save_to_excel_by_sheet(
        filename=excel_path,
        dfs=[df_by_distance, df_by_elctrode_num],
        sheet_names=["By Distance", "By Electrode Numbers"]
    )

    df_plot = pd.DataFrame({
        'X': X,
        'Y': Y
    })

    if plot:
        # Siapkan data first dan last
        first = df_plot[df_by_distance['A'] == x1]
        last = df_plot[df_by_distance['M'] == x2]

        # Buat figure dan axis menggunakan subplots
        fig, ax = plt.subplots(figsize=(15, 5), facecolor='white', layout='constrained')

        # Scatter plot
        ax.scatter(X, Y, label='Measurement Point', s=10, color='black')

        # Tambahkan anotasi dari first dan last
        for txt, x, y in zip(first.index, first['X'].values, first['Y'].values):
            ax.annotate(f'{txt + 1}', (x, y), fontsize=8)

        for txt, x, y in zip(last.index, last['X'].values, last['Y'].values):
            ax.annotate(f'{txt + 1}', (x, y), fontsize=8)

        # Judul dan label
        ax.set_title('Stacking Chart of Pole-Pole Configuration', fontsize=14, pad=20)
        ax.set_xlabel('Electrode Distance (m)')
        ax.set_ylabel('Level n')

        # Ubah tampilan sumbu
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        ax.yaxis.tick_left()

        # Fungsi mapping untuk secondary x-axis
        position_to_index = make_position_to_index(a)
        index_to_position = make_index_to_position(a)

        # Secondary x-axis di bawah (bukan atas, supaya tidak tabrakan dengan yang utama)
        secax = ax.secondary_xaxis(1.2, functions=(position_to_index, index_to_position))
        secax.set_xlabel('Electrode Number')
        secax.xaxis.tick_top()
        secax.xaxis.set_label_position('top')

        # Atur ticks jika electrode_pos tidak terlalu banyak
        if len(electrode_pos) <= 40:
            electrode_num = np.arange(1, len(electrode_pos) + 1)
            secax.set_xticks(electrode_num)
            ax.set_xticks(electrode_pos)

        if max(Y) <= 30:
            ax.set_yticks(np.unique(Y))

        # Tambahan styling sumbu
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['top'].set_color('black')

        # Legenda dan simpan
        ax.legend(loc='lower right')
        fig.savefig(image_path)
        plt.close(fig)

        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{excel_path}[/]")
        console.print(f"🖼  Chart: [bold]{image_path}[/]")
    else:
        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{excel_path}[/]")
        console.print(f"🖼  Chart: [yellow]Skipped (--no-plot)[/]")
