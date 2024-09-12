# Simulation Source code

## Getting Started

#### First, install all the packages (both models can be executed with the same environment)
The recommended way would be to create a conda environment, from the `env_hipp.yaml` file. 
This requires to have conda installed as prerequisite. 
For more details visit the [Conda Documentation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

With conda installed, you can run:

```bash
conda env create -f env_hipp.yaml
```

followed by:

```bash
conda hipp_sim activate
```
to activate the created environment.

(alternatively the packages defined in the file can be installed manually)


## Model Versions

The two subfolders of this directory represent the two versions of the model.

`SimualationCode` contains the primary model version (v1), which was used to investigate the synthetic input.

`hippoSimUpdated` contains the newer and way better written version of the model (v2). It was used for all further work and especially the integration of electromagnetic attacks.

More specifics regarding their use, can be found in the **README.md** files of each folder. 




