import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from geolistrik.utils.utils import (
    make_position_to_index,
    make_index_to_position
)

def make_plot(first, last, X, Y, a, electrode_pos, title):
	'''
	argument 1: penomoran titik ukur (first, last) => pandas.Dataframe
	argument 2: sumbu x dan y dari stacking chart
	argument 3: data spasi a dan electrode_pos
	argument 4: judul plot
	'''
	
	# Buat figure dan axis menggunakan subplots
	fig, ax = plt.subplots(figsize=(15, 5), facecolor='white', layout='constrained')

	# Penomoran titik ukur
	# Tambahkan anotasi dari first dan last
	for txt, x, y in zip(first.index, first['X'].values, first['Y'].values):
		ax.annotate(f'{txt + 1}', (x, y), fontsize=8)

	for txt, x, y in zip(last.index, last['X'].values, last['Y'].values):
		ax.annotate(f'{txt + 1}', (x, y), fontsize=8)

	# Mulai lakukan plot titik pengukuran
	# Scatter plot
	ax.scatter(X, Y, label='Measurement Point', s=10, color='black')

	# Judul dan label
	ax.set_title(title, fontsize=14, pad=20)
	ax.set_xlabel('Electrode Distance (m)')
	ax.set_ylabel('Level n')

	# Ubah tampilan sumbu
	ax.invert_yaxis()
	ax.xaxis.tick_top()
	ax.xaxis.set_label_position('top')
	ax.yaxis.tick_left()

	# Menambah sumbu x kedua untuk nomor elektroda
	# Fungsi mapping untuk secondary x-axis
	position_to_index = make_position_to_index(electrode_pos)
	index_to_position = make_index_to_position(electrode_pos)

	# Secondary x-axis di bawah (bukan atas, supaya tidak tabrakan dengan yang utama)
	secax = ax.secondary_xaxis(1.2, functions=(position_to_index, index_to_position))
	secax.set_xlabel('Electrode Number')
	secax.xaxis.tick_top()
	secax.xaxis.set_label_position('top')

	print("xlim before save:", ax.get_xlim())
	print("secax before save:", secax.get_xlim())

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

	# Legenda
	ax.legend(loc='lower right')

	return fig
	