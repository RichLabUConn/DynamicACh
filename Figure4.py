import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Measure_funcs
from matplotlib.lines import Line2D

# Figure initialization
fig = plt.figure(figsize=(8, 8))
gs = GridSpec(3, 1)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[2, 0])

axes = [ax1, ax2, ax3]
for ax in axes:
    ax.set_xlim(1.5, 0)
    ax.set_ylim(0, 1)

# Tonic g_ks simulations and plotting
static_gks_list = [0.4, 0.7, 1.0] # Tonic g_ks values in mS
associated_marker_symbol = ['o', 's', '^'] # Markers for each g_ks value in plot

t_max = 2000
network_structures = [
    ("inter_dom", 0.00175, 0.00175, 0.00025, 0.0000625, 1, ax1),
    ("intra_dom", 0.00025, 0.00025, 0.0005, 0.000125, 1, ax2),
    ("intra_dom_no_inh_mod", 0.00025, 0.00025, 0.0005, 0.000125, 0, ax3),
]

for gks_idx, static_g_ks in enumerate(static_gks_list):
    for label, EI, IE, II, EE, inh_mod, ax in network_structures:
        neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
            EI, IE, II, EE, 1, inh_mod, t_max, static_g_ks = static_g_ks
        )

        synch_value, g_ks_avg = Measure_funcs.synch_array_generator(
            neurons_exc, t_max, 0, g_ks_t, 1000
        )

        ax.plot(static_g_ks, synch_value, color='blue',
                marker=associated_marker_symbol[gks_idx],
                markersize=10, linestyle='')

# Dynamic g_ks simulations and plotting
t_max_list = [2000, 3000, 5000, 9000]
colors = ['green', 'orange', 'red', 'black']

network_structures = [
    ("inter_dom", 0.00175, 0.00175, 0.00025, 0.0000625, 1, ax1),
    ("intra_dom", 0.00025, 0.00025, 0.0005, 0.000125, 1, ax2),
    ("intra_dom_no_inh_mod", 0.00025, 0.00025, 0.0005, 0.000125, 0, ax3),
]

for t_max_index in range(len(t_max_list)):
    t_max = t_max_list[t_max_index]
    chosen_color = colors[t_max_index]
    rate_of_gks_decline = 1.5 / (t_max - 1000)

    for label, EI, IE, II, EE, inh_mod, ax in network_structures:
        neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
            EI, IE, II, EE, 1, inh_mod, t_max
        )

        synch_array, g_ks_avg_array = Measure_funcs.synch_array_generator(
            neurons_exc, t_max, 0, g_ks_t
        )

        ax.plot(g_ks_avg_array, synch_array, color=chosen_color, label=f'Rate of $g_{{ks}}$ decline = {round(rate_of_gks_decline * 1000, 2)} mS / cm$^2$s')

legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label=r"$g_{k_{s}}$ = 0.4 mS / cm$^2$"),
                   Line2D([0], [0], marker='s', color='w', markerfacecolor='blue', markersize=10, label="$g_{k_{s}}$ = 0.7 mS / cm$^2$"),
                   Line2D([0], [0], marker='^', color='w', markerfacecolor='blue', markersize=10, label="$g_{k_{s}}$ = 1.0 mS / cm$^2$")]
legend_elements += ax1.get_legend_handles_labels()[0]
ax2.legend(handles=legend_elements, loc='upper right', fontsize='small')

fig.tight_layout()
plt.show()


