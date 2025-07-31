import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rich.console import Console
from rich.progress import track

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

    df = pd.DataFrame({
        'A': A, 'M': M, 'N': N, 'B': B,
        'X': X, 'Y': Y
    })

    excel_name = f"wenner_schlumberger_{x1}_{x2}_a{a}.xlsx"
    image_name = f"wenner_schlumberger_{x1}_{x2}_a{a}.png"
    excel_path = os.path.join(output_dir, excel_name)
    image_path = os.path.join(output_dir, image_name)

    df.to_excel(excel_path, index=False)

    if plot:
        first = df[df['A'] == x1]
        last = df[df['B'] == x2]

        plt.figure(figsize=(15, 5), facecolor='white')
        plt.scatter(X, Y, label='Datum', s=10, color='black')

        for txt, x, y in zip(first.index, first['X'].values, first['Y'].values):
            plt.annotate(f'{txt + 1}', (x, y), fontsize=8)
        for txt, x, y in zip(last.index, last['X'].values, last['Y'].values):
            plt.annotate(f'{txt + 1}', (x, y), fontsize=8)

        plt.title('Stacking Chart - Wenner-Schlumberger Configuration', fontsize=14, pad=20)
        plt.xlabel('Electrode', fontsize=12, labelpad=15)
        plt.ylabel('Level n', fontsize=12)

        ax = plt.gca()
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        ax.yaxis.tick_left()
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['top'].set_color('black')

        plt.grid(False)

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
