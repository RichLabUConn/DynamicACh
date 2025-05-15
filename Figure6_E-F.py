import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Measure_funcs
from matplotlib.lines import Line2D

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True)
fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(7, 8), sharex=True)


ax1.set_ylabel("Synchrony Measure", fontsize=15)
ax2.set_ylabel("Synchrony Measure", fontsize=15)
ax3.set_ylabel("Synchrony Measure", fontsize=15)
ax4.set_ylabel("Synchrony Measure", fontsize=15)

ax1.set_xlim(1.5, 0)
ax2.set_xlim(1.5, 0)
ax3.set_xlim(1.5, 0)
ax4.set_xlim(1.5, 0)

ax2.set_xlabel(r"$g_{k_{s}}$ (mS / cm$^2$)", fontsize=15)
ax4.set_xlabel(r"$g_{k_{s}}$ (mS / cm$^2$)", fontsize=15)

ax1.set_ylim(0, 1)
ax2.set_ylim(0, 1)
ax3.set_ylim(0, 1)
ax4.set_ylim(0, 1)


# Simulations
t_max = 2000

network_structures = [
    # With inhibitory cell g_ks modulation
    ("Test Case", 0.00025, 0.0004375, 0.0005, 0.000125, 1, (0, 0)),
    # ("High I-E Connectivity", 0.00025, 0.00175, 0.0005, 0.000125, 1, (0, 0)),
    # ("Low I-E Connectivity", 0.00025, 0.00025, 0.0005, 0.000125, 1, (0, 0)),
    # ("High to Low I-E Connectivity", 0.00025, 0.00175, 0.0005, 0.000125, 1, (2500, -0.0015)),
    # ("Low to High I-E Connectivity", 0.00025, 0.00025, 0.0005, 0.000125, 1, (1500, 0.0015)),
    # # Without inhibitory cell g_ks modulation
    # ("High I-E Connectivity", 0.00025, 0.00175, 0.0005, 0.000125, 0, (0, 0)),
    # ("Low I-E Connectivity", 0.00025, 0.00025, 0.0005, 0.000125, 0, (0, 0)),
    # ("High to Low I-E Connectivity", 0.00175, 0.00025, 0.0005, 0.000125, 0, (2500, -0.0015)),
    # ("Low to High I-E Connectivity", 0.00025, 0.00025, 0.0005, 0.000125, 0, (1500, 0.0015)),
]
#T_MAX
for index, (label, EI, IE, II, EE, inh_mod, (shift_time, shift_val)) in enumerate(network_structures):
    neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
        EI, IE, II, EE, 1, inh_mod, t_max, IE_connectivity_shift=(shift_time, shift_val), static_g_ks=0.0
    )

    # Generate synchrony array and g_ks_avg_array
    synch_array, g_ks_avg_array = Measure_funcs.synch_array_generator(
        neurons_exc, t_max, 0, g_ks_t, bin_size=150
    )

    synch_array2, g_ks_avg_array = Measure_funcs.synch_array_generator(
        neurons_inh, t_max, 1, g_ks_t, bin_size=150
    )


    print(synch_array)
    print(synch_array2)
    print(g_ks_avg_array)

    # if index == 0:
    #     ax1.plot(g_ks_avg_array, synch_array, color='red', label=label)
    #     ax2.plot(g_ks_avg_array, synch_array, color='black', linestyle='dotted', label=label)
    # elif index == 1:
    #     ax1.plot(g_ks_avg_array, synch_array, color='black', linestyle='dotted', label=label)
    #     ax2.plot(g_ks_avg_array, synch_array, color='red', label=label)
    # elif index == 2:
    #     ax1.plot(g_ks_avg_array, synch_array, color='blue', label=label)
    # elif index == 3:
    #     ax2.plot(g_ks_avg_array, synch_array, color='blue', label=label)
    # elif index == 4:
    #     ax3.plot(g_ks_avg_array, synch_array, color='red', label=label)
    #     ax4.plot(g_ks_avg_array, synch_array, color='black', linestyle='dotted', label=label)
    # elif index == 5:
    #     ax3.plot(g_ks_avg_array, synch_array, color='black', linestyle='dotted', label=label)
    #     ax4.plot(g_ks_avg_array, synch_array, color='red', label=label)
    # elif index == 6:
    #     ax3.plot(g_ks_avg_array, synch_array, color='blue', label=label)
    # elif index == 7:
    #     ax4.plot(g_ks_avg_array, synch_array, color='blue', label=label)

plt.show()