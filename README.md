# DynamicACh
Code associated with the manuscript "Dynamic cholinergic signaling differentially desynchronizes cortical microcircuits dependent on modulation rate and network topology." 

The repository contains Python 3 code to generate each of the figures in the paper. Aside from using basic Python libraries 
such as NumPy, the repository contains custom modules that are used in the figure generation codes-

Simul_funcs_and_data.py: Contains functions required to run E-I network simulations. This module accesses
data in the three json files 'ficurves.json', 'ficurves_inh.json', and 'ficurves_keys.json'.

Measure_funcs.py: Contains functions that implement the Golomb Synchrony measure (Golomb and Rinzel, 1993/1994) detailed 
in Materials and Methods. 

Plotting_funcs.py: Contains functions to generate raster plots. 

As random seeds are not fixed, results may have slight differences from the figures in the paper. 


