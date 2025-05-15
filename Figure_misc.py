import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Measure_funcs
import Plotting_funcs

# Preparing simulation parameters
t_max = 4250
t_max_tonic = 2000
ie_connectivities = np.linspace(0.0000625, 0.00175, 10)
ie_connectivities = np.insert(ie_connectivities, 0, [0])

exc_synchrony_dataset = []
inh_synchrony_dataset = []

exc_synchrony_dataset_no_inh_mod = []
inh_synchrony_dataset_no_inh_mod = []

save_dir = r"C:\Users\sibip\OneDrive\Desktop\Sibi\Work\Research\figs\Fig 6 new exps"


# Simulations
for ie_connectivity in ie_connectivities:
    for inh_mod, exc_dataset, inh_dataset in [
        (1, exc_synchrony_dataset, inh_synchrony_dataset),
        (0, exc_synchrony_dataset_no_inh_mod, inh_synchrony_dataset_no_inh_mod)
    ]:
        neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
            0.00025, ie_connectivity, 0.0005, 0.000125, 1, inh_mod, t_max, g_ks_zero_time=t_max-1000
        )

        for start in range(0, t_max, 200):
            end = start + 200
            if end > t_max:
                break
            fig, ax = plt.subplots()
            Plotting_funcs.configure_spike_raster_plot(ax, neurons_exc, neurons_inh, (start, end))
            fig.savefig(os.path.join(save_dir, f"dynamic_{ie_connectivity}_{start}.png"), bbox_inches='tight')
            plt.close(fig)

        exc_synch_array, _ = Measure_funcs.synch_array_generator(
            neurons_exc, t_max, 0, g_ks_t, 150
        )

        inh_synch_array, _ = Measure_funcs.synch_array_generator(
            neurons_inh, t_max, 1, g_ks_t, 150
        )

        exc_synch_array = exc_synch_array[:15] + [exc_synch_array[-1]]
        inh_synch_array = inh_synch_array[:15] + [inh_synch_array[-1]]

        exc_dataset.append(exc_synch_array)
        inh_dataset.append(inh_synch_array)

exc_synchrony_tonic_gks = []
inh_synchrony_tonic_gks = []

exc_synchrony_no_inh_mod_tonic_gks = []
inh_synchrony_no_inh_mod_tonic_gks = []

#Simulations for tonic cases
for ie_connectivity in ie_connectivities:
    for inh_mod, exc_dataset, inh_dataset in [
        (1, exc_synchrony_tonic_gks, inh_synchrony_tonic_gks),
        (0, exc_synchrony_no_inh_mod_tonic_gks, inh_synchrony_no_inh_mod_tonic_gks)
    ]:
        neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
            0.00025, ie_connectivity, 0.0005, 0.000125, 1, inh_mod, t_max_tonic, static_g_ks=0
        )

        for start in range(0, t_max_tonic, 200):
            end = start + 200
            if end > t_max:
                break
            fig, ax = plt.subplots()
            Plotting_funcs.configure_spike_raster_plot(ax, neurons_exc, neurons_inh, (start, end))
            fig.savefig(os.path.join(save_dir, f"tonic_{ie_connectivity}_{start}.png"), bbox_inches='tight')
            plt.close(fig)

        exc_synch_array, _ = Measure_funcs.synch_array_generator(
            neurons_exc, t_max_tonic, 0, g_ks_t, 500
        )

        inh_synch_array, _ = Measure_funcs.synch_array_generator(
            neurons_inh, t_max_tonic, 1, g_ks_t, 500
        )

        exc_synch_array = exc_synch_array[-1]
        inh_synch_array = inh_synch_array[-1]

        exc_dataset.append(exc_synch_array)
        inh_dataset.append(inh_synch_array)


# Reverse the datasets
exc_synchrony_dataset = exc_synchrony_dataset[::-1]
inh_synchrony_dataset = inh_synchrony_dataset[::-1]

exc_synchrony_dataset_no_inh_mod = exc_synchrony_dataset_no_inh_mod[::-1]
inh_synchrony_dataset_no_inh_mod = inh_synchrony_dataset_no_inh_mod[::-1]

# Preparing plot axes
heatmap_x_axis = np.arange(1.45, 0, -0.1)
heatmap_x_axis = np.append(heatmap_x_axis, 0)
heatmap_x_axis = [round(point, 2) for point in heatmap_x_axis]
heatmap_y_axis = ie_connectivities[::-1]
heatmap_y_axis = [round(point, 7) for point in heatmap_y_axis]

# Create the figure and GridSpec layout
fig = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 2)  # 2x2 grid

# Define the colorbar axis as an additional axis outside the GridSpec layout
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])

datasets = [exc_synchrony_dataset, inh_synchrony_dataset, exc_synchrony_dataset_no_inh_mod, inh_synchrony_dataset_no_inh_mod]
titles = ["Synchrony of Excitatory Cells", "Synchrony of Inhibitory Cells",
          "Synchrony of Excitatory Cells", "Synchrony of Inhibitory Cells"]
positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
show_cbar = [True, False, False, False]

for i in range(4):
    data = datasets[i]
    pos = positions[i]
    title = titles[i]
    cbar_flag = show_cbar[i]

    ax = fig.add_subplot(gs[pos[0], pos[1]])
    sns.heatmap(data, annot=False, vmin=0, vmax=1, fmt=".2f", cmap="viridis",
                xticklabels=heatmap_x_axis,
                yticklabels=[f"{ytick:.7f}" for ytick in heatmap_y_axis],
                ax=ax, cbar=cbar_flag if i != 0 else cbar_ax,  # Only first plot gets the shared colorbar
                linecolor='black', linewidths='0.5')

    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_title(title, fontsize=15)

    if pos[0] == 1:
        ax.set_xlabel(r"$g_{k_{s}}$ (mS / cm$^2$)", fontsize=15)

    ax.set_ylabel("I-E synaptic weight (mS / cm$^2$)", fontsize=15)

save_path = r"C:\Users\sibip\OneDrive\Desktop\Sibi\Work\Research\figs"
plt.savefig(os.path.join(save_path, "EB.png"), bbox_inches='tight')



# --- Start: New Code for Plotting Tonic/Static g_ks Cases ---

# Reverse the tonic datasets to match the reversed y-axis
exc_synchrony_tonic_gks = exc_synchrony_tonic_gks[::-1]
inh_synchrony_tonic_gks = inh_synchrony_tonic_gks[::-1]
exc_synchrony_no_inh_mod_tonic_gks = exc_synchrony_no_inh_mod_tonic_gks[::-1]
inh_synchrony_no_inh_mod_tonic_gks = inh_synchrony_no_inh_mod_tonic_gks[::-1]

# Reshape data into N x 1 arrays for single-column heatmap plotting
tonic_datasets = [
    np.array(exc_synchrony_tonic_gks).reshape(-1, 1),
    np.array(inh_synchrony_tonic_gks).reshape(-1, 1),
    np.array(exc_synchrony_no_inh_mod_tonic_gks).reshape(-1, 1),
    np.array(inh_synchrony_no_inh_mod_tonic_gks).reshape(-1, 1)
]

# Titles for the new plots
tonic_titles = [
    "Tonic Excitatory Synchrony (Inh Mod)",
    "Tonic Inhibitory Synchrony (Inh Mod)",
    "Tonic Excitatory Synchrony (No Inh Mod)",
    "Tonic Inhibitory Synchrony (No Inh Mod)"
]

# Create the new figure and GridSpec layout for tonic cases
fig_tonic = plt.figure(figsize=(10, 6)) # Adjusted size for 4 single columns
gs_tonic = GridSpec(1, 4, width_ratios=[1, 1, 1, 1], wspace=0.5) # 1 row, 4 columns

# Define the colorbar axis for the new figure
cbar_ax_tonic = fig_tonic.add_axes([0.93, 0.15, 0.03, 0.7]) # Adjusted position

# Plot each tonic dataset as a single-column heatmap
for i in range(4):
    data = tonic_datasets[i]
    title = tonic_titles[i]

    ax = fig_tonic.add_subplot(gs_tonic[0, i])
    sns.heatmap(data, annot=False, vmin=0, vmax=1, fmt=".2f", cmap="viridis",
                xticklabels=["Synchrony"], # Single label for the column
                yticklabels=[f"{ytick:.7f}" for ytick in heatmap_y_axis],
                ax=ax,
                cbar=True if i == 0 else False, # Only first plot gets the shared colorbar in cbar_ax_tonic
                cbar_ax=cbar_ax_tonic if i == 0 else None,
                linecolor='black', linewidths='0.5')

    # Rotate y-axis labels for clarity if needed (already horizontal)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    # Adjust x-axis label rotation if needed
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_title(title, fontsize=12)

    ax.set_ylabel("I-E synaptic weight (mS / cm$^2$)", fontsize=15)


# Adjust layout to prevent overlap
plt.subplots_adjust(top=0.85) # Adjust top margin to fit titles
fig_tonic.suptitle("Tonic $g_{ks}$ Synchrony", fontsize=16, y=0.98)

# Save the new figure (optional)
save_path = r"C:\Users\sibip\OneDrive\Desktop\Sibi\Work\Research\figs" # From user's code
if not os.path.exists(save_path):
     os.makedirs(save_path)
plt.savefig(os.path.join(save_path, "EB_tonic.png"), bbox_inches='tight')

# Show the new plot
plt.show()

# --- End: New Code ---
