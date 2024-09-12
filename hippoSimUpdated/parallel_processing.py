#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: aussel
"""

from brian2 import *

from joblib import Parallel, delayed
import multiprocessing
import os

from model_files.global_vars_and_eqs import *
from model_files.single_process import *
#from model_files.analysis_functions import *
from model_files.annex_functions import *
from model_files.set_vars_and_process import *

import time
import ntpath
from itertools import *


os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_DYNAMIC'] = 'FALSE'


timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
if os.name == 'nt':
    base_dir = os.path.dirname(os.path.abspath(__file__))
else:
    base_dir = os.getcwd()

path = os.path.join(base_dir, "results_" + timestamp)
os.mkdir(path)

#Basic network parameters
liste_Ntypes = [[1, 1]] #list of couples of the form [number of excitatory neuron types, number of inhibitory neuron types], with each number being 1 or 2
liste_maxN = [10000] #list of integers, representing the number of excitatory neurons in the CA1 region
liste_p_tri = [0.4] #list of floats, representing the synaptic connection probability on the tri-synaptic pathway
liste_p_mono = [0.3] #list of floats, representing the synaptic connection probability on the mono-synaptic pathway
liste_g_max_i = [600*psiemens] #list of floats (in siemens), representing the maximum synaptic conductances of inhibitory synapses
liste_g_max_e = [60*psiemens] #list of floats (in siemens), representing the maximum synaptic conductances of excitatory synapses
liste_topo_type = ['normal'] #list of strings ('normal' or 'rectangle'), to choose between realistic and rectangular topology of the network
liste_co_type = ['normal'] #list of strings ('normal' or 'uniform'), to choose between distance-related or uniform connection probability profiles between hippocampal regions
liste_co_type2 = ['normal'] #list of strings ('normal' or 'uniform'), to choose between distance-related or uniform connection probability profiles within hippocampal regions

#sleep-wake parameters (in set_vars_and_process.py related to: duo_gCAN,hasCAN,var_coeff,fco)
liste_gCAN = [(0.5*usiemens*cmeter**-2, 25*usiemens*cmeter**-2)] #list of couples of the form (sleep CAN channel conductance, wakefulness CAN channel conductance), each value in siemens*meter**-2
liste_CAN = ['sleep'] #list of strings ('wake' or 'sleep') to choose between sleep and wakefulness CAN channel conductances --- 'sleep' = gCAN[0], 'wake' = gCAN[1]
liste_G_ACh = [3] #list of floats, representing the gain applied on some synaptic conductances under cholinergic modulation --- ONLY APPLIED WHEN functional_co = 'wake'
liste_functional_co = ['sleep']  #list of strings ('wake' or 'sleep') to choose between sleep and wakefulness functional connectivity --- ONLY decides if G_ACh has effect or not


#epilepsy parameters :
liste_sprouting = [0] #list of floats, representing the mossy fiber sprouting in the DG (between 0 (healthy) and 1)
liste_sclerosis = [0] #list of floats, representing the hippocampal sclerosis (between 0 (healthy) and 1)
liste_lesion_region = ['all',] #list of strings ('all','EC','DG','CA3','CA1') representing the region(s) to which hippocampal sclerosis applies
liste_tau_Cl = [0.1*second] #list of floats, representing the removal rate of chloride ions in excitatory cells (in second)
liste_Ek = [-100*mV]  #list of floats, representing the resting potential of potassium channels in excitatory cells (in volt)


#Input parameters
liste_input_type = ['custom'] #list of strings ('custom' or 'square') representing the type of inputs to apply

#for custom inputs only :
liste_custom_inputs = [('input_data/input_nonepi_sleep_1.txt', 'input_data/input_nonepi_sleep_2.txt', 'input_data/input_nonepi_sleep_3.txt', 1024*Hz)] # Waking input: ('input_data/input_nonepi_wake_1.txt','input_data/input_nonepi_wake_2.txt','input_data/input_nonepi_wake_3.txt',1024*Hz)

#square current input only : 
liste_A0 = [0] #list of floats, representing the minimum value of the input current (without unit, representing nA)
liste_A1 = [1.2] #list of floats, representing the maximum value of the input current (without unit, representing nA)
liste_dur = [4000*msecond,] #list of floats, representing the duration of the stimulation
liste_f1 = [0.05*Hz] #list of floats, representing the frequency of the input square wave (in Hz)
liste_duty_cycle = [0.5] #list of floats, representing the duty cycle of the square wave (between 0 and 1)


#simulation duration
liste_runtime = [60*second] #list of floats, representing the duration of the simulation (in second)

#simulation output :
plot_raster, save_raster, save_neuron_pos, save_syn_mat, save_all_FR = False, False, False, False, False #each boolean indicates if the specified output must be saved for all set of simulations


liste_simus = list(product(liste_Ntypes, liste_maxN, liste_p_tri, liste_p_mono, liste_g_max_i, liste_g_max_e, liste_topo_type, liste_co_type, liste_co_type2, liste_gCAN, liste_CAN, liste_G_ACh, liste_functional_co, liste_sprouting, liste_sclerosis, liste_lesion_region, liste_tau_Cl, liste_Ek, liste_input_type, liste_custom_inputs, liste_A0, liste_A1, liste_dur, liste_f1, liste_duty_cycle, liste_runtime))

liste_simus = [list(liste_simus[i])+[plot_raster, save_raster, save_neuron_pos, save_syn_mat, save_all_FR]+[i] for i in range(len(liste_simus))]
important_params = [-1] #indices of the parameters to be put to generate result file name. -1=index of the simulation


#setting the number of cores to used (all cpus by default)
num_cores = multiprocessing.cpu_count()
if os.name == 'nt':
    num_cores = -3 #using all cpus on a windows does not work for an unknown reason

Parallel(n_jobs=num_cores)(delayed(set_vars_and_process)(simu, path, important_params) for simu in liste_simus)
