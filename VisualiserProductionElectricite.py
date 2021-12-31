import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import mplcyberpunk
from scipy.ndimage import gaussian_filter1d

plt.style.use("cyberpunk")

__SUBPLOTS_LIGNE__ = 2
__SUBPLOTS_COLONNE__ = 2
__SIGMA__ = 3
__DECALAGE_Y__ = 1.08
__NOM_XTICKS__ = 9

DATAFRAME = pd.read_csv('Production.csv')
FIGURE, AXE = plt.subplots(__SUBPLOTS_LIGNE__, __SUBPLOTS_COLONNE__, figsize=(15, 11))

plt.subplots_adjust(left=0.125, bottom=0.1,  right=0.9, top=0.9, wspace=0.2, hspace=0.35)
plt.get_current_fig_manager().window.state('zoomed')
pylab.rcParams.update({   
            'legend.fontsize': 'x-large',
            'figure.figsize': (15, 5),
            'legend.fontsize': 13,
            'axes.labelsize': 12,
            'axes.titlesize':17,
            'xtick.labelsize':12,
            'ytick.labelsize':13,
            'font.family' : 'S-Core Dream'})

FIGURE.patch.set_facecolor('black')
for j in range(__SUBPLOTS_COLONNE__):
    for k in range(__SUBPLOTS_LIGNE__):
        AXE[j][k].set_facecolor('black')


for i in range(len(DATAFRAME)):
    heure = [''] * __NOM_XTICKS__
    date = ""
    SoleilTerre = [0] * __NOM_XTICKS__
    VentTerre = [0] * __NOM_XTICKS__
    SoleilJeju = [0] * __NOM_XTICKS__
    VentJeju = [0] * __NOM_XTICKS__
    ProportionSomme = [0] * __NOM_XTICKS__

    for j in range(__NOM_XTICKS__):
        date_cru = str(DATAFRAME.loc[i + j]['Date']).split('-')
        if(0 == j):
            date = date_cru[1] + "월 " + date_cru[2] + "일 "

        if(j % 2 != 0):
            heure[j] = ""
        else:
            heure[j] = str(DATAFRAME.loc[i + j]['Heure']) + "H"
        
        SoleilTerre[j] = float(DATAFRAME.loc[i + j]['SoleilTerre'])
        VentTerre[j] = float(DATAFRAME.loc[i + j]['VentTerre'])
        SoleilJeju[j] = float(DATAFRAME.loc[i + j]['SoleilJeju'])
        VentJeju[j] = float(DATAFRAME.loc[i+ j]['VentJeju'])
        ProportionSomme[j] = (SoleilJeju[j] + VentJeju[j]) / (SoleilTerre[j] + VentTerre[j])

    # Nettoyer les AXEs
    for j in range(__SUBPLOTS_COLONNE__):
        for k in range(__SUBPLOTS_LIGNE__):
            AXE[j][k].cla()
                
    ### AXE[0][0]
    AXE[0][0].set_title('제주 지역 전력생산량 (kW/h)', y = __DECALAGE_Y__)
    
    AXE[0][0].plot(np.arange(__NOM_XTICKS__), 
                gaussian_filter1d(VentJeju, sigma = __SIGMA__),   
                '-', 
                label = '풍력')
    AXE[0][0].plot(np.arange(__NOM_XTICKS__), 
                gaussian_filter1d(SoleilJeju, sigma = __SIGMA__), 
                '-',
                label = '태양열',
                color='#FF4444')

    AXE[0][0].legend(loc='upper right')

    AXE[0][0].set_ylim(0, 330)
    AXE[0][0].set_yticks(np.arange(60, 360, 60))
    plt.setp(AXE[0][0].get_xticklabels(), visible = False)

    ### AXE[1][0] 
    AXE[1][0].set_title('본토 전력생산량 (kW/h)', y = __DECALAGE_Y__)

    AXE[1][0].plot(np.arange(__NOM_XTICKS__), 
                gaussian_filter1d(VentTerre, sigma = __SIGMA__), 
                '-')
    AXE[1][0].plot(np.arange(__NOM_XTICKS__), 
                gaussian_filter1d(SoleilTerre, sigma = __SIGMA__),
                '-', 
                color='#FF4444')
    
    AXE[1][0].set_xticks(np.arange(__NOM_XTICKS__))
    AXE[1][0].set_xticklabels(heure)
    AXE[1][0].set_xlabel(date, 
                        labelpad = 15,
                        loc = 'left',
                        fontdict = {'family' : 'S-Core Dream', 'size' : 13})
    AXE[1][0].set_ylim(0, 2000)
    AXE[1][0].set_yticks(np.arange(400, 2400, 400))
    
    ### AXE[0][1] 
    AXE[0][1].set_title('합산 생산량', y = __DECALAGE_Y__)

    AXE[0][1].scatter(SoleilTerre[0], 
                    VentTerre[0], 
                    s = 20 ** 2, 
                    alpha = 0.5, 
                    color='#FFCC00')
    
    AXE[0][1].set_xlim(0, 2500)
    AXE[0][1].set_xticks(np.arange(800, 3200, 800))
    AXE[0][1].set_xlabel('태양열', family = 'S-Core Dream')
    AXE[0][1].set_ylim(0, 2500)
    AXE[0][1].set_yticks(np.arange(800, 3200, 800))
    AXE[0][1].set_ylabel('풍력', family = 'S-Core Dream')

    ### AXE[1][1] 
    AXE[1][1].set_title('본토 대비 제주 지역의 전력생산비율', y = __DECALAGE_Y__)

    AXE[1][1].plot(np.arange(__NOM_XTICKS__), 
                gaussian_filter1d(ProportionSomme, sigma = __SIGMA__), 
                '-', 
                label = '백분율', 
                color='#FFCC00')

    AXE[1][1].legend(loc='upper right')

    AXE[1][1].set_xticks(np.arange(__NOM_XTICKS__))
    AXE[1][1].set_xticklabels(heure)
    AXE[1][1].set_xlabel(date, 
                        labelpad = 15,
                        loc = 'left',
                        fontdict = {'family' : 'S-Core Dream', 'size' : 13})
    AXE[1][1].axhline(1, 0, __NOM_XTICKS__ - 1, color='lightgray', linestyle='--', linewidth=1)
    AXE[1][1].set_ylim(0, 1.4)
    AXE[1][1].set_yticks(np.arange(0.25, 1.5, 0.25))
    AXE[1][1].set_yticklabels(["25%", "50%", "75%", "100%", "125%"])
    
    ### Mettre les effets de Cyberpunk 
    mplcyberpunk.make_lines_glow(AXE[0][0])
    mplcyberpunk.add_underglow(AXE[0][0])
    mplcyberpunk.make_lines_glow(AXE[1][0])
    mplcyberpunk.add_underglow(AXE[1][0])
    mplcyberpunk.make_lines_glow(AXE[1][1])
    mplcyberpunk.add_underglow(AXE[1][1])

    plt.pause(0.01)

print("Flotting s'est acheve")
time.sleep(300)