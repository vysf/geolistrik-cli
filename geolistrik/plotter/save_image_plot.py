import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def save_image_plot(fig, image_path):
	# Simpan gambar plot
	fig.savefig(image_path)
	plt.close(fig)
