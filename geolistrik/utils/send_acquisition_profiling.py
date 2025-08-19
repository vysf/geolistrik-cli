def send_acquisition_profiling(x1, x2, a, Y, electrode_pos, configuration_array):
	print(f"Configuration array: {configuration_array}")
	print(f"Minimum electrode spacing (a): {a} meters")
	print(f"Total number of electrodes: {len(electrode_pos)}")
	print(f"Total number of data points: {len(Y)}")
	print(f"Total number of levels: {max(Y)}")
	print(f"Measurement line length: {abs(x1 - x2)} meters")
	print(f"First electrode position: {x1}")
	print(f"Last electrode position: {x2}")
