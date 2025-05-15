import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import cm
import Simul_funcs_and_data

# Figure initialization
fig = plt.figure(figsize=(12, 4), constrained_layout=True)
gs = GridSpec(1, 2, figure=fig)

# First subplot for F-I curve
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlabel(r'Current ($\mu$A / cm$^2$)', fontsize=14)
ax1.set_ylabel('Frequency (Hz)', fontsize=14)

# Second subplot for PRC
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlabel('Normalized Phase', fontsize=14)
ax2.set_ylabel('Normalized Phase Difference', fontsize=14)
ax2.set_ylim(-0.1, 0.15)
ax2.set_xlim(0.0, 1)
ax2.axhline(y=0, color='grey', linestyle=':', linewidth=1.2)

# F-I CURVE DERIVATION
# Simulation parameters
t_max = 3000  # ms
dt = 0.01  # ms
steps = int(t_max / dt)
g_ks_values = np.arange(0, 1.5, 0.1) # F-I curves will be found for 15 g_ks values from 0.0 to 1.5
spike_threshold = 0  # mV

i_app_array_group = [] # To store current arrays for each F-I curve corresponding to each g_ks value
freq_array_group = [] # To store frequency arrays for each F-I curve corresponding to each g_ks value

for g_ks in g_ks_values: # Finding F-I curves for each g_ks value

    i_app = np.arange(0, 25.1, 0.05) # Different current values to stimulate neuron with to find corresponding firing frequency
    spike_times = [[] for num in range(len(i_app))] # To store neuron spike times for each simulation

    for current_index in range(len(i_app)): # A simulation for each current value
        should_record_spike = True # Spike detection flag

        # Neuron state variables initialization
        v = np.zeros(5) # Membrane voltage
        h = np.zeros(5) # Gating variables
        z = np.zeros(5)
        n = np.zeros(5)

        v[0] = -42 #mV
        h[0] = 0.5
        n[0] = 0.5
        z[0] = 0.2

        for i in range(1, steps):
            update_no = i % 5 # Updating modulo 5 index to remember only 5 values of v,h,z,n at a time

            # Runge-kutta used to update state variables
            dh, dn, dz, dv = Simul_funcs_and_data.rk_slope(v[update_no - 1], i_app[current_index], 0, h[update_no - 1], n[update_no - 1], z[update_no - 1], g_ks, timestep=dt)
            h[update_no], n[update_no], z[update_no], v[update_no] = h[update_no - 1] + dh, n[update_no - 1] + dn, z[
                update_no - 1] + dz, v[update_no - 1] + dv

            # Store spike time if spike is triggered and modify spike detection flag
            should_record_spike = Simul_funcs_and_data.record_spike(v[update_no-1], spike_threshold, i, should_record_spike, spike_times[current_index], timestep=dt)

    frequency_array = np.zeros(len(i_app)) # Initialize frequency array

    for freq_index, frequency in enumerate(frequency_array):
        filtered_spikes = ([spikes for spikes in spike_times[freq_index] if spikes > 1000]) # Consider only spikes after 1000 ms, allowing initial transients to decay
        frequency_array[freq_index] = len(filtered_spikes) / 2 # Frequency of spikes is number of spikes divided by period over which spikes occured, i.e. (t_max - 1 s) = 2 s

    freq_for_plot = [] # Frequency list for plotting
    i_app_for_plot = [] # Current list for plotting

    # Due to depolarization block, with excess current stimulation, neurons may cease to fire, leading to a sharp dip in F-I curve at a certain current threshold
    # We exclude these physiologically unrealistic data points for the F-I curve plot
    prev_value = 0
    for freq_index, frequency in enumerate(frequency_array):
        if frequency != 0 and frequency > prev_value:
            freq_for_plot.append(frequency)
            i_app_for_plot.append(i_app[freq_index])
        prev_value = frequency

    # Storing F-I curve results for the given g_ks value
    i_app_array_group.append(i_app_for_plot)
    freq_array_group.append(freq_for_plot)

# Plot F-I Curve with color coding
color = cm.coolwarm(np.linspace(0, 1, 16)) # Colors to correspond to each g_ks value in plot
for i, c in enumerate(color[:3]):
    ax1.plot(i_app_array_group[i], freq_array_group[i], c=c)


# PRC DERIVATION
# Simulation parameters
t_max = 1750  # ms
steps = int(t_max / dt)

# Phase response variables
number_of_perturbation_points = 101 # We deliver perturbations at points from 1, 2... to 100% of the neuron's phase cycle
norm_phase_diffs = np.zeros((16, number_of_perturbation_points)) # Initialize array storing changes in phase from perturbations for each g_ks value


current_values = [
    1.0, 1.4, 1.95, 2.45, 2.95, 3.5, 4.075, 4.675,
    5.3, 5.95, 6.65, 7.45, 8.3, 9.2, 10.3, 11.55
]  # Current values in µA that allow the neuron to fire at ~60Hz for each g_ks value from 0 to 1.5 mS (values can be found in ficurves.json in Simul_funcs_and_data.py)

curr_perturbation_values = [curr_value + 2 for curr_value in current_values] # Amplitude of current perturbations

for index, g_ks in enumerate(g_ks_values): # Finding PRCs for each g_ks value

    for perturbation_point in range(1, number_of_perturbation_points):

        # Neuron state variables initialization
        v = np.zeros(5)  # Membrane voltage
        h = np.zeros(5)  # Gating variables
        z = np.zeros(5)
        n = np.zeros(5)

        v[0] = -42  # mV
        h[0] = 0.5
        n[0] = 0.5
        z[0] = 0.2

        spike_times = [] # To store neuron spike times
        should_record_spike = True # Spike detection flag
        current_value = current_values[index] # Selecting current value needed for neuron to fire at ~60Hz
        i_app = current_value * np.ones(steps) # Array with the current value for all steps

        for i in range(1, int(steps/3)): # Until 1000 ms
            update_no = i % 5 # Updating modulo 5 index to remember only 5 values of v,h,z,n at a time

            dh, dn, dz, dv = Simul_funcs_and_data.rk_slope(v[update_no - 1], i_app[i], 0, h[update_no - 1],
                                                           n[update_no - 1], z[update_no - 1], g_ks, timestep=dt)
            h[update_no], n[update_no], z[update_no], v[update_no] = h[update_no - 1] + dh, n[update_no - 1] + dn, z[
                update_no - 1] + dz, v[update_no - 1] + dv  # Runge-Kutta used to update state variables

        for i in range(int(steps/3), steps): # After 1000 ms
            update_no = i % 5 # Updating modulo 5 index to remember only 5 values of v,h,z,n at a time
            if len(spike_times) < 15: # Wait for the 15th spike
                dh, dn, dz, dv = Simul_funcs_and_data.rk_slope(v[update_no - 1], i_app[i], 0, h[update_no - 1],
                                                               n[update_no - 1], z[update_no - 1], g_ks, timestep=dt)
                h[update_no], n[update_no], z[update_no], v[update_no] = h[update_no - 1] + dh, n[update_no - 1] + dn, z[update_no - 1] + dz, v[
                                                                             update_no - 1] + dv  # Runge-Kutta used to update state variables

                should_record_spike = Simul_funcs_and_data.record_spike(v[update_no], spike_threshold, i, should_record_spike, spike_times, timestep=dt) # Store only spikes after 1000 ms to allow initial transients to decay

                if len(spike_times) == 15: # 15th spike is triggered
                    sum_of_interspike_times = 0
                    for j in range(1, 15):
                        sum_of_interspike_times += spike_times[j] - spike_times[j - 1]
                    avg_interspike_time = sum_of_interspike_times / 14 # Average inter-spike interval time

                    step_of_spike_prior_to_perturbation = i # Time step at which 15th spike fired

            if len(spike_times) == 15:
                step_of_perturbation = int((perturbation_point/100)*(avg_interspike_time/dt)) # Time step at which perturbation will be delivered

                for current in range(step_of_spike_prior_to_perturbation + step_of_perturbation, step_of_spike_prior_to_perturbation + step_of_perturbation + int(1 / dt)):
                    i_app[current] = curr_perturbation_values[index] # Deliver a perturbation that lasts 1 ms

                dh, dn, dz, dv = Simul_funcs_and_data.rk_slope(v[update_no - 1], i_app[i], 0, h[update_no - 1],
                                                               n[update_no - 1], z[update_no - 1], g_ks, timestep=dt)
                h[update_no], n[update_no], z[update_no], v[update_no] = h[update_no - 1] + dh, n[update_no - 1] + dn, z[update_no - 1] + dz, v[
                                                                             update_no - 1] + dv  # Runge-Kutta used to update state variables

                # Detect 16th spike
                if v[update_no] < spike_threshold:
                    should_record_spike = True

                if should_record_spike == True:
                    if v[update_no] > spike_threshold: # 16th spike has been detected
                        new_interspike_time = dt*i - dt*step_of_spike_prior_to_perturbation # Time between 15th and 16th spike
                        norm_phase_diffs[index, perturbation_point] = (avg_interspike_time - new_interspike_time) / (avg_interspike_time) # Store difference in interspike interval with respect to previous interspike interval
                        break


# Plot PRC with color coding
ax2.set_ylim(-0.05, 0.15)
ax2.set_xlim(0.0, 1)

prc_x_axis = np.linspace(0, 1, number_of_perturbation_points)
for i, c in enumerate(color[:3]):
    ax2.plot(prc_x_axis, norm_phase_diffs[i], c=c)

# Add common color bar
sm = plt.cm.ScalarMappable(cmap=cm.coolwarm, norm=plt.Normalize(vmin=min(g_ks_values), vmax=max(g_ks_values)))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax2)
cbar.set_label(r"$g_{k_{s}}$ (mS / cm$^2$)", fontsize=14)

plt.show()




