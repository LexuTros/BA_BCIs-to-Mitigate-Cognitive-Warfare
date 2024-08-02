#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from brian2 import *
from mpl_toolkits.mplot3d import Axes3D


def topologie(types,all_N):   
        
    #Création de l'électrode
#    depart_electrode=array([-21, 0, 50])
#    arrivee_electrode=array([15, 0, 50])
    depart_electrode=array([-21, -10, 50])
    arrivee_electrode=array([15, -10, 50])
    len_elec=norm(arrivee_electrode-depart_electrode)
#    print(len_elec*150*umetre)
    dir_elec=(arrivee_electrode-depart_electrode)/norm(arrivee_electrode-depart_electrode)
    elec=[]
    #psi = arccos(dot(depart_electrode[:-1],arrivee_electrode[:-1])/(norm(depart_electrode[:-1])*norm(arrivee_electrode[:-1])))
    psi = arccos(dot(dir_elec,array([0,1,0])))
    diametre = 400/150 #en fait c'est un rayon
    for t in linspace(0,1,33):
        centre=(1-t)*depart_electrode+t*arrivee_electrode
        #print(centre)
        for theta in arange(0,2*pi,pi/6):
            point=[centre[0]+diametre*cos(theta)*cos(psi),centre[1]-diametre*cos(theta)*sin(psi),centre[2]+diametre*sin(theta)]
            #print(point)
            elec.append(point)
    elec_array=array(elec[:144]+elec[252:])
    
    def topo_one_pop(init_segs,end_segs,N,i_soma): #donne la position du soma (pour le calcul de Im) et des dendrites (pour Isyn)
        if N==0:
            return array([]),array([]),array([])
    
        seg=randint(0,len(init_segs))
        t=uniform(i_soma[0],i_soma[1])
        all_t=zeros(int(N))
        all_z=zeros(int(N))
        all_t[0]=seg
        z=100*random()
        all_z[0]=z
        topo=append((1-t)*init_segs[seg]  + t * end_segs[seg],z)
        topo_end=append(end_segs[seg],z)
        topo_inh=append(init_segs[seg],z)
        
        for i in range(int(N-1)):
            seg=randint(0,len(init_segs)-1)
            t=random()
            init=t*init_segs[seg]+(1-t)*init_segs[seg+1]
            all_t[i+1]=seg+t
            end=t*end_segs[seg]+(1-t)*end_segs[seg+1] #les dendrites sont positionnées en "end"
            t2=uniform(i_soma[0],i_soma[1]) #le soma est dans la "première moitié" de la couche de neurones
            z=100*random()
            all_z[i+1]=z
            coords=append((1 - t2)*init  + t2 * end,z)
            topo=vstack((topo,coords)) 
            topo_end=vstack((topo_end,append(end,z))) 
            topo_inh=vstack((topo_inh,append(0.9*init+0.1*end,z))) 
        sort_index=argsort(all_t)
        topo=topo[sort_index]
        topo_end=topo_end[sort_index]
        topo_inh=topo_inh[sort_index]
        all_z=all_z[sort_index]
        sort_index2=argsort(all_z)
        topo=topo[sort_index2]
        topo_end=topo_end[sort_index2]
        topo_inh=topo_inh[sort_index2]
        all_z=all_z[sort_index2]
#        print(all_z[:5],topo[:5,2])        
        #Décalage vertical pour tenir compte de l'électrode :
        for i in range(int(N)):
            x=topo[i,0]
            y=topo[i,1]
            z=topo[i,2]
            dist_elec=norm(cross((array([x,y,50])-depart_electrode),dir_elec))
            if dist_elec<diametre/2:
                #print("distance inférieure")
                #print(topo[i,2])  
                if z<50:
                    topo[i,2]-=diametre*(1-(dist_elec/diametre)**2)
                    topo_end[i,2]-=diametre*(1-(dist_elec/diametre)**2)
                    topo_inh[i,2]-=diametre*(1-(dist_elec/diametre)**2)
                else :
                    topo[i,2]+=diametre*(1-(dist_elec/diametre)**2) 
                    topo_end[i,2]+=diametre*(1-(dist_elec/diametre)**2) 
                    topo_inh[i,2]+=diametre*(1-(dist_elec/diametre)**2)
                #print(topo[i,2])    
        
        return topo,topo_end,topo_inh
    
    ###CA1
    init_CA1=[[0,16],[-3.5,16],[-8,15.5],[-12,14],[-15,12],[-19,9],[-21.5,4.6],[-22,-0.15],[-21,-4],[-19,-9],[-17,-12],[-13.8,-15],[-9,-17],[-6,-18]]
    end_CA1=[[0,9],[-2,8.5],[-4,7],[-5.8,5.6],[-7,4],[-7.9,2],[-8,0.25],[-8,-1],[-7.75,-2],[-7.5,-2.5],[-6,-4],[-4.5,-5.5],[-2,-7.25],[0,-8.5]]
    init_CA1=array(init_CA1)
    end_CA1=array(end_CA1)

    ###DG
    end_DG=[[4.5,3.6],[4.75,3],[5,2.5],[5.7,1.75],[6,1.4],[7.3,0.6],[9,0.5],[10,0.4],[10.9,0.6],[11.6,1.4],[12.5,2.25],[13,3],[12.75,3.5],[12.5,4]]
    init_DG=[[0.5,7],[-1.5,5.5],[-4,3],[-3.7,0],[-1.5,-4],[2,-6],[5.4,-7],[10,-7.2],[13.5,-6],[16,-2.8],[17,1],[18,4],[16.5,6.5],[13.5,7.5]]
    init_DG=array(init_DG)
    end_DG=array(end_DG)

    ###CA3
    init_CA3=[[3,15.5],[5,14.75],[6.5,14],[8,12.8],[9.5,11],[10.5,7.5],[10.8,4.5],[10,2]]
    end_CA3=[[2,9],[3,8.9],[4,8.5],[4.75,8],[5.5,7.5],[6,6],[6.5,5.25],[7,4.5]]
    init_CA3=array(init_CA3)
    end_CA3=array(end_CA3)
    
    ###EC  
    init_EC=[[5,-21],[6.6,-21],[8.3,-21],[10,-21],[11,-21.8],[12,-22.8],[13,-25],[13.3,-27],[13.6,-29],[14,-32],[13.6,-35],[13.3,-37],[13,-40],[12,-42.5],[11,-44],[10,-45],[8,-45],[6,-45],[4,-45],[2,-45],[0,-45],[-2,-45],[-4,-45],[-6,-45],[-8,-45],[-10,-45]]
    end_EC=[[6,-10.5],[7.3,-10.5],[8.6,-10.5],[10,-10.5],[13.5,-11],[16.5,-13],[19,-16],[21.5,-20],[23,-25],[24,-32],[23.2,-38],[22.2,-44],[20.4,-49],[17,-52.5],[14,-54],[11,-55],[8,-55],[6,-55],[4,-55],[2,-55],[0,-55],[-2,-55],[-4,-55],[-6,-55],[-8,-55],[-10,-55]]
    init_EC=array(init_EC)
    end_EC=array(end_EC)

    all_pos=[[],[],[],[]]

    if types[0]==1 and types[1]==1:
        N_ECe,N_DGe,N_CA3e,N_CA1e,N_ECi,N_DGi,N_CA3i,N_CA1i=all_N
#        print(all_N)
        CA1_e,CA1_e_end,CA1_e_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e,(0.1,0.7))
        CA1_i,CA1_i_end,CA1_i_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i,(0,0.1))
        CA3_e,CA3_e_end,CA3_e_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e,(0.1,0.6))
        CA3_i,CA3_i_end,CA3_i_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i,(0,0.1))
        DG_e,DG_e_end,DG_e_inh=topo_one_pop(init_DG,end_DG,N_DGe,(0.1,0.6))
        DG_i,DG_i_end,DG_i_inh=topo_one_pop(init_DG,end_DG,N_DGi,(0,0.1))
        EC_e,EC_e_end,EC_e_inh=topo_one_pop(init_EC,end_EC,N_ECe,(0.1,0.6))
        EC_i,EC_i_end,EC_i_inh=topo_one_pop(init_EC,end_EC,N_ECi,(0,0.1))
        all_pos[0]=[EC_e,EC_e_end,EC_e_inh,EC_i,EC_i_end,EC_i_inh]
        all_pos[1]=[DG_e,DG_e_end,DG_e_inh,DG_i,DG_i_end,DG_i_inh]
        all_pos[2]=[CA3_e,CA3_e_end,CA3_e_inh,CA3_i,CA3_i_end,CA3_i_inh]
        all_pos[3]=[CA1_e,CA1_e_end,CA1_e_inh,CA1_i,CA1_i_end,CA1_i_inh]
    elif types[0]==2 and types[1]==1:
        N_ECe1,N_DGe1,N_CA3e1,N_CA1e1,N_ECe2,N_DGe2,N_CA3e2,N_CA1e2,N_ECi,N_DGi,N_CA3i,N_CA1i=all_N             
        CA1_e1,CA1_e1_end,CA1_e1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e1,(0.1,0.7))
        CA1_e2,CA1_e2_end,CA1_e2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e2,(0.1,0.7)) 
        CA1_i,CA1_i_end,CA1_i_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i,(0,0.1))
        CA3_e1,CA3_e1_end,CA3_e1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e1,(0.1,0.6))
        CA3_e2,CA3_e2_end,CA3_e2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e2,(0.1,0.6)) 
        CA3_i,CA3_i_end,CA3_i_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i,(0,0.1))
        DG_e1,DG_e1_end,DG_e1_inh=topo_one_pop(init_DG,end_DG,N_DGe1,(0.1,0.6))
        DG_e2,DG_e2_end,DG_e2_inh=topo_one_pop(init_DG,end_DG,N_DGe2,(0.1,0.6)) 
        DG_i,DG_i_end,DG_i_inh=topo_one_pop(init_DG,end_DG,N_DGi,(0,0.1))
        EC_e1,EC_e1_end,EC_e1_inh=topo_one_pop(init_EC,end_EC,N_ECe1,(0.1,0.6))
        EC_e2,EC_e2_end,EC_e2_inh=topo_one_pop(init_EC,end_EC,N_ECe2,(0.1,0.6)) 
        EC_i,EC_i_end,EC_i_inh=topo_one_pop(init_EC,end_EC,N_ECi,(0,0.1))
        all_pos[0]=[EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i,EC_i_end,EC_i_inh]
        all_pos[1]=[DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i,DG_i_end,DG_i_inh]
        all_pos[2]=[CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i,CA3_i_end,CA3_i_inh]
        all_pos[3]=[CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i,CA1_i_end,CA1_i_inh]
        
    elif types[0]==1 and types[1]==2:
        N_ECe,N_DGe,N_CA3e,N_CA1e,N_ECi1,N_DGi1,N_CA3i1,N_CA1i1,N_ECi2,N_DGi2,N_CA3i2,N_CA1i2=all_N                                        
        CA1_e,CA1_e_end,CA1_e_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e,(0.1,0.7))       
        CA1_i1,CA1_i1_end,CA1_i1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i1,(0,0.1))
        CA1_i2,CA1_i2_end,CA1_i2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i2,(0,0.1))
        CA3_e,CA3_e_end,CA3_e_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e,(0.1,0.6))       
        CA3_i1,CA3_i1_end,CA3_i1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i1,(0,0.1))
        CA3_i2,CA3_i2_end,CA3_i2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i2,(0,0.1))
        DG_e,DG_e_end,DG_e_inh=topo_one_pop(init_DG,end_DG,N_DGe,(0.1,0.6))       
        DG_i1,DG_i1_end,DG_i1_inh=topo_one_pop(init_DG,end_DG,N_DGi1,(0,0.1))
        DG_i2,DG_i2_end,DG_i2_inh=topo_one_pop(init_DG,end_DG,N_DGi2,(0,0.1))
        EC_e,EC_e_end,EC_e_inh=topo_one_pop(init_EC,end_EC,N_ECe,(0.1,0.6))       
        EC_i1,EC_i1_end,EC_i1_inh=topo_one_pop(init_EC,end_EC,N_ECi1,(0,0.1))
        EC_i2,EC_i2_end,EC_i2_inh=topo_one_pop(init_EC,end_EC,N_ECi2,(0,0.1))
        all_pos[0]=[EC_e,EC_e_end,EC_e_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh]
        all_pos[1]=[DG_e,DG_e_end,DG_e_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh]
        all_pos[2]=[CA3_e,CA3_e_end,CA3_e_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh]
        all_pos[3]=[CA1_e,CA1_e_end,CA1_e_inh,CA1_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh]

    else:
        N_ECe1,N_DGe1,N_CA3e1,N_CA1e1,N_ECe2,N_DGe2,N_CA3e2,N_CA1e2,N_ECi1,N_DGi1,N_CA3i1,N_CA1i1,N_ECi2,N_DGi2,N_CA3i2,N_CA1i2=all_N    
#        print(N_ECe1,N_DGe1,N_CA3e1,N_CA1e1,N_ECe2,N_DGe2,N_CA3e2,N_CA1e2,N_ECi1,N_DGi1,N_CA3i1,N_CA1i1,N_ECi2,N_DGi2,N_CA3i2,N_CA1i2)            
        CA1_e1,CA1_e1_end,CA1_e1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e1,(0.1,0.7))
        CA1_e2,CA1_e2_end,CA1_e2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e2,(0.1,0.7))        
        CA1_i1,CA1_i1_end,CA1_i1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i1,(0,0.1))
        CA1_i2,CA1_i2_end,CA1_i2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i2,(0,0.1))
        CA3_e1,CA3_e1_end,CA3_e1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e1,(0.1,0.6))
        CA3_e2,CA3_e2_end,CA3_e2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e2,(0.1,0.6))        
        CA3_i1,CA3_i1_end,CA3_i1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i1,(0,0.1))
        CA3_i2,CA3_i2_end,CA3_i2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i2,(0,0.1))
        DG_e1,DG_e1_end,DG_e1_inh=topo_one_pop(init_DG,end_DG,N_DGe1,(0.1,0.6))
        DG_e2,DG_e2_end,DG_e2_inh=topo_one_pop(init_DG,end_DG,N_DGe2,(0.1,0.6))        
        DG_i1,DG_i1_end,DG_i1_inh=topo_one_pop(init_DG,end_DG,N_DGi1,(0,0.1))
        DG_i2,DG_i2_end,DG_i2_inh=topo_one_pop(init_DG,end_DG,N_DGi2,(0,0.1))
        EC_e1,EC_e1_end,EC_e1_inh=topo_one_pop(init_EC,end_EC,N_ECe1,(0.1,0.6))
        EC_e2,EC_e2_end,EC_e2_inh=topo_one_pop(init_EC,end_EC,N_ECe2,(0.1,0.6))        
        EC_i1,EC_i1_end,EC_i1_inh=topo_one_pop(init_EC,end_EC,N_ECi1,(0,0.1))
        EC_i2,EC_i2_end,EC_i2_inh=topo_one_pop(init_EC,end_EC,N_ECi2,(0,0.1))
        all_pos[0]=[EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh]
        all_pos[1]=[DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh]
        all_pos[2]=[CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh]
        all_pos[3]=[CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh]
#
#    figure(figsize=(10,8))
#    subplot(111, projection='3d')
#    couleurs_exc=['k','r','g','b']
#    couleurs_inh=['w','m','y','c']
#    for region in range(3,-1,-1):
#        for n_exc in range(types[0]):
#            plot(all_pos[region][3*n_exc][:,0],all_pos[region][3*n_exc][:,1],all_pos[region][3*n_exc][:,2],'o',color=couleurs_exc[region])
#        for n_inh in range(types[1]):
#            plot(all_pos[region][3*types[0]+3*n_inh][:,0],all_pos[region][3*types[0]+3*n_inh][:,1],all_pos[region][3*types[0]+3*n_inh][:,2],'o',color=couleurs_inh[region])    
#    plot(elec_array[:,0],elec_array[:,1],elec_array[:,2],'y+')
#    print(elec[0],elec[-1])
    return(all_pos, elec_array) 
    
    
#temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9,temp10,temp11,temp12,temp13,temp14,temp15,temp16,temp17,temp18,temp19,temp20,temp21,elec_pos=topologie(1000,100,10,0.95, True)   
#temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9,temp10,temp11,temp12,temp13,temp14,temp15,temp16,temp17,temp18,temp19,temp20,temp21,temp22,temp23,temp24,temp25,temp26,temp27,temp28,elec_pos=topologie(10000,1000,100,1, False)

def topologie_rectangle(types,all_N):
#    print('rectangle')
    
    depart_electrode=array([-21, 0, 50])
    arrivee_electrode=array([15, 0, 50])
    len_elec=norm(arrivee_electrode-depart_electrode)
#    print(len_elec*150*umetre)
    dir_elec=(arrivee_electrode-depart_electrode)/norm(arrivee_electrode-depart_electrode)
    elec=[]
    #psi = arccos(dot(depart_electrode[:-1],arrivee_electrode[:-1])/(norm(depart_electrode[:-1])*norm(arrivee_electrode[:-1])))
    psi = arccos(dot(dir_elec,array([0,1,0])))
    diametre = 400/150 #en fait c'est un rayon
    for t in linspace(0,1,33):
        centre=(1-t)*depart_electrode+t*arrivee_electrode
        #print(centre)
        for theta in arange(0,2*pi,pi/6):
            point=[centre[0]+diametre*cos(theta)*cos(psi),centre[1]-diametre*cos(theta)*sin(psi),centre[2]+diametre*sin(theta)]
            #print(point)
            elec.append(point)
    elec_array=array(elec[:144]+elec[252:])
    
    def topo_one_pop(init_segs,end_segs,N,i_soma): #donne la position du soma (pour le calcul de Im) et des dendrites (pour Isyn)
        seg=randint(0,len(init_segs))
        t=uniform(i_soma[0],i_soma[1])
        all_t=zeros(int(N))
        all_z=zeros(int(N))
        all_t[0]=seg
        z=100*random()
        all_z[0]=z
        topo=append((1-t)*init_segs[seg]  + t * end_segs[seg],z)
        topo_end=append(end_segs[seg],z)
        topo_inh=append(init_segs[seg],z)
        
        for i in range(int(N-1)):
            seg=randint(0,len(init_segs)-1)
            t=random()
            init=t*init_segs[seg]+(1-t)*init_segs[seg+1]
            all_t[i]=seg+t
            end=t*end_segs[seg]+(1-t)*end_segs[seg+1] #les dendrites sont positionnées en "end"
            t2=uniform(i_soma[0],i_soma[1]) #le soma est dans la "première moitié" de la couche de neurones
            z=100*random()
            all_z[i]=z
            coords=append((1 - t2)*init  + t2 * end,z)
            topo=vstack((topo,coords)) 
            topo_end=vstack((topo_end,append(end,z))) 
            topo_inh=vstack((topo_inh,append(0.9*init+0.1*end,z))) 
        sort_index=argsort(all_t)
        topo=topo[sort_index]
        topo_end=topo_end[sort_index]
        topo_inh=topo_inh[sort_index]
        all_z=all_z[sort_index]
        sort_index2=argsort(all_z)
        topo=topo[sort_index2]
        topo_end=topo_end[sort_index2]
        topo_inh=topo_inh[sort_index2]
        #Décalage vertical pour tenir compte de l'électrode :
        for i in range(int(N)):
            x=topo[i,0]
            y=topo[i,1]
            z=topo[i,2]
            dist_elec=norm(cross((array([x,y,50])-depart_electrode),dir_elec))
            if dist_elec<diametre/2:
                #print("distance inférieure")
                #print(topo[i,2])  
                if z<50:
                    topo[i,2]-=diametre*(1-(dist_elec/diametre)**2)
                    topo_end[i,2]-=diametre*(1-(dist_elec/diametre)**2)
                    topo_inh[i,2]-=diametre*(1-(dist_elec/diametre)**2)
                else :
                    topo[i,2]+=diametre*(1-(dist_elec/diametre)**2) 
                    topo_end[i,2]+=diametre*(1-(dist_elec/diametre)**2) 
                    topo_inh[i,2]+=diametre*(1-(dist_elec/diametre)**2)
                #print(topo[i,2])    
        
        return topo,topo_end,topo_inh
    ###CA1
    init_CA1=[[-20,-15],[-20,5]]
    end_CA1=[[-5,-15],[-5,5]]
    init_CA1=array(init_CA1)
    end_CA1=array(end_CA1)
    
    ###DG
    
    init_DG=[[0,-20],[15,-20]]
    end_DG=[[0,-5],[15,-5]]
    init_DG=array(init_DG)
    end_DG=array(end_DG)

    ###CA3
    
    init_CA3=[[0,0],[15,0]]
    end_CA3=[[0,10],[15,10]]
    init_CA3=array(init_CA3)
    end_CA3=array(end_CA3)

    ###EC
    
    init_EC=[[-5,-40],[15,-40]]
    end_EC=[[-5,-22],[15,-22]]
    init_EC=array(init_EC)
    end_EC=array(end_EC)

    all_pos=[[],[],[],[]]

    if types[0]==1 and types[1]==1:
        N_ECe,N_DGe,N_CA3e,N_CA1e,N_ECi,N_DGi,N_CA3i,N_CA1i=all_N
#        print(all_N)
        CA1_e,CA1_e_end,CA1_e_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e,(0.1,0.7))
        CA1_i,CA1_i_end,CA1_i_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i,(0,0.1))
        CA3_e,CA3_e_end,CA3_e_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e,(0.1,0.6))
        CA3_i,CA3_i_end,CA3_i_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i,(0,0.1))
        DG_e,DG_e_end,DG_e_inh=topo_one_pop(init_DG,end_DG,N_DGe,(0.1,0.6))
        DG_i,DG_i_end,DG_i_inh=topo_one_pop(init_DG,end_DG,N_DGi,(0,0.1))
        EC_e,EC_e_end,EC_e_inh=topo_one_pop(init_EC,end_EC,N_ECe,(0.1,0.6))
        EC_i,EC_i_end,EC_i_inh=topo_one_pop(init_EC,end_EC,N_ECi,(0,0.1))
        all_pos[0]=[EC_e,EC_e_end,EC_e_inh,EC_i,EC_i_end,EC_i_inh]
        all_pos[1]=[DG_e,DG_e_end,DG_e_inh,DG_i,DG_i_end,DG_i_inh]
        all_pos[2]=[CA3_e,CA3_e_end,CA3_e_inh,CA3_i,CA3_i_end,CA3_i_inh]
        all_pos[3]=[CA1_e,CA1_e_end,CA1_e_inh,CA1_i,CA1_i_end,CA1_i_inh]
    elif types[0]==2 and types[1]==1:
        N_ECe1,N_ECe2,N_DGe1,N_DGe2,N_CA3e1,N_CA3e2,N_CA1e1,N_CA1e2,N_ECi,N_DGi,N_CA3i,N_CA1i=all_N                
        CA1_e1,CA1_e1_end,CA1_e1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e1,(0.1,0.7))
        CA1_e2,CA1_e2_end,CA1_e2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e2,(0.1,0.7)) 
        CA1_i,CA1_i_end,CA1_i_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i,(0,0.1))
        CA3_e1,CA3_e1_end,CA3_e1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e1,(0.1,0.6))
        CA3_e2,CA3_e2_end,CA3_e2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e2,(0.1,0.6)) 
        CA3_i,CA3_i_end,CA3_i_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i,(0,0.1))
        DG_e1,DG_e1_end,DG_e1_inh=topo_one_pop(init_DG,end_DG,N_DGe1,(0.1,0.6))
        DG_e2,DG_e2_end,DG_e2_inh=topo_one_pop(init_DG,end_DG,N_DGe2,(0.1,0.6)) 
        DG_i,DG_i_end,DG_i_inh=topo_one_pop(init_DG,end_DG,N_DGi,(0,0.1))
        EC_e1,EC_e1_end,EC_e1_inh=topo_one_pop(init_EC,end_EC,N_ECe1,(0.1,0.6))
        EC_e2,EC_e2_end,EC_e2_inh=topo_one_pop(init_EC,end_EC,N_ECe2,(0.1,0.6)) 
        EC_i,EC_i_end,EC_i_inh=topo_one_pop(init_EC,end_EC,N_ECi,(0,0.1))
        all_pos[0]=[EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i,EC_i_end,EC_i_inh]
        all_pos[1]=[DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i,DG_i_end,DG_i_inh]
        all_pos[2]=[CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i,CA3_i_end,CA3_i_inh]
        all_pos[3]=[CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i,CA1_i_end,CA1_i_inh]
        
    elif types[0]==1 and types[1]==2:
        N_ECe,N_DGe,N_CA3e,N_CA1e,N_ECi1,N_ECi2,N_DGi1,N_DGi2,N_CA3i1,N_CA3i2,N_CA1i1,N_CA1i2=all_N                                        
        CA1_e,CA1_e_end,CA1_e_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e,(0.1,0.7))       
        CA1_i1,CA1_i1_end,CA1_i1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i1,(0,0.1))
        CA1_i2,CA1_i2_end,CA1_i2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i2,(0,0.1))
        CA3_e,CA3_e_end,CA3_e_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e,(0.1,0.6))       
        CA3_i1,CA3_i1_end,CA3_i1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i1,(0,0.1))
        CA3_i2,CA3_i2_end,CA3_i2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i2,(0,0.1))
        DG_e,DG_e_end,DG_e_inh=topo_one_pop(init_DG,end_DG,N_DGe,(0.1,0.6))       
        DG_i1,DG_i1_end,DG_i1_inh=topo_one_pop(init_DG,end_DG,N_DGi1,(0,0.1))
        DG_i2,DG_i2_end,DG_i2_inh=topo_one_pop(init_DG,end_DG,N_DGi2,(0,0.1))
        EC_e,EC_e_end,EC_e_inh=topo_one_pop(init_EC,end_EC,N_ECe,(0.1,0.6))       
        EC_i1,EC_i1_end,EC_i1_inh=topo_one_pop(init_EC,end_EC,N_ECi1,(0,0.1))
        EC_i2,EC_i2_end,EC_i2_inh=topo_one_pop(init_EC,end_EC,N_ECi2,(0,0.1))
        all_pos[0]=[EC_e,EC_e_end,EC_e_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh]
        all_pos[1]=[DG_e,DG_e_end,DG_e_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh]
        all_pos[2]=[CA3_e,CA3_e_end,CA3_e_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh]
        all_pos[3]=[CA1_e,CA1_e_end,CA1_e_inh,CA1_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh]

    else:
        N_ECe1,N_ECe2,N_DGe1,N_DGe2,N_CA3e1,N_CA3e2,N_CA1e1,N_CA1e2,N_ECi1,N_ECi2,N_DGi1,N_DGi2,N_CA3i1,N_CA3i2,N_CA1i1,N_CA1i2=all_N                
        CA1_e1,CA1_e1_end,CA1_e1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e1,(0.1,0.7))
        CA1_e2,CA1_e2_end,CA1_e2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1e2,(0.1,0.7))        
        CA1_i1,CA1_i1_end,CA1_i1_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i1,(0,0.1))
        CA1_i2,CA1_i2_end,CA1_i2_inh=topo_one_pop(init_CA1,end_CA1,N_CA1i2,(0,0.1))
        CA3_e1,CA3_e1_end,CA3_e1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e1,(0.1,0.6))
        CA3_e2,CA3_e2_end,CA3_e2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3e2,(0.1,0.6))        
        CA3_i1,CA3_i1_end,CA3_i1_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i1,(0,0.1))
        CA3_i2,CA3_i2_end,CA3_i2_inh=topo_one_pop(init_CA3,end_CA3,N_CA3i2,(0,0.1))
        DG_e1,DG_e1_end,DG_e1_inh=topo_one_pop(init_DG,end_DG,N_DGe1,(0.1,0.6))
        DG_e2,DG_e2_end,DG_e2_inh=topo_one_pop(init_DG,end_DG,N_DGe2,(0.1,0.6))        
        DG_i1,DG_i1_end,DG_i1_inh=topo_one_pop(init_DG,end_DG,N_DGi1,(0,0.1))
        DG_i2,DG_i2_end,DG_i2_inh=topo_one_pop(init_DG,end_DG,N_DGi2,(0,0.1))
        EC_e1,EC_e1_end,EC_e1_inh=topo_one_pop(init_EC,end_EC,N_ECe1,(0.1,0.6))
        EC_e2,EC_e2_end,EC_e2_inh=topo_one_pop(init_EC,end_EC,N_ECe2,(0.1,0.6))        
        EC_i1,EC_i1_end,EC_i1_inh=topo_one_pop(init_EC,end_EC,N_ECi1,(0,0.1))
        EC_i2,EC_i2_end,EC_i2_inh=topo_one_pop(init_EC,end_EC,N_ECi2,(0,0.1))
        all_pos[0]=[EC_e1,EC_e1_end,EC_e1_inh,EC_e2,EC_e2_end,EC_e2_inh,EC_i1,EC_i1_end,EC_i1_inh,EC_i2,EC_i2_end,EC_i2_inh]
        all_pos[1]=[DG_e1,DG_e1_end,DG_e1_inh,DG_e2,DG_e2_end,DG_e2_inh,DG_i1,DG_i1_end,DG_i1_inh,DG_i2,DG_i2_end,DG_i2_inh]
        all_pos[2]=[CA3_e1,CA3_e1_end,CA3_e1_inh,CA3_e2,CA3_e2_end,CA3_e2_inh,CA3_i1,CA3_i1_end,CA3_i1_inh,CA3_i2,CA3_i2_end,CA3_i2_inh]
        all_pos[3]=[CA1_e1,CA1_e1_end,CA1_e1_inh,CA1_e2,CA1_e2_end,CA1_e2_inh,CA1_i1,CA1_i1_end,CA1_i1_inh,CA1_i2,CA1_i2_end,CA1_i2_inh]

#    figure(figsize=(10,8))
#    subplot(111, projection='3d')
#    couleurs_exc=['k','r','g','b']
#    couleurs_inh=['w','m','y','c']
#    for region in range(3,-1,-1):
#        for n_exc in range(types[0]):
#            plot(all_pos[region][3*n_exc][:,0],all_pos[region][3*n_exc][:,1],all_pos[region][3*n_exc][:,2],'o',color=couleurs_exc[region])
#        for n_inh in range(types[1]):
#            plot(all_pos[region][3*types[0]+3*n_inh][:,0],all_pos[region][3*types[0]+3*n_inh][:,1],all_pos[region][3*types[0]+3*n_inh][:,2],'o',color=couleurs_inh[region])
#  
#    figure(figsize=(10,8))
#    for region in range(3,-1,-1):
#        for n_exc in range(types[0]):
#            plot(all_pos[region][3*n_exc][:,0],all_pos[region][3*n_exc][:,1],'o',color=[0.6,0.6,0.6])
#        for n_inh in range(types[1]):
#            plot(all_pos[region][3*types[0]+3*n_inh][:,0],all_pos[region][3*types[0]+3*n_inh][:,1],'o',color=[0.2,0.2,0.2])
#       
    
    return(all_pos, elec) 


def topologie_NC():   
    
    def topo_one_pop(hmin,hmax,N): #donne la position du soma (pour le calcul de Im) et des dendrites (pour Isyn)
        z=uniform(hmin,hmax)
        L=15*50/150
        x,y=-50+uniform(0,L),-50+uniform(0,L)
        all_x=zeros(int(N))
        all_x[0]=x
        topo=array([x,y,z])
        topo_end=array([x,y,hmax])
        topo_inh=array([x,y,hmin])
        
        for i in range(int(N-1)):
            z=uniform(hmin,hmax)
            x,y=-50+uniform(0,L),-50+uniform(0,L)
            all_x[i+1]=x
            coords=array([x,y,z])
            topo=vstack((topo,coords)) 
            topo_end=vstack((topo_end,[x,y,hmax])) 
            topo_inh=vstack((topo_inh,[x,y,hmin])) 
        sort_index=argsort(all_x)
        topo=topo[sort_index]
        topo_end=topo_end[sort_index]
        topo_inh=topo_inh[sort_index]
        
        return topo,topo_end,topo_inh
    
    hL1=-128/150
    hL2=-269/150
    hL3=-418/150
    hL4=-588/150
    hL5a=-708/150
    hL5b=-890/150
    hL6=-1154/150
    
    #L2/3
    L23_py,L23_py_end,L23_py_inh=topo_one_pop(hL3,hL1,10000)
    L23_inh,L23_inh_end,L23_inh_inh=topo_one_pop(hL3,hL1,2500)  
    
    #L4
    L4_py,L4_py_end,L4_py_inh=topo_one_pop(hL4,hL3,10000)
    L4_inh,L4_inh_end,L4_inh_inh=topo_one_pop(hL4,hL3,2500)   
      
    #L5
    L5_py,L5_py_end,L5_py_inh=topo_one_pop(hL5b,hL4,2500)
    L5_inh,L5_inh_end,L5_inh_inh=topo_one_pop(hL5b,hL4,500) 
    
    #L6
    L6_py,L6_py_end,L6_py_inh=topo_one_pop(hL6,hL5b,7500)
    L6_inh,L6_inh_end,L6_inh_inh=topo_one_pop(hL6,hL5b,1500)  

    
    return(L23_py,L23_py_end,L23_py_inh,L23_inh,L4_py,L4_py_end,L4_py_inh,L4_inh,L5_py,L5_py_end,L5_py_inh,L5_inh,L6_py,L6_py_end,L6_py_inh,L6_inh) 
        
