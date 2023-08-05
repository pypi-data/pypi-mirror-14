import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq
import time

SAMPLING_RATE = 44100.


def compute_schroeder(h):
    # time-reversed integration of the square of the signal
    return 10 * np.log(np.cumsum((h ** 2)[::-1])[::-1])


def t60_fitfunc(p, x):
    return p[0] + p[1] * x


def compute_t60(schroeder_dB, t):
    # t60 is the time to go from -5 dB (0 dB is direct path amplitude) to -65 dB on the Shroeder plot
    # do a

    # find ref level at max energy
    ref_level_dB = schroeder_dB[0]

    position0_level_dB = 5
    position1_level_dB = 35  # 25

    # find where the cumulative energy is 5dB below
    position0_samples = np.where(schroeder_dB < ref_level_dB - position0_level_dB)[0][0]
    # find where the cumulative energy is 25dB below (from ISO3382)
    position1_samples = np.where(schroeder_dB < ref_level_dB - position1_level_dB)[0][0]

    s_fit = schroeder_dB[position0_samples:position1_samples]
    t_fit = t[position0_samples:position1_samples]

    # def errfunc(p, x, y):
    #       return t60_fitfunc(p, x) - y
    # p0 = [0., -0.5]
    # do a least square fit of the data between the -5dB and -25dB positions to extract decay slope
    # p, success = leastsq(errfunc, p0, args=(t_fit, s_fit))

    # least square fit with an affine function is easy:
    y = s_fit
    x = t_fit

    sum_x = np.sum(x)
    sum_x2 = np.sum(x ** 2)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    N = x.size

    det = N * sum_x2 - sum_x ** 2

    p0 = 1. / det * (sum_x2 * sum_y - sum_x * sum_xy)
    p1 = 1. / det * (-sum_x * sum_y + N * sum_xy)
    p = [p0, p1]

    # compute T60 from decay slope. T60 is the time it takes to lose 60dB
    t60 = 60. / (-p[1])
    return t60, t_fit, s_fit, p


STI_modulation_frequencies = [0.63, 0.8, 1., 1.25, 1.6, 2., 2.5, 3.15, 4., 5., 6.3, 8., 10., 12.5]

# FIXME should take into account room noise level !!


def compute_sti(h, t, SNR_dB):
    # we will need a frequency resolution of 0.1 Hz => zero-pad h**2 to 10s
    # however we do not need to go above 12.5 Hz => downsample h**2 to 25 Hz
    # (apart from total energy whic is computed before downsampling)
    h2_SAMPLING_RATE = 50.  # SAMPLING_RATE/300.

    # 1. square of the impulse response
    # h2 = h**2
    h2_unpadded = h ** 2

    # 2. compute the total energy
    H2 = np.sum(h2_unpadded)

    h2 = np.zeros(SAMPLING_RATE * 10.)
    h2[:len(h2_unpadded)] = h2_unpadded

    N = h2_SAMPLING_RATE * 10.

    h2.shape = (N, SAMPLING_RATE / h2_SAMPLING_RATE)
    h2 = np.mean(h2, axis=1)

    # 3. compute the enveloppe spectrum
    h2_ = fft(h2) * (SAMPLING_RATE / h2_SAMPLING_RATE)

    # 4. normalize the enveloppe spectrum
    h2n_ = h2_ / H2

    # 5. take its modulus
    h2n_m = np.abs(h2n_)

    freq = fftfreq(h2.size, 1. / h2_SAMPLING_RATE)

    modulation_indices = []
    for f in STI_modulation_frequencies:
        # find indexes
        i = np.where((freq[:-1] <= f) * (freq[1:] > f))[0][0]
        modulation_indices.append(i)
    # print "mod indices", modulation_indices

    # 6. retrieve modulation for the characteristic speech frequencies
    m = h2n_m[modulation_indices]
    # print "m", m

    # 6.bis. take noise level into account in the modulation
    m = m / (1. + 10 ** (-SNR_dB / 10.))

    # 7. convert the modulation to an apparent SNR
    apparent_SNR = 10. * np.log(m / (1. - m))
    # print "apparent_SNR", apparent_SNR

    # 8. limit the range
    apparent_SNR = np.clip(apparent_SNR, -15., +15.)

    # 9. compute the mean
    mean_apparent_SNR = np.mean(apparent_SNR)

    # 10. convert to STI
    STI = (mean_apparent_SNR + 15.) / 30.

    return STI


def compute_spectrogram(h, fft_size):
    sfft_freq = fftfreq(fft_size, 1. / SAMPLING_RATE)
    overlap = 3. / 4.
    n = fft_size * (1. - overlap)
    realizable = int(np.floor(h.size / n))

    window = np.hanning(fft_size)

    spn = np.zeros((fft_size / 2 + 1, realizable), dtype=np.float64)

    for i in range(realizable):
        floatdata = h[i * n:i * n + fft_size]

        if floatdata.size < fft_size:
            bak = floatdata.copy()
            floatdata = np.zeros(fft_size)
            floatdata[:len(bak)] = bak

        # FIXME We should allow here for more intelligent transforms, especially when the log freq scale is selected
        spn[:, i] = 20. * np.log(np.abs(fft(floatdata * window)[:fft_size / 2 + 1]))

    return spn

# this code is also in filter.py


def octave_frequencies(Nbands, BandsPerOctave):
    f0 = 1000.  # audio reference frequency is 1 kHz

    b = 1. / BandsPerOctave

    imax = Nbands / 2
    if Nbands % 2 == 0:
        i = np.arange(-imax, imax)
    else:
        i = np.arange(-imax, imax + 1)

    if BandsPerOctave % 2 == 1:
        fi = f0 * 2 ** (i * b)
    else:
        # FIXME the official formula does not seem to work !
        fi = f0 * 2 ** (i * b)  # fi = f0 * 2**((2*i+1)*b/2.)

    f_low = fi * np.sqrt(2 ** (-b))
    f_high = fi * np.sqrt(2 ** b)

    return fi, f_low, f_high


def compute_delay(h):
    h2 = h ** 2

    h2_ = fft(h2)

    N = len(h2_)
    Nf = 100
    h2_[N / Nf:-N / Nf] = 0.
    h2_filtered = ifft(h2_)

    delay_samples = np.argmax(h2)
    delay_s = delay_samples / float(SAMPLING_RATE)
    delay_ms = delay_s * 1e3
    c_sound = 340.  # m/s
    delay_m = delay_s * c_sound

    return delay_samples, delay_ms, delay_m, h2, h2_filtered


def w(x, sigma):
    # FWHM is 2*sigma
    return 1. / (np.sqrt(2 * np.pi) * sigma) * np.exp(-x ** 2 / (2 * sigma ** 2)) * (abs(x) < 4 * sigma)

# can be accelerated with Cython
# need only to be computed once when sigma is chosen or when range of frequencies change


def precompute_W(flog_, f_, sigma):
    sumW = np.zeros((flog_.size))
    W = np.zeros((flog_.size, f_.size))

    for i, f in enumerate(flog_):
        W[i, :] = w(np.log10(f_ / f), sigma)
        sumW[i] = np.sum(W[i, :])

    return W, sumW

# can be accelerated with Cython


def convolve(h_, W, sumW):
    hlog_ = np.zeros(W[:, 0].size)
    for i in range(len(hlog_)):
        hlog_[i] = np.sum(W[i, :] * h_) / sumW[i]
    return hlog_


def main():
    filename = "IR_auxerre.npy"  # "rir_npvss_sc_ipmdf.npy" # "rir.npy"
    print(filename)

    h = np.load(filename)
    t = np.arange(len(h)) / float(SAMPLING_RATE)
    freq = fftfreq(h.size, 1. / SAMPLING_RATE)

    t0 = time.time()

    delay_samples, delay_ms, delay_m, h2, h2_filtered = compute_delay(h)
    print("delay = %d samples = %f ms = %f m" % (delay_samples, delay_ms, delay_m))

    schroeder_dB = compute_schroeder(h)

    t60, t_fit, s_fit, p1 = compute_t60(schroeder_dB, t)
    print("t60 = %.3f s" % (t60))
    # FIXME handle nonlinear decay curve with two reverberation times
    # FIXME handle noise level of the impulse response

    # Subband reverberation times
    # first, filter the impulse response in bands

    # then recompute t60 in each band

    # spectrogram of the impulse response, to identify room modes
    fft_size = 1024
    spn = compute_spectrogram(h, fft_size)

    # octave spectrum of the impulse response (for equalization)
    Nbands = 7
    BandsPerOctave = 1
    fi, f_low, f_high = octave_frequencies(Nbands, BandsPerOctave)

    h_ = fft(h)

    t60_subband = []
    p1_subband = []
    h_subband = []
    schroder_subband = []
    sti_subband = []

    for f, fl, fh in zip(fi, f_low, f_high):
        # filter in the frequency domain
        hi_ = h_.copy()
        ifl = np.where((freq[:-1] <= fl) * (freq[1:] > fl))[0][0]
        ifh = np.where((freq[:-1] <= fh) * (freq[1:] > fh))[0][0]
        hi_[:ifl] = 0.
        hi_[ifh:1 - ifh] = 0.
        hi_[1 - ifl:] = 0.

        # normalize by the bandwidth
        hi_ /= np.sqrt(ifh - ifl)

        # back to time domain
        hi = ifft(hi_).real
        h_subband.append(hi)

        # compute schroeder decay curve
        schroder_i = compute_schroeder(hi)
        schroder_subband.append(schroder_i)

        # compute t60
        t60, t_fit_i, s_fit_i, p1_i = compute_t60(schroder_i, t)
        t60_subband.append(t60)
        p1_subband.append(p1_i)

        # compute STI
        SNR_dB = 5.
        sti = compute_sti(hi, t, SNR_dB)
        sti_subband.append(sti)

        print(f, "t60", t60, "power", 10. * np.log(np.sum(hi ** 2)), "STI", sti)

    # fullband STI

    # Weighting factors
    # octave center   125    250    500     1k     2k     4k     8k
    alpha_male = [0.085, 0.127, 0.230, 0.233, 0.309, 0.224, 0.173]
    beta_male = [0.085, 0.078, 0.065, 0.011, 0.047, 0.095]
    alpha_female = [0.,    0.117, 0.223, 0.216, 0.328, 0.250, 0.194]
    beta_female = [0.,    0.099, 0.066, 0.062, 0.025, 0.076]

    STIr_male = np.sum(np.array(alpha_male) * np.array(sti_subband)) - np.sum(np.array(beta_male) * np.array(sti_subband[1:]) * np.array(sti_subband[:-1]))
    STIr_female = np.sum(np.array(alpha_female) * np.array(sti_subband)) - np.sum(np.array(beta_female) * np.array(sti_subband[1:]) * np.array(sti_subband[:-1]))
    print("STIr male = %.2f STIr female = %.2f" % (STIr_male, STIr_female))

    # STI here does not take absolute hearing threshold into account (because measurement is not calibrated in SPL)
    # nor does it take masking effects into account (that depend on the signal being diffused)

    t1 = time.time()
    print("computed in %.3f s" % (t1 - t0))

    x = np.linspace(-5., 5., 100)
    sigma = 1.
    y = 1. / (np.sqrt(2 * np.pi) * sigma) * np.exp(-x ** 2 / (2 * sigma ** 2)) * (abs(x) < 4 * sigma)
    # FWHM is 2*sigma

    # plt.semilogx(freq[:len(h)/2], 20.*np.log(np.abs(fft(h)[:len(h)/2])))

    h_ = np.abs(fft(h)[:len(h) / 2])
    f_ = freq[:len(h) / 2]

    b = 1. / 24  # 1/12-octave smoothing
    sigma = b * np.log(2.) / 2.

    # how many points do I need for proper sampling ?
    Nlog = 4 * int(np.ceil((np.log10(22000.) - np.log10(20.)) / sigma))

    flog_ = np.logspace(np.log10(20.), np.log10(22000.), Nlog)

    W, sumW = precompute_W(flog_, f_, sigma)

    hlog_ = convolve(h_, W, sumW)

    t2 = time.time()
    print("smoothing computed in %.3f s" % (t2 - t1))

    if False:
        plt.figure()
        plt.semilogx(f_, 20. * np.log10(h_))
        plt.semilogx(flog_, 20. * np.log10(hlog_))
        plt.show()
