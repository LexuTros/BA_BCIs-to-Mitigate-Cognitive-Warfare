# Simulation Model v2
This is the more mature, better structured and mostly used model version. 
It contains the adjusted event detection functionality and the whole scale of plotting functions. 

## Running Simulations
To run a single simulation, you can execute either `user_interface_simple.py` or `user_interface_extended.py` to configure the simulation parameters with a graphical user interface.

In order to run multiple simulations in parallel, configure and execute the `parallel_processing.py` (details regarding this can be found in my thesis - Chapter 5.3).

Simulations produce a result folder in the root directory of the model code, containing many LFP files and more. Usually the standard `LFP.txt` file was extracted from these results and sorted for analysis.

## Performing The Output Analysis
To analyse the simulation output, employ the `plotting_Toellke.py` file. It contains many functions to read and analyse LFP.txt files.

Some example function calls can be found at the bottom of the file. All data used for the attack analysis performed in the thesis, is sorted and stored in the `sorted_output` folder. It contains folders for every explored paramter combination, which again hold a folders with at least 8 output files, for every parameter value.
Most powerful analysis functions were configured to work with this folder structure to extract parameters and their values.

Example plots that were produce with these functions can be found in the `result_plot` folder.


