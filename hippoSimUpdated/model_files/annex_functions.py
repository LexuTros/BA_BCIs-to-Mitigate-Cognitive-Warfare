#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from numpy import savetxt

def make_flat(liste):
    new_liste=[]
    for elem in liste :
        if type(elem)==list:
            elem_flat=make_flat(elem)
            new_liste+=elem_flat
        else :
            new_liste.append(elem)
    return new_liste

def timedarray2array(t_array,tmax,dt):
    t,ind=0*second,0
    res_array=zeros((int(tmax/dt),1))
    while t<tmax:
        res_array[ind]=t_array(t)
        t+=dt
        ind+=1
    return res_array
    
def send_file(liste_fichiers,sprouting,lesion,cell_loss):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    fromaddr = "amelie.aussel.pro@gmail.com"
    toaddr = "amelaussel@yahoo.fr"
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Resultat de la simulation "+str(liste_fichiers[0])+" sur LabLady"
    
    body = "Parametres :\n sprouting=%.2f \n lesion=%s \n cell_loss=%.2f " %(sprouting,lesion,cell_loss)
    
    msg.attach(MIMEText(body, 'plain'))
    
    for fichier in liste_fichiers:
        filename = fichier
        #print(fichier)
        attachment = open(fichier, "rb")
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        #print("filename= %s" % str(filename))
        part.add_header('Content-Disposition', "attachment; filename= %s" % str(filename))
        
        msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Coton2694")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()  


def save_pos(types,all_pos,path):
    os.mkdir(path+'/positions')
    zone_names=['EC','DG','CA3','CA1']
    if types[0]==1 and types[1]==1:
        types_names=['exc','inh']
    elif types[0]==2 and types[1]==1:
        types_names=['exc1','exc2','inh']
    elif types[0]==1 and types[1]==2:
        types_names=['exc','inh1','inh2']
    else :
        types_names=['exc1','exc2','inh1','inh2']
        
    for region in range(4):
        for i_type in range(types[0]+types[1]):
            pos_file=open(path+'/positions/positions_'+zone_names[region]+'_'+types_names[i_type]+'.txt','w')
            for elem in all_pos[region][i_type] :
                pos_file.write(str(elem))
                pos_file.write(',')
                pos_file.write('\n')
            pos_file.close()
            
def save_dir(types,all_dir,path):
    os.mkdir(path+'/directions')
    zone_names=['EC','DG','CA3','CA1']
    if types[0]==1 and types[1]==1:
        types_names=['exc','inh']
    elif types[0]==2 and types[1]==1:
        types_names=['exc1','exc2','inh']
    elif types[0]==1 and types[1]==2:
        types_names=['exc','inh1','inh2']
    else :
        types_names=['exc1','exc2','inh1','inh2']
        
    for region in range(4):
        for i_type in range(types[0]+types[1]):
            pos_file=open(path+'/directions/directions_'+zone_names[region]+'_'+types_names[i_type]+'.txt','w')
            for elem in all_dir[region][i_type] :
                pos_file.write(str(elem))
                pos_file.write(',')
                pos_file.write('\n')
            pos_file.close()


def save_raster(types,all_raster_i_exc,all_raster_i_inh,all_raster_t_exc,all_raster_t_inh,path):
    print('Saving rasters')
    os.mkdir(path+'/rasters')
    zone_names=['EC','DG','CA3','CA1']
    if types[0]==1 and types[1]==1:
        types_names=['exc','inh']
    elif types[0]==2 and types[1]==1:
        types_names=['exc1','exc2','inh']
    elif types[0]==1 and types[1]==2:
        types_names=['exc','inh1','inh2']
    else :
        types_names=['exc1','exc2','inh1','inh2']
        
    for region in [0,1,2,3]:
        for i_type in range(types[0]):
            raster_file=open(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[i_type]+'_i.txt','w')
            for subraster in all_raster_i_exc[region][i_type] :
                for elem in subraster:
                    #print(elem)
                    raster_file.write(str(elem)+',')
            raster_file.close()
            #savetxt(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[i_type]+'_i.txt', all_raster_i_exc[region][i_type], delimiter=',')
            raster_file=open(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[i_type]+'_t.txt','w')
            for subraster in all_raster_t_exc[region][i_type] :
                for elem in subraster:
                    raster_file.write(str(elem)+',')
            raster_file.close()
            #savetxt(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[i_type]+'_t.txt', all_raster_t_exc[region][i_type], delimiter=',')
        for i_type in range(types[1]):
            raster_file=open(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[types[0]+i_type]+'_i.txt','w')
            for subraster in all_raster_i_inh[region][i_type] :
                for elem in subraster:
                    raster_file.write(str(elem)+',')
            raster_file.close()
            #savetxt(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[types[0]+i_type]+'_i.txt', all_raster_i_inh[region][i_type], delimiter=',')
            raster_file=open(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[types[0]+i_type]+'_t.txt','w')
            for subraster in all_raster_t_inh[region][i_type] :
                for elem in subraster:
                    raster_file.write(str(elem)+',')
            raster_file.close()
            #savetxt(path+'/rasters/raster_'+zone_names[region]+'_'+types_names[types[0]+i_type]+'_t.txt', all_raster_t_inh[region][i_type], delimiter=',')
    return

def save_syn(CA1_EcI,CA1_IEc,CA1_II,CA3_EcI,CA3_IEc,CA3_EcEc,EC_EcI,EC_IEc,DG_EI,DG_IE,ECc_DG_E,ECc_DG_I,ECc_CA3c_E,ECc_CA3_I,ECc_CA1c_E,ECc_CA1_I,DG_CA3c_E,DG_CA3_I,CA3c_CA1c_E,CA3c_CA1_I,CA1c_ECc_E,CA1c_EC_I):
    
    syn_file=open('syn_CA1_EI.txt','w')
    for elem in CA1_EcI.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA1_EcI.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')          
    syn_file.close()
    
    syn_file=open('syn_CA1_IE.txt','w')
    for elem in CA1_IEc.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA1_IEc.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()

    syn_file=open('syn_CA1_II.txt','w')
    for elem in CA1_II.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA1_II.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()
    
    
    syn_file=open('syn_CA3_EI.txt','w')
    for elem in CA3_EcI.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA3_EcI.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_CA3_IE.txt','w')
    for elem in CA3_IEc.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA3_IEc.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()

    syn_file=open('syn_CA3_EE.txt','w')
    for elem in CA3_EcEc.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA3_EcEc.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()    
    
    
    syn_file=open('syn_EC_EI.txt','w')
    for elem in EC_EcI.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in EC_EcI.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_EC_IE.txt','w')
    for elem in EC_IEc.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in EC_IEc.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()
    

    syn_file=open('syn_DG_EI.txt','w')
    for elem in DG_EI.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in DG_EI.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_DG_IE.txt','w')
    for elem in DG_IE.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in DG_IE.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()

 
    syn_file=open('syn_EC_E_DG_E.txt','w')
    for elem in ECc_DG_E.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in ECc_DG_E.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_EC_E_DG_I.txt','w')
    for elem in ECc_DG_I.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in ECc_DG_I.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()    
    
    syn_file=open('syn_EC_E_CA3_E.txt','w')
    for elem in ECc_CA3c_E.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in ECc_CA3c_E.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_EC_E_CA3_I.txt','w')
    for elem in ECc_CA3_I.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in ECc_CA3_I.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()      

    
    syn_file=open('syn_EC_E_CA1_E.txt','w')
    for elem in ECc_CA1c_E.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in ECc_CA1c_E.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_EC_E_CA1_I.txt','w')
    for elem in ECc_CA1_I.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in ECc_CA1_I.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close() 
    
    syn_file=open('syn_DG_E_CA3_E.txt','w')
    for elem in DG_CA3c_E.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in DG_CA3c_E.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_DG_E_CA3_I.txt','w')
    for elem in DG_CA3_I.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in DG_CA3_I.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()   
    
    syn_file=open('syn_CA3_E_CA1_E.txt','w')
    for elem in CA3c_CA1c_E.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA3c_CA1c_E.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_CA3_E_CA1_I.txt','w')
    for elem in CA3c_CA1_I.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA3c_CA1_I.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()    
    
    syn_file=open('syn_CA1_E_EC_E.txt','w')
    for elem in CA1c_ECc_E.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA1c_ECc_E.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',')         
    syn_file.close()
    
    syn_file=open('syn_CA1_E_EC_I.txt','w')
    for elem in CA1c_EC_I.i:
        syn_file.write(str(int(elem)))
        syn_file.write(',')
    syn_file.write('\n')  
    for elem in CA1c_EC_I.j:
        syn_file.write(str(int(elem)))
        syn_file.write(',') 
    syn_file.close()   
    

def save_params(liste_params,liste_params_names,path):
    param_file=open(path+'/parameters.txt','w')
    for i in range(len(liste_params)):
        param_file.write(liste_params_names[i]+': '+str(liste_params[i]))
        param_file.write('\n')
    param_file.close()
 
    
def ecriture_FR(nom,data,path): 
#    print(data)
    time_series=open(path+'/'+nom+'.txt','w')
    time_series.write('[')
    for n in data:
        time_series.write('%.2E,'%n)
    time_series.write(']\n')
    time_series.close()  
    
def save_FR(types,data_exc,data_inh,path,save_all_FR):
#    print(data_exc)
    os.mkdir(path+'/FR')
    
    if save_all_FR:
        zone_names=['EC','DG','CA3','CA1']
        if types[0]==1 and types[1]==1:
            types_names=['exc','inh']
        elif types[0]==2 and types[1]==1:
            types_names=['exc1','exc2','inh']
        elif types[0]==1 and types[1]==2:
            types_names=['exc','inh1','inh2']
        else :
            types_names=['exc1','exc2','inh1','inh2']
            
        for j in range(4):
            for i in range(types[0]):
    #            print(data_exc[j][i])
                ecriture_FR('FR_'+zone_names[j]+'_'+types_names[i],data_exc[j][i],path+'/FR')
            for i in range(types[1]):
                ecriture_FR('FR_'+zone_names[j]+'_'+types_names[i+types[0]],data_inh[j][i],path+'/FR')
    else :
        zone_names=['CA1']
        if types[0]==1:
            types_names=['exc']
        else :
            types_names=['exc1','exc2']
            
        for i in range(types[0]):
            ecriture_FR('FR_'+zone_names[0]+'_'+types_names[i],data_exc[0][i],path+'/FR')
