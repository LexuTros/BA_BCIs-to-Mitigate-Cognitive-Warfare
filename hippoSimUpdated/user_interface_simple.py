#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:27:34 2019

@author: aussel
"""

from brian2 import *

import os
import datetime

from model_files.global_vars_and_eqs import *
from model_files.single_process import *
from model_files.annex_functions import *


os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_DYNAMIC'] = 'FALSE'

import time
from itertools import *

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import ntpath

BG='white'
myfont=('Helvetica',12)


interface=Tk()
interface.minsize(1000, 600)
interface.option_add("*Font", "courier")
interface.option_add("*Background", "white")


maxN=DoubleVar(interface,10000)
ptri=DoubleVar(interface,0.45)
pmono=DoubleVar(interface,0.2)
g_max_e=DoubleVar(interface,60)
g_max_i=DoubleVar(interface,600)

gains=DoubleVar(interface,3)
functional_co=StringVar()
functional_co.set('sleep')
gCAN=DoubleVar(interface,25)
CAN=StringVar()
CAN.set('sleep')

sclerosis=DoubleVar(interface,0)
sprouting=DoubleVar(interface,0)
tau_Cl=DoubleVar(interface,0.1)
Ek=DoubleVar(interface,-100)

input_type=StringVar()
A0=DoubleVar(interface,0)
A1=DoubleVar(interface,1)
f1=DoubleVar(interface,2.5)
duty=DoubleVar(interface,0.5)
dur=DoubleVar(interface,4.5)
in_fs=DoubleVar(interface,1024)
runtime=DoubleVar(interface,0.5)
plot_raster=StringVar()
save_figs=StringVar()
save_raster=StringVar()
save_neuron_pos=StringVar()
save_syn_mat=StringVar()
save_all_FR=StringVar()

in_file_1 = StringVar()
in_file_2 = StringVar()
in_file_3 = StringVar()


aborted=True


def start():
    global runtime,plot_raster,gCAN,maxN,A0,A1,dur,f1,duty,input_type,ptri,pmono,gains,g_max_i,g_max_e,save_figs,save_raster,save_neuron_pos,save_syn_mat,path,save_all_FR,tau_Cl,Ek,in_file_1,in_file_2,in_file_3,in_fs,aborted,functional_co,gCAN,CAN,sclerosis,sprouting
    
    if CAN.get()=='sleep': #no CAN
        gCAN=0.5*usiemens*cmeter**-2
    else :
        gCAN=gCAN.get()*usiemens*cmeter**-2
    
    all_N=[]
    all_p_inter=[]
    all_p_intra=[]
    all_g_max_e=[]
    all_g_max_i=[]
    all_gains=[]
    types=[1,1]
    
    in_file_1,in_file_2,in_file_3,in_fs=in_file_1.get(),in_file_2.get(),in_file_3.get(),in_fs.get()*Hz
        
    maxN=int(maxN.get())
    cell_loss=sclerosis.get()

    Ne1=maxN
    Ne2=maxN
    Ne3=maxN//10
    Ne4=maxN
    Ne1=maxN*(1-0.75*cell_loss)
    Ne2=maxN*(1-0.6*cell_loss)
    Ne3=maxN//10*(1-0.8*cell_loss)
    Ne4=maxN*(1-0.8*cell_loss)
    
    N1=[Ne1*(1-i) for i in range(types[0])]+[maxN//10//types[0] for j in range(types[1])]
    N2=[Ne2*int(types[0]==1)+maxN*i*int(types[0]==2) for i in range(types[0])]+[maxN//100//types[0] for j in range(types[1])]
    N3=[Ne3*(1-i) for i in range(types[0])]+[maxN//100//types[0] for j in range(types[1])]
    N4=[Ne4*(1-i) for i in range(types[0])]+[maxN//10//types[0] for j in range(types[1])]
    
    all_N=[N1,N2,N3,N4]
    all_N=[int(all_N[i][j]) for j in range(types[0]+types[1]) for i in range(4)]
    
    p_tri=ptri.get()
    p_mono=pmono.get()
    sprouting=sprouting.get()
    topo='normal'
    co='normal'
    rapp_inter=1*int(co=='normal')+6.5*int(co=='uniform')
    all_p_inter=[[[[0 for k in range(types[0]+types[1])] for l in range(types[0])] for i in range(4)] for j in range(4)]
    all_p_inter[0][1]=[[p_tri/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[1][2]=[[p_tri/rapp_inter*(1+sprouting) for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[2][3]=[[p_tri/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[3][0]=[[p_tri/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[0][2]=[[p_mono/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[0][3]=[[p_mono/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter[1][3]=[[p_mono*sprouting/rapp_inter for i in range(types[0]+types[1])] for j in range(types[0])]
    
    
    co2='normal'
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
    
    
    all_g_max_e=[g_max_e.get()*psiemens for i in range(types[0])]
    all_g_max_i=[g_max_i.get()*psiemens for i in range(types[1])]            
    
    all_gains=[[1 for i in range(types[0]+types[1])] for j in range(4)]
    
    fco=functional_co.get()
    var_coeff=gains.get()
    if fco=='wake': #wakefulness connectivity
        all_gains[0][:types[0]]=[1/var_coeff]*types[0]
        all_gains[1]=[var_coeff]*(types[0]+types[1])
        all_gains[2][:types[0]]=[1/var_coeff]*types[0]
        all_gains[3][types[0]:]=[var_coeff]*types[1]
        
    tau_Cl=tau_Cl.get()*second
    Ek=Ek.get()*mV
    input_type=input_type.get()
    A0=A0.get()
    A1=A1.get()
    dur=dur.get()*second
    f1=f1.get()*Hz
    duty_cycle=duty.get()
    runtime=runtime.get()*second

    if plot_raster.get()=='True':
        plot_raster=True
    else :
        plot_raster=False
        
    if save_figs.get()=='True':
        save_figs=True
    else :
        save_figs=False
    
    if save_raster.get()=='True':
        save_raster=True
    else :
        save_raster=False
        
    if save_neuron_pos.get()=='True':
        save_neuron_pos=True
    else :
        save_neuron_pos=False
        
    if save_syn_mat.get()=='True':
        save_syn_mat=True
    else :
        save_syn_mat=False
        
    if save_all_FR.get()=='True':
        save_all_FR=True
    else :
        save_all_FR=False
    
    interface.destroy()
    start_scope()
    
    path=''
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

    if os.name == 'nt':
        path=os.path.join(ntpath.dirname(os.path.abspath(__file__)),"results_"+timestamp)
    else :
        path="./results_"+timestamp #TODO!!!


    os.mkdir(path)
    
#    process(runtime,plot_raster,types,all_N,topo,co,co2,A0,A1,dur,f1,duty,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,gCAN,save_raster,save_neuron_pos,save_syn_mat,path) 
    res_1024, all_FR_exc,all_FR_inh=process(runtime, plot_raster,types,all_N,topo,co,co2,A0,A1,dur,f1,duty_cycle,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,gCAN,save_raster,save_neuron_pos,save_syn_mat,save_all_FR,path,in_file_1,in_file_2,in_file_3,in_fs,tau_Cl,Ek) 

    aborted=False
    return


s = ttk.Style()
s.configure('TNotebook.Tab', font=('URW Gothic L','9','bold') )
s.configure('TNotebook', font=('URW Gothic L','9','bold') )
interface.option_add("*Label.Font", "times 8")
interface.option_add("*Font", "times 8") #"Verdana 10 bold"

tab_parent=ttk.Notebook(interface)
tab1=Frame(tab_parent,bg=BG)
tab2=Frame(tab_parent,bg=BG)
tab3=Frame(tab_parent,bg=BG)
tab4=Frame(tab_parent,bg=BG)
tab5=Frame(tab_parent,bg=BG)
tab6=Frame(tab_parent,bg=BG)

tab_parent.add(tab1,text='Network parameters')
tab_parent.add(tab2,text='Sleep-wake parameters')
tab_parent.add(tab3,text='Epilepsy parameters')
tab_parent.add(tab4,text='Inputs et outputs')

tab_parent.pack(expand=1,fill='both')

bquit=Button(interface,text='Quit',command=interface.destroy)
bquit.place(x=10,y=560) 
bstart=Button(interface,text='End setup and start',command=start)
bstart.place(x=80,y=560) 



### Tab 1 : Basic network parameters choices:

question=Label(tab1,text='Choose the maximum number of neurons in the network (in the CA1 excitatory neurons group) :\nThe total number of neurons will be 3.32*N')
question.place(x=10,y=20)
entry=Entry(tab1,textvariable=maxN)
entry.place(x=560,y=25)

question_type=Label(tab1,text='Connection probabilities:')
lab=Label(tab1,text='Trisynaptic pathway : ')
lab.place(x=10,y=100)   
entry=Entry(tab1,textvariable=ptri)
entry.place(x=150,y=100) 
lab=Label(tab1,text='Monosynaptic pathway : ')
lab.place(x=410,y=100)   
entry=Entry(tab1,textvariable=pmono)
entry.place(x=550,y=100)   



question_type=Label(tab1,text='Choose the maximum conductance of each synapse type (in pS):')
question_type.place(x=10,y=150)
lab=Label(tab1,text='Excitatory synapses:')
lab.place(x=10,y=180)
entry=Entry(tab1,textvariable=g_max_e)
entry.place(x=150,y=180)
lab=Label(tab1,text='Inhibitory synapses:')
lab.place(x=10,y=210)
entry=Entry(tab1,textvariable=g_max_i)
entry.place(x=150,y=210)

### Tab 2 : Sleep-wake parameters:

question_type=Label(tab2,text='Choose the gains to be put on synaptic conductances to represent cholinergic modulation:')
question_type.place(x=10,y=100) 
entryg=Entry(tab2,textvariable=gains)
entryg.place(x=550,y=100)

question_type=Label(tab2,text='Functional connectivity:')
question_type.place(x=10,y=130) 
b0 = Radiobutton(tab2, variable=functional_co, text='Slow-wave sleep', value='sleep')
b0.place(x=200, y=130) 
b1 = Radiobutton(tab2, variable=functional_co, text='Wakefulness', value='wake')
b1.place(x=400, y=130)

question_type=Label(tab2,text='Choose the conductance of CAN channel under cholinergic modulation:')
question_type.place(x=10,y=200) 
entryg=Entry(tab2,textvariable=gCAN)
entryg.place(x=350,y=200)

question_type=Label(tab2,text='CAN currents:')
question_type.place(x=10,y=230) 
b0 = Radiobutton(tab2, variable=CAN, text='Slow-wave sleep', value='sleep')
b0.place(x=200, y=230) 
b1 = Radiobutton(tab2, variable=CAN, text='Wakefulness', value='wake')
b1.place(x=400, y=230)

### Tab 3 : Epilepsy parameters:
question_type=Label(tab3,text='Network abonormalities:')
question_type.place(x=10,y=100) 

Labscl=Label(tab3,text='Hippocampal sclerosis (0 = healthy, 1 = high sclerosis):')
Labscl.place(x=10,y=150)
entryscl=Entry(tab3,textvariable=sclerosis)
entryscl.place(x=350,y=150)

Labspr=Label(tab3,text='Mossy fiber sprouting (0 = healthy, 1 = high sprouting):')
Labspr.place(x=10,y=180)
entryspr=Entry(tab3,textvariable=sclerosis)
entryspr.place(x=350,y=180)


question_type=Label(tab3,text='Individual neurons abonormalities:')
question_type.place(x=10,y=250) 

Labtau=Label(tab3,text='Internal chloride ion depletion rate (in s, 0.1 = healthy):')
Labtau.place(x=10,y=300)
entrytau=Entry(tab3,textvariable=tau_Cl)
entrytau.place(x=350,y=300)

LabEk=Label(tab3,text='Potassium channel reversal potential (in mV, -100 = healthy):')
LabEk.place(x=10,y=330)
entryEk=Entry(tab3,textvariable=Ek)
entryEk.place(x=350,y=330)




### Tab 4 : inputs and outputs
lab=Label(tab4,text='Duration of the simulation (s)')
lab.place(x=10,y=30)  
entry=Entry(tab4,textvariable=runtime)
entry.place(x=210,y=30)


question_type=Label(tab4,text='Choose the input to provide to the network:')
question_type.place(x=10,y=70)

vals = ['custom','square']
etiqs = ['User-provided input','Square current input']

b0 = Radiobutton(tab4, variable=input_type, text=etiqs[0], value=vals[0])
b0.place(x=10,y=100)
b1 = Radiobutton(tab4, variable=input_type, text=etiqs[1], value=vals[1])
b1.place(x=210,y=100)

input_type.set('square')

question_type=Label(tab4,text='If custom input is applied:')
question_type.place(x=10,y=150)

lab=Label(tab4,text='File 1 :')
lab.place(x=10,y=180) 
e = Entry(tab4, textvariable=in_file_1)
b = Button(tab4, text="Browse",
           command=lambda:in_file_1.set(askopenfilename()))
e.place(x=110,y=180)
b.place(x=200,y=180)
lab=Label(tab4,text='File 2 :')
lab.place(x=10,y=210) 
e = Entry(tab4, textvariable=in_file_2)
b = Button(tab4, text="Browse",
           command=lambda:in_file_2.set(askopenfilename()))
e.place(x=110,y=210)
b.place(x=200,y=210)
lab=Label(tab4,text='File 3 :')
lab.place(x=10,y=240) 
e = Entry(tab4, textvariable=in_file_3)
b = Button(tab4, text="Browse",
           command=lambda:in_file_3.set(askopenfilename()))
e.place(x=110,y=240)
b.place(x=200,y=240)

lab=Label(tab4,text='Sampling frequency (Hz)')
lab.place(x=10,y=270) 
entry=Entry(tab4,textvariable=in_fs)
entry.place(x=150,y=270)

question_type=Label(tab4,text='If artificial input is applied:')
question_type.place(x=10,y=300)

lab=Label(tab4,text='Minimum current (nA)')
lab.place(x=10,y=330) 
entry=Entry(tab4,textvariable=A0)
entry.place(x=150,y=330)

lab=Label(tab4,text='Maximum current (nA)')
lab.place(x=310,y=330) 
entry=Entry(tab4,textvariable=A1)
entry.place(x=450,y=330)

lab=Label(tab4,text='Frequency (Hz)')
lab.place(x=610,y=330)
entry=Entry(tab4,textvariable=f1)
entry.place(x=750,y=330)

lab=Label(tab4,text='Duration (s)')
lab.place(x=10,y=360)  
entry=Entry(tab4,textvariable=dur)
entry.place(x=150,y=360)

lab=Label(tab4,text='Duty cycle (between 0 and 1)')
lab.place(x=310,y=360)
entry=Entry(tab4,textvariable=duty)
entry.place(x=530,y=360)


question_type=Label(tab4,text='Simulation outputs:')
question_type.place(x=10,y=400)

lab = Label(tab4,text='Plot raster ?')
lab.place(x=10,y=430)
b0 = Radiobutton(tab4, variable=plot_raster, text='Yes', value='True')
b0.place(x=250,y=430)
b1 = Radiobutton(tab4, variable=plot_raster, text='No', value='False')
b1.place(x=300,y=430) 
plot_raster.set('True')

lab = Label(tab4,text='Save figure(s) as png ?')
lab.place(x=10,y=460)
b0 = Radiobutton(tab4, variable=save_figs, text='Yes', value='True')
b0.place(x=250,y=460) 
b1 = Radiobutton(tab4, variable=save_figs, text='No', value='False')
b1.place(x=300,y=460) 
save_figs.set('True')    

lab = Label(tab4,text='Save rasters as txt files ?')
lab.place(x=10,y=490)
b0 = Radiobutton(tab4, variable=save_raster, text='Yes', value='True')
b0.place(x=250,y=490)
b1 = Radiobutton(tab4, variable=save_raster, text='No', value='False')
b1.place(x=300,y=490) 
save_raster.set('False')    

lab = Label(tab4,text='Save neuron positions as txt files ?')
lab.place(x=510,y=430)
b0 = Radiobutton(tab4, variable=save_neuron_pos, text='Yes', value='True')
b0.place(x=750,y=430)
b1 = Radiobutton(tab4, variable=save_neuron_pos, text='No', value='False')
b1.place(x=800,y=430)
save_neuron_pos.set('False')  

lab = Label(tab4,text='Save synaptic matrices as txt files ?')
lab.place(x=510,y=460)
b0 = Radiobutton(tab4, variable=save_syn_mat, text='Yes', value='True')
b0.place(x=750,y=460)
b1 = Radiobutton(tab4, variable=save_syn_mat, text='No', value='False')
b1.place(x=800,y=460)  
save_syn_mat.set('False')   

lab = Label(tab4,text='Save firing rates as txt files ?')
lab.place(x=510,y=490)
b0 = Radiobutton(tab4, variable=save_all_FR, text='Yes', value='True')
b0.place(x=750,y=490)
b1 = Radiobutton(tab4, variable=save_all_FR, text='No', value='False')
b1.place(x=800,y=490)  
save_all_FR.set('False')   



interface.mainloop()

if not aborted : 
    simu=lecture(path+'/LFP.txt')[0]
    figure()
    plot(simu)
    
    if save_figs:
        os.mkdir(path+'/figures')
        for i in get_fignums():
            current_fig=figure(i)
            current_fig.savefig(path+'/figures/figure'+str(i)+'.png')

