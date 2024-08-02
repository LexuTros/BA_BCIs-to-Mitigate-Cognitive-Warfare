#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from brian2 import *

from model_files.global_vars_and_eqs import *
from model_files.annex_functions import *


def preparation(input_type,inputs1,types,all_pos,dir_hipp,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,co,co2,tau_Cl):
#    print(all_g_max_i,all_g_max_e)
    taille_inh_normale=14e3 * umetre ** 2
    taille_inh_2=0.5*taille_inh_normale
    
    taille_exc_normale=29e3 * umetre ** 2
    taille_exc_2=0.5*taille_exc_normale
    
    if types[0]==1 and types[1]==1:
        EC_e,EC_e_end,EC_e_inh,EC_i,EC_i_end,EC_i_inh=all_pos[0]
        DG_e,DG_e_end,DG_e_inh,DG_i,DG_i_end,DG_i_inh=all_pos[1]
        CA3_e,CA3_e_end,CA3_e_inh,CA3_i,CA3_i_end,CA3_i_inh=all_pos[2]
        CA1_e,CA1_e_end,CA1_e_inh,CA1_i,CA1_i_end,CA1_i_inh=all_pos[3]
        dir_EC,dir_DG,dir_CA3,dir_CA1=dir_hipp
  
    elif types[0]==2 and types[1]==1:
        EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i,EC_i_end,EC_i_inh=all_pos[0]
        DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i,DG_i_end,DG_i_inh=all_pos[1]
        CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i,CA3_i_end,CA3_i_inh=all_pos[2]
        CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i,CA1_i_end,CA1_i_inh=all_pos[3]
        dir_EC1,dir_EC2,dir_DG1,dir_DG2,dir_CA31,dir_CA32,dir_CA11,dir_CA12=dir_hipp
        
    elif types[0]==1 and types[1]==2:
        EC_e,EC_e_end,EC_e_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh=all_pos[0]
        DG_e,DG_e_end,DG_e_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh=all_pos[1]
        CA3_e,CA3_e_end,CA3_e_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh=all_pos[2]
        CA1_e,CA1_e_end,CA1_e_inh,CA1_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh=all_pos[3]
        dir_EC,dir_DG,dir_CA3,dir_CA1=dir_hipp
        
    else :
        EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh=all_pos[0]
        DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh=all_pos[1]
        CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh=all_pos[2]
        CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh=all_pos[3]
        dir_EC1,dir_EC2,dir_DG1,dir_DG2,dir_CA31,dir_CA32,dir_CA11,dir_CA12=dir_hipp
    
    pas_de_temps=defaultclock.dt
    
    sigma= 0.3*siemens/meter
    scale=150*umetre #75 umetre
    scale_str='150*umetre'
        
 
#    integ_method='rk4'
    integ_method='exponential_euler'
    #######Définition des groupes de neurones#################
    
    
    def create_group_py(zone_name,coord,Dcoord,Icoord,direction,taille):
        if len(coord)==0:
            return
        N_exc=len(coord[:,0])
        G_exc_coords=coord
        G_exc_Dcoords=Dcoord
        G_exc_Icoords=Icoord
        G_exc_dir=direction
        G_exc=NeuronGroup(N_exc,py_eqs,threshold='v>V_th',reset=reset_eqs,refractory=3*ms,method=integ_method)
        G_exc.v = '-60*mvolt-rand()*10*mvolt'
        G_exc.glu = 1
        G_exc.x_soma=G_exc_coords[:,0]*scale
        G_exc.y_soma=G_exc_coords[:,1]*scale
        G_exc.z_soma=G_exc_coords[:,2]*scale
        G_exc.x_dendrite=G_exc_Dcoords[:,0]*scale
        G_exc.y_dendrite=G_exc_Dcoords[:,1]*scale
        G_exc.z_dendrite=G_exc_Dcoords[:,2]*scale
        G_exc.x_inh=G_exc_Icoords[:,0]*scale
        G_exc.y_inh=G_exc_Icoords[:,1]*scale
        G_exc.z_inh=G_exc_Icoords[:,2]*scale
        G_exc.dir_x =G_exc_dir[:,0]
        G_exc.dir_y =G_exc_dir[:,1]
        G_exc.dir_z =G_exc_dir[:,2]
        G_exc.taille=taille
        return G_exc
       
        
    def create_group_pyCAN(zone_name,coord,Dcoord,Icoord,direction,taille):
        if len(coord)==0:
            return
        N_exc=len(coord[:,0])
        G_exc_coords=coord
        G_exc_Dcoords=Dcoord
        G_exc_Icoords=Icoord
        G_exc_dir=direction
        G_exc=NeuronGroup(N_exc,py_CAN_eqs,threshold='v>V_th',reset=reset_eqs,refractory=3*ms,method=integ_method)
        G_exc.v = '-60*mvolt-rand()*10*mvolt'
        G_exc.glu = 1
        G_exc.x_soma=G_exc_coords[:,0]*scale
        G_exc.y_soma=G_exc_coords[:,1]*scale
        G_exc.z_soma=G_exc_coords[:,2]*scale
        G_exc.x_dendrite=G_exc_Dcoords[:,0]*scale
        G_exc.y_dendrite=G_exc_Dcoords[:,1]*scale
        G_exc.z_dendrite=G_exc_Dcoords[:,2]*scale
        G_exc.x_inh=G_exc_Icoords[:,0]*scale
        G_exc.y_inh=G_exc_Icoords[:,1]*scale
        G_exc.z_inh=G_exc_Icoords[:,2]*scale
        G_exc.dir_x =G_exc_dir[:,0]
        G_exc.dir_y =G_exc_dir[:,1]
        G_exc.dir_z =G_exc_dir[:,2]
        G_exc.taille=taille
        return G_exc
        
    def create_group_pystim(zone_name,coord,Dcoord,Icoord,direction,taille):
        if len(coord)==0:
            return
        N_exc=len(coord[:,0])
        G_exc_coords=coord
        G_exc_Dcoords=Dcoord
        G_exc_Icoords=Icoord
        G_exc_dir=direction
        G_exc=NeuronGroup(N_exc,py_stim_eqs,threshold='v>V_th',reset=reset_eqs,refractory=3*ms,method=integ_method)
        G_exc.v = '-60*mvolt-rand()*10*mvolt'
        G_exc.glu = 1
        G_exc.x_soma=G_exc_coords[:,0]*scale
        G_exc.y_soma=G_exc_coords[:,1]*scale
        G_exc.z_soma=G_exc_coords[:,2]*scale
        G_exc.x_dendrite=G_exc_Dcoords[:,0]*scale
        G_exc.y_dendrite=G_exc_Dcoords[:,1]*scale
        G_exc.z_dendrite=G_exc_Dcoords[:,2]*scale
        G_exc.x_inh=G_exc_Icoords[:,0]*scale
        G_exc.y_inh=G_exc_Icoords[:,1]*scale
        G_exc.z_inh=G_exc_Icoords[:,2]*scale
        G_exc.dir_x =G_exc_dir[:,0]
        G_exc.dir_y =G_exc_dir[:,1]
        G_exc.dir_z =G_exc_dir[:,2]
        G_exc.taille=taille
        return G_exc
        
    def create_group_inh(zone_name,coord,taille):
        if len(coord)==0:
            return
        G_inh_coords=coord
        Ninh=len(coord[:,0])
        G_inh=NeuronGroup(Ninh,inh_eqs,threshold='v>V_th',refractory=3*ms,method=integ_method)
        G_inh.v = -60*mvolt-rand()*10*mvolt
        G_inh.x_soma=G_inh_coords[:,0]*scale
        G_inh.y_soma=G_inh_coords[:,1]*scale
        G_inh.z_soma=G_inh_coords[:,2]*scale
        G_inh.taille=taille
        return G_inh
        
        
    def create_group_py_curr(zone_name,coord,Dcoord,Icoord,direction,taille):
        if len(coord)==0:
            return
        N_exc=len(coord[:,0])
        G_exc_coords=coord
        G_exc_Dcoords=Dcoord
        G_exc_Icoords=Icoord
        G_exc_dir=direction
        G_exc=NeuronGroup(N_exc,py_eqs_curr,threshold='v>V_th',reset=reset_eqs,refractory=3*ms,method=integ_method)
        G_exc.v = '-60*mvolt-rand()*10*mvolt'
        G_exc.glu = 1
        G_exc.x_soma=G_exc_coords[:,0]*scale
        G_exc.y_soma=G_exc_coords[:,1]*scale
        G_exc.z_soma=G_exc_coords[:,2]*scale
        G_exc.x_dendrite=G_exc_Dcoords[:,0]*scale
        G_exc.y_dendrite=G_exc_Dcoords[:,1]*scale
        G_exc.z_dendrite=G_exc_Dcoords[:,2]*scale
        G_exc.x_inh=G_exc_Icoords[:,0]*scale
        G_exc.y_inh=G_exc_Icoords[:,1]*scale
        G_exc.z_inh=G_exc_Icoords[:,2]*scale
        G_exc.dir_x =G_exc_dir[:,0]
        G_exc.dir_y =G_exc_dir[:,1]
        G_exc.dir_z =G_exc_dir[:,2]
        G_exc.taille=taille
        return G_exc
       
        
    def create_group_pyCAN_curr(zone_name,coord,Dcoord,Icoord,direction,taille):
        if len(coord)==0:
            return
        N_exc=len(coord[:,0])
        G_exc_coords=coord
        G_exc_Dcoords=Dcoord
        G_exc_Icoords=Icoord
        G_exc_dir=direction
        G_exc=NeuronGroup(N_exc,py_CAN_eqs_curr,threshold='v>V_th',reset=reset_eqs,refractory=3*ms,method=integ_method)
        G_exc.v = '-60*mvolt-rand()*10*mvolt'
        G_exc.glu = 1
        G_exc.x_soma=G_exc_coords[:,0]*scale
        G_exc.y_soma=G_exc_coords[:,1]*scale
        G_exc.z_soma=G_exc_coords[:,2]*scale
        G_exc.x_dendrite=G_exc_Dcoords[:,0]*scale
        G_exc.y_dendrite=G_exc_Dcoords[:,1]*scale
        G_exc.z_dendrite=G_exc_Dcoords[:,2]*scale
        G_exc.x_inh=G_exc_Icoords[:,0]*scale
        G_exc.y_inh=G_exc_Icoords[:,1]*scale
        G_exc.z_inh=G_exc_Icoords[:,2]*scale
        G_exc.dir_x =G_exc_dir[:,0]
        G_exc.dir_y =G_exc_dir[:,1]
        G_exc.dir_z =G_exc_dir[:,2]
        G_exc.taille=taille
        return G_exc
        
    def create_group_pystim_curr(zone_name,coord,Dcoord,Icoord,direction,taille):
        if len(coord)==0:
            return
        N_exc=len(coord[:,0])
        G_exc_coords=coord
        G_exc_Dcoords=Dcoord
        G_exc_Icoords=Icoord
        G_exc_dir=direction
        G_exc=NeuronGroup(N_exc,py_stim_eqs_curr,threshold='v>V_th',reset=reset_eqs,refractory=3*ms,method=integ_method)
        G_exc.v = '-60*mvolt-rand()*10*mvolt'
        G_exc.glu = 1
        G_exc.x_soma=G_exc_coords[:,0]*scale
        G_exc.y_soma=G_exc_coords[:,1]*scale
        G_exc.z_soma=G_exc_coords[:,2]*scale
        G_exc.x_dendrite=G_exc_Dcoords[:,0]*scale
        G_exc.y_dendrite=G_exc_Dcoords[:,1]*scale
        G_exc.z_dendrite=G_exc_Dcoords[:,2]*scale
        G_exc.x_inh=G_exc_Icoords[:,0]*scale
        G_exc.y_inh=G_exc_Icoords[:,1]*scale
        G_exc.z_inh=G_exc_Icoords[:,2]*scale
        G_exc.dir_x =G_exc_dir[:,0]
        G_exc.dir_y =G_exc_dir[:,1]
        G_exc.dir_z =G_exc_dir[:,2]
        G_exc.taille=taille
        return G_exc
        
    def create_group_inh_curr(zone_name,coord,taille):
        if len(coord)==0:
            return
        G_inh_coords=coord
        Ninh=len(coord[:,0])
        G_inh=NeuronGroup(Ninh,inh_eqs_curr,threshold='v>V_th',refractory=3*ms,method=integ_method)
        G_inh.v = -60*mvolt-rand()*10*mvolt
        G_inh.x_soma=G_inh_coords[:,0]*scale
        G_inh.y_soma=G_inh_coords[:,1]*scale
        G_inh.z_soma=G_inh_coords[:,2]*scale
        G_inh.taille=taille
        return G_inh
        
    print('Creating the neurons')    
    
    if types[0]==1 and types[1]==1:
        if input_type=='courant_sin' or input_type=='courant_creneau' or input_type=='courant_blanc' or input_type=='square':
            EC_py=create_group_pyCAN_curr('EC',EC_e,EC_e_end,EC_e_inh,dir_EC,taille_exc_normale)
            EC_inh=create_group_inh_curr('EC',EC_i,taille_inh_normale)
        else:
            EC_py=create_group_pyCAN('EC',EC_e,EC_e_end,EC_e_inh,dir_EC,taille_exc_normale)
            EC_inh=create_group_inh('EC',EC_i,taille_inh_normale)
        DG_py=create_group_py('DG',DG_e,DG_e_end,DG_e_inh,dir_DG,taille_exc_normale)
        DG_inh=create_group_inh('DG',DG_i,taille_inh_normale)
        CA3_py=create_group_pyCAN('CA3',CA3_e,CA3_e_end,CA3_e_inh,dir_CA3,taille_exc_normale)
        CA3_inh=create_group_inh('CA3',CA3_i,taille_inh_normale)
        CA1_py=create_group_pyCAN('CA1',CA1_e,CA1_e_end,CA1_e_inh,dir_CA1,taille_exc_normale)
        CA1_inh=create_group_inh('CA1',CA1_i,taille_inh_normale)
        all_EC_py,all_EC_inh=[EC_py],[EC_inh]
        all_DG_py,all_DG_inh=[DG_py],[DG_inh]
        all_CA3_py,all_CA3_inh=[CA3_py],[CA3_inh]
        all_CA1_py,all_CA1_inh=[CA1_py],[CA1_inh]  
  
    elif types[0]==2 and types[1]==1:
        if input_type=='courant_sin' or input_type=='courant_creneau' or input_type=='square':
            EC_py1=create_group_pyCAN_curr('EC',EC_e1,EC_e1_end,EC_e1_inh,dir_EC1,taille_exc_normale)
            EC_py2=create_group_pyCAN_curr('EC',EC_e2,EC_e2_end,EC_e2_inh,dir_EC2,taille_exc_2)
            EC_inh=create_group_inh_curr('EC',EC_i,taille_inh_normale)
        else:
            EC_py1=create_group_pyCAN('EC',EC_e1,EC_e1_end,EC_e1_inh,dir_EC1,taille_exc_normale)
            EC_py2=create_group_pyCAN('EC',EC_e2,EC_e2_end,EC_e2_inh,dir_EC2,taille_exc_2)
            EC_inh=create_group_inh('EC',EC_i,taille_inh_normale)
        DG_py1=create_group_py('DG',DG_e1,DG_e1_end,DG_e1_inh,dir_DG1,taille_exc_normale)
        DG_py2=create_group_py('DG',DG_e2,DG_e2_end,DG_e2_inh,dir_DG2,taille_exc_2)
        DG_inh=create_group_inh('DG',DG_i,taille_inh_normale)
        CA3_py1=create_group_pyCAN('CA3',CA3_e1,CA3_e1_end,CA3_e1_inh,dir_CA31,taille_exc_normale)
        CA3_py2=create_group_pyCAN('CA3',CA3_e2,CA3_e2_end,CA3_e2_inh,dir_CA32,taille_exc_2)
        CA3_inh=create_group_inh('CA3',CA3_i,taille_inh_normale)
        CA1_py1=create_group_pyCAN('CA1',CA1_e1,CA1_e1_end,CA1_e1_inh,dir_CA11,taille_exc_normale)
        CA1_py2=create_group_pyCAN('CA1',CA1_e2,CA1_e2_end,CA1_e2_inh,dir_CA12,taille_exc_2)
        CA1_inh=create_group_inh('CA1',CA1_i,taille_inh_normale)
        all_EC_py,all_EC_inh=[EC_py1,EC_py2],[EC_inh]
        all_DG_py,all_DG_inh=[DG_py1,DG_py2],[DG_inh]
        all_CA3_py,all_CA3_inh=[CA3_py1,CA3_py2],[CA3_inh]
        all_CA1_py,all_CA1_inh=[CA1_py1,CA1_py2],[CA1_inh]
        
    elif types[0]==1 and types[1]==2:
        if input_type=='courant_sin' or input_type=='courant_creneau'  or input_type=='square':
            EC_py=create_group_pyCAN_curr('EC',EC_e,EC_e_end,EC_e_inh,dir_EC,taille_exc_normale)
            EC_inh1=create_group_inh_curr('EC',EC_i1,taille_inh_normale)
            EC_inh2=create_group_inh_curr('EC',EC_i2,taille_inh_2)
        else:
            EC_py=create_group_pyCAN('EC',EC_e,EC_e_end,EC_e_inh,dir_EC,taille_exc_normale)
            EC_inh1=create_group_inh('EC',EC_i1,taille_inh_normale)
            EC_inh2=create_group_inh('EC',EC_i2,taille_inh_2)
        DG_py=create_group_py('DG',DG_e,DG_e_end,DG_e_inh,dir_DG,taille_exc_normale)
        DG_inh1=create_group_inh('DG',DG_i1,taille_inh_normale)
        DG_inh2=create_group_inh('DG',DG_i2,taille_inh_2)
        CA3_py=create_group_pyCAN('CA3',CA3_e,CA3_e_end,CA3_e_inh,dir_CA3,taille_exc_normale)
        CA3_inh1=create_group_inh('CA3',CA3_i1,taille_inh_normale)
        CA3_inh2=create_group_inh('CA3',CA3_i2,taille_inh_2)
        CA1_py=create_group_pyCAN('CA1',CA1_e,CA1_e_end,CA1_e_inh,dir_CA1,taille_exc_normale)
        CA1_inh1=create_group_inh('CA1',CA1_i1,taille_inh_normale)
        CA1_inh2=create_group_inh('CA1',CA1_i2,taille_inh_2)
        all_EC_py,all_EC_inh=[EC_py],[EC_inh1,EC_inh2]
        all_DG_py,all_DG_inh=[DG_py],[DG_inh1,DG_inh2]
        all_CA3_py,all_CA3_inh=[CA3_py],[CA3_inh1,CA3_inh2]
        all_CA1_py,all_CA1_inh=[CA1_py],[CA1_inh1,CA1_inh2]
        
    else :
        if input_type=='courant_sin' or input_type=='courant_creneau' or input_type=='square':
            EC_py1=create_group_pyCAN_curr('EC',EC_e1,EC_e1_end,EC_e1_inh,dir_EC1,taille_exc_normale)
            EC_py2=create_group_pyCAN_curr('EC',EC_e2,EC_e2_end,EC_e2_inh,dir_EC2,taille_exc_2)
            EC_inh1=create_group_inh_curr('EC',EC_i1,taille_inh_normale)
            EC_inh2=create_group_inh_curr('EC',EC_i2,taille_inh_2)
        else:
            EC_py1=create_group_pyCAN('EC',EC_e1,EC_e1_end,EC_e1_inh,dir_EC1,taille_exc_normale)
            EC_py2=create_group_pyCAN('EC',EC_e2,EC_e2_end,EC_e2_inh,dir_EC2,taille_exc_2)
            EC_inh=create_group_inh('EC',EC_i,taille_inh_normale)
            EC_inh=create_group_inh_curr('EC',EC_i,taille_inh_normale)
        DG_py1=create_group_py('DG',DG_e1,DG_e1_end,DG_e1_inh,dir_DG1,taille_exc_normale)
        DG_py2=create_group_py('DG',DG_e2,DG_e2_end,DG_e2_inh,dir_DG2,taille_exc_2)
        DG_inh1=create_group_inh('DG',DG_i1,taille_inh_normale)
        DG_inh2=create_group_inh('DG',DG_i2,taille_inh_2)
        CA3_py1=create_group_pyCAN('CA3',CA3_e1,CA3_e1_end,CA3_e1_inh,dir_CA31,taille_exc_normale)
        CA3_py2=create_group_pyCAN('CA3',CA3_e2,CA3_e2_end,CA3_e2_inh,dir_CA32,taille_exc_2)
        CA3_inh1=create_group_inh('CA3',CA3_i1,taille_inh_normale)
        CA3_inh2=create_group_inh('CA3',CA3_i2,taille_inh_2)
        CA1_py1=create_group_pyCAN('CA1',CA1_e1,CA1_e1_end,CA1_e1_inh,dir_CA11,taille_exc_normale)
        CA1_py2=create_group_pyCAN('CA1',CA1_e2,CA1_e2_end,CA1_e2_inh,dir_CA12,taille_exc_2)
        CA1_inh1=create_group_inh('CA1',CA1_i1,taille_inh_normale)
        CA1_inh2=create_group_inh('CA1',CA1_i2,taille_inh_2)
        all_EC_py,all_EC_inh=[EC_py1,EC_py2],[EC_inh1,EC_inh2]
        all_DG_py,all_DG_inh=[DG_py1,DG_py2],[DG_inh1,DG_inh2]
        all_CA3_py,all_CA3_inh=[CA3_py1,CA3_py2],[CA3_inh1,CA3_inh2]
        all_CA1_py,all_CA1_inh=[CA1_py1,CA1_py2],[CA1_inh1,CA1_inh2]
    
    all_neuron_groups=[[all_EC_py,all_EC_inh],[all_DG_py,all_DG_inh],[all_CA3_py,all_CA3_inh],[all_CA1_py,all_CA1_inh]]
    print('Adding synapses')
    ####### Définition des connexions synaptiques au sein de chaque zone #################
        
    def create_syn(all_G_py,all_G_inh,all_p,sigE,sigI, all_var,co_type,all_g_max_i,all_g_max_e):
        Npy=len(all_G_py)
        Ninh=len(all_G_inh)
        all_syn=[[0]*(Npy+Ninh) for i in range(Npy+Ninh)]
#        print(all_var)
        if co_type=='normal':
#            print(co_type)
            formuleE='*exp(-((x_soma_pre-x_soma_post)**2+(y_soma_pre-y_soma_post)**2+(z_soma_pre-z_soma_post)**2)/(2*'+sigE+'**2))'
            formuleI='*exp(-((x_soma_pre-x_soma_post)**2+(y_soma_pre-y_soma_post)**2+(z_soma_pre-z_soma_post)**2)/(2*'+sigI+'**2))'
        else :
            formuleE=''
            formuleI=''
        for npy in range(Npy):
            if all_p[npy][npy]!='0' and all_G_py[npy]:
#                print(str(all_g_max_e[npy]),str(all_var[npy]))
#                print(str(all_var[npy])+"*"+str(all_g_max_e[npy]/siemens)+"*siemens")
#                print(all_var,all_g_max_e)
#                print(str(all_var[npy])+"*"+str(all_g_max_e[npy]))
                syn_EE=Synapses(all_G_py[npy],all_G_py[npy],on_pre="he_post+="+str(all_var[npy])+"*"+str(all_g_max_e[npy]/siemens)+"*siemens*glu_pre")
                syn_EE.connect(condition='i!=j',p=str(all_p[npy][npy])+formuleE)
                all_syn[npy][npy]=syn_EE
            for ninh in range(Ninh):
                if all_p[npy][Npy+ninh]!='0' and all_G_py[npy] and all_G_inh[ninh]:
#                    print(str(all_var[npy])+"*"+str(all_g_max_e[npy]/siemens)+"*siemens")
                    syn_EI=Synapses(all_G_py[npy],all_G_inh[ninh],on_pre="he_post+="+str(all_var[npy])+"*"+str(all_g_max_e[npy]/siemens)+"*siemens*glu_pre")
                    syn_EI.connect(condition='i!=j',p=str(all_p[npy][Npy+ninh])+formuleE)
                    all_syn[npy][Npy+ninh]=syn_EI
                if all_p[Npy+ninh][npy]!='0' and all_G_py[npy] and all_G_inh[ninh]:
#                    print(str(all_g_max_i[ninh]),str(all_var[Npy+ninh]))
#                    print(str(all_var[Npy+ninh])+"*"+str(all_g_max_i[ninh]/siemens)+"*siemens")
                    syn_IE=Synapses(all_G_inh[ninh],all_G_py[npy],on_pre="hi_post+="+str(all_var[Npy+ninh])+"*"+str(all_g_max_i[ninh]/siemens)+"*siemens")
                    syn_IE.connect(condition='i!=j',p=str(all_p[Npy+ninh][npy])+formuleI)
                    all_syn[Npy+ninh][npy]=syn_IE
        for ninh in range(Ninh):
            if all_p[Npy+ninh][Npy+ninh]!='0' and all_G_inh[ninh]: 
#                print(str(all_var[Npy+ninh])+"*"+str(all_g_max_i[ninh]/siemens)+"*siemens")
                syn_II=Synapses(all_G_inh[ninh],all_G_inh[ninh],on_pre="hi_post+="+str(all_var[Npy+ninh])+"*"+str(all_g_max_i[ninh]/siemens)+"*siemens")
                syn_II.connect(condition='i!=j',p=str(all_p[Npy+ninh][Npy+ninh])+formuleI)
                all_syn[Npy+ninh][Npy+ninh]=syn_II
        return all_syn


    sigEstr, sigIstr='(2500*umetre)', '(350*umetre)'
    sigE, sigI='(2500*umetre)', '(350*umetre)'  #350  
    
    all_syn_EC=create_syn(all_EC_py,all_EC_inh,all_p_intra[0],sigEstr,sigIstr,all_gains[0],co2,all_g_max_i,all_g_max_e)
    all_syn_DG=create_syn(all_DG_py,all_DG_inh,all_p_intra[1],sigEstr,sigIstr,all_gains[1],co2,all_g_max_i,all_g_max_e)
    all_syn_CA3=create_syn(all_CA3_py,all_CA3_inh,all_p_intra[2],sigEstr,sigIstr,all_gains[2],co2,all_g_max_i,all_g_max_e)
    all_syn_CA1=create_syn(all_CA1_py,all_CA1_inh,all_p_intra[3],sigEstr,sigIstr,all_gains[3],co2,all_g_max_i,all_g_max_e)
                             
    all_syn_intra=[all_syn_EC,all_syn_DG,all_syn_CA3,all_syn_CA1]
    
#    print('connexions intra')
#    print('EC')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_EC])
#    print('DG')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_DG])
#    print('CA3')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_CA3])
#    print('CA1')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_CA1])
#    print([[(syn.source, syn.target) for syn in liste_syn] for liste_syn in all_syn_EC])
#    print([[(syn.source, syn.target) for syn in liste_syn] for liste_syn in all_syn_DG])
#    print([[(syn.source, syn.target) for syn in liste_syn] for liste_syn in all_syn_CA3])
#    print([[(syn.source, syn.target) for syn in liste_syn] for liste_syn in all_syn_CA1])
    ## Définition des connections synaptiques entre chaque zone ##
    
    def connect_2zones(all_G_py_depart,all_G_py_arrivee,all_G_inh_arrivee,sig_E,all_p,all_var,co_type,all_g_max_e):
        if co_type=='normal':
#            print(co_type)
            formule='*exp(-((z_soma_pre-z_soma_post)**2)/(2*'+sig_E+'**2))'
        else :
            formule=''
        Npy1=len(all_G_py_depart)
        Npy2=len(all_G_py_arrivee)
        Ninh=len(all_G_inh_arrivee)
        all_syn=[[0]*(Npy2+Ninh) for i in range(Npy1)]
#        print(all_var)
        
        for n1 in range(Npy1):
            Gpy1=all_G_py_depart[n1]
            if Gpy1:
                for n2 in range(Npy2):
                    Gpy2=all_G_py_arrivee[n2]
                    if Gpy2:
#                        print(str(all_var[n1])+"*"+str(all_g_max_e[n1]/siemens)+"*siemens")
                        syn_E = Synapses(Gpy1,Gpy2,on_pre="he_ext_post+="+str(all_var[n1])+"*"+str(all_g_max_e[n1]/siemens)+"*siemens*glu_pre")
                        syn_E.connect(p=str(all_p[n1][n2])+formule)
                        all_syn[n1][n2]=syn_E
                for n2 in range(Ninh):
                    Ginh=all_G_inh_arrivee[n2]
                    if Ginh:
#                        print(str(all_var[n1])+"*"+str(all_g_max_e[n1]/siemens)+"*siemens")
                        syn_I = Synapses(Gpy1,Ginh,on_pre="he_ext_post+="+str(all_var[n1])+"*"+str(all_g_max_e[n1]/siemens)+"*siemens*glu_pre")
                        syn_I.connect(p=str(all_p[n1][Npy2+n2])+formule)
                        all_syn[n1][Npy2+n2]=syn_I
        return all_syn
    
    #Du cortex entorhinal vers le gyrus denté ##
    sig_E='(1000*umetre)'  

    all_syn_EC_DG=connect_2zones(all_EC_py,all_DG_py,all_DG_inh,sig_E,all_p_inter[0][1],all_gains[0],co,all_g_max_e)
    all_syn_EC_CA3=connect_2zones(all_EC_py,all_CA3_py,all_CA3_inh,sig_E,all_p_inter[0][2],all_gains[0],co,all_g_max_e)
    all_syn_EC_CA1=connect_2zones(all_EC_py,all_CA1_py,all_CA1_inh,sig_E,all_p_inter[0][3],all_gains[0],co,all_g_max_e)

    all_syn_DG_CA3=connect_2zones(all_DG_py,all_CA3_py,all_CA3_inh,sig_E,all_p_inter[1][2],all_gains[1],co,all_g_max_e)
    all_syn_DG_CA1=connect_2zones(all_DG_py,all_CA1_py,all_CA1_inh,sig_E,all_p_inter[1][3],all_gains[1],co,all_g_max_e)
    
    all_syn_CA3_CA1=connect_2zones(all_CA3_py,all_CA1_py,all_CA1_inh,sig_E,all_p_inter[2][3],all_gains[2],co,all_g_max_e)  
      
    all_syn_CA1_EC=connect_2zones(all_CA1_py,all_EC_py,all_EC_inh,sig_E,all_p_inter[3][0],all_gains[3],co,all_g_max_e)   

    all_syn_inter=[all_syn_EC_DG,all_syn_EC_CA3,all_syn_EC_CA1,all_syn_DG_CA3,all_syn_DG_CA1,all_syn_CA3_CA1,all_syn_CA1_EC]
    
#    print('Connexions inter')
#    print('EC DG')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_EC_DG])
#    print('EC CA3')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_EC_CA3])
#    print('EC CA1')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_EC_CA1])
#    print('DG CA3')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_DG_CA3])
#    print('DG CA1')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_DG_CA1])
#    print('CA3 CA1')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_CA3_CA1])
#    print('CA1 EC')
#    print([[len(syn.j) for syn in liste_syn] for liste_syn in all_syn_CA1_EC])
    

#    print('saving synaptic matrices')
#    CA1_EcI,CA1_IEc,CA1_II=all_syn_CA1[0][1],all_syn_CA1[1][0],all_syn_CA1[1][1]
#    CA3_EcI,CA3_IEc,CA3_EcEc=all_syn_CA3[0][1],all_syn_CA3[1][0],all_syn_CA3[0][0]
#    EC_EcI,EC_IEc=all_syn_EC[0][1],all_syn_EC[1][0]
#    DG_EI,DG_IE=all_syn_DG[0][1],all_syn_DG[1][0]
#    ECc_DG_E,ECc_DG_I=all_syn_EC_DG[0][0],all_syn_EC_DG[0][1]
#    ECc_CA3c_E,ECc_CA3_I=all_syn_EC_CA3[0][0],all_syn_EC_CA3[0][1]
#    ECc_CA1c_E,ECc_CA1_I=all_syn_EC_CA1[0][0],all_syn_EC_CA1[0][1]
#    DG_CA3c_E,DG_CA3_I=all_syn_DG_CA3[0][0],all_syn_DG_CA3[0][1]
#    CA3c_CA1c_E,CA3c_CA1_I=all_syn_CA3_CA1[0][0],all_syn_CA3_CA1[0][1]
#    CA1c_ECc_E,CA1c_EC_I=all_syn_CA1_EC[0][0],all_syn_CA1_EC[0][1]
#    save_syn(CA1_EcI,CA1_IEc,CA1_II,CA3_EcI,CA3_IEc,CA3_EcEc,EC_EcI,EC_IEc,DG_EI,DG_IE,ECc_DG_E,ECc_DG_I,ECc_CA3c_E,ECc_CA3_I,ECc_CA1c_E,ECc_CA1_I,DG_CA3c_E,DG_CA3_I,CA3c_CA1c_E,CA3c_CA1_I,CA1c_ECc_E,CA1c_EC_I)

    return all_neuron_groups,all_syn_intra,all_syn_inter

