import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import Simul_funcs_and_data
import Measure_funcs

# Preparing simulation parameters
t_max = 3250
ie_connectivities = np.linspace(0.0000625, 0.00175, 10)
ie_connectivities = np.insert(ie_connectivities, 0, [0])

# Simulations with different I-E synaptic weights and with and without cholinergic modulation for inh cels
exc_synchrony_dataset = []
inh_synchrony_dataset = []

exc_synchrony_dataset_no_inh_mod = []
inh_synchrony_dataset_no_inh_mod = []

for ie_connectivity in ie_connectivities:
    for inh_mod, exc_dataset, inh_dataset in [
        (1, exc_synchrony_dataset, inh_synchrony_dataset),
        (0, exc_synchrony_dataset_no_inh_mod, inh_synchrony_dataset_no_inh_mod)
    ]:
        neurons_exc, neurons_inh, exc_currs, g_ks_t = Simul_funcs_and_data.simulation(
            0.00025, ie_connectivity, 0.0005, 0.000125, 1, inh_mod, t_max
        )

        exc_synch_array, _ = Measure_funcs.synch_array_generator(
            neurons_exc, t_max, 0, g_ks_t, 150
        )

        inh_synch_array, _ = Measure_funcs.synch_array_generator(
            neurons_inh, t_max, 1, g_ks_t, 150
        )

        exc_dataset.append(exc_synch_array)
        inh_dataset.append(inh_synch_array)

# Reverse the datasets for plotting
exc_synchrony_dataset = exc_synchrony_dataset[::-1]
inh_synchrony_dataset = inh_synchrony_dataset[::-1]

exc_synchrony_dataset_no_inh_mod = exc_synchrony_dataset_no_inh_mod[::-1]
inh_synchrony_dataset_no_inh_mod = inh_synchrony_dataset_no_inh_mod[::-1]

# Preparing plot axes
heatmap_x_axis = np.arange(1.45, 0, -0.1)
heatmap_x_axis = [round(point, 2) for point in heatmap_x_axis]
heatmap_y_axis = ie_connectivities[::-1]
heatmap_y_axis = [round(point, 7) for point in heatmap_y_axis]

# Figure initialization
fig = plt.figure(figsize=(15, 10))
gs = GridSpec(2, 2)  # 2x2 grid

# Define the colorbar axis as an additional axis
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])

# Plotting
datasets = [exc_synchrony_dataset, inh_synchrony_dataset, exc_synchrony_dataset_no_inh_mod,
            inh_synchrony_dataset_no_inh_mod]
titles = ["Synchrony of Excitatory Cells", "Synchrony of Inhibitory Cells",
          "Synchrony of Excitatory Cells", "Synchrony of Inhibitory Cells"]
positions = [(0, 0), (1, 0), (0, 1), (1, 1)]

for i in range(4):
    data = datasets[i]
    pos = positions[i]
    title = titles[i]

    ax = fig.add_subplot(gs[pos[0], pos[1]])

    # Plot the heatmap
    if i == 0:
        sns.heatmap(data, annot=False, vmin=0, vmax=1, fmt=".2f", cmap="viridis",
                    xticklabels=heatmap_x_axis,
                    yticklabels=[f"{ytick:.7f}" for ytick in heatmap_y_axis],
                    ax=ax, cbar=True, cbar_ax=cbar_ax,
                    linecolor='black', linewidths='0.5')
    else:
        sns.heatmap(data, annot=False, vmin=0, vmax=1, fmt=".2f", cmap="viridis",
                    xticklabels=heatmap_x_axis,
                    yticklabels=[f"{ytick:.7f}" for ytick in heatmap_y_axis],
                    ax=ax, cbar=False,
                    linecolor='black', linewidths='0.5')

    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_title(title, fontsize=12)

    if pos[0] == 1:
        ax.set_xlabel(r"$g_{k_{s}}$ (mS / cm$^2$)", fontsize=15)
    if pos[1] == 0:
        ax.set_ylabel("I-E synaptic weight (mS / cm$^2$)", fontsize=15)

plt.show()
