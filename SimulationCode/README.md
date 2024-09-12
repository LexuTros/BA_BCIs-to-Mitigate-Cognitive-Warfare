# Simulation Model v1
This is the initial version of the model, which contains some problematic code. 
The parallel processing functionality, had to be deactivated in order to make it work.
Further, the event detection function was not adjusted and the plotting functionality is compared to the second model version limited.
It was however used for the investigation of the synthetic input.

## Configuring the Model
Since this model code is not that well-structured, certain configurations still need to be performed inside the main file `hippocampus_Aussel.py`. The most important adjustments are followingly pointed out with their according line number in the file:

`Select EEG or Synthetic input:` line 510 - by adjusting the "use_eeg_files" boolean

`Adjust Parameters of Synthetic input:` line 584 - by adjusting parameters of the "generate_input" function


## Running Simulations
In order to run a simulation, the `hippocampus_Aussel.py` file needs to be executed.

This requires however to pass 3 arguments to it, which was configured this way to allow its parameterization from a terminal. These parameters are `simulation type`, `simulation time`, `research parameter`.

`simulation type` refers to the combination of input and connectivity type. Possible options are: {'S_S', 'S_W', 'W_S', 'W_W', 'S_S_CAN', 'S_W_noCAN', 'W_S_CAN', 'W_W_noCAN'}. For this model however, mostly the "S_S" option (standing for sleep input and connectivity) was used and of relevance.

`simulation time` defines the length of the simulation in seconds and has to be supplied as integer.

`research parameter` is a float value that defines the input frequency, but could also be placed somewhere else in the **hippocampus_Aussel.py** to explore multiple simulation configurations with the same code.

To run the simulation it is recommended to execute a statement of the following form in a terminal:

#### python hippocampus_Aussel.py "simulation type" "simulation time" "research parameter"
To simulate for example the healthy brain with the best identified parameter combination, for 60s, execute the following:
```bash
python hippocampus_Aussel.py S_S 60 1.5
```

## Performing The Output Analysis
To analyse the simulation output, employ the `plotting_Toellke.py` file. It contains many functions to read and analyse LFP.txt files.

Some example function calls can be found at the bottom of the file. Data that was used for thesis plots is sorted and stored in the `sorted_output` folder. The rest of relevant LFP output can be found inside "Out/Timeseries/S_S".





