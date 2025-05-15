import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Measure_funcs

# Figure initialization
fig = plt.figure(figsize=(8, 8))
gs = GridSpec(2, 1)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])

axes = [ax1, ax2]
for ax in axes:
    ax.set_xlim(1.5, 0)
    ax.set_ylim(0, 1)

# Simulations and plotting
t_max = 3000
colors = ['blue', 'red', 'purple', 'blue', 'red', 'purple']
labels = ['Dominant inter-connectivity', 'Dominant intra-connectivity', 'Strong inter and inter-connectivity', 'Dominant inter-connectivity', 'Dominant intra-connectivity', 'Strong inter and inter-connectivity']

network_structures = [
    ("inter_dom", 0.00175, 0.00175, 0.00025, 0.0000625, 1, ax1),
    ("intra_dom", 0.00025, 0.00025, 0.0005, 0.000125, 1, ax1),
    ("strong_inter_and_intra", 0.00175, 0.00175, 0.0005, 0.000125, 1, ax1),
    ("inter_dom_no_inh_mod", 0.00175, 0.00175, 0.00025, 0.0000625, 0, ax2),
    ("intra_dom_no_inh_mod", 0.00025, 0.00025, 0.0005, 0.000125, 0, ax2),
    ("strong_inter_and_intra_no_inh_mod", 0.00175, 0.00175, 0.0005, 0.000125, 0, ax2),
]

for index, (label, EI, IE, II, EE, inh_mod, ax) in enumerate(network_structures):
    neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
        EI, IE, II, EE, 1, inh_mod, t_max
    )

    synch_array, g_ks_avg_array = Measure_funcs.synch_array_generator(
        neurons_exc, t_max, 0, g_ks_t
    )

    ax.plot(g_ks_avg_array, synch_array, color=colors[index], label=labels[index])

ax1.legend(loc='upper right', fontsize='small')
fig.tight_layout()
plt.show()



