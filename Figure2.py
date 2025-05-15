import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Plotting_funcs

# Simulations
t_max = 5500

neurons_exc_inter_dom, neurons_inh_inter_dom, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
    0.00175, 0.00175, 0.00025, 0.0000625, 0, 1, t_max
)  # Inter-connectivity dominated network with cholinergic modulation

neurons_exc_inter_dom_curr_mod, neurons_inh_inter_dom_curr_mod, exc_currs_curr_mod, _ = Simul_funcs_and_data.simulation(
    0.00175, 0.00175, 0.00025, 0.0000625, 1, 1, t_max
)  # Inter-connectivity dominated network with cholinergic modulation and current modulation to keep firing rates approximately constant

neurons_exc_intra_dom, neurons_inh_intra_dom, _, _ = Simul_funcs_and_data.simulation(
    0.00025, 0.00025, 0.0005, 0.000125, 0, 1, t_max
)  # Intra-connectivity dominated network with cholinergic modulation

neurons_exc_intra_dom_curr_mod, neurons_inh_intra_dom_curr_mod, _, _ = Simul_funcs_and_data.simulation(
    0.00025, 0.00025, 0.0005, 0.000125, 1, 1, t_max
)  # Intra-connectivity dominated network with cholinergic modulation and current modulation to keep firing rates approximately constant

# Figure initialization
fig = plt.figure(figsize=(10, 8))
gs = GridSpec(3, 2, height_ratios=[3, 3, 1])

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[2, 0])
ax6 = fig.add_subplot(gs[2, 1])

# Plotting
ax1 = Plotting_funcs.configure_spike_raster_plot(ax1, neurons_exc_inter_dom, neurons_inh_inter_dom, (5200, 5300))
ax2 = Plotting_funcs.configure_spike_raster_plot(ax2, neurons_exc_inter_dom_curr_mod, neurons_inh_intra_dom_curr_mod, (5200, 5300))

ax3 = Plotting_funcs.configure_spike_raster_plot(ax3, neurons_exc_intra_dom, neurons_inh_inter_dom, (5200, 5300))
ax4 = Plotting_funcs.configure_spike_raster_plot(ax4, neurons_exc_intra_dom_curr_mod, neurons_inh_intra_dom_curr_mod, (5200, 5300))

ax5 = Plotting_funcs.plot_exc_curr_and_g_ks(ax5, t_max, g_ks_t, exc_currs, (5200, 5300))
ax6 = Plotting_funcs.plot_exc_curr_and_g_ks(ax6, t_max, g_ks_t, exc_currs_curr_mod, (5200, 5300))

fig.align_ylabels()
plt.tight_layout()
plt.show()
