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

def wenner_schlumberger(x1, x2, a):
    elektroda = np.arange(x1, x2 + 1, a)
    A, M, N, B = [], [], [], []
    X, Y = [], []
    n = 1

    # Tidak bisa prediksi max_n mudah, jadi buat loop dengan progress track manual
    max_iterations = len(elektroda)  # upper bound supaya track ada progress
    for _ in track(range(max_iterations), description="Processing levels"):
        level_processed = False
        for i in range(len(elektroda)):
            num = i + (2 * n) + 1
            if num >= len(elektroda):
                break
            A.append(elektroda[i])
            M.append(elektroda[i + (1 * n)])
            N.append(elektroda[i + (1 + n)])
            B.append(elektroda[i + (2 * n) + 1])
            X.append(M[-1] + (N[-1] - M[-1]) / 2)
            Y.append(n)
            level_processed = True
        if not level_processed:
            break
        n += 1

    return np.array(A), np.array(M), np.array(N), np.array(B), np.array(X), np.array(Y), elektroda

def run(x1, x2, a, output_dir=".", plot=True):
    console.print("[bold cyan]⏳ Generating Wenner-Schlumberger configuration...[/]")

    A, M, N, B, X, Y, elektroda = wenner_schlumberger(x1, x2, a)

    measurement_points = list(range(1, len(A)+1))
    geometry_factor = np.pi * Y * (Y + 1) * a

    df_by_distance = pd.DataFrame({
        'Measurement Points': measurement_points,
        'Levels n': Y,
        'A': A,
        'M': M,
        'N': N,
        'B': B,
        'V': [None] *  len(A),
        'I': [None] * len(A),
        'k': geometry_factor
    })

    df_by_elctrode_num = df_by_distance.copy()
    df_by_elctrode_num['A'] = mapping_by_index(A, elektroda)
    df_by_elctrode_num['M'] = mapping_by_index(M, elektroda)
    df_by_elctrode_num['N'] = mapping_by_index(N, elektroda)
    df_by_elctrode_num['B'] = mapping_by_index(B, elektroda)

    excel_name = f"wenner_schlumberger_{x1}_{x2}_a{a}.xlsx"
    image_name = f"wenner_schlumberger_{x1}_{x2}_a{a}.png"
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
        last = df_plot[df_by_distance['B'] == x2]

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
        ax.set_title('Stacking Chart of Wenner-Schlumberger Configuration', fontsize=14, pad=20)
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

        # Atur ticks jika elektroda tidak terlalu banyak
        if len(elektroda) <= 30:
            secax.set_xticks(np.arange(len(elektroda)))
            ax.set_xticks(elektroda)
        else:
            secax.set_xticks([])
            ax.set_xticks([])

        # Tambahan styling sumbu
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['top'].set_color('black')

        # Grid dan ticks
        ax.grid(False)
        ax.set_yticks(Y)

        # Legenda dan simpan
        ax.legend(loc='lower right')
        # fig.tight_layout()
        fig.savefig(image_path)
        plt.close(fig)

        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{excel_path}[/]")
        console.print(f"🖼  Chart: [bold]{image_path}[/]")
    else:
        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{excel_path}[/]")
        console.print(f"🖼  Chart: [yellow]Skipped (--no-plot)[/]")
