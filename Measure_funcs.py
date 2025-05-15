import numpy as np

# Functions used for measures
def synch_array_generator(neuron_list, t_max, neuron_type, g_ks_t, dt=0.1, bin_size=None):
    """
    This function calculates the Golomb synchrony measure and average g_ks values
    over successive time bins for a specified neuron population (excitatory or inhibitory).

    Inputs:
        neuron_list (dict of dicts):
            Nested dictionary of neurons.
            - Keys: Integers (0–799 for excitatory or 0–199 for inhibitory)
            - Each entry is a dictionary with:
                - "spike times": List of floats representing spike times in ms

        t_max (int): Length of simulation in ms

        neuron_type (int):
            - 0 for excitatory neurons
            - 1 for inhibitory neurons

        g_ks_t (numpy array): Time series of g_ks values, one per simulation step.

        dt (float, optional): Integration time step in ms (default is 0.1 ms)

        bin_size (int, optional): Time window size for each synchrony measurement in ms.
                                  Defaults to int(400 / (8000 / (t_max - 1000)))

    Outputs:
        synchrony_array (list of floats):
            Golomb synchrony values calculated in each bin over the simulation period

        g_ks_average_array (list of floats):
            Average g_ks values corresponding to each bin
    """

    if neuron_type == 0:
        spike_list_for_golomb = [neuron_list[neuron]["spike times"] for neuron in range(800)]
        cell_count = 800
    elif neuron_type == 1:
        spike_list_for_golomb = [neuron_list[neuron]["spike times"] for neuron in range(200)]
        cell_count = 200

    if bin_size is None:
        bin_size = int(400 / (8000 / (t_max - 1000)))

    synchrony_array = []
    g_ks_average_array = []

    for bin_number in range(1000, t_max, bin_size):
        measure_start_duration = bin_number
        measure_end_duration = bin_number + bin_size
        measure_length = measure_end_duration - measure_start_duration

        spike_list_window = processSpikesForSync(
            spike_list_for_golomb,
            measure_start_duration,
            measure_end_duration,
            cell_count
        )

        synchrony = syncmeasure(
            cell_count,
            spike_list_window,
            gauss_width=2,
            duration_sec=measure_length / 1000
        )

        synchrony_array.append(synchrony)

        g_ks_interval_average = np.mean(
            g_ks_t[int(measure_start_duration / dt): int(measure_end_duration / dt)]
        )
        g_ks_average_array.append(g_ks_interval_average)

    return synchrony_array, g_ks_average_array


def syncmeasure(cellnum, spikes, gauss_width, duration_sec):
    """
    This function calculates the Golomb synchrony measure for a given population of neurons.

    Inputs:
        cellnum (int): Number of neurons in the population (set to 800 for excitatory and 200 for inhibitory).

        spikes (list of lists): Each sublist contains spike times in ms for a single neuron.

        gauss_width (float): Width of the Gaussian kernel in ms.

        duration_sec (float): Total duration of the simulation in s.

    Outputs:
        G_rescaled (float): Golomb synchrony measure quantifying the level of synchronization across neurons. Assumes
                            values from 0 to 1.
    """

    srate = 1000  # Sampling rate in Hz
    duration = duration_sec
    times = np.arange(1000 / srate, duration * 1000 + 1, 1000 / srate)
    timeseries = np.zeros((int(srate * duration), cellnum))

    # Convert spike times to binary time series at 1000Hz
    for i in range(cellnum):
        times, timeseries[:, i] = convert_spiketimes(spikes[i], duration, srate)

    if gauss_width <= 0:
        gauss_width = 2

    # Convolve binary time series with Gaussian kernel
    conv_sig = np.zeros_like(timeseries)
    for i in range(cellnum):
        conv_sig[:, i] = conv_gaussian(timeseries[:, i], srate, gauss_width)

    # Compute Golomb synchrony measure
    G_rescaled, meansig = golomb_synch(conv_sig, times)

    return G_rescaled


def convert_spiketimes(spike_times, duration, srate):
    """
    This function takes a vector 'spike_times' (which lists spike times in
    ms), then converts the list of spike times into a time series of
    ones and zeros, with a one indicating a spike at a certain time. The user
    specifies the sampling rate (in Hz) and the duration of the resulting
    signal (in s)
    """
    times = 1000 * np.arange(1 / srate, duration + 1 / srate,
                             1 / srate);  # time stamps (in ms) corresonding to each entry in signal
    signal = np.zeros((int(duration * srate),
                       1));  # number of points in final signal will be the number of seconds multiplied by samples per second
    Npoints = len(signal);
    # use the vector 'spike_times' to insert ones in 'signal' where appropriate
    for i_s in range(len(spike_times)):
        # 1000*duration is the duration of the signal in ms;
        # multiply the fraction of the way through the signal the spike
        # occurs by the number of points in the discrete signal, and round
        # to obtain the index of the spike
        if int(np.floor(spike_times[i_s] / (duration * 1000) * Npoints)) == 1000:
            signal[int(np.floor(spike_times[i_s] / (duration * 1000) * Npoints)) - 1] = 1;
        else:
            signal[int(np.floor(spike_times[i_s] / (duration * 1000) * Npoints))] = 1;

    return times, signal[:, 0]


def conv_gaussian(signal, srate, gauss_width):
    """
    This function takes a time series sampled at a rate 'srate' (specified in Hz)
    and convolves it with a Gaussain with sd 'gauss_width (ms)'
    """

    N_gauss = round(6 * (gauss_width / 1000) * srate);  # want a standard deviation of 2ms typically

    # Want the number of points in the Gaussian to be odd, so that it is
    # centrally peaked, rather than flat at the top
    if (N_gauss % 2) == 0:
        N_gauss = N_gauss - 1
    x = np.linspace(-3, 3, N_gauss)
    g = np.exp(-x ** 2)  # note that this does not integrate to 1; instead, the peak is always 1
    newsig = np.convolve(signal, g, 'same')
    return newsig


def golomb_synch(sig_mat, times):
    """
    This function calculates the "Golomb synchrony" of multiple signals
    (Golomb and Rinzel, 1993/1994). sig_mat is a matrix of signals in which
    each COLUMN is a different signal
    """
    N = len(sig_mat[:, 0]);  # number of neurons (or signals) is equal to number of columns in sig_mat
    mean_sig = np.mean(sig_mat, axis=1);  # calculate the mean signal
    variances = np.var(sig_mat,
                       axis=0);  # this is a row vector, where each entry is the variance of one of the columns in sig_mat
    G = np.sqrt(np.var(mean_sig, axis=0) / np.mean(variances));  # calculate the actual synchrony measure
    # the Golomb measure only goes to zero for asynchronous signals in the limit as the number of
    # neurons goes to infinity; with N neurons, the lowest possible value is
    # 1/sqrt(N), so we rescale G according to N so that it goes from 0 to 1
    G_rescaled = (G - 1 / np.sqrt(N)) / (1 - 1 / np.sqrt(N));
    # with this transformation, G_rescaled can go slightly negative due to
    # randomness in the signals, so we should just set G_rescaled to 0 if it
    # goes negative
    if G_rescaled < 0:
        G_rescaled = 0

    return G_rescaled, mean_sig


def processSpikesForSync(spikes, start, end, numcells):
    spikes_end = []
    for k in range(numcells):
        spikes_end.append([(j - (start)) for j in spikes[k] if (j > start) and (j < end)])
    return spikes_end
