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
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import ntpath

BG='white'
myfont=('Helvetica',12)


interface=Tk()
interface.minsize(1000, 600)
interface.option_add("*Font", "courier")
interface.option_add("*Background", "white")


neuron_type=StringVar()
N_type_exc=DoubleVar(interface,1)
N_type_inh=DoubleVar(interface,1)
gCAN=DoubleVar(interface,0.5)
topo_type=StringVar()
co_type=StringVar()
co_type2=StringVar()

tau_Cl=DoubleVar(interface,0.1)
Ek=DoubleVar(interface,-100)

all_N=[]
all_p_inter=[]
all_p_intra=[]
all_g_max_e=[]
all_g_max_i=[]
all_gains=[]

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
    global runtime,plot_raster,gCAN,types,all_N,topo,co,A0,A1,dur,f1,duty,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,save_figs,save_raster,save_neuron_pos,save_syn_mat,path,save_all_FR,tau_Cl,Ek,in_file_1,in_file_2,in_file_3,in_fs,aborted
    
    #récupérations des valeurs du formulaire + duplication si plusieurs types de neurones E ou I
    types=[int(N_type_exc.get()),int(N_type_inh.get())]
    
    Nexc=[int(all_N[0][0].get()/types[0]) for i in range(types[0])]+[int(all_N[1][0].get()/types[0]) for i in range(types[0])]+[int(all_N[2][0].get()/types[0]) for i in range(types[0])]+[int(all_N[3][0].get()/types[0]) for i in range(types[0])]
    Ninh=[int(all_N[0][1].get()/types[1]) for i in range(types[1])]+[int(all_N[1][1].get()/types[1]) for i in range(types[1])]+[int(all_N[2][1].get()/types[1]) for i in range(types[1])]+[int(all_N[3][1].get()/types[1]) for i in range(types[1])]
    
    all_N=Nexc+Ninh

    tau_Cl=tau_Cl.get()*second
    Ek=Ek.get()*mV
    topo=topo_type.get()
    co=co_type.get()
    co2=co_type2.get()
    gCAN=gCAN.get()*usiemens*cmeter**-2
    
    ind_i=[0,1]
    if types[0]==2 and types[1]==1:
        ind_i=[0,0,1]
    elif types[0]==1 and types[1]==2:
        ind_i=[0,1,1]
    elif types[0]==2 and types[1]==2:
        ind_i=[0,0,1,1]

    all_p_inter2=[[[[0 for k in range(types[0]+types[1])] for l in range(types[0])] for i in range(4)] for j in range(4)]
    all_p_inter2[0][1]=[[all_p_inter[0][1][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter2[1][2]=[[all_p_inter[1][2][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter2[2][3]=[[all_p_inter[2][3][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter2[3][0]=[[all_p_inter[3][0][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter2[0][2]=[[all_p_inter[0][2][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter2[0][3]=[[all_p_inter[0][3][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter2[1][3]=[[all_p_inter[1][3][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(types[0])]
    all_p_inter=all_p_inter2

    for i in range(4):
        p_e=[all_p_intra[i][0][0].get() for k in range(types[0])]+[all_p_intra[i][0][1].get() for k in range(types[1])]
        p_i=[all_p_intra[i][1][0].get() for k in range(types[0])]+[all_p_intra[i][1][1].get() for k in range(types[1])]
        all_p_intra[i]=[p_e for k in range(types[0])]+[p_i for k in range(types[1])]
    
    all_g_max_e=[all_g_max_e.get()*psiemens for i in range(types[0])]
    all_g_max_i=[all_g_max_i.get()*psiemens for i in range(types[1])]
    all_gains=[[all_gains[j][ind_i[i]].get() for i in range(types[0]+types[1])] for j in range(4)]
    input_type=input_type.get()
    A0=A0.get()
    A1=A1.get()
    dur=dur.get()*second
    f1=f1.get()*Hz
    duty=duty.get()
    runtime=runtime.get()*second
    in_file_1 = in_file_1.get()
    in_file_2 = in_file_2.get()
    in_file_3 = in_file_3.get()
    in_fs=in_fs.get()*Hz
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
        path=".\results_"+timestamp


    os.mkdir(path)
    
#    process(runtime,plot_raster,types,all_N,topo,co,co2,A0,A1,dur,f1,duty,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,gCAN,save_raster,save_neuron_pos,save_syn_mat,path) 
    res_1024, all_FR_exc,all_FR_inh=process(runtime,plot_raster,types,all_N,topo,co,co2,A0,A1,dur,f1,duty,input_type,all_p_intra,all_p_inter,all_gains,all_g_max_i,all_g_max_e,gCAN,save_raster,save_neuron_pos,save_syn_mat,save_all_FR,path,in_file_1,in_file_2,in_file_3,in_fs,tau_Cl,Ek)     
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

tab_parent.add(tab1,text='Neuron types and numbers')
tab_parent.add(tab2,text='Topology')
tab_parent.add(tab3,text='Connectivity intra-region')
tab_parent.add(tab4,text='Connectivity inter-region')
tab_parent.add(tab5,text='Synaptic conductances and gains')
tab_parent.add(tab6,text='Inputs et outputs')

tab_parent.pack(expand=1,fill='both')

bquit=Button(interface,text='Quit',command=interface.destroy)
bquit.place(x=10,y=560) 
bstart=Button(interface,text='End setup and start',command=start)
bstart.place(x=80,y=560) 



### Onglet 1 : choix des types et nombres de neurones:
question=Label(tab1,text='Choose how many neuron types to model :')
question.place(x=10,y=60) 

LabNexc=Label(tab1,text='Types of excitatory neurons:',font="arial 8")
LabNexc.place(x=50,y=90)

b0 = Radiobutton(tab1, variable=N_type_exc, text='1', value=1)
b0.place(x=250,y=90)
b1 = Radiobutton(tab1, variable=N_type_exc, text='2', value=2)
b1.place(x=300,y=90)

LabNexc=Label(tab1,text='Types of inhibitory neurons:')
LabNexc.place(x=400,y=90)

b0 = Radiobutton(tab1, variable=N_type_inh, text='1', value=1)
b0.place(x=600,y=90)
b1 = Radiobutton(tab1, variable=N_type_inh, text='2', value=2)
b1.place(x=650,y=90)

LabCAN=Label(tab1,text='CAN channel maximum conductance (in uS/cm²):')
LabCAN.place(x=10,y=120)
entryCAN=Entry(tab1,textvariable=gCAN)
entryCAN.place(x=350,y=120)

Labtau=Label(tab1,text='Internal chloride ion depletion rate (in s):')
Labtau.place(x=10,y=150)
entrytau=Entry(tab1,textvariable=tau_Cl)
entrytau.place(x=350,y=150)

LabEk=Label(tab1,text='Potassium channel reversal potential (in mV):')
LabEk.place(x=10,y=180)
entryEk=Entry(tab1,textvariable=Ek)
entryEk.place(x=350,y=180)

types=[1,1]

N1=[DoubleVar(interface,10000)]+[DoubleVar(interface,1000)]
N2=[DoubleVar(interface,10000)]+[DoubleVar(interface,100)]
N3=[DoubleVar(interface,1000)]+[DoubleVar(interface,100)]
N4=[DoubleVar(interface,10000)]+[DoubleVar(interface,1000)]

all_N=[N1,N2,N3,N4]

#    interface.title('Choose the number of neurons in each region :')
question=Label(tab1,text='Choose the total number of neurons in each region :')
question.place(x=10,y=220)

labEC=Label(tab1,text='Entorhinal Cortex')
labEC.place(x=50,y=250)
labDG=Label(tab1,text='Dentate Gyrus')
labDG.place(x=280,y=250)
labCA3=Label(tab1,text='CA3')
labCA3.place(x=530,y=250)
labCA1=Label(tab1,text='CA1')
labCA1.place(x=750,y=250)

all_labels=['Excitatory neurons :','Inhibitory neurons :']
for i in range(4):
    for j in range(2):
        lab=Label(tab1,text=all_labels[j])
        lab.place(x=30+220*i,y=270+100*j)
        entry=Entry(tab1,textvariable=all_N[i][j])
        entry.place(x=30+220*i,y=300+100*j)



### Onglet 2 : choix de la topologie :
question=Label(tab2,text='Choose the topology of the network :')
question.place(x=10,y=30)

vals = ['normal', 'rect']
etiqs = ['Realistic', 'Rectangle']

b0 = Radiobutton(tab2, variable=topo_type, text=etiqs[0], value=vals[0])
b0.place(x=100, y=90) 
b1 = Radiobutton(tab2, variable=topo_type, text=etiqs[1], value=vals[1])
b1.place(x=700, y=90) 

topo_type.set('normal')

image_real = Image.open("model_files/topo_realiste.jpg")
photo_real = ImageTk.PhotoImage(image_real)

label_real = Label(tab2,image=photo_real)
label_real.image = photo_real # keep a reference!
label_real.place(x=50,y=120)

image_rect = Image.open("model_files/topo_rectangle.png")
photo_rect = ImageTk.PhotoImage(image_rect)

label_rect = Label(tab2,image=photo_rect)
label_rect.image = photo_rect # keep a reference!
label_rect.place(x=550,y=120)



### Onglet 3 : choix de la connectivité intra-region :
p_EC_e=[DoubleVar(interface,0),DoubleVar(interface,0.37)]
p_EC_i=[DoubleVar(interface,0.54),DoubleVar(interface,0)]
all_p_EC=[p_EC_e,p_EC_i]
p_DG_e=[DoubleVar(interface,0),DoubleVar(interface,0.06)]
p_DG_i=[DoubleVar(interface,0.14),DoubleVar(interface,0)]
all_p_DG=[p_DG_e,p_DG_i]
p_CA3_e=[DoubleVar(interface,0.56),DoubleVar(interface,0.75)]
p_CA3_i=[DoubleVar(interface,0.75),DoubleVar(interface,0)]
all_p_CA3=[p_CA3_e,p_CA3_i]
p_CA1_e=[DoubleVar(interface,0),DoubleVar(interface,0.28)]
p_CA1_i=[DoubleVar(interface,0.3),DoubleVar(interface,0.7)]
all_p_CA1=[p_CA1_e,p_CA1_i]

all_p_intra=[all_p_EC,all_p_DG,all_p_CA3,all_p_CA1]

question_type=Label(tab3,text='Connectivity type :')
question_type.place(x=10,y=30)
vals = ['normal', 'uniform']
etiqs = ['Distance-related', 'Uniform']

b0 = Radiobutton(tab3, variable=co_type2, text=etiqs[0], value=vals[0])
b0.place(x=10,y=60)
b1 = Radiobutton(tab3, variable=co_type2, text=etiqs[1], value=vals[1])
b1.place(x=160,y=60)

co_type2.set('normal')

question_type=Label(tab3,text='Connection probabilities:')
question_type.place(x=10,y=120)
labEC=Label(tab3,text='In the EC : ')
labEC.place(x=110,y=150)
labEC=Label(tab3,text='In the DG : ')
labEC.place(x=310,y=150) 
labEC=Label(tab3,text='In CA3 : ')
labEC.place(x=510,y=150)
labEC=Label(tab3,text='In CA1 : ')
labEC.place(x=710,y=150)

all_labels=[['From E to E : ','From E to I : '],['From I to E : ','From I to I : ']]

for i in range(4):
    for j in range(2):
        for k in range(2):
            if i==0:
                lab=Label(tab3,text=all_labels[j][k])
                lab.place(x=10,y=180+60*j+30*k)   
            entry=Entry(tab3,textvariable=all_p_intra[i][j][k])
            entry.place(x=110+200*i,y=180+60*j+30*k)    
    


### Onglet 4 : choix de la connectivité inter-region :
all_p_inter=[[[0 for k in range(2)] for i in range(4)] for j in range(4)]
all_p_inter[0][1]=[DoubleVar(interface,0.4) for i in range(2)]
all_p_inter[1][2]=[DoubleVar(interface,0.4) for i in range(2)]
all_p_inter[2][3]=[DoubleVar(interface,0.4) for i in range(2)]
all_p_inter[3][0]=[DoubleVar(interface,0.4) for i in range(2)]
all_p_inter[0][2]=[DoubleVar(interface,0.3) for i in range(2)]
all_p_inter[0][3]=[DoubleVar(interface,0.3) for i in range(2)]
all_p_inter[1][3]=[DoubleVar(interface,0.0) for i in range(2)]

question_type=Label(tab4,text='Connectivity type :')
question_type.place(x=10,y=30)
vals = ['normal', 'uniform']
etiqs = ['Distance-related', 'Uniform']

b0 = Radiobutton(tab4, variable=co_type, text=etiqs[0], value=vals[0])
b0.place(x=10,y=60)
b1 = Radiobutton(tab4, variable=co_type, text=etiqs[1], value=vals[1])
b1.place(x=160,y=60)

co_type.set('normal')

question_type=Label(tab4,text='Connection probabilities:')
question_type.place(x=10,y=120)

labEC=Label(tab4,text='From the EC: ')
labEC.place(x=110,y=150)
labEC=Label(tab4,text='To DG : ')
labEC.place(x=110,y=180) 
labEC=Label(tab4,text='To CA3 : ')
labEC.place(x=210,y=180)
labEC=Label(tab4,text='To CA1: ')
labEC.place(x=310,y=180) 
labEC=Label(tab4,text='From the DG : ')
labEC.place(x=510,y=150) 
labEC=Label(tab4,text='To CA3 : ')
labEC.place(x=510,y=180)
labEC=Label(tab4,text='To CA1 : ')
labEC.place(x=610,y=180)
labEC=Label(tab4,text='From CA3 to CA1 : ')
labEC.place(x=110,y=350)
labEC=Label(tab4,text='From CA1 to EC :')
labEC.place(x=510,y=350)

all_labels=['From E to E : ','From E to I : ']
xpos=[110,210,310,510,610,110,510]
deb_reg=[0,0,0,1,1,2,3]
fin_reg=[1,2,3,2,3,3,0]
    

for j in range(2):
    for k in range(7):
        lab=Label(tab4,text=all_labels[j])
        lab.place(x=xpos[k],y=210+k//5*170+j*60)  
        entry=Entry(tab4,textvariable=all_p_inter[deb_reg[k]][fin_reg[k]][j])
        entry.place(x=xpos[k],y=240+k//5*170+j*60) 
        entry=Entry(tab4,textvariable=all_p_inter[deb_reg[k]][fin_reg[k]][j])
        entry.place(x=xpos[k],y=240+k//5*170+j*60) 
        entry=Entry(tab4,textvariable=all_p_inter[deb_reg[k]][fin_reg[k]][j])
        entry.place(x=xpos[k],y=240+k//5*170+j*60) 
        entry=Entry(tab4,textvariable=all_p_inter[deb_reg[k]][fin_reg[k]][j])
        entry.place(x=xpos[k],y=240+k//5*170+j*60) 
        entry=Entry(tab4,textvariable=all_p_inter[deb_reg[k]][fin_reg[k]][j])
        entry.place(x=xpos[k],y=240+k//5*170+j*60) 
        entry=Entry(tab4,textvariable=all_p_inter[deb_reg[k]][fin_reg[k]][j])
        entry.place(x=xpos[k],y=240+k//5*170+j*60) 
        entry=Entry(tab4,textvariable=all_p_inter[deb_reg[k]][fin_reg[k]][j])
        entry.place(x=xpos[k],y=240+k//5*170+j*60) 


### Onglet 5 : conductances et gains synaptiques
all_g_max_e=DoubleVar(interface,60)
all_g_max_i=DoubleVar(interface,600)

question_type=Label(tab5,text='Choose the maximum conductance of each synapse type (in pS):')
question_type.place(x=10,y=30)

all_labels=['Excitatory synapses','Inhibitory synapses']

for i in range(1):
    lab=Label(tab5,text=all_labels[i])
    lab.place(x=60,y=60)
    entry=Entry(tab5,textvariable=all_g_max_e)
    entry.place(x=60,y=90)
for j in range(1):
    lab=Label(tab5,text=all_labels[types[0]+j])
    lab.place(x=260,y=60)
    entry=Entry(tab5,textvariable=all_g_max_i)
    entry.place(x=260,y=90)

all_gains=[[DoubleVar(interface,1) for i in range(2)] for j in range(4)]

question_type=Label(tab5,text='Choose the gains to be put on each synapse:')
question_type.place(x=10,y=200)

labEC=Label(tab5,text='In the EC : ')
labEC.place(x=60,y=230)
labEC=Label(tab5,text='In the DG : ')
labEC.place(x=260,y=230)
labEC=Label(tab5,text='In CA3 : ')
labEC.place(x=460,y=230)
labEC=Label(tab5,text='In CA1 : ')
labEC.place(x=660,y=230)

all_labels=['Excitatory synapses','Inhibitory synapses']

for i in range(4):
    for row in range(len(all_labels)):
        labg=Label(tab5,text=all_labels[row])
        labg.place(x=60+i*200,y=260+60*row)  
        entryg=Entry(tab5,textvariable=all_gains[i][row])
        entryg.place(x=60+i*200,y=290+60*row)



### Onglet 6 : inputs and outputs
lab=Label(tab6,text='Duration of the simulation (s)')
lab.place(x=10,y=30)  
entry=Entry(tab6,textvariable=runtime)
entry.place(x=210,y=30)


question_type=Label(tab6,text='Choose the input to provide to the network:')
question_type.place(x=10,y=70)

vals = ['custom','square']
etiqs = ['User-provided input','Square current input']

b0 = Radiobutton(tab6, variable=input_type, text=etiqs[0], value=vals[0])
b0.place(x=10,y=100)
b1 = Radiobutton(tab6, variable=input_type, text=etiqs[1], value=vals[1])
b1.place(x=210,y=100)

input_type.set('square')

question_type=Label(tab6,text='If custom input is applied:')
question_type.place(x=10,y=150)

lab=Label(tab6,text='File 1 :')
lab.place(x=10,y=180) 
e = Entry(tab6, textvariable=in_file_1)
b = Button(tab6, text="Browse",
           command=lambda:in_file_1.set(askopenfilename()))
e.place(x=110,y=180)
b.place(x=200,y=180)
lab=Label(tab6,text='File 2 :')
lab.place(x=10,y=210) 
e = Entry(tab6, textvariable=in_file_2)
b = Button(tab6, text="Browse",
           command=lambda:in_file_2.set(askopenfilename()))
e.place(x=110,y=210)
b.place(x=200,y=210)
lab=Label(tab6,text='File 3 :')
lab.place(x=10,y=240) 
e = Entry(tab6, textvariable=in_file_3)
b = Button(tab6, text="Browse",
           command=lambda:in_file_3.set(askopenfilename()))
e.place(x=110,y=240)
b.place(x=200,y=240)

lab=Label(tab6,text='Sampling frequency (Hz)')
lab.place(x=10,y=270) 
entry=Entry(tab6,textvariable=in_fs)
entry.place(x=150,y=270)

question_type=Label(tab6,text='If artificial input is applied:')
question_type.place(x=10,y=300)

lab=Label(tab6,text='Minimum current (nA)')
lab.place(x=10,y=330) 
entry=Entry(tab6,textvariable=A0)
entry.place(x=150,y=330)

lab=Label(tab6,text='Maximum current (nA)')
lab.place(x=310,y=330) 
entry=Entry(tab6,textvariable=A1)
entry.place(x=450,y=330)

lab=Label(tab6,text='Frequency (Hz)')
lab.place(x=610,y=330)
entry=Entry(tab6,textvariable=f1)
entry.place(x=750,y=330)

lab=Label(tab6,text='Duration (s)')
lab.place(x=10,y=360)  
entry=Entry(tab6,textvariable=dur)
entry.place(x=150,y=360)

lab=Label(tab6,text='Duty cycle (between 0 and 1)')
lab.place(x=310,y=360)
entry=Entry(tab6,textvariable=duty)
entry.place(x=530,y=360)


question_type=Label(tab6,text='Simulation outputs:')
question_type.place(x=10,y=400)

lab = Label(tab6,text='Plot raster ?')
lab.place(x=10,y=430)
b0 = Radiobutton(tab6, variable=plot_raster, text='Yes', value='True')
b0.place(x=250,y=430)
b1 = Radiobutton(tab6, variable=plot_raster, text='No', value='False')
b1.place(x=300,y=430) 
plot_raster.set('True')

lab = Label(tab6,text='Save figure(s) as png ?')
lab.place(x=10,y=460)
b0 = Radiobutton(tab6, variable=save_figs, text='Yes', value='True')
b0.place(x=250,y=460) 
b1 = Radiobutton(tab6, variable=save_figs, text='No', value='False')
b1.place(x=300,y=460) 
save_figs.set('True')    

lab = Label(tab6,text='Save rasters as txt files ?')
lab.place(x=10,y=490)
b0 = Radiobutton(tab6, variable=save_raster, text='Yes', value='True')
b0.place(x=250,y=490)
b1 = Radiobutton(tab6, variable=save_raster, text='No', value='False')
b1.place(x=300,y=490) 
save_raster.set('False')    

lab = Label(tab6,text='Save neuron positions as txt files ?')
lab.place(x=510,y=430)
b0 = Radiobutton(tab6, variable=save_neuron_pos, text='Yes', value='True')
b0.place(x=750,y=430)
b1 = Radiobutton(tab6, variable=save_neuron_pos, text='No', value='False')
b1.place(x=800,y=430)
save_neuron_pos.set('False')  

lab = Label(tab6,text='Save synaptic matrices as txt files ?')
lab.place(x=510,y=460)
b0 = Radiobutton(tab6, variable=save_syn_mat, text='Yes', value='True')
b0.place(x=750,y=460)
b1 = Radiobutton(tab6, variable=save_syn_mat, text='No', value='False')
b1.place(x=800,y=460)  
save_syn_mat.set('False')   

lab = Label(tab6,text='Save firing rates as txt files ?')
lab.place(x=510,y=490)
b0 = Radiobutton(tab6, variable=save_all_FR, text='Yes', value='True')
b0.place(x=750,y=490)
b1 = Radiobutton(tab6, variable=save_all_FR, text='No', value='False')
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

