#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from brian2 import *

from model_files.global_vars_and_eqs import *
from model_files.topology import topologie,topologie_rectangle
from model_files.apply_input import *
from model_files.annex_functions import *
from model_files.preparation import *
import scipy
import time
import datetime
import os


def nanzero(tableau1D):
    newtab=array(tableau1D)
    newtab[where(isnan(newtab))]=0
    return newtab


def process(runtime, plot_raster,types,all_N,topo,co,co2,A0,A1,dur,f1,duty_cycle,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,gCAN,save_sim_raster,save_neuron_pos,save_syn_mat,save_all_FR,path,in_file_1,in_file_2,in_file_3,in_fs,tau_Cl,Ek) :
    liste_params=[runtime, plot_raster,types,all_N,topo,co,co2,A0,A1,dur,f1,duty_cycle,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,gCAN,save_sim_raster,save_neuron_pos,save_syn_mat,in_file_1,in_file_2,in_file_3,in_fs,tau_Cl,Ek]
    liste_params_names=['runtime', 'plot_raster','types','all_N','topo','co','co2','A0','A1','dur','f1','duty_cycle','input_type','all_p_intra','all_p_inter','all_gains','all_g_max_i','all_g_max_e','gCAN','save_sim_raster','save_neuron_pos','save_syn_mat','in_file_1','in_file_2','in_file_3','in_fs','tau_Cl','Ek']
#    print(liste_params)
    save_params(liste_params,liste_params_names,path)
    print('Simulations parameters saved')
    
    print('Generating neurons positions')
    
    pas_de_temps=defaultclock.dt 
    p_in=0.05
    debut=time.time()
    bis=False
    #    version='_'+str(ver)+input_num
#    input_num=ord(input_num)-64
    if topo=='normal':
        all_pos, elec_pos=topologie(types,all_N)
    else :
        all_pos, elec_pos=topologie_rectangle(types,all_N)
        
#    print(elec_pos[0],elec_pos[-1])
        
    if types[0]==1 and types[1]==1:
        EC_e,EC_e_end,EC_e_inh,EC_i,EC_i_end,EC_i_inh=all_pos[0]
        DG_e,DG_e_end,DG_e_inh,DG_i,DG_i_end,DG_i_inh=all_pos[1]
        CA3_e,CA3_e_end,CA3_e_inh,CA3_i,CA3_i_end,CA3_i_inh=all_pos[2]
        CA1_e,CA1_e_end,CA1_e_inh,CA1_i,CA1_i_end,CA1_i_inh=all_pos[3]
        dir_EC=(EC_e-EC_e_end)/norm(EC_e-EC_e_end,2,1).reshape(-1,1)
        dir_DG=(DG_e-DG_e_end)/norm(DG_e-DG_e_end,2,1).reshape(-1,1)
        dir_CA3=(CA3_e-CA3_e_end)/norm(CA3_e-CA3_e_end,2,1).reshape(-1,1)
        dir_CA1=(CA1_e-CA1_e_end)/norm(CA1_e-CA1_e_end,2,1).reshape(-1,1)
        dir_ECi=(EC_i-EC_i_end)/norm(EC_i-EC_i_end,2,1).reshape(-1,1)
        dir_DGi=(DG_i-DG_i_end)/norm(DG_i-DG_i_end,2,1).reshape(-1,1)
        dir_CA3i=(CA3_i-CA3_i_end)/norm(CA3_i-CA3_i_end,2,1).reshape(-1,1)
        dir_CA1i=(CA1_i-CA1_i_end)/norm(CA1_i-CA1_i_end,2,1).reshape(-1,1)
        dir_hipp=(dir_EC,dir_DG,dir_CA3,dir_CA1)
        all_dir=[[dir_EC,dir_ECi],[dir_DG,dir_DGi],[dir_CA3,dir_CA3i],[dir_CA1,dir_CA1i]]
  
    elif types[0]==2 and types[1]==1:
        EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i,EC_i_end,EC_i_inh=all_pos[0]
        DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i,DG_i_end,DG_i_inh=all_pos[1]
        CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i,CA3_i_end,CA3_i_inh=all_pos[2]
        CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i,CA1_i_end,CA1_i_inh=all_pos[3]
        dir_EC1=(EC_e1-EC_e1_end)/norm(EC_e1-EC_e1_end,2,1).reshape(-1,1)
        dir_EC2=(EC_e2-EC_e2_end)/norm(EC_e2-EC_e2_end,2,1).reshape(-1,1)
        dir_DG1=(DG_e1-DG_e1_end)/norm(DG_e1-DG_e1_end,2,1).reshape(-1,1)
        dir_DG2=(DG_e2-DG_e2_end)/norm(DG_e2-DG_e2_end,2,1).reshape(-1,1)
        dir_CA31=(CA3_e1-CA3_e1_end)/norm(CA3_e1-CA3_e1_end,2,1).reshape(-1,1)
        dir_CA32=(CA3_e2-CA3_e2_end)/norm(CA3_e2-CA3_e2_end,2,1).reshape(-1,1)
        dir_CA11=(CA1_e1-CA1_e1_end)/norm(CA1_e1-CA1_e1_end,2,1).reshape(-1,1)
        dir_CA12=(CA1_e2-CA1_e2_end)/norm(CA1_e2-CA1_e2_end,2,1).reshape(-1,1)
        dir_hipp=(dir_EC1,dir_EC2,dir_DG1,dir_DG2,dir_CA31,dir_CA32,dir_CA11,dir_CA12)
        
    elif types[0]==1 and types[1]==2:
        EC_e,EC_e_end,EC_e_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh=all_pos[0]
        DG_e,DG_e_end,DG_e_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh=all_pos[1]
        CA3_e,CA3_e_end,CA3_e_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh=all_pos[2]
        CA1_e,CA1_e_end,CA1_e_inh,EC_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh=all_pos[3]
        dir_EC=(EC_e-EC_e_end)/norm(EC_e-EC_e_end,2,1).reshape(-1,1)
        dir_DG=(DG_e-DG_e_end)/norm(DG_e-DG_e_end,2,1).reshape(-1,1)
        dir_CA3=(CA3_e-CA3_e_end)/norm(CA3_e-CA3_e_end,2,1).reshape(-1,1)
        dir_CA1=(CA1_e-CA1_e_end)/norm(CA1_e-CA1_e_end,2,1).reshape(-1,1)
        dir_hipp=(dir_EC,dir_DG,dir_CA3,dir_CA1)
        
    else :
        EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh=all_pos[0]
        DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh=all_pos[1]
        CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh=all_pos[2]
        CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh=all_pos[3]
        dir_hipp=[]
        for i_zone in range(4):
            for j_exc in range(2):
                if len(all_pos[i_zone][3*j_exc])>0:
#                    print(len(all_pos[i_zone][3*j_exc]))
                    dir_hipp.append((all_pos[i_zone][3*j_exc]-all_pos[i_zone][3*j_exc+1])/norm(all_pos[i_zone][3*j_exc]-all_pos[i_zone][3*j_exc+1],2,1).reshape(-1,1))
                else :
                    dir_hipp.append(array([]))
#        dir_EC1=(EC_e1-EC_e1_end)/norm(EC_e1-EC_e1_end,2,1).reshape(-1,1)
#        dir_EC2=(EC_e2-EC_e2_end)/norm(EC_e2-EC_e2_end,2,1).reshape(-1,1)
#        dir_DG1=(DG_e1-DG_e1_end)/norm(DG_e1-DG_e1_end,2,1).reshape(-1,1)
#        dir_DG2=(DG_e2-DG_e2_end)/norm(DG_e2-DG_e2_end,2,1).reshape(-1,1)
#        dir_CA31=(CA3_e1-CA3_e1_end)/norm(CA3_e1-CA3_e1_end,2,1).reshape(-1,1)
#        dir_CA32=(CA3_e2-CA3_e2_end)/norm(CA3_e2-CA3_e2_end,2,1).reshape(-1,1)
#        dir_CA11=(CA1_e1-CA1_e1_end)/norm(CA1_e1-CA1_e1_end,2,1).reshape(-1,1)
#        dir_CA12=(CA1_e2-CA1_e2_end)/norm(CA1_e2-CA1_e2_end,2,1).reshape(-1,1)
#        dir_hipp=(dir_EC1,dir_EC2,dir_DG1,dir_DG2,dir_CA31,dir_CA32,dir_CA11,dir_CA12)

    if save_neuron_pos:
        save_pos(types,all_pos,path)
        save_dir(types,all_dir,path)
        
#    print('positions generated')
    

    nb_runs=int(10*runtime/second)

    start_scope()
    prefs.codegen.target = 'numpy'  # use the Python fallback
    
    record_dt=1./1024 *second

    print('Generating the inputs')
    inputs1,inputs2,inputs3=apply_input(input_type,A0,A1,dur,f1,duty_cycle,runtime,in_file_1,in_file_2,in_file_3,in_fs)
#    print(inputs1(500*msecond))
    
    print('Building the network')    
    myNetwork=Network()         
    all_neuron_groups,all_syn_intra,all_syn_inter=preparation(input_type,inputs1,types,all_pos,dir_hipp,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,co,co2,tau_Cl)
#    print([[[(syn.source, syn.target) for syn in liste_syn] for liste_syn in region] for region in all_syn_intra])
    for zone_i in range(4):
        for liste_groups in all_neuron_groups[zone_i]:
            for group in liste_groups:
                if group:
#                    print(group)
                    myNetwork.add(group)
    
    if input_type=='custom':
#        print('input reel')
        In_exc1=NeuronGroup(10000, 'rates : Hz', threshold='rand()<inputs1(t)*pas_de_temps')    #dt ? record_dt ?
        In_exc2=NeuronGroup(10000, 'rates : Hz', threshold='rand()<inputs2(t)*pas_de_temps')    #dt ? record_dt ? 
        In_exc3=NeuronGroup(10000, 'rates : Hz', threshold='rand()<inputs3(t)*pas_de_temps')    #dt ? record_dt ?    
        myNetwork.add([In_exc1,In_exc2,In_exc3])
        for Gpy in all_neuron_groups[0][0]:
            S11 = Synapses(In_exc1, Gpy, on_pre='he_post+='+str(all_g_max_e[0]/siemens)+'*siemens')
            S11.connect(p='p_in*int(66*scale<z_soma_post)*int(z_soma_post<100*scale)')
            S21 = Synapses(In_exc2, Gpy, on_pre='he_post+='+str(all_g_max_e[0]/siemens)+'*siemens')
            S21.connect(p='p_in*int(33*scale<z_soma_post)*int(z_soma_post<66*scale)')
            S31 = Synapses(In_exc3, Gpy, on_pre='he_post+='+str(all_g_max_e[0]/siemens)+'*siemens')
            S31.connect(p='p_in*int(0*scale<z_soma_post)*int(z_soma_post<33*scale)') 
            myNetwork.add([S11,S21,S31])
        for Ginh in all_neuron_groups[0][1]:
            S11 = Synapses(In_exc1, Ginh, on_pre='he_post+='+str(all_g_max_e[0]/siemens)+'*siemens')
            S11.connect(p='p_in*int(66*scale<z_soma_post)*int(z_soma_post<100*scale)')
            S21 = Synapses(In_exc2, Ginh, on_pre='he_post+='+str(all_g_max_e[0]/siemens)+'*siemens')
            S21.connect(p='p_in*int(33*scale<z_soma_post)*int(z_soma_post<66*scale)')
            S31 = Synapses(In_exc3, Ginh, on_pre='he_post+='+str(all_g_max_e[0]/siemens)+'*siemens')
            S31.connect(p='p_in*int(0*scale<z_soma_post)*int(z_soma_post<33*scale)') 
            myNetwork.add([S11,S21,S31])
#    else :
#        print(all_neuron_groups[0][0][0].I_exc[:])
    #### Simultation #######
    print('Compiling with cython')
    prefs.codegen.target = 'cython' 
#    print(all_neuron_groups)
    
   
#    print('syn_inter')
    for syn_inter in make_flat(all_syn_inter):
        if syn_inter!=0:
#            print(syn_inter,syn_inter.source, syn_inter.target)
            myNetwork.add(syn_inter)
#    print('syn_intra')
#    print(all_syn_intra)
    for syn_intra in make_flat(all_syn_intra):
        if syn_intra!=0:
#            print(syn_intra,syn_intra.source,syn_intra.target)
            myNetwork.add(syn_intra)
    single_runtime=runtime/nb_runs
    signal_principal=zeros(int(runtime/pas_de_temps))
    isyn_EC_e1=zeros(int(runtime/pas_de_temps))
    isyn_DG_e1=zeros(int(runtime/pas_de_temps))
    isyn_CA3_e1=zeros(int(runtime/pas_de_temps))
    isyn_CA1_e1=zeros(int(runtime/pas_de_temps))
    isyn_EC_i1=zeros(int(runtime/pas_de_temps))
    isyn_DG_i1=zeros(int(runtime/pas_de_temps))
    isyn_CA3_i1=zeros(int(runtime/pas_de_temps))
    isyn_CA1_i1=zeros(int(runtime/pas_de_temps))
    
    isyn_EC_e2=zeros(int(runtime/pas_de_temps))
    isyn_DG_e2=zeros(int(runtime/pas_de_temps))
    isyn_CA3_e2=zeros(int(runtime/pas_de_temps))
    isyn_CA1_e2=zeros(int(runtime/pas_de_temps))
    isyn_EC_i2=zeros(int(runtime/pas_de_temps))
    isyn_DG_i2=zeros(int(runtime/pas_de_temps))
    isyn_CA3_i2=zeros(int(runtime/pas_de_temps))
    isyn_CA1_i2=zeros(int(runtime/pas_de_temps))
    
    if bis :
        signal_principal_bis=zeros(int(runtime/pas_de_temps))
        isyn_EC_e1_bis=zeros(int(runtime/pas_de_temps))
        isyn_DG_e1_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA3_e1_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA1_e1_bis=zeros(int(runtime/pas_de_temps))
        isyn_EC_i1_bis=zeros(int(runtime/pas_de_temps))
        isyn_DG_i1_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA3_i1_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA1_i1_bis=zeros(int(runtime/pas_de_temps))
        
        isyn_EC_e2_bis=zeros(int(runtime/pas_de_temps))
        isyn_DG_e2_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA3_e2_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA1_e2_bis=zeros(int(runtime/pas_de_temps))
        isyn_EC_i2_bis=zeros(int(runtime/pas_de_temps))
        isyn_DG_i2_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA3_i2_bis=zeros(int(runtime/pas_de_temps))
        isyn_CA1_i2_bis=zeros(int(runtime/pas_de_temps))        
#    return

    global all_rasters_i_exc,all_rasters_i_inh,all_rasters_t_exc,all_rasters_t_inh
    
    all_rasters_i_exc=[[[] for i in range(types[0])] for j in range(4)]
    all_rasters_t_exc=[[[] for i in range(types[0])] for j in range(4)]
    all_rasters_i_inh=[[[] for i in range(types[1])] for j in range(4)]
    all_rasters_t_inh=[[[] for i in range(types[1])] for j in range(4)]

    all_FR_exc=[[[] for i in range(types[0])] for j in range(4)]
    all_FR_inh=[[[] for i in range(types[1])] for j in range(4)]

    for test_ind in range(nb_runs):
#        print(test_ind,single_runtime)
        all_syn_intra_E_monitors=[[StateMonitor(Gpy,'I_SynE',record=True,dt=pas_de_temps) if Gpy else None for Gpy in all_neuron_groups[i][0]] for i in range(4)]
        all_syn_intra_I_monitors=[[StateMonitor(Gpy,'I_SynI',record=True,dt=pas_de_temps) if Gpy else None for Gpy in all_neuron_groups[i][0]] for i in range(4)]
        all_syn_inter_monitors=[[StateMonitor(Gpy,'I_SynExt',record=True,dt=pas_de_temps) if Gpy else None for Gpy in all_neuron_groups[i][0]] for i in range(4)]
#        print(all_syn_intra_E_monitors)
#        print(all_syn_intra_I_monitors)
#        print(all_syn_inter_monitors)
        all_rate_E_monitors=[[PopulationRateMonitor(Gpy) if Gpy else None for Gpy in all_neuron_groups[i][0]] for i in range(4)]
        all_rate_I_monitors=[[PopulationRateMonitor(Ginh) if Ginh else None for Ginh in all_neuron_groups[i][1]] for i in range(4)]
   
#        print(all_rate_E_monitors)
        if plot_raster or save_sim_raster:
            all_spike_E_monitors=[[SpikeMonitor(Gpy,record=[all_N[i]//2-5+k for k in range(10)]) for Gpy in all_neuron_groups[i][0] if Gpy] for i in range(4)]
            all_spike_I_monitors=[[SpikeMonitor(Ginh,record=[all_N[i+4]-5+k for k in range(all_N[i+4]//100)]) for Ginh in all_neuron_groups[i][1] if Ginh] for i in range(4)]
            #print([[all_N[i]//2-5+k for k in range(10)]for i in range(4)])
            #print([[all_N[i+4]//2-5+k for k in range(10)]for i in range(4)])
            myNetwork.add(all_spike_E_monitors)
            myNetwork.add(all_spike_I_monitors)

        for monitor in make_flat(all_syn_intra_E_monitors):
#            print(monitor)
            if monitor!=None:  
#                print(monitor)
                myNetwork.add(monitor)
                
        for monitor in make_flat(all_syn_intra_I_monitors):
            if monitor!=None:  
#                print(monitor)
                myNetwork.add(monitor)
        for monitor in make_flat(all_syn_inter_monitors):
            if monitor!=None: 
#                print(monitor)
                myNetwork.add(monitor)
        for monitor in make_flat(all_rate_E_monitors):
            if monitor!=None:  
#                print(monitor)
                myNetwork.add(monitor)
        for monitor in make_flat(all_rate_I_monitors):
            if monitor!=None:  
#                print(monitor)
                myNetwork.add(monitor)
#        myNetwork.add(all_syn_inter_monitors)
#        myNetwork.add(all_rate_E_monitors)
#        myNetwork.add(all_rate_I_monitors)
        myNetwork.run(duration=single_runtime,report='text',report_period=300*second)
#        run(single_runtime,report='text',report_period=300*second)

#        print(all_neuron_groups[0][0][0][5:10].I_SynI)
#        print(all_neuron_groups[1][0][0][5:10].I_SynI)
#        print(all_neuron_groups[2][0][0][5:10].I_SynI)
#        print(all_neuron_groups[3][0][0][5:10].I_SynI)
#        print(all_neuron_groups[0][0][0][5:10].I_SynExt)
#        print(all_neuron_groups[1][0][0][5:10].I_SynExt)
#        print(all_neuron_groups[2][0][0][5:10].I_SynExt)
#        print(all_neuron_groups[3][0][0][5:10].I_SynExt)
        
        for j in range(4):
            for i in range(len(all_rate_E_monitors[j])):
                if all_rate_E_monitors[j][i]:
    #                print(list(array(all_rate_E_monitors[j][i].smooth_rate(window='flat',width=10*ms))))
                    all_FR_exc[j][i]+=list(array(all_rate_E_monitors[j][i].smooth_rate(window='flat',width=10*ms)))
            for i in range(len(all_rate_I_monitors[j])):
                if all_rate_I_monitors[j][i]:
                    all_FR_inh[j][i]+=list(array(all_rate_I_monitors[j][i].smooth_rate(window='flat',width=10*ms)))
        

        if plot_raster or save_sim_raster:
            for j in range(4):
                for i in range(len(all_spike_E_monitors[j])):
                    #print(all_spike_E_monitors[j][i].i)
                    all_rasters_i_exc[j][i].append(all_spike_E_monitors[j][i].i)
                    all_rasters_t_exc[j][i].append(all_spike_E_monitors[j][i].t)
                for i in range(len(all_spike_I_monitors[i])):
                    all_rasters_i_inh[j][i].append(all_spike_I_monitors[j][i].i)
                    all_rasters_t_inh[j][i].append(all_spike_I_monitors[j][i].t)
       

        ###Calcul du LFP
        print('Computing the LFP')  
        start_plot_time=500*msecond
        start_ind=int(start_plot_time/record_dt)      
        

        all_isyn=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        
        all_isyn_EC_e=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        all_isyn_DG_e=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        all_isyn_CA3_e=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        all_isyn_CA1_e=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        
        all_isyn_EC_i=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        all_isyn_DG_i=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        all_isyn_CA3_i=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        all_isyn_CA1_i=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        
        if bis :
            all_isyn_EC_e_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
            all_isyn_DG_e_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
            all_isyn_CA3_e_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
            all_isyn_CA1_e_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
            
            all_isyn_EC_i_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
            all_isyn_DG_i_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
            all_isyn_CA3_i_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
            all_isyn_CA1_i_bis=zeros((len(elec_pos),int(single_runtime/pas_de_temps)))
        
        def lfp_1groupe(Gpy,I_E,I_Ext,I_I,contact_point,elec_pos):
#            print(elec_pos[0],elec_pos[-1])
            xx=array(elec_pos)[:,0]*scale
            yy=array(elec_pos)[:,1]*scale
            zz=array(elec_pos)[:,2]*scale
            
            x=tile(xx,(len(Gpy.x_soma),1)).T
            y=tile(yy,(len(Gpy.x_soma),1)).T
            z=tile(zz,(len(Gpy.x_soma),1)).T
            dx=x-(Gpy.x_soma+Gpy.x_dendrite)*0.5
            dy=y-(Gpy.y_soma+Gpy.y_dendrite)*0.5
            dz=z-(Gpy.z_soma+Gpy.z_dendrite)*0.5
            dist=(dx**2+dy**2+dz**2)**0.5
            w=1/(4*pi*sigma*dist**2)*((Gpy.x_soma-Gpy.x_dendrite)**2+(Gpy.y_soma-Gpy.y_dendrite)**2+(Gpy.z_soma-Gpy.z_dendrite)**2)**0.5
            cos_angle=(Gpy.dir_x*dx+Gpy.dir_y*dy+Gpy.dir_z*dz)/dist
#            print(len(where(cos_angle<0)[0]),len(where(cos_angle>0)[0]))
#            print(len(where(w<0)[0]),len(where(w>0)[0]))
            lfp_e=w*cos_angle@nanzero(I_E.I_SynE)
#            print(len(where(lfp<0)[0]),len(where(lfp>0)[0]))
#            print(lfp)
#            print(I_E.I_SynE)
            if contact_point=='apical':
#                print('apical')
                lfp_e+=w*cos_angle@nanzero(I_Ext.I_SynExt)
            
            dx=x-(Gpy.x_soma+Gpy.x_inh)*0.5
            dy=y-(Gpy.y_soma+Gpy.y_inh)*0.5
            dz=z-(Gpy.z_soma+Gpy.z_inh)*0.5
            dist=(dx**2+dy**2+dz**2)**0.5
            w=1/(4*pi*sigma*dist**2)*((Gpy.x_soma-Gpy.x_inh)**2+(Gpy.y_soma-Gpy.y_inh)**2+(Gpy.z_soma-Gpy.z_inh)**2)**0.5
            cos_angle=(Gpy.dir_x*dx+Gpy.dir_y*dy+Gpy.dir_z*dz)/dist
            lfp_i=w*cos_angle@nanzero(I_I.I_SynI)
            
#            print(I_E.I_SynE.shape,I_I.I_SynI.shape,I_Ext.I_SynExt.shape)
            
            if contact_point=='basal':
#                print('basal')
                lfp_e+=w*cos_angle@nanzero(I_Ext.I_SynExt) 
                
#            print(len(where(cos_angle<0)[0]),len(where(cos_angle>0)[0]))
#            print(len(where(w<0)[0]),len(where(w>0)[0]))
#            print(len(where(lfp<0)[0]),len(where(lfp>0)[0]))
#            print(lfp)
#            print()
#            print(lfp.shape)
            return lfp_e,lfp_i
        
        test = True
        def lfp_1groupe_bis(Gpy,I_E,I_Ext,I_I,contact_point,elec_pos):
            global test
#            print(elec_pos[0],elec_pos[-1])
            xx=array(elec_pos)[:,0]*scale
            yy=array(elec_pos)[:,1]*scale
            zz=array(elec_pos)[:,2]*scale
            
            x=tile(xx,(len(Gpy.x_soma),1)).T
            y=tile(yy,(len(Gpy.x_soma),1)).T
            z=tile(zz,(len(Gpy.x_soma),1)).T
            debut_x,debut_y,debut_z=Gpy.x_soma,Gpy.y_soma,Gpy.z_soma
            debut=array([debut_x,debut_y,debut_z])
            fin_theo_x,fin_theo_y,fin_theo_z=Gpy.x_dendrite,Gpy.y_dendrite,Gpy.z_dendrite
            t1=uniform(0.8,1.2,size=debut_x.shape)
            t2=uniform(-1,1,size=debut_x.shape)*100*umetre
            t3=uniform(-1,1,size=debut_x.shape)*100*umetre
            vect_z=array([0*metre,0*metre,1*metre])
#            print((array([fin_theo_x,fin_theo_y,fin_theo_z])-array([debut_x,debut_y,debut_z])).shape,vect_z.shape)
            vect_ortho=cross((array([fin_theo_x,fin_theo_y,fin_theo_z])-array([debut_x,debut_y,debut_z])).T,vect_z)
#            print(vect_ortho)
            vect_ortho=t3*vect_ortho.T/norm(vect_ortho)
            fin=t1*(array([fin_theo_x,fin_theo_y,fin_theo_z])-array([debut_x,debut_y,debut_z]))*metre+array([debut_x,debut_y,debut_z])*metre+vect_ortho
            fin_x,fin_y,fin_z=fin[0],fin[1],fin[2]
#            if test :
#                figure()
#                print(t1[0],t2[0],t3[0])
#                print(((fin_theo_x[0]-debut_x[0])**2+(fin_theo_y[0]-debut_y[0])**2)**0.5)
#                plot([debut_x[0],fin_theo_x[0]],[debut_y[0],fin_theo_y[0]])
#                plot([debut_x[0],fin_x[0]],[debut_y[0],fin_y[0]])
#                plot([fin_theo_x[0],fin_theo_x[0]+vect_ortho[0,0]],[fin_theo_y[0],fin_theo_y[0]+vect_ortho[0,1]])
#                test=False
#                (a,c)=(3,b)
                
            fin_z+=t2
            dx=x-(debut_x+fin_x)*0.5
            dy=y-(debut_y+fin_y)*0.5
            dz=z-(debut_z+fin_z)*0.5
            dist=(dx**2+dy**2+dz**2)**0.5
            w=1/(4*pi*sigma*dist**2)*((debut_x-fin_x)**2+(debut_y-fin_y)**2+(debut_z-fin_z)**2)**0.5
            dir_x,dir_y,dir_z=-(fin-debut*metre)/norm(fin-debut*metre)
            cos_angle=(dir_x*dx+dir_y*dy+dir_z*dz)/dist
#            print(len(where(cos_angle<0)[0]),len(where(cos_angle>0)[0]))
#            print(len(where(w<0)[0]),len(where(w>0)[0]))
            lfp_e=w*cos_angle@nanzero(I_E.I_SynE)
#            print(len(where(lfp<0)[0]),len(where(lfp>0)[0]))
#            print(lfp)
#            print(I_E.I_SynE)
            if contact_point=='apical':
#                print('apical')
                lfp_e+=w*cos_angle@nanzero(I_Ext.I_SynExt)
            
            fin_theo_x,fin_theo_y,fin_theo_z=Gpy.x_inh,Gpy.y_inh,Gpy.z_inh
            t1=uniform(0.8,1.2,size=debut_x.shape)
            t2=uniform(-1,1,size=debut_x.shape)*5*umetre
            t3=uniform(-1,1,size=debut_x.shape)*5*umetre
            vect_z=array([0*metre,0*metre,1*metre])
#            print((array([fin_theo_x,fin_theo_y,fin_theo_z])-array([debut_x,debut_y,debut_z])).shape,vect_z.shape)
            vect_ortho=cross((array([fin_theo_x,fin_theo_y,fin_theo_z])-array([debut_x,debut_y,debut_z])).T,vect_z)
#            print(vect_ortho)
            vect_ortho=t3*vect_ortho.T/norm(vect_ortho)
            fin=t1*(array([fin_theo_x,fin_theo_y,fin_theo_z])-array([debut_x,debut_y,debut_z]))*metre+array([debut_x,debut_y,debut_z])*metre+vect_ortho
            fin_x,fin_y,fin_z=fin[0],fin[1],fin[2]
                
            fin_z+=t2
            dx=x-(debut_x+fin_x)*0.5
            dy=y-(debut_y+fin_y)*0.5
            dz=z-(debut_z+fin_z)*0.5
            dist=(dx**2+dy**2+dz**2)**0.5
            w=1/(4*pi*sigma*dist**2)*((debut_x-fin_x)**2+(debut_y-fin_y)**2+(debut_z-fin_z)**2)**0.5
            dir_x,dir_y,dir_z=-(fin-debut*metre)/norm(fin-debut*metre)
            cos_angle=(dir_x*dx+dir_y*dy+dir_z*dz)/dist
            lfp_i=w*cos_angle@nanzero(I_I.I_SynI)
            
#            print(I_E.I_SynE.shape,I_I.I_SynI.shape,I_Ext.I_SynExt.shape)
            
            if contact_point=='basal':
#                print('basal')
                lfp_e+=w*cos_angle@nanzero(I_Ext.I_SynExt) 
                
#            print(len(where(cos_angle<0)[0]),len(where(cos_angle>0)[0]))
#            print(len(where(w<0)[0]),len(where(w>0)[0]))
#            print(len(where(lfp<0)[0]),len(where(lfp>0)[0]))
#            print(lfp)
#            print()
#            print(lfp.shape)
            return lfp_e,lfp_i
        
        

        for i in range(types[0]):
#            print(i)
            if all_neuron_groups[0][0][i]:
#                print(all_neuron_groups[0][0][i],all_syn_intra_E_monitors[0][i],all_syn_inter_monitors[0][i],all_syn_intra_I_monitors[0][i])
                lfp_EC_e,lfp_EC_i=lfp_1groupe(all_neuron_groups[0][0][i],all_syn_intra_E_monitors[0][i],all_syn_inter_monitors[0][i],all_syn_intra_I_monitors[0][i],'basal',elec_pos)
                all_isyn_EC_e+=lfp_EC_e
                all_isyn_EC_i+=lfp_EC_i
#            print(all_isyn[0])
            if all_neuron_groups[1][0][i]:
                lfp_DG_e,lfp_DG_i=lfp_1groupe(all_neuron_groups[1][0][i],all_syn_intra_E_monitors[1][i],all_syn_inter_monitors[1][i],all_syn_intra_I_monitors[1][i],'basal',elec_pos)
                all_isyn_DG_e-=lfp_DG_e
                all_isyn_DG_i-=lfp_DG_i
#            print(all_isyn[0])
            if all_neuron_groups[2][0][i]:
                lfp_CA3_e,lfp_CA3_i=lfp_1groupe(all_neuron_groups[2][0][i],all_syn_intra_E_monitors[2][i],all_syn_inter_monitors[2][i],all_syn_intra_I_monitors[2][i],'apical',elec_pos)
                all_isyn_CA3_e+=lfp_CA3_e
                all_isyn_CA3_i+=lfp_CA3_i
#            print(all_isyn[0])
            if all_neuron_groups[3][0][i] :
                lfp_CA1_e,lfp_CA1_i=lfp_1groupe(all_neuron_groups[3][0][i],all_syn_intra_E_monitors[3][i],all_syn_inter_monitors[3][i],all_syn_intra_I_monitors[3][i],'apical',elec_pos)
                all_isyn_CA1_e+=lfp_CA1_e
                all_isyn_CA1_i+=lfp_CA1_i
    #       print(all_isyn[0])    
        if bis :
            for i in range(types[0]):
    #            print(i)
                if all_neuron_groups[0][0][i]:
    #                print(all_neuron_groups[0][0][i],all_syn_intra_E_monitors[0][i],all_syn_inter_monitors[0][i],all_syn_intra_I_monitors[0][i])
                    lfp_EC_e_bis,lfp_EC_i_bis=lfp_1groupe_bis(all_neuron_groups[0][0][i],all_syn_intra_E_monitors[0][i],all_syn_inter_monitors[0][i],all_syn_intra_I_monitors[0][i],'basal',elec_pos)
                    all_isyn_EC_e_bis+=lfp_EC_e_bis
                    all_isyn_EC_i_bis+=lfp_EC_i_bis
    #            print(all_isyn[0])
                if all_neuron_groups[1][0][i]:
                    lfp_DG_e_bis,lfp_DG_i_bis=lfp_1groupe_bis(all_neuron_groups[1][0][i],all_syn_intra_E_monitors[1][i],all_syn_inter_monitors[1][i],all_syn_intra_I_monitors[1][i],'basal',elec_pos)
                    all_isyn_DG_e_bis-=lfp_DG_e_bis
                    all_isyn_DG_i_bis-=lfp_DG_i_bis
    #            print(all_isyn[0])
                if all_neuron_groups[2][0][i]:
                    lfp_CA3_e_bis,lfp_CA3_i_bis=lfp_1groupe_bis(all_neuron_groups[2][0][i],all_syn_intra_E_monitors[2][i],all_syn_inter_monitors[2][i],all_syn_intra_I_monitors[2][i],'apical',elec_pos)
                    all_isyn_CA3_e_bis+=lfp_CA3_e_bis
                    all_isyn_CA3_i_bis+=lfp_CA3_i_bis
    #            print(all_isyn[0])
                if all_neuron_groups[3][0][i] :
                    lfp_CA1_e_bis,lfp_CA1_i_bis=lfp_1groupe_bis(all_neuron_groups[3][0][i],all_syn_intra_E_monitors[3][i],all_syn_inter_monitors[3][i],all_syn_intra_I_monitors[3][i],'apical',elec_pos)
                    all_isyn_CA1_e_bis+=lfp_CA1_e_bis
                    all_isyn_CA1_i_bis+=lfp_CA1_i_bis
    #            print(all_isyn[0])    

        isyn_EC_e1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_e[:144,:],axis=0)/144
        isyn_DG_e1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_e[:144,:],axis=0)/144
        isyn_CA3_e1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_e[:144,:],axis=0)/144
        isyn_CA1_e1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_e[:144,:],axis=0)/144
        isyn_EC_i1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_i[:144,:],axis=0)/144
        isyn_DG_i1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_i[:144,:],axis=0)/144
        isyn_CA3_i1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_i[:144,:],axis=0)/144
        isyn_CA1_i1[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_i[:144,:],axis=0)/144

        isyn_EC_e2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_e[144:288,:],axis=0)/144
        isyn_DG_e2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_e[144:288,:],axis=0)/144
        isyn_CA3_e2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_e[144:288,:],axis=0)/144
        isyn_CA1_e2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_e[144:288,:],axis=0)/144
        isyn_EC_i2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_i[144:288,:],axis=0)/144
        isyn_DG_i2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_i[144:288,:],axis=0)/144
        isyn_CA3_i2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_i[144:288,:],axis=0)/144
        isyn_CA1_i2[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_i[144:288,:],axis=0)/144

#        isyn_principal_1=sum(all_isyn[:144,:],axis=0)/144
#        isyn_principal_2=sum(all_isyn[144:288,:],axis=0)/144
        isyn_principal_2=(isyn_EC_e2+isyn_DG_e2+isyn_CA3_e2+isyn_CA1_e2+isyn_EC_i2+isyn_DG_i2+isyn_CA3_i2+isyn_CA1_i2)[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]
        isyn_principal_1=(isyn_EC_e1+isyn_DG_e1+isyn_CA3_e1+isyn_CA1_e1+isyn_EC_i1+isyn_DG_i1+isyn_CA3_i1+isyn_CA1_i1)[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]
        isyn_principal=isyn_principal_2-isyn_principal_1
#        print(max(isyn_principal_1),max(isyn_principal_2),max(isyn_principal))
#        print(min(isyn_principal_1),min(isyn_principal_2),min(isyn_principal))
        
        signal_principal[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=isyn_principal

        if bis :
            isyn_EC_e1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_e_bis[:144,:],axis=0)/144
            isyn_DG_e1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_e_bis[:144,:],axis=0)/144
            isyn_CA3_e1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_e_bis[:144,:],axis=0)/144
            isyn_CA1_e1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_e_bis[:144,:],axis=0)/144
            isyn_EC_i1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_i_bis[:144,:],axis=0)/144
            isyn_DG_i1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_i_bis[:144,:],axis=0)/144
            isyn_CA3_i1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_i_bis[:144,:],axis=0)/144
            isyn_CA1_i1_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_i_bis[:144,:],axis=0)/144
    
            isyn_EC_e2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_e_bis[144:288,:],axis=0)/144
            isyn_DG_e2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_e_bis[144:288,:],axis=0)/144
            isyn_CA3_e2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_e_bis[144:288,:],axis=0)/144
            isyn_CA1_e2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_e_bis[144:288,:],axis=0)/144
            isyn_EC_i2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_EC_i_bis[144:288,:],axis=0)/144
            isyn_DG_i2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_DG_i_bis[144:288,:],axis=0)/144
            isyn_CA3_i2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA3_i_bis[144:288,:],axis=0)/144
            isyn_CA1_i2_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=sum(all_isyn_CA1_i_bis[144:288,:],axis=0)/144
    
    #        isyn_principal_1=sum(all_isyn[:144,:],axis=0)/144
    #        isyn_principal_2=sum(all_isyn[144:288,:],axis=0)/144
            isyn_principal_2_bis=(isyn_EC_e2_bis+isyn_DG_e2_bis+isyn_CA3_e2_bis+isyn_CA1_e2_bis+isyn_EC_i2_bis+isyn_DG_i2_bis+isyn_CA3_i2_bis+isyn_CA1_i2_bis)[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]
            isyn_principal_1_bis=(isyn_EC_e1_bis+isyn_DG_e1_bis+isyn_CA3_e1_bis+isyn_CA1_e1_bis+isyn_EC_i1_bis+isyn_DG_i1_bis+isyn_CA3_i1_bis+isyn_CA1_i1_bis)[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]
            isyn_principal_bis=isyn_principal_2_bis-isyn_principal_1_bis
    #        print(max(isyn_principal_1),max(isyn_principal_2),max(isyn_principal))
    #        print(min(isyn_principal_1),min(isyn_principal_2),min(isyn_principal))
            
            signal_principal_bis[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=isyn_principal_bis


#        signal_principal_pc[test_ind*int(single_runtime/pas_de_temps):(test_ind+1)*int(single_runtime/pas_de_temps)]=all_isyn_pc
        for monitor in make_flat(all_syn_intra_E_monitors):
            if monitor!=None:  
                myNetwork.remove(monitor)
        for monitor in make_flat(all_syn_intra_I_monitors):
            if monitor!=None:  
                myNetwork.remove(monitor)
        for monitor in make_flat(all_syn_inter_monitors):
            if monitor!=None: 
                myNetwork.remove(monitor)
        for monitor in make_flat(all_rate_E_monitors):
            if monitor!=None:  
                myNetwork.remove(monitor)
        for monitor in make_flat(all_rate_I_monitors):
            if monitor!=None:  
                myNetwork.remove(monitor)
        if plot_raster :
            myNetwork.remove(all_spike_E_monitors)
            myNetwork.remove(all_spike_I_monitors)
#        print(myNetwork.objects)

    print('This simulation has been run completely')
    fin=time.time()
    print('Simulation time : '+str((fin-debut)/60)+' minutes')
    print('Saving the results')
    
    def post_process(signal):
        N=3
        fs=1/pas_de_temps*second
        nyq = 0.5 * fs
        low=0.15 / nyq
        high = 480 / nyq
        #high2=33000 / nyq
        b, a = scipy.signal.butter(N, high, btype='low')
        res_filt=scipy.signal.filtfilt(b,a,signal)  
        b, a = scipy.signal.butter(N, low, btype='high')
        res_filt=scipy.signal.filtfilt(b,a,res_filt) 
        #décimation pour avoir un sampling rate de 1024Hz
        step=int(1/1024/pas_de_temps*second)
        res_1024=res_filt[::step]
        return res_1024
    
    res_1024=post_process(signal_principal)
    lfp_EC_e1=post_process(isyn_EC_e1)
    lfp_EC_i1=post_process(isyn_EC_i1)
    lfp_DG_e1=post_process(isyn_DG_e1)
    lfp_DG_i1=post_process(isyn_DG_i1)    
    lfp_CA3_e1=post_process(isyn_CA3_e1)
    lfp_CA3_i1=post_process(isyn_CA3_i1)    
    lfp_CA1_e1=post_process(isyn_CA1_e1)
    lfp_CA1_i1=post_process(isyn_CA1_i1)    
    
    lfp_EC_e2=post_process(isyn_EC_e2)
    lfp_EC_i2=post_process(isyn_EC_i2)
    lfp_DG_e2=post_process(isyn_DG_e2)
    lfp_DG_i2=post_process(isyn_DG_i2)    
    lfp_CA3_e2=post_process(isyn_CA3_e2)
    lfp_CA3_i2=post_process(isyn_CA3_i2)    
    lfp_CA1_e2=post_process(isyn_CA1_e2)
    lfp_CA1_i2=post_process(isyn_CA1_i2)    
    

    if plot_raster :
        zones=['EC', 'DG', 'CA3', 'CA1']
        figure()
        for i in range(4):
#            print(len(all_rasters_t_exc[i]),len(all_rasters_t_inh[i]))
            for j in range(len(all_rasters_t_exc[i])):
                subplot(4,types[0]+types[1],j+1+(types[0]+types[1])*i)
                title('raster '+zones[i]+' exc '+str(j))
                for ind in range(len(all_rasters_t_exc[i][j])):
                    plot(all_rasters_t_exc[i][j][ind]/msecond, all_rasters_i_exc[i][j][ind], '.r')
                xlim(0,runtime/msecond)
                ylim(0,all_N[i+4*j])
                xlabel('Time (ms)')
                ylabel('Neuron index')
            for j in range(len(all_rasters_t_inh[i])):
                subplot(4,types[0]+types[1],j+1+types[0]+(types[0]+types[1])*i)
                title('raster '+zones[i]+' inh '+str(j))
                for ind in range(len(all_rasters_t_inh[i][j])):
                    plot(all_rasters_t_inh[i][j][ind]/msecond, all_rasters_i_inh[i][j][ind], '.r') 
                xlim(0,runtime/msecond)
                ylim(0,all_N[4*types[0]+i+4*j])
                xlabel('Time (ms)')
                ylabel('Neuron index')
        tight_layout()
    try :
        analyse(res_1024,params)
    except :
        pass

    ver='X'
    params='xxx'
    texte=str(params)
    simu_hipp=path+'/LFP.txt'
    ecriture(simu_hipp,res_1024,0*second,runtime)
    
    ecriture(path+'/LFP_EC_e1.txt',lfp_EC_e1,0*second,runtime)
    ecriture(path+'/LFP_DG_e1.txt',lfp_DG_e1,0*second,runtime)
    ecriture(path+'/LFP_CA3_e1.txt',lfp_CA3_e1,0*second,runtime)
    ecriture(path+'/LFP_CA1_e1.txt',lfp_CA1_e1,0*second,runtime)
    ecriture(path+'/LFP_EC_i1.txt',lfp_EC_i1,0*second,runtime)
    ecriture(path+'/LFP_DG_i1.txt',lfp_DG_i1,0*second,runtime)
    ecriture(path+'/LFP_CA3_i1.txt',lfp_CA3_i1,0*second,runtime)
    ecriture(path+'/LFP_CA1_i1.txt',lfp_CA1_i1,0*second,runtime)
    
    ecriture(path+'/LFP_EC_e2.txt',lfp_EC_e2,0*second,runtime)
    ecriture(path+'/LFP_DG_e2.txt',lfp_DG_e2,0*second,runtime)
    ecriture(path+'/LFP_CA3_e2.txt',lfp_CA3_e2,0*second,runtime)
    ecriture(path+'/LFP_CA1_e2.txt',lfp_CA1_e2,0*second,runtime)
    ecriture(path+'/LFP_EC_i2.txt',lfp_EC_i2,0*second,runtime)
    ecriture(path+'/LFP_DG_i2.txt',lfp_DG_i2,0*second,runtime)
    ecriture(path+'/LFP_CA3_i2.txt',lfp_CA3_i2,0*second,runtime)
    ecriture(path+'/LFP_CA1_i2.txt',lfp_CA1_i2,0*second,runtime)
            
#    print(all_FR_exc)
    save_FR(types,all_FR_exc,all_FR_inh,path,save_all_FR)
    
    if save_sim_raster:
        save_raster(types,all_rasters_i_exc,all_rasters_i_inh,all_rasters_t_exc,all_rasters_t_inh,path)
     
#    figure()
#    plot(all_FR_exc[0][0],label='EC')
#    plot(all_FR_exc[1][0],label='DG')
#    plot(all_FR_exc[2][0],label='CA3')
#    plot(all_FR_exc[3][0],label='CA1')
#    legend()
    
    if bis:
        res_bis=post_process(signal_principal_bis)
        M=max((max(res_bis),max(res_1024)))
        
        f1, spec1 = signal.periodogram(res_1024, 1024*Hz,'flattop',scaling='spectrum')
        f2, spec2 = signal.periodogram(res_bis, 1024*Hz,'flattop',scaling='spectrum')
        Ms=max((max(spec1),max(spec2)))
        
        figure()
        subplot(221)
        plot(array(res_1024)/M)
        xlabel('Time (ms)')
        ylabel('Normalized LFP (a.u.)')
        subplot(223)
        plot(array(res_bis)/M)
        xlabel('Time (ms)')
        ylabel('Normalized LFP (a.u.)')
        subplot(222)
        loglog(f1,spec1/Ms)
        xlabel('Frequency (Hz)')
        ylabel('Normalized spectrum')
        subplot(224)
        loglog(f2,spec2/Ms)
        xlabel('Frequency (Hz)')
        ylabel('Normalized spectrum')
        print(corrcoef(res_1024,res_bis))
        
    
    return res_1024, all_FR_exc,all_FR_inh
