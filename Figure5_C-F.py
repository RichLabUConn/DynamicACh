import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Plotting_funcs

# Figure initialization
fig = plt.figure(figsize=(10, 8))
gs = GridSpec(3, 1, height_ratios=[3, 3, 1])

fig2 = plt.figure(figsize=(10, 8))
gs2 = GridSpec(3, 1, height_ratios=[3, 3, 1])

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[2, 0])

ax4 = fig2.add_subplot(gs2[0, 0])
ax5 = fig2.add_subplot(gs2[1, 0])
ax6 = fig2.add_subplot(gs2[2, 0])

# Simulations
t_max = 3250
ei_connectivities = [0.00025, 0.00175, 0.000625, 0.001]
inh_mod_values = [1, 1, 0, 0]

# Plotting
for i in range(4):
    neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
        ei_connectivities[i], 0.00025, 0.0005, 0.000125, 1, inh_mod_values[i], t_max
    )

    if i == 0:
        ax1 = Plotting_funcs.configure_spike_raster_plot(ax1, neurons_exc, neurons_inh, (1700, 2100))
        ax3 = Plotting_funcs.plot_exc_curr_and_g_ks(ax3, t_max, g_ks_t, exc_currs, (1700, 2100))

    if i == 1:
        ax2 = Plotting_funcs.configure_spike_raster_plot(ax2, neurons_exc, neurons_inh, (1700, 2100))

    if i == 2:
        ax4 = Plotting_funcs.configure_spike_raster_plot(ax4, neurons_exc, neurons_inh, (1200, 1600))
        ax6 = Plotting_funcs.plot_exc_curr_and_g_ks(ax6, t_max, g_ks_t, exc_currs, (1200, 1600))

    if i == 3:
        ax5 = Plotting_funcs.configure_spike_raster_plot(ax5, neurons_exc, neurons_inh, (1200, 1600))


fig.align_ylabels()
plt.tight_layout()
plt.show()
