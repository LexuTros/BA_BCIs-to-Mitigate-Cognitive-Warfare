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
from model_files.annex_functions import *
from model_files.set_vars_and_process import *


os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_DYNAMIC'] = 'FALSE'

import time
import ntpath
from itertools import *


def set_vars_and_process(simu_params,path,var_importantes):
    types,maxN,p_tri,p_mono,g_max_i,g_max_e,topo,co,co2,duo_gCAN,hasCAN,var_coeff,fco,sprouting,cell_loss,lesion,tau_Cl,Ek,input_type,custom_inputs,A0,A1,dur,f1,duty_cycle,runtime,plot_raster,save_raster,save_neuron_pos,save_syn_mat,save_all_FR,indices=simu_params
    print('Setting up simulation number '+str(indices+1))
    
    if hasCAN=='sleep': #no CAN
        gCAN=duo_gCAN[0]
    else :
        gCAN=duo_gCAN[1]
    
    all_N=[]
    all_p_inter=[]
    all_p_intra=[]
    all_g_max_e=[]
    all_g_max_i=[]
    all_gains=[]
    
    in_file_1,in_file_2,in_file_3,in_fs=custom_inputs
        
    Ne1=maxN
    Ne2=maxN
    Ne3=maxN//10
    Ne4=maxN
    if lesion=='EC' or lesion=='all':
        Ne1=maxN*(1-0.75*cell_loss)
    if lesion=='DG' or lesion=='all':
        Ne2=maxN*(1-0.6*cell_loss)
    if lesion=='CA3' or lesion=='all':
        Ne3=maxN//10*(1-0.8*cell_loss)
    if lesion=='CA1' or lesion=='all':
        Ne4=maxN*(1-0.8*cell_loss)
    N1=[Ne1*(1-i) for i in range(types[0])]+[maxN//10//types[0] for j in range(types[1])]
    N2=[Ne2*int(types[0]==1)+maxN*i*int(types[0]==2) for i in range(types[0])]+[maxN//100//types[0] for j in range(types[1])]
    N3=[Ne3*(1-i) for i in range(types[0])]+[maxN//100//types[0] for j in range(types[1])]
    N4=[Ne4*(1-i) for i in range(types[0])]+[maxN//10//types[0] for j in range(types[1])]
    
    #N1=[Ne1*(1-i) for i in range(types[0])]+[Ne1//10//types[0] for j in range(types[1])]
    #N2=[Ne2*int(types[0]==1)+maxN*i*int(types[0]==2) for i in range(types[0])]+[Ne2//100//types[0] for j in range(types[1])]
    #N3=[Ne3*(1-i) for i in range(types[0])]+[Ne3//10//types[0] for j in range(types[1])]
    #N4=[Ne4*(1-i) for i in range(types[0])]+[Ne4//10//types[0] for j in range(types[1])]
    
    all_N=[N1,N2,N3,N4]
    all_N=[int(all_N[i][j]) for j in range(types[0]+types[1]) for i in range(4)]
    
    
    rapp_inter=1*int(co=='normal')+6.5*int(co=='uniform')
    all_p_inter=[[[[0 for k in range(types[0]+types[1])] for l in range(types[0])] for i in range(4)] for j in range(4)]
    all_p_inter[0][1]=[[p_tri/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[1][2]=[[p_tri/rapp_inter*(1+sprouting) for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[2][3]=[[p_tri/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[3][0]=[[p_tri/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[0][2]=[[p_mono/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[0][3]=[[p_mono/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[1][3]=[[p_mono*sprouting/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    
    
    rapp_intra_e=1*int(co2=='normal')+4.7*int(co2=='uniform')
    rapp_intra_i=1*int(co2=='normal')+360*int(co2=='uniform')
    p_EC_e=[0 for i in range(types[0])]+[0.37/rapp_intra_e for i in range(types[1])]
    p_EC_i=[0.54/rapp_intra_i for i in range(types[0])]+[0 for i in range(types[1])]
    all_p_EC=[p_EC_e for i in range(types[0])]+[p_EC_i for i in range(types[1])]
    p_DG_e=[0.1*sprouting/rapp_intra_e for i in range(types[0])]+[0.06*(1+sprouting)/rapp_intra_e for i in range(types[1])]
    p_DG_i=[0.14/rapp_intra_i for i in range(types[0])]+[0 for i in range(types[1])]
    all_p_DG=[p_DG_e for i in range(types[0])]+[p_DG_i for i in range(types[1])]
    p_CA3_e=[0.56/rapp_intra_e for i in range(types[0])]+[0.75/rapp_intra_e for i in range(types[1])]
    p_CA3_i=[0.75/rapp_intra_i for i in range(types[0])]+[0 for i in range(types[1])]
    all_p_CA3=[p_CA3_e for i in range(types[0])]+[p_CA3_i for i in range(types[1])]
    p_CA1_e=[0 for i in range(types[0])]+[0.28/rapp_intra_e for i in range(types[1])]
    p_CA1_i=[0.3/rapp_intra_i for i in range(types[0])]+[0.7/rapp_intra_i for i in range(types[1])]
    all_p_CA1=[p_CA1_e for i in range(types[0])]+[p_CA1_i for i in range(types[1])]
    all_p_intra=[all_p_EC,all_p_DG,all_p_CA3,all_p_CA1]
    
    
    all_g_max_e=[g_max_e for i in range(types[0])]
    all_g_max_i=[g_max_i for i in range(types[1])]            
    
    all_gains=[[1 for i in range(types[0]+types[1])] for j in range(4)]
    
    if fco=='wake': #wakefulness connectivity
        all_gains[0][:types[0]]=[1/var_coeff]*types[0] # relevant for synapses in EC
        all_gains[1]=[var_coeff]*(types[0]+types[1]) # relevant for synapses in DG
        all_gains[2][:types[0]]=[1/var_coeff]*types[0] # relevant for synapses in CA3
        all_gains[3][types[0]:]=[var_coeff]*types[1] # relevant for synapses in CA1

    start_scope()
    param_importants=str([simu_params[i] for i in var_importantes])

    new_path=path+"/results_"+param_importants
    os.mkdir(new_path)
    
    
    res_1024, all_FR_exc,all_FR_inh=process(runtime, plot_raster,types,all_N,topo,co,co2,A0,A1,dur,f1,duty_cycle,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,gCAN,save_raster,save_neuron_pos,save_syn_mat,save_all_FR,new_path,in_file_1,in_file_2,in_file_3,in_fs,tau_Cl,Ek) 

    return res_1024


def de_normalize(vect):
#    print(vect)
    vect_denorm=vect
    lim_f=[0.05*Hz,20*Hz]
    lim_A=[0.5,1.5]
    lim_p_tri=[0.2,0.7]
    lim_p_mono=[0.1,0.5]
    lim_g_max_i=[500*psiemens,700*psiemens]
    lim_g_max_e=[50*psiemens,70*psiemens]
    lim_gain_e_augm=[1,5]
    lim_gain_e_dim=[1,5]
    lim_gain_i_augm=[1,5]
    lim_gCAN=[0.5*usiemens*cmeter**-2,25*usiemens*cmeter**-2]
    
    all_lims=[lim_f,lim_A,lim_p_tri,lim_p_mono,lim_g_max_i,lim_g_max_e,lim_gain_e_augm,lim_gain_e_dim,lim_gain_i_augm,lim_gCAN]
#    print(len(all_lims))
    for i in range(len(all_lims)):
        vect_denorm[i]=all_lims[i][0]+(vect[i]+1)/2*(all_lims[i][1]-all_lims[i][0])
    gains=[[1/vect_denorm[7],1],[vect_denorm[6],vect_denorm[8]],[1/vect_denorm[7],1],[1,vect_denorm[8]]]    
    return vect_denorm[:6]+[gains]+[vect_denorm[-1]]

def open_doe_file(filename):
    all_doe=[]
    file=open(filename,'r')
    for line in file:
        all_doe.append([float(val) for val in line.split(',')])
    return [de_normalize(doe) for doe in all_doe]