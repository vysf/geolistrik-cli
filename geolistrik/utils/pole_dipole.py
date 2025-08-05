import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rich.console import Console
from rich.progress import track

console = Console()

def pole_dipole(x1, x2, a):
    elektroda = np.arange(x1, x2 + 1, a)
    A, M, N, X, Y = [], [], [], [], []
    max_n = len(elektroda)  # estimasi maksimal level n

    for n in track(range(1, max_n), description="Processing levels"):
        for i in range(len(elektroda)):
            num = i + (1 + n)
            if num >= len(elektroda):
                break
            A.append(elektroda[i])
            M.append(elektroda[i + n])
            N.append(elektroda[i + (1 + n)])
            X.append(A[-1] + (M[-1] - A[-1]) / 2)
            Y.append(n)
        if n == 1 and len(A) == 0:
            break

    return np.array(A), np.array(M), np.array(N), np.array(X), np.array(Y), elektroda

def run(x1, x2, a, output_dir=".", plot=True):
    console.print("[bold cyan]⏳ Generating Pole-Dipole configuration...[/]")

    A, M, N, X, Y, elektroda = pole_dipole(x1, x2, a)

    df = pd.DataFrame({
        'A': A,
        'M': M,
        'N': N,
        'V': [None] *  len(A),
        'I': [None] * len(A)
    })

    excel_name = f"pole_dipole_{x1}_{x2}_a{a}.xlsx"
    image_name = f"pole_dipole_{x1}_{x2}_a{a}.png"
    excel_path = os.path.join(output_dir, excel_name)
    image_path = os.path.join(output_dir, image_name)

    df.to_excel(excel_path, index=False)

    df_plot = pd.DataFrame({
        'X': X,
        'Y': Y
    })

    if plot:
        first = df_plot[df['A'] == x1]
        last = df_plot[df['N'] == x2]

        plt.figure(figsize=(15, 5), facecolor='white')
        plt.scatter(X, Y, label='Datum', s=10, color='black')

        for txt, x, y in zip(first.index, first['X'], first['Y']):
            plt.annotate(f'{txt + 1}', (x, y), fontsize=8)
        for txt, x, y in zip(last.index, last['X'], last['Y']):
            plt.annotate(f'{txt + 1}', (x, y), fontsize=8)

        plt.title('Stacking Chart - Pole-Dipole Configuration', fontsize=14, pad=20)
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
