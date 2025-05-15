import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Plotting_funcs

# Simulations
t_max = 5500

neurons_exc_inter_dom_tonic_gks, neurons_inh_inter_dom_tonic_gks, exc_currs_tonic_gks, tonic_gks_t = Simul_funcs_and_data.simulation(
    0.00175, 0.00175, 0.00025, 0.0000625, 1, 1, t_max, static_g_ks=1.5
)  # Inter-connectivity dominated network with g_ks set to 1.5 mS

neurons_exc_inter_dom, neurons_inh_inter_dom, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
    0.00175, 0.00175, 0.00025, 0.0000625, 1, 1, t_max
)  # Inter-connectivity dominated network with cholinergic modulation

neurons_exc_intra_dom_tonic_gks, neurons_inh_intra_dom_tonic_gks, _, _ = Simul_funcs_and_data.simulation(
    0.00025, 0.00025, 0.0005, 0.000125, 1, 1, t_max, static_g_ks=1.5
)  # Intra-connectivity dominated network with g_ks set to 1.5 mS

neurons_exc_intra_dom, neurons_inh_intra_dom, _, _ = Simul_funcs_and_data.simulation(
    0.00025, 0.00025, 0.0005, 0.000125, 1, 1, t_max
)  # Intra-connectivity dominated network with cholinergic modulation

neurons_exc_intra_dom_tonic_gks_2, neurons_inh_intra_dom_tonic_gks_2, _, _ = Simul_funcs_and_data.simulation(
    0.00025, 0.00025, 0.0005, 0.000125, 1, 0, t_max, static_g_ks=1.5
)  # Intra-connectivity dominated network with g_ks set to 1.5 mS and inhibitory cell g_ks set to 0 mS

neurons_exc_intra_dom_2, neurons_inh_intra_dom_2, _, _ = Simul_funcs_and_data.simulation(
    0.00025, 0.00025, 0.0005, 0.000125, 1, 0, t_max
)  # Intra-connectivity dominated network with cholinergic modulation for only excitatory cells


# Figure initialization
fig = plt.figure(figsize=(10, 10))
gs = GridSpec(4, 2, height_ratios=[3, 3, 3, 1])

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[2, 0])
ax6 = fig.add_subplot(gs[2, 1])
ax7 = fig.add_subplot(gs[3, 0])
ax8 = fig.add_subplot(gs[3, 1])

# Plotting
ax1 = Plotting_funcs.configure_spike_raster_plot(ax1, neurons_exc_inter_dom_tonic_gks, neurons_inh_inter_dom_tonic_gks, (1900, 2000))
ax2 = Plotting_funcs.configure_spike_raster_plot(ax2, neurons_exc_inter_dom, neurons_inh_inter_dom, (1900, 2000))

ax3 = Plotting_funcs.configure_spike_raster_plot(ax3, neurons_exc_intra_dom_tonic_gks, neurons_inh_intra_dom_tonic_gks, (1900, 2000))
ax4 = Plotting_funcs.configure_spike_raster_plot(ax4, neurons_exc_intra_dom, neurons_inh_intra_dom, (1900, 2000))

ax5 = Plotting_funcs.configure_spike_raster_plot(ax5, neurons_exc_intra_dom_tonic_gks_2, neurons_inh_intra_dom_tonic_gks_2, (1900, 2000))
ax6 = Plotting_funcs.configure_spike_raster_plot(ax6, neurons_exc_intra_dom_2, neurons_inh_intra_dom_2, (1900, 2000))

ax7 = Plotting_funcs.plot_exc_curr_and_g_ks(ax7, t_max, tonic_gks_t, exc_currs_tonic_gks, (1900, 2000))
ax8 = Plotting_funcs.plot_exc_curr_and_g_ks(ax8, t_max, g_ks_t, exc_currs, (1900, 2000))

fig.align_ylabels()
plt.tight_layout()
plt.show()
