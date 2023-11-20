# -*- coding: utf-8 -*-
"""
Author: David Specht
Last Updated: 11/20/2023
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mpl_toolkits.axes_grid1 import Divider, Size

c = sns.color_palette("colorblind")

from matplotlib import rcParams
rcParams['font.family'] = 'Roboto'

def FigMaker(data, x, y, ylabel, ylim, xlabel, color, linthresh, ax_size, title, hline = '', xlim = '', xticks = '', plot_type = 'line', plotAvg1 = False, xlog=False, linthreshX = 0, hue = '', data2 = [], x2 = '', y2 = '', ylabel2 = '', ylim2 = '', color2 = '', plotAvg2 = False, marker2 = '.', linthresh2 = 1E-06):
    plt.rcParams['legend.markerscale'] = 1.8
    label_fontsize = 7
    tick_fontsize = 6
    s = 5
    linewidth = 1

    fig = plt.figure()
    
    h = [Size.Fixed(1), Size.Fixed(ax_size[0])]
    v = [Size.Fixed(1), Size.Fixed(ax_size[1])]

    divider = Divider(fig, (0.25, 0.25, 1, 1), h, v, aspect=False)
    # The width and height of the rectangle are ignored.
    ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))    
    
    if hue == '' and plot_type == 'bar':
        sns.barplot(data = data, x = x, y = y, color = color, errorbar = None) 
        sns.stripplot(data = data, x = x, y = y, s = 0.45*s, ax = ax, color = 'black', linewidth = 0, jitter = 0.1) #Why the fuck is stripplot dot scaling off?
    elif plot_type == 'bar':
        sns.barplot(data = data, x = x, y = y, color = color, errorbar = None, hue = hue, palette=[c[2],c[7]]) 
        sns.stripplot(data = data, x = x, y = y, s = 0.45*s, ax = ax, palette='dark:black', linewidth = 0, jitter = 0.1, hue = hue, dodge = True) #Why the fuck is stripplot dot scaling off?
        ax.get_legend().remove()

    plt.yscale('symlog', linthresh = linthresh)
    if xlog == True:
        plt.xscale('symlog', linthresh = linthreshX)
    ax.set_ylabel(ylabel, fontsize = label_fontsize)
    ax.set_xlabel(xlabel, fontsize = label_fontsize)
    ax.set_ylim(ylim)

    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    yticks = ax.yaxis.get_major_ticks()
    #yticks[1].set_visible(False)    
    
    avg_data = data.groupby([x]).mean(numeric_only = True)
    if plotAvg1 == True and hue == '':
        sns.lineplot(data = avg_data, x = x, y = y, linewidth = linewidth, color = color)
        temp = sns.scatterplot(data = data, x = x, y = y, s = 2*s, ax = ax, color = color, marker = '.', linewidth = 0)
    elif plot_type != 'bar':
        sns.lineplot(data = avg_data, x = x, y = y, linewidth = linewidth, color = color)        
    if len(data2)>0 and plot_type!='bar':
        ax2 = ax.twinx()
        temp = sns.scatterplot(data = data2, x = x2, y = y2, s = 2*s, ax = ax2, color = color2, marker = marker2, linewidth = 0)#???, err_style = 'bars')
        if plotAvg2 == True:
            avg_data2 = data2.groupby([x]).mean()
            sns.lineplot(data = avg_data2, x = x2, y = y2, linewidth = linewidth, color = color2)
        plt.yscale('symlog', linthresh = linthresh)
        ax2.set_ylabel(ylabel2, fontsize = label_fontsize)
        ax2.set_ylim(ylim2)
        ax2.set_xlabel(xlabel)
        ax.yaxis.get_label().set_color(color)    
        ax2.yaxis.get_label().set_color(color2)
        ax2.set_ylim(ylim2)
        plt.yticks(fontsize=tick_fontsize)
        ax.hlines(0, min(data[x]), max(data2[x2]), linestyle = 'dashed', linewidth = linewidth, color = 'black')
    elif plot_type != 'bar':
        ax.hlines(0, min(data[x]), max(data[x]), linestyle = 'dashed', linewidth = linewidth, color = 'black')
    elif plot_type == 'bar' and len(data2)>0:
        ax2 = ax.twinx()
        sns.stripplot(data = data2, x = x2, y = y2, s = 0.45*s, ax = ax2, color = color2, linewidth = 0, jitter = 0.1) #Stripplot dot scaling off?
        if plotAvg2 == True:
            avg_data2 = data2.groupby([x]).mean()
            sns.lineplot(data = avg_data2, x = [0,1,2,3,4,5,6,7,8,9], y = y2, linewidth = linewidth, color = c[1])
            
        plt.yscale('symlog', linthresh = linthresh2)
        ax2.set_ylabel(ylabel2, fontsize = label_fontsize)
        ax2.set_ylim(ylim2)
        #ax2.set_xlabel(xlabel)
        ax.yaxis.get_label().set_color(color)    
        ax2.yaxis.get_label().set_color(color2)
        ax2.set_ylim(ylim2)
        plt.yticks(fontsize=tick_fontsize)
        yticks = ax2.yaxis.get_major_ticks()
        yticks[1].set_visible(False)  
        yticks[-1].set_visible(False)
        yticks[-2].set_visible(False)  
        yticks[-3].set_visible(False)
        ax2.set_xlabel(xlabel, fontsize = label_fontsize)
        #ax.hlines(0, min(data[x]), max(data2[x2]), linestyle = 'dashed', linewidth = linewidth, color = 'black')        
    if hline!='':
        plt.axhline(y = hline, linestyle = 'dashed', linewidth = linewidth, color = c[1])
    if xticks != '':
        plt.xticks(xticks)
    plt.xticks(fontsize=tick_fontsize, rotation = 90)
    if xlim != '':
        plt.xlim(xlim)
    #plt.subplots_adjust(left=0.19)
    #plt.subplots_adjust(bottom=0.20)
    #plt.tight_layout()
    plt.savefig(title+'.svg', transparent = 'True')
    plt.savefig(title+'.png', dpi = 1000)

    #plt.figtext(0.5,0.3,'ND', fontsize = tick_fontsize)
    return

#--------------------------- Data ---------------------------
#Fig1Compare
Fig1_selective = np.array([0,0,0,4000,2000,6000, 50, 40, 60])
Fig1_nonselective = np.array([2.50E+06,4.60E+06,1.00E+06,3.50E+06,2.10E+06,5.70E+06, 3.30E+06, 3.60E+06, 2.10E+06])
Fig1_cfu_ug = np.array([0,0,0,368*4000, 368*2000, 368*6000, 280*50, 280*40, 280*60])

Fig1_freq = Fig1_selective/Fig1_nonselective
Fig1_Conc = pd.DataFrame({'Selected': Fig1_selective,'cfu_ug': Fig1_cfu_ug,'Unselected': Fig1_nonselective, 'Freq': Fig1_freq, 'Category':3*[' ']+3*['']+3*['   ']}) #3*['No VC tfoX']+3*['High Efficiency Transform.']+3*['0 Capital Transform.']

#Initial control experiment (will not be used in publication)
control_selected = np.array([3,22,4,0,0,0,2,0,1,4,3,4,0,0,0])
control_unselected = np.array([39E05,25E05,25E05,29E05, 26E05, 40E05,27E05, 26E05, 46E05,31E05, 31E05,30E05,36E05, 6E05, 43E05])
control_freq = control_selected/control_unselected
control = pd.DataFrame({'Selected': control_selected,'Unselected': control_unselected, 'Freq': control_freq, 'Induced': [True,True,True,False,False,False,True,True,True,False,False,False, False, False, False], 'Construct': ['5.20','5.20','5.20','5.20','5.20','5.20','NC1','NC1','NC1','NC1','NC1','NC1', 'NC4', 'NC4', 'NC4']})

#pH, buffer test 2/22/23 (will not be used in publication)
pHBuffer_selective = np.array([0,1,2,0,1,0,0,7,46,11,1,0])
pHBuffer_nonselective = np.array([7E06,6E06,3E06,15E06,15E06,12E06,1E06,3E06,6E06,4E06,7E06,22E06])
pHBuffer_freq = pHBuffer_selective/pHBuffer_nonselective
pHBuffer = pd.DataFrame({'Selected': pHBuffer_selective,'Unselected': pHBuffer_nonselective, 'Freq': pHBuffer_freq, 'Feed': ['Acetate','Acetate','Acetate','Acetate','Acetate','Sucrose','Acetate','Acetate','Acetate','Acetate','Acetate','Sucrose'], 'pH':[6,6.5,7,7.5,8,7,6,6.5,7,7.5,8,7], 'Buffered':['Unbuffered','Unbuffered','Unbuffered','Unbuffered','Unbuffered','Unbuffered','Buffered','Buffered','Buffered','Buffered','Buffered','Buffered']})

#Acetate Concentration
AcetateConc_selective = np.array([0, 0, 0, 7, 5, 0, 12, 15, 10, 61, 38, 58, 40,	110, 40, 320, 440, 210, 70, 30, 40, 10, 7, 5])
AcetateConc_nonselective = np.array([3.70E+05,	4.00E+05,	2.00E+05,	1.40E+05,	2.70E+05,	2.70E+05, 2.50E+06,	6.00E+05,	
                                     4.00E+05,	7.00E+05,	1.10E+06,	1.20E+06,   1.30E+06,	1.80E+06,	1.10E+06,	8.00E+06,	
                                     5.00E+06,	7.00E+06,   1.60E+06,	1.20E+06,	1.00E+06,	3.40E+05,	3.60E+05,	3.00E+05])
AcetateConc_cfuug = AcetateConc_selective*7*(1000/25)
AcetateConc_freq = AcetateConc_selective/AcetateConc_nonselective
AcetateConc = pd.DataFrame({'Selected': AcetateConc_selective,'cfu_ug': AcetateConc_cfuug,'Unselected': AcetateConc_nonselective, 'Freq': AcetateConc_freq, 'Concentration':[100,100,100,50,50,50,25,25,25,12.5,12.5,12.5,6.25,6.25,6.25,3,3,3,1.5,1.5,1.5,0.75,0.75,0.75]})

#Salnity
NaConc_selective = np.array([31,41,21,46,53,58,120,220,360,2,4,3,13,7,10,0,0,0,0,0,0])
NaConc_nonselective = np.array([2700000,1900000,2500000,1700000,1300000,1400000,8000000,4000000,6000000,
                                     500000,200000,100000,200000,500000,300000,7000,8000,11000,15000,15000,17000])
NaConc_cfuug = NaConc_selective*7*(1000/25)
NaConc_freq = NaConc_selective/NaConc_nonselective
NaConc = pd.DataFrame({'Selected': NaConc_selective,'cfu_ug': NaConc_cfuug,'Unselected': NaConc_nonselective, 'Freq': NaConc_freq, 'Concentration':[150,150,150,250,250,250,350,350,350,450,450,450,600,600,600,800,800,800,1000,1000,1000]})

#pH, PIPES
pH_selective = np.array([0,0,0,3,2,3,30,32,24,160,160,100,200,140,40,140,90,80,130,80,70,70,60,80,100,40,150,200,250,280,170,120,60,50,120])
pH_nonselective = np.array([1000000,1500000,1100000,900000,1400000,1100000,4000000,6000000,2400000,2000000,1000000,1300000,4000000,7000000,4000000,2000000,2000000,1000000,4000000,5000000,1000000,3000000,5000000,1000000,5000000,5000000,2700000,1600000,1900000,2300000,1200000,1600000,1400000,1600000,1900000])
pH_cfuug = pH_selective*7*(1000/25)

pH_freq = pH_selective/pH_nonselective
pHConc = pd.DataFrame({'Selected': pH_selective,'cfu_ug': pH_cfuug,'Unselected': pH_nonselective, 'Freq': pH_freq, 'pH':[6.12,6.12,6.12,6.45,6.45,6.45,6.74,6.74,6.74,6.81,6.81,6.81,6.89,6.89,6.89,6.96,6.96,6.96,7,7,7,7.11,7.11,7.15,7.15,7.15,7.3,7.3,7.3,7.49,7.49,7.49,7.6,7.6,7.6]})

#pH, HEPES
pH_HEPES_selective = np.array([180,170,190,140,260,170,230,180,320,160,270,340,140,110,200,290,250,380,290,210,320,80,110,110])
pH_HEPES_nonselective = np.array([9000000,3000000,11000000,2000000,7000000,2000000,3000000,3000000,3000000,5000000,4000000,11000000,10000000,10000000,4000000,3000000,11000000,10000000,4000000,7000000,8000000,5000000,7000000,6000000])
pH_HEPES_cfuug = pH_HEPES_selective*7*(1000/25)*(1460/50)

pH_HEPES_freq = pH_HEPES_selective/pH_HEPES_nonselective
pH_HEPES_Conc = pd.DataFrame({'Selected': pH_HEPES_selective,'cfu_ug': pH_HEPES_cfuug,'Unselected': pH_HEPES_nonselective, 'Freq': pH_HEPES_freq, 'pH':[7.19,7.19,7.19,7.3,7.3,7.3,7.38,7.38,7.38,7.42,7.42,7.42,7.6,7.6,7.6,7.78,7.78,7.78,7.88,7.88,7.88,7.99,7.99,7.99]})

#Time Course, 30C
TC_30C_selective = np.array([46,30,18,30,57,42,11,20,15,190,110,330,360,600,350,390,230,200,150,140,100,730,420,850])
TC_30C_nonselective = np.array([700000,200000,200000,900000,1000000,600000,100000,500000,800000,3000000,2000000,8000000,1000000,4000000,1000000,500000,600000,100000,600000,800000,900000,4000000,1000000,3000000])
TC_30C_cfuug = TC_30C_selective*7*(1000/25)*(1460/50)

TC_30C_freq = TC_30C_selective/TC_30C_nonselective
TC_30C_Conc = pd.DataFrame({'Selected': TC_30C_selective,'cfu_ug': TC_30C_cfuug,'Unselected': TC_30C_nonselective, 'Freq': TC_30C_freq, 'Hours':[10,10,10,12,12,12,14,14,14,16,16,16,18,18,18,20,20,20,22,22,22,24,24,24], 'temp': 24*[30]})

#Time Course, 20C
TC_20C_selective = np.array([5,2,5,14,10,11,6,8,7,7,3,2,6,4,6,25,31,33,60,30,90,20,50,360,280,250,200,350,320,110,160,180])
TC_20C_nonselective = np.array([50000,59000,31000,40000,40000,15000,54000,55000,55000,40000,20000,20000,60000,60000,10000,110000,110000,280000,240000,180000,220000,110000,20000,670000,800000,900000,530000,300000,100000,670000,300000,200000])
TC_20C_cfuug = TC_20C_selective*7*(1000/25)

TC_20C_freq = TC_20C_selective/TC_20C_nonselective
TC_20C_Conc = pd.DataFrame({'Selected': TC_20C_selective,'cfu_ug': TC_20C_cfuug,'Unselected': TC_20C_nonselective, 'Freq': TC_20C_freq, 'Hours':[10,10,10,12,12,12,14,14,14,16,16,16,18,18,18,20,20,20,22,22,24,24,24,31,31,31,38,38,38,49,49,49], 'Temp': 32*[20]})

#RecoveryMedia
Recovery_selective = np.array([200,100,200,200,200,100,300,200,200,2700,2400,2500])
Recovery_nonselective = np.array([1900000,700000,2000000,1200000,600000,1000000,1800000,1100000,1300000,2000000,5000000,2000000])

Recovery_freq = Recovery_selective/Recovery_nonselective
Recovery_Conc = pd.DataFrame({'Selected': Recovery_selective,'cfu_ug': 0,'Unselected': Recovery_nonselective, 'Freq': Recovery_freq, 'Category':['LBv2','LBv2','LBv2','RM','RM','RM','MCM','MCM','MCM','None*','None*','None*'], 'Temp': 12*[30]}) 

#Vortexing
Vortex_selective = np.array([2200,2100,1900,2200,2000,2100])
Vortex_nonselective = np.array([1000000,8000000,5000000,5000000,2000000,5000000])

Vortex_freq = Vortex_selective/Vortex_nonselective
Vortex_Conc = pd.DataFrame({'Selected': Vortex_selective,'cfu_ug': 0,'Unselected': Vortex_nonselective, 'Freq': Vortex_freq, 'Category':['1','1','1','60','60','60'], 'Temp': 6*[30]}) 

#Shaking
Shaking_selective = np.array([39,40,32])
Shaking_nonselective = np.array([5.00E05,4.00E05,3.00E05])

Shaking_freq = Shaking_selective/Shaking_nonselective
Shaking_Conc = pd.DataFrame({'Selected': Shaking_selective,'cfu_ug': 0,'Unselected': Shaking_nonselective, 'Freq': Shaking_freq, 'Category':3*['+Shaking\nIncubation'], 'Temp': 3*[37]}) 

#Incubation
Incubation_selective = np.array([14,24,17,40,100,150,1100,600,1300,1300,1100,1300,2300,1900,1800,2400,1400,2600,2400,1300,2000,2500,2100,2300,1500,1100,400,600,1100,300,80,220,200,1000,400,800,1800,1800,1700,1500,2400,1900,2200,2100,1900,1500,2600,3000,3400,4200,2400,1000,800,400,600,1400,800,60,100,30,400,500,200,1000,1000,1100,1800,1500,1400,900,1300,700,500,300,1300,1400,800,1600,200,800,700,300,400,300])
Incubation_nonselective = np.array([3000000,2000000,5000000,1300000,1800000,2500000,3000000,2100000,3000000,2800000,2300000,4000000,2400000,3100000,2900000,1000000,400000,1600000,3200000,2000000,5400000,6000000,4700000,3900000,300000,700000,1400000,2200000,2100000,3100000,1600000,2400000,1900000,3000000,3300000,3300000,2200000,3400000,1200000,3400000,3300000,2100000,1000000,8000000,5000000,2200000,3500000,4300000,6300000,5000000,5300000,1200000,900000,700000,1600000,1700000,1400000,1400000,1900000,2300000,3400000,2500000,2400000,1300000,1900000,1500000,2000000,2500000,2600000,2000000,600000,1100000,2500000,3200000,1700000,4700000,3100000,2300000,200000,400000,900000,1100000,1700000,2300000])
Incubation_cfu_ug = 9200*Incubation_selective/25
Incubation_pos_override = [0,0,0]+3*[1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,9,9,9]
    
Incubation_freq = Incubation_selective/Incubation_nonselective
Incubation_Conc = pd.DataFrame({'Selected': Incubation_selective,'Override': Incubation_pos_override, 'cfu_ug': Incubation_cfu_ug,'Unselected': Incubation_nonselective, 'Freq': Incubation_freq, 'Hours':[0,0,0,.25,.25,.25,.5,.5,.5,.75,.75,.75,1,1,1,1.5,1.5,1.5,2,2,2,3,3,3,4.5,4.5,4.5,6,6,6,.25,.25,.25,.5,.5,.5,.75,.75,.75,1,1,1,1.5,1.5,1.5,2,2,2,3,3,3,4.5,4.5,4.5,6,6,6,.25,.25,.25,.5,.5,.5,.75,.75,.75,1,1,1,1.5,1.5,1.5,2,2,2,3,3,3,4.5,4.5,4.5,6,6,6,], 'Temp': 3*[0] + 27 * [37] + 27 * [30] + 27* [20]}) 

#RT Melt
RT_selective = np.array([1500,1600,1900])
RT_nonselective = np.array([1.70E+06, 2.30E+06, 2.70E+06])

RT_freq = RT_selective/RT_nonselective
RT_Conc = pd.DataFrame({'Selected': RT_selective,'cfu_ug': 0,'Unselected': RT_nonselective, 'Freq': RT_freq, 'Category':[' ',' ',' '], 'Temp': 3*[30]}) 

#NgTest
Ng_list = np.array(3*[1000]+3*[500]+3*[250]+3*[100]+3*[50]+3*[25]+3*[10]+3*[5]+3*[2.5]+3*[250]+3*[100]+3*[50]+3*[25]+3*[10]+3*[5]+3*[2.5])

NgTest_selective = np.array([4000,6000,13000,13000,10000,18000,10000,5000,4000,12000,6000,7000,5000,2000,3000,4000,2000,6000,600,500,600,20,15,19,6,6,5,600,1900,2100,900,900,1600,1000,1100,1000,150,290,290,90,160,110,20,70,20,13,21,18])
NgTest_nonselective = np.array([3900000,2800000,4100000,5200000,2400000,3300000,4500000,3000000,3000000,5800000,2700000,3900000,3500000,4500000,5100000,3500000,2100000,5700000,5300000,4300000,3800000,2300000,3400000,2200000,2500000,800000,2600000,2100000,1600000,1700000,1700000,2800000,2600000,2700000,1900000,1600000,2200000,3400000,2500000,3400000,3400000,2000000,3200000,1600000,2800000,2200000,2600000,1700000])
NgTest_cfu_ug = 9200*np.array([4000,6000,13000,13000,10000,18000,10000,5000,4000,12000,6000,7000,5000,2000,3000,4000,2000,6000,600,500,600,20,15,19,6,6,5,600,1900,2100,900,900,1600,1000,1100,1000,150,290,290,90,160,110,20,70,20,13,21,18])/Ng_list

Ng_list_strvar = [str(i).strip('0').strip('.') for i in Ng_list.tolist()]
Ng_list_strvar.reverse()

NgTest_freq = NgTest_selective/NgTest_nonselective
NgTest_Conc = pd.DataFrame({'Selected': NgTest_selective,'cfu_ug': NgTest_cfu_ug,'Unselected': NgTest_nonselective, 'Freq': NgTest_freq, 'Category':Ng_list, 'Temp': 27*['pDS5.30']+21*['pUC19']})

#MolBio
MolBio_selective = np.array([11000,140])
MolBio_nonselective = np.array([2.7E06,2E06])

MolBio_freq = MolBio_selective/MolBio_nonselective
MolBio_Conc = pd.DataFrame({'Selected': MolBio_selective,'cfu_ug': 0,'Unselected': MolBio_nonselective, 'Freq': MolBio_freq, 'Category':['Ligation', 'Gibson']}) 

#VNSrc
VNSrc_selective = np.array([6.00E+03,3.00E+03,5.00E+03])
VNSrc_nonselective = np.array([4.00E+05, 1.10E+06, 1.50E+06])
VNSrc_cfu_ug = 9200*VNSrc_selective/25

VNSrc_freq = VNSrc_selective/VNSrc_nonselective
VNSrc_Conc = pd.DataFrame({'Selected': VNSrc_selective,'cfu_ug': VNSrc_cfu_ug,'Unselected': VNSrc_nonselective, 'Freq': VNSrc_freq, 'Category':3*['']}) 

#NoStop
NoStop_selective = np.array([400,400,200,50,40,60])
NoStop_nonselective = np.array([1600000,1600000,1900000,3300000,3600000,2100000])

NoStop_freq = NoStop_selective/NoStop_nonselective
NoStop_Conc = pd.DataFrame({'Selected': NoStop_selective,'cfu_ug': 0,'Unselected': NoStop_nonselective, 'Freq': NoStop_freq, 'Category':3*['HE']+3*['0Cap']}) 

#NoStopGlycerol
NoStopGly_selective = np.array([300,300,190,400,400,200])
NoStopGly_nonselective = np.array([1500000,1800000,1300000,1600000,1600000,1900000])

NoStopGly_freq = NoStopGly_selective/NoStopGly_nonselective
NoStopGly_Conc = pd.DataFrame({'Selected': NoStopGly_selective,'cfu_ug': 0,'Unselected': NoStopGly_nonselective, 'Freq': NoStopGly_freq, 'Category':3*['+glycerol']+3*['-glycerol']}) 

#CarbonSrc - fresh
CarbonSrcFresh_selective = np.array([0,0,0,45,60,62,0,0,0,500,100,600,2,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,3])
CarbonSrcFresh_nonselective = np.array([11000000,10000000,9000000,30000000,50000000,40000000,200000000,200000000,300000000,3000000,6000000,3000000,400000,200000,200000,700000,1500000,400000,200000,200000,200000,300000,300000,200000,20000000,20000000,5000000,13000000,13000000,8000000])

CarbonSrcFresh_freq = CarbonSrcFresh_selective/CarbonSrcFresh_nonselective
CarbonSrcFresh_Conc = pd.DataFrame({'Selected': CarbonSrcFresh_selective,'cfu_ug': 0,'Unselected': CarbonSrcFresh_nonselective, 'Freq': CarbonSrcFresh_freq, 'Category':3*['1% LBv2']+3*['10% LB2']+3*['LBv2']+3*['Pyruvate (MCM)']+3*['Formate (MCM)']+3*['Sucrose (MCM)']+3*['Gluconate (MCM)']+3*['Sorbitol (MCM)']+3*['Glucose (MCM)']+3*['Tryptone (MCM)']}) 

#Carbonsrc - frozen
CarbonSrcFroz_selective = np.array([900,900,700,100,100,200])
CarbonSrcFroz_nonselective = np.array([4000000,2000000,2700000,20000000,70000000,30000000])

CarbonSrcFroz_freq = CarbonSrcFroz_selective/CarbonSrcFroz_nonselective
CarbonSrcFroz_Conc = pd.DataFrame({'Selected': CarbonSrcFroz_selective,'cfu_ug': 0,'Unselected': CarbonSrcFroz_nonselective, 'Freq': CarbonSrcFroz_freq, 'Category':3*['Pyruvate (MCM)']+3*['10% LB2']}) 

#dDNS
dDNS_selective = np.array([0,0,0])
dDNS_nonselective = np.array([2.50E+06,4.60E+06,1.00E+06])

dDNS_freq = dDNS_selective/dDNS_nonselective
dDNS_Conc = pd.DataFrame({'Selected': dDNS_selective,'cfu_ug': 0,'Unselected': dDNS_nonselective, 'Freq': dDNS_freq, 'Category':3*['dDNS']}) 

#NC7
NC7_selective = np.array([1000,500,400])
NC7_nonselective = np.array([2.20E+06, 1.20E+06, 9.00E+05])

NC7_freq = NC7_selective/NC7_nonselective
NC7_Conc = pd.DataFrame({'Selected': NC7_selective,'cfu_ug': 0,'Unselected': NC7_nonselective, 'Freq': NC7_freq, 'Category':3*['']}) 

#NC8
NC8_selective = np.array([1,1,0,1,1,23,7,1,4,15,33,72,120,30,90,60,10,100,1800,300,600,1100,900,700,190,100,300])
NC8_nonselective = np.array([2.40E+03,3.80E+03,2.70E+03,1.40E+04,1.70E+04,1.00E+05,3.00E+04,3.70E+04,4.10E+04,8.00E+03,1.20E+04,1.00E+05,5.50E+05,8.00E+04,5.00E+04,1.00E+05,1.00E+05,1.00E+05,8.00E+05,1.20E+06,1.30E+06,1.30E+06,3.00E+05,1.00E+05,6.00E+05,8.00E+05,3.00E+05])
NC8_cfu_ug = 9200*np.array([1,1,0,1,1,23,7,1,4,15,33,72,120,30,90,60,10,100,1800,300,600,1100,900,700,190,100,300])
NC8_total_cfu = (460/50)*np.array([2.40E+03,3.80E+03,2.70E+03,1.40E+04,1.70E+04,1.00E+05,3.00E+04,3.70E+04,4.10E+04,8.00E+03,1.20E+04,1.00E+05,5.50E+05,8.00E+04,5.00E+04,1.00E+05,1.00E+05,1.00E+05,8.00E+05,1.20E+06,1.30E+06,1.30E+06,3.00E+05,1.00E+05,6.00E+05,8.00E+05,3.00E+05])

IPTG_list = np.array(3*[200]+3*[100]+3*[50]+3*[25]+3*[6]+3*[3]+3*[1.5]+3*[0.75]+3*[0])
IPTG_list_strvar = [str(i).strip('0').strip('.') for i in IPTG_list.tolist()]
IPTG_list_strvar.reverse()

NC8_freq = NC8_selective/NC8_nonselective
NC8_Conc = pd.DataFrame({'Selected': NC8_selective,'cfu_ug': NC8_cfu_ug, 'tot_cfu': NC8_total_cfu, 'Unselected': NC8_nonselective, 'Freq': NC8_freq, 'Category':IPTG_list})

#dDNS + pMMB-tfoX
pMMB_selective = np.array([0,0,0,1000,1000,1200])
pMMB_nonselective = np.array([8.00E+04,9.00E+04,2.70E+05,8.00E+05,1.60E+06,1.60E+06])

IPTG_shortlist = np.array(3*[50]+3*[0])
IPTG_shortlist_strvar = [str(i).strip('0').strip('.') for i in IPTG_shortlist.tolist()]
IPTG_shortlist_strvar.reverse()

pMMB_freq = pMMB_selective/pMMB_nonselective
pMMB_Conc = pd.DataFrame({'Selected': pMMB_selective,'Unselected': pMMB_nonselective, 'Freq': pMMB_freq, 'Category':['- IPTG','- IPTG','- IPTG','+ IPTG','+ IPTG','+ IPTG']})

#qPCR results
RQ = np.array([3.171400325,3.361627805,3.031349085,415.8962885,404.3385646,550.9814737,69.07539491,65.40912455,90.67607256,26.30292079,28.27607038,27.64394515,21.2030514,21.52488543,22.65745809,17.19068537,22.47472654,29.43865981,23.97853701,18.63905081,15.02206123,6.669196013,31.50614835,40.7722011,17.2783893,20.25427279,15.82347062,41.69125368,35.42184422,31.21777274,30.46079048,24.85708271,29.34195279,33.43075463,27.10159337,14.15126388,20.48296715,15.10119942,20.72408727,36.11098572,38.00103192,41.00674558])
qPCR_Conc = pd.DataFrame({'RQ': RQ, 'Category': 3*['pMMB'] + 3*['pMMB']+ 3*['NC1']+ 3*['NC7']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8']+ 3*['NC8'], 'IPTG': 3*['- IPTG'] + 3*['+ IPTG']+ 3*['-']+ 3*['-']+ 3*['0']+ 3*['0.75']+ 3*['1.5']+ 3*['3']+ 3*['6']+ 3*['12.5']+ 3*['25']+ 3*['50']+ 3*['100']+ 3*['200']})

#NC1 w/ Dalia protocol
DaliaProt_selective = np.array([2400,900,1600,900,600,600])
DaliaProt_nonselective = np.array([8.00E+06,7.00E+06,7.00E+06,2.30E+06,1.80E+06,2.90E+06])
DaliaProt_freq = DaliaProt_selective/DaliaProt_nonselective

DaliaProt_Conc = pd.DataFrame({'Selected': DaliaProt_selective,'Unselected': DaliaProt_nonselective, 'Freq': DaliaProt_freq, 'Category': ['- Recovery','- Recovery','- Recovery','+ Recovery','+ Recovery','+ Recovery']})
# --------------------------- Subfigure Content ---------------------------
plt.close('all')
plt.ion()

#Draft
#FigMaker(control, 'Construct', 'Freq', 'Frequency', [-1E-08,5E-04], '', c[0], 2E-08, [4,4], hue = 'Induced')
#FigMaker(pHBuffer[(pHBuffer['Feed']=='Acetate')], 'pH', 'Freq', 'Transformation\nFrequency', [-1E-07,5E-05], 'pH', c[0], 2E-07, [4.9,3], hue = 'Buffered')
#FigMaker(pHConc, 'pH', 'Freq', 'Frequency', [-1E-06,5E-04], 'pH', c[0], 2E-06, [4.9,3], plotAvg1 = True, xlog = False, linthreshX = 1E-06, data2 = pHConc, x2 = 'pH', y2 = 'Unselected', ylabel2 = 'cfu', ylim2 = [5E04, 1.5E07], color2 = c[1], plotAvg2 = True)
#FigMaker(TC_30C_Conc, 'Hours', 'Freq', 'Frequency', [-1E-06,5E-04], 'Hours', c[0], 2E-06, [4.9,3], plotAvg1 = True, xlog = False, linthreshX = 1E-06)
#FigMaker(TC_20C_Conc, 'Hours', 'Freq', 'Frequency', [-1E-06,5E-04], 'Hours', c[0], 2E-06, [4.9,3], plotAvg1 = True, xlog = False, linthreshX = 1E-06)
#FigMaker(Fig1_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-01], '', c[2], 1E-07, [0.5,1.4], 'Fig1_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-06, plot_type = 'bar')

#For TJ -> conversion to cfu/ug
#FigMaker(AcetateConc, 'Concentration', 'cfu_ug', 'cfu/$\mu$g', [-1,1E6], 'Acetate Concentration (mM)', c[0], 1, [4.9,3], plotAvg1 = True, xlog = True, linthreshX = 1, data2 = AcetateConc, x2 = 'Concentration', y2 = 'Unselected', ylabel2 = 'total viable\nunselected colonies', ylim2 = [2E04, 1.5E07], color2 = c[1], plotAvg2 = True)
#FigMaker(NaConc, 'Concentration', 'cfu_ug', 'cfu/$\mu$g', [-1,1E6], 'Na Concentration (mM)', c[0], 1, [4.9,3], plotAvg1 = True, xlog = False, linthreshX = 1, data2 = NaConc, x2 = 'Concentration', y2 = 'Unselected', ylabel2 = 'total viable\nunselected colonies', ylim2 = [2E02, 1.5E07], color2 = c[1], plotAvg2 = True)
#FigMaker(pHConc, 'pH', 'cfu_ug', 'cfu/$\mu$g - PIPES', [-1,1E6], 'pH', c[0], 1, [4.9,3], plotAvg1 = True, xlog = False, linthreshX = 1, data2 = pH_HEPES_Conc, x2 = 'pH', y2 = 'cfu_ug', ylabel2 = 'cfu/$\mu$g - HEPES', ylim2 = [-1,5E6], color2 = c[2], plotAvg2 = True)
#FigMaker(TC_20C_Conc, 'Hours', 'cfu_ug', 'cfu/$\mu$g - 20C growth', [-1,1E6], 'Hours', c[0], 1, [4.9,3], plotAvg1 = True, xlog = False, linthreshX = 1)
#FigMaker(TC_30C_Conc, 'Hours', 'cfu_ug', 'cfu/$\mu$g - 30C growth', [-1,1E6], 'Hours', c[0], 1, [4.9,3], plotAvg1 = True, xlog = False, linthreshX = 1)

#Figure 1
# FigMaker(Fig1_Conc, 'Category', 'cfu_ug', 'cfu/$\mu$g', [-0.5,1E07], '', c[2], 1, [0.5,1.1], 'Fig1_Conc_cfu_ug', plotAvg1 = False, xlog = False, linthreshX = 1E-06, plot_type = 'bar')

#Figure 2
# FigMaker(AcetateConc, 'Concentration', 'Freq', 'Frequency', [-5E-07,8E-03], 'Acetate Concentration (mM)', c[4], 1E-06, [1,0.6], 'AcetateConc', plotAvg1 = True, xlog = True, linthreshX = 1E-05, data2 = AcetateConc, x2 = 'Concentration', y2 = 'Unselected', ylabel2 = 'Total viable\nunselected cfus', ylim2 = [2E04, 1.5E07], color2 = c[1], plotAvg2 = True, marker2 = '^')
# FigMaker(NaConc, 'Concentration', 'Freq', 'Frequency', [-5E-07,8E-03], 'Na Concentration (mM)', c[4], 1E-06, [1,0.6], 'NaConc', plotAvg1 = True, xlog = False, linthreshX = 1E-06, data2 = NaConc, x2 = 'Concentration', y2 = 'Unselected', ylabel2 = 'Total viable\nunselected cfus', ylim2 = [2E02, 1.5E07], color2 = c[1], plotAvg2 = True, marker2 = '^')
# FigMaker(pHConc, 'pH', 'Freq', 'Frequency\nin PIPES buffer', [-5E-07,8E-03], 'pH', c[4], 1E-06, [1.2,0.6], 'pHConc', xlim = [6,8.1], plotAvg1 = True, xlog = False, linthreshX = 1E-06, data2 = pH_HEPES_Conc, x2 = 'pH', y2 = 'Freq', ylabel2 = 'Frequency\nin HEPES Buffer', ylim2 = [-5E-07,5E-03], color2 = c[2], plotAvg2 = True)
# FigMaker(TC_30C_Conc, 'Hours', 'Freq', 'Frequency', [-5E-07,8E-03], '', c[2], 1E-06, [1.5,0.6], 'TC_30C_Conc', plotAvg1 = True, xlog = False, linthreshX = 1E-06)
# FigMaker(TC_20C_Conc, 'Hours', 'Freq', 'Frequency', [-5E-07,8E-03], '', c[2], 1E-06, [2.5,0.6], 'TC_20C_Conc', plotAvg1 = True, xlog = False, linthreshX = 1E-06)
# FigMaker(TC_30C_Conc, 'Hours', 'cfu_ug', 'cfu/$\mu$g', [50,5E07], 'Hours of\n30 $^\circ$C Static Outgrowth', c[6], 100, [1.5,0.8], 'TC_30C_Conc_select', plotAvg1 = True, xlog = False, linthreshX = 1E-06)
# FigMaker(TC_20C_Conc, 'Hours', 'cfu_ug', 'cfu/$\mu$g', [50,5E07], 'Hours of\n20 $^\circ$C Static Outgrowth', c[6], 100, [2.5,0.8], 'TC_20C_Conc_select', plotAvg1 = True, xlog = False, linthreshX = 1E-06)

# #Figure 3
# FigMaker(Recovery_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], 'Recovery\nMedia', c[2], 1E-06, [0.5*(4/3),0.8], 'Recovery_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
# FigMaker(Vortex_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], 'Vortex\nTime (s)', c[2], 1E-06, [0.5*(2/3),0.8], 'Vortex_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
# FigMaker(Shaking_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], ' ', c[2], 1E-06, [0.5*(1/3),0.8], 'Shaking_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
# FigMaker(Incubation_Conc[(Incubation_Conc['Temp']==20) | (Incubation_Conc['Temp']==0)], 'Hours', 'Freq', 'Frequency', [-5E-07,1E-02], 'Hours', c[2], 1E-06, [0.5*(10/3),0.8], 'Incubation_Conc20', plotAvg1 = False, xlog = False, plot_type = 'bar', data2 = Incubation_Conc[(Incubation_Conc['Temp']==20) | (Incubation_Conc['Temp']==0)], x2 = 'Hours', y2 = 'cfu_ug', ylabel2 = 'cfu/$\mu$g', ylim2 = [-0.5,1E09],color2 = c[1], plotAvg2 = True, linthresh2 = 1000)
# FigMaker(Incubation_Conc[(Incubation_Conc['Temp']==30) | (Incubation_Conc['Temp']==0)], 'Hours', 'Freq', 'Frequency', [-5E-07,1E-02], 'Hours', c[2], 1E-06, [0.5*(10/3),0.8], 'Incubation_Conc30', plotAvg1 = False, xlog = False, plot_type = 'bar', data2 = Incubation_Conc[(Incubation_Conc['Temp']==30) | (Incubation_Conc['Temp']==0)], x2 = 'Hours', y2 = 'cfu_ug', ylabel2 = 'cfu/$\mu$g', ylim2 = [-0.5,1E09],color2 = c[1], plotAvg2 = True, linthresh2 = 1000)
# FigMaker(Incubation_Conc[(Incubation_Conc['Temp']==37) | (Incubation_Conc['Temp']==0)], 'Hours', 'Freq', 'Frequency', [-5E-07,1E-02], 'Hours', c[2], 1E-06, [0.5*(10/3),0.8], 'Incubation_Conc37', plotAvg1 = False, xlog = False, plot_type = 'bar', data2 = Incubation_Conc[(Incubation_Conc['Temp']==37) | (Incubation_Conc['Temp']==0)], x2 = 'Hours', y2 = 'cfu_ug', ylabel2 = 'cfu/$\mu$g', ylim2 = [-0.5,1E09],color2 = c[1], plotAvg2 = True, linthresh2 = 1000)
# FigMaker(RT_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], 'RT\nMelt', c[2], 1E-06, [0.5*(1/3),0.8], 'RT_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
# FigMaker(CarbonSrcFroz_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], 'Energy Source', c[2], 1E-06, [0.5*(2/3),0.8], 'CarbonSrcFroz_Conc', plotAvg1 = False, xlog = False, plot_type = 'bar', hline = 0.001027)
# FigMaker(NoStop_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], 'Immediate\nTransform.', c[2], 1E-06, [0.5*(2/3),0.8], 'NoStop_Conc', plotAvg1 = False, xlog = False, plot_type = 'bar', hline = 0.001027)
# FigMaker(NgTest_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], 'ng Plasmid Transformed', c[2], 1E-06, [2.5,0.8], 'NgTest_Conc', plotAvg1 = False, xlog = False, plot_type = 'bar', hue = 'Temp', hline = 0.001027)
# FigMaker(NgTest_Conc, 'Category', 'cfu_ug', 'cfu/$\mu$g', [-0.5,1E07], 'ng Plasmid Transformed', c[2], 1000, [2.5,0.8], 'NgTest_Conc_cfu_ug', plotAvg1 = False, xlog = False, plot_type = 'bar', hue = 'Temp')
# FigMaker(Incubation_Conc[(Incubation_Conc['Temp']==37) | (Incubation_Conc['Temp']==0)], 'Hours', 'Freq', 'Frequency', [-5E-07,1E-02], 'Incubation Time\nwith DNA (Hours)', c[2], 1E-06, [0.5*(9.35/3),0.8], 'Incubation_Conc_bottomAxis', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar') #Use for corrected x axis

#Figure 4
# FigMaker(VNSrc_Conc, 'Category', 'cfu_ug', 'cfu/$\mu$g', [-0.5,1E07], 'Plasmid\nfrom VN\nMiniprep', c[2], 100, [0.5*(1/3),0.7], 'VNSrc_Conc_cfu_ug', plotAvg1 = False, xlog = False, plot_type = 'bar')
# FigMaker(MolBio_Conc, 'Category', 'Selected', 'cfu/rxn', [-0.5,1E05], ' ', c[2], 100, [0.5*(2/3),0.7], 'MolBio_Conc_Selected', plotAvg1 = False, xlog = False, plot_type = 'bar')

#Figure 5
# FigMaker(NC7_Conc, 'Category', 'Freq', 'NPT\nFrequency', [-5E-07,1E-02], 'New\ncamR-\nstrain', c[2], 1E-06, [0.5*(1/3),0.8], 'NC7_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)

#Figure 6
#FigMaker(NC8_Conc, 'Category', 'Freq', 'NPT\nFrequency', [-5E-07,5E-02], 'IPTG Concentration ($\mu$M)', c[2], 1E-06, [0.5*(9/3),0.8], 'NC8_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
#FigMaker(NC8_Conc, 'Category', 'cfu_ug', 'Yield cfu/$\mu$g\nadded DNA', [-0.5,5E07], 'IPTG Concentration ($\mu$M)', c[2], 5000, [0.5*(9/3),0.8], 'NC8_Yield', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar')
#FigMaker(NC8_Conc, 'Category', 'tot_cfu', 'Survival (total\nunselected cfus)', [-0.5,5E07], 'IPTG Concentration ($\mu$M)', c[2], 50000, [0.5*(9/3),0.8], 'NC8_Survival', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar')

#FigMaker(pMMB_Conc, 'Category', 'Freq', 'NPT\nFrequency', [-5E-07,5E-02], 'IPTG induction\nof pMMB67EH-tfoX', c[2], 1E-06, [0.5*(2/3),0.8], 'pMMB_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)

#Supplemental
# FigMaker(pHConc, 'pH', 'Unselected', 'Unselected cfus\n- PIPES', [1000,5E07], 'pH', c[4], 1, [1.2,0.6], 'pHConc_Unselect', xlim = [5.9,8.15], xticks = [6,7,8], plotAvg1 = True, xlog = False, data2 = pH_HEPES_Conc, x2 = 'pH', y2 = 'Unselected', ylabel2 = 'Unselected cfus\n- HEPES', ylim2 = [1000,5E07], color2 = c[2], plotAvg2 = True)
# FigMaker(NoStopGly_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,1E-02], '', c[2], 1E-06, [0.5*(2/3),0.8], 'NoStopGly_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
# FigMaker(CarbonSrcFresh_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,8E-03], 'Energy Source -\nImmediate Transformation', c[2], 1E-06, [0.5*(10/3),0.8], 'CarbonSrcFresh_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
# FigMaker(CarbonSrcFroz_Conc, 'Category', 'Freq', 'Frequency', [-5E-07,8E-03], 'Energy Source -\nFrom Frozen', c[2], 1E-06, [0.5*(2/3),0.8], 'CarbonSrcFroz_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
#FigMaker(qPCR_Conc, 'Category', 'RQ', 'Expression Rel.\n to gyrB', [1,800],'', c[2], 1E-06, [0.5*(14/3),0.8], 'qPCR_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-02, plot_type = 'bar')
#FigMaker(qPCR_Conc[(qPCR_Conc['Category']=='pMMB')], 'IPTG', 'RQ', '$\it{tfoX}$ Expression\nRel. to $\it{gyrB}$', [1,800],'pMMB67EH\n-tfoX', c[2], 1E-06, [0.5*(2/3),0.8], 'qPCR_Conc_pMMB', plotAvg1 = False, xlog = False, linthreshX = 1E-02, plot_type = 'bar')
#FigMaker(qPCR_Conc[(qPCR_Conc['Category']=='NC1')], 'Category', 'RQ', '', [1,800],'', c[2], 1E-06, [0.5*(1/3),0.8], 'qPCR_Conc_NC1', plotAvg1 = False, xlog = False, linthreshX = 1E-02, plot_type = 'bar')
#FigMaker(qPCR_Conc[(qPCR_Conc['Category']=='NC7')], 'Category', 'RQ', '', [1,800],'', c[2], 1E-06, [0.5*(1/3),0.8], 'qPCR_Conc_NC7', plotAvg1 = False, xlog = False, linthreshX = 1E-02, plot_type = 'bar')
#FigMaker(qPCR_Conc[(qPCR_Conc['Category']=='NC8')], 'IPTG', 'RQ', '', [1,800],'NC8 - IPTG Induction ($\mu$M)', c[2], 1E-06, [0.5*(10/3),0.8], 'qPCR_Conc_NC8', plotAvg1 = False, xlog = False, linthreshX = 1E-02, plot_type = 'bar')
#FigMaker(DaliaProt_Conc, 'Category', 'Freq', 'NPT\nFrequency', [-5E-07,5E-02], '', c[2], 1E-06, [0.5*(2/3),0.8], 'DaliaProt_Conc', plotAvg1 = False, xlog = False, linthreshX = 1E-05, plot_type = 'bar', hline = 0.001027)
