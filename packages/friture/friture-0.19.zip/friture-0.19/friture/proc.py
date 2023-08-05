from numpy import log10, floor, zeros, float64, tile, array

def process_data(data, freqs, w, spec_min, spec_max, proc):
    print("Process data")
    spn = zeros((len(freqs), data.shape[1]), dtype=float64)

    for i in range(data.shape[1]):
        spn[:, i] = proc.analyzelive(data[:, i])

    tiled_w = tile(w, (1, data.shape[1]))
    sp = log_spectrogram(spn) + tiled_w
    norm_spectrogram = (sp - spec_min) / (spec_max - spec_min)

    return norm_spectrogram

def log_spectrogram(sp):
    # Note: implementing the log10 of the array in Cython did not bring
    # any speedup.
    # Idea: Instead of computing the log of the data, I could pre-compute
    # a list of values associated with the colormap, and then do a search...
    epsilon = 1e-30
    return 10. * log10(sp + epsilon)