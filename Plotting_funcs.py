import numpy as np
import matplotlib.pyplot as plt

def configure_spike_raster_plot(ax, neuron_list_exc, neuron_list_inh, time_window):
    """
    Modifies an Axes object to display a spike raster plot for excitatory and inhibitory neurons.

    Inputs:
        ax (matplotlib.axes.Axes): The Axes object to modify for plotting.

        neuron_list_exc (dict of dicts):
            Nested dictionary containing excitatory neurons sorted by firing frequency.
            - 800 string keys ("0" to "799")
            - Each key maps to a dictionary with:
                - "spike times": List of floats representing spike times in ms in chronological order.

        neuron_list_inh (dict of dicts):
            Nested dictionary containing inhibitory neurons sorted by firing frequency.
            - 200 string keys ("0" to "199")
            - Each key maps to a dictionary with:
                - "spike times": List of floats representing spike times in ms in chronological order.

        time_window (tuple):
            Tuple (start_time, end_time) defining x-axis limits in ms.
    """
    ax.set_ylabel("Neuron Index", fontsize=12)
    ax.locator_params(axis="y", integer=True, tight=True)

    # Plot excitatory neurons
    for neuron in range(800):
        spike_times = neuron_list_exc[neuron]["spike times"]
        ax.scatter(spike_times, [neuron] * len(spike_times), s=2, color="green",
                   label="Excitatory Neuron" if neuron == 0 else None)

    # Plot inhibitory neurons
    for neuron in range(800, 1000):
        inh_index = neuron - 800
        spike_times = neuron_list_inh[inh_index]["spike times"]
        ax.scatter(spike_times, [neuron] * len(spike_times), s=2, color="red",
                   label="Inhibitory Neuron" if neuron == 800 else None)

    ax.set_xlim(time_window)
    ax.legend(loc='best')

    return ax


def plot_exc_curr_and_g_ks(ax, t_max, g_ks_t, exc_currs, time_window, dt = 0.1):
    """
    Generates a plot with two y-axes:
    - The left y-axis plots the excitatory current (`I_app`) in green.
    - The right y-axis plots the `g_ks_t` values in blue.

    Inputs:
        ax (matplotlib.axes.Axes): The Axes object to modify for plotting.
        t_max (float): Length of simulation in ms
        g_ks_t (numpy array): Time series of g_ks values, one per simulation step.
        exc_currs (list of floats): Applied current in µA to an excitatory neuron with average firing frequency,
        given as a list of values at each simulation step.
        time_window (tuple):
            Tuple (start_time, end_time) defining x-axis limits in ms.
        dt (float, optional): Integration time step in ms (default is 0.1 ms)
    """
    # Create time range based on t_max and dt
    steps = int(t_max / dt)
    t_range = np.linspace(0, t_max, steps)

    # Set up the left y-axis (for excitatory current)
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel("Excitatory Cell\n$\mathrm{I}_{app}$", color='green', fontsize=12)
    ax.tick_params(axis='y', colors='green')
    ax.set_xlim(time_window)
    # ax.set_ylim(5, 10)

    # Create the right y-axis (for g_ks_t)
    ax_twin = ax.twinx()
    # ax_twin.set_ylim(0.065, 0.1)
    ax_twin.tick_params(axis='y', colors='blue')

    # Plot the data
    ax_twin.plot(t_range, g_ks_t[:steps], color='blue', label="g_ks_t")
    ax.plot(t_range, exc_currs, color='green', label="Excitatory Current")

    # Add the legend
    ax.legend(loc='upper left')

    return ax


