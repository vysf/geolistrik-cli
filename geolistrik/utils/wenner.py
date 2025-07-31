import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rich.console import Console
from rich.spinner import Spinner
from rich.progress import track

console = Console()

def wenner(x1, x2, a):
    elektroda = np.arange(x1, x2 + 1, a)
    A, M, N, B = [], [], [], []
    X, Y = [], []

    max_n = (len(elektroda) - 1) // 3

    for n in track(range(1, max_n + 1), description="Processing levels"):
        for i in range(len(elektroda)):
            num = i + (3 * n)
            if num >= len(elektroda):
                break
            A.append(elektroda[i])
            M.append(elektroda[i + (1 * n)])
            N.append(elektroda[i + (2 * n)])
            B.append(elektroda[i + (3 * n)])
            X.append(M[-1] + (N[-1] - M[-1]) / 2)
            Y.append(n)
        
        # Kalau di iterasi pertama pun tidak bisa proses, hentikan
        if n == 1 and len(A) == 0:
            break
    return np.array(A), np.array(M), np.array(N), np.array(B), np.array(X), np.array(Y), elektroda

def run(x1, x2, a, output_dir=".", plot=True):
    console.print("[bold cyan]⏳ Generating Wenner configuration...[/]")

    # Data processing (dengan progress bar di fungsi wenner)
    A, M, N, B, X, Y, elektroda = wenner(x1, x2, a)

    df = pd.DataFrame({
        'A': A, 'M': M, 'N': N, 'B': B,
        'X': X, 'Y': Y
    })

    # File paths
    excel_name = f"wenner_{x1}_{x2}_a{a}.xlsx"
    image_name = f"wenner_{x1}_{x2}_a{a}.png"
    excel_path = os.path.join(output_dir, excel_name)
    image_path = os.path.join(output_dir, image_name)

    # Save to Excel
    df.to_excel(excel_path, index=False)

    # Plotting
    if plot:
        first = df[df['A'] == x1]
        last = df[df['B'] == x2]

        plt.figure(figsize=(15, 5), facecolor='white')  # Kanvas putih
        plt.scatter(X, Y, label='Datum', s=10, color='black')  # Titik berwarna hitam

        # Anotasi untuk titik awal dan akhir
        for txt, x, y in zip(first.index, first['X'].values, first['Y'].values):
            plt.annotate(f'{txt + 1}', (x, y), fontsize=8)
        for txt, x, y in zip(last.index, last['X'].values, last['Y'].values):
            plt.annotate(f'{txt + 1}', (x, y), fontsize=8)

        # Judul dan label
        plt.title('Stacking Chart - Wenner Configuration', fontsize=14, pad=20)
        plt.xlabel('Electrode', fontsize=12, labelpad=15)
        plt.ylabel('Level n', fontsize=12)

        # Set sumbu dan posisi garis
        ax = plt.gca()
        ax.invert_yaxis()                   # Arah Y ke bawah
        ax.xaxis.tick_top()                # Sumbu X di atas
        ax.xaxis.set_label_position('top')
        ax.yaxis.tick_left()               # Sumbu Y di kiri
        ax.spines['right'].set_visible(False)  # Hilangkan sisi kanan
        ax.spines['bottom'].set_visible(False) # Hilangkan sisi bawah
        ax.spines['left'].set_color('black')   # Warna sumbu kiri
        ax.spines['top'].set_color('black')    # Warna sumbu atas

        # Tidak pakai grid
        plt.grid(False)

        # Atur jumlah tick
        plt.xticks(elektroda if len(elektroda) <= 30 else None)
        plt.yticks(Y)

        plt.legend()
        plt.tight_layout()
        plt.savefig(image_path)
        plt.close()


        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{excel_path}[/]")
        console.print(f"🖼  Chart: [bold]{image_path}[/]")
    else:
        console.print(f"\n[green]✔ Data saved successfully![/]")
        console.print(f"📄 Excel: [bold]{excel_path}[/]")
        console.print(f"🖼  Chart: [yellow]Skipped (--no-plot)[/]")