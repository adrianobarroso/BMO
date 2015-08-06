# -*- coding: utf-8 -*-
'''
Programa principal

Compara os dados reprocessados em python com o arquivo Summary (calculado
pela boia) e os do argos (baixados do site)

Henrique P. P. Pereira
LIOc/COPPE/UFRJ

-- Descricao --
Verificar se mesmo com a data baguncada do arquivo Summary
conseguimos coincidir as data utilizando o plot_date, ou 
tentando ler os dados e fazer um 'sort'.

Ultima modificacao: 21/01/2015
'''

import numpy as np
from matplotlib import pylab as pl
from datetime import datetime
import os

pl.close('all')

# ============================================================================== #
#Carrega os dados

estado = 'pe'
local1 = 'recife'
local = 'Recife'
id_argos = '69154'

pathname = os.environ['HOME'] + '/Dropbox/pnboia/rot/saida/' + local1 + '/'

#Saida do Python
#      					0   1   2    3   4     5    6  7  8
#parametros de onda = [Data,Hs,H10,Hmax,Tmed,THmax,Hm0,Tp,Dp]
py = np.loadtxt(pathname + 'paramwp_8-' + local1 + '.out',delimiter=',',skiprows = 0)

#Saida da Axys
#  0        1            2          3        4        5         6        7            8            9         10     11           12       13      14              15  
#YearJulian Date/Zero Crossings/Ave. Ht./Ave. Per./Max Ht./Sig. Wave/Sig. Per./Peak Per.(Tp)/Peak Per.(READ)/HM0/Mean Theta/Sigma Theta/ H1/10 / T.H1/10	/Mean Per.(Tz)
ax = np.loadtxt(pathname + 'Summary_todos.txt',skiprows = 1, usecols = (range(2,18)))
ax_data = np.loadtxt(pathname + 'Summary_todos.txt',dtype = str, skiprows = 1, usecols = (0,1))

#Saida site (baixado em 08/09/2013)
#  0   1   2   3     4    5    6   7   8
# ano mes dia hora minuto Hs Hmax Tp Dirm
site = np.loadtxt(pathname + 'pnboia.B' + id_argos + '_argos.dat',delimiter=',', skiprows = 1, usecols = (2,3,4,5,6,45,46,47,48))

# ============================================================================== #
#cria variaveis de datas

#python
datam_py = []
for i in range(len(py)):
	datam_py.append(datetime(int(str(py[i,0])[0:4]),int(str(py[i,0])[4:6]),int(str(py[i,0])[6:8]),int(str(py[i,0])[8:10])))

#deixa datas com numeros inteiros
ano_ax = [int(ax_data[i,0][0:4]) for i in range(len(ax_data))]
mes_ax = [int(ax_data[i,0][5:7]) for i in range(len(ax_data))]
dia_ax = [int(ax_data[i,0][8:10]) for i in range(len(ax_data))]
hora_ax = [int(ax_data[i,1][:2]) for i in range(len(ax_data))]
min_ax = [int(ax_data[i,1][3:]) for i in range(len(ax_data))]

datam_ax = []
for i in range(len(ax_data)):
	datam_ax.append(datetime(ano_ax[i],mes_ax[i],dia_ax[i],hora_ax[i],min_ax[i]))

#site
#deixa os valores com -99999 (erro) com nan
for i in range(site.shape[1]):
	site[np.where(site[:,i] == -99999),i] = np.nan

ano_st = site[:,0]
mes_st = site[:,1]
dia_st = site[:,2]
hora_st = site[:,3] 
min_st = np.zeros(len(site))

datam_st = []
for i in range(len(site)):
	datam_st.append(datetime(int(ano_st[i]),int(mes_st[i]),int(dia_st[i]),int(hora_st[i]),int(min_st[i])))

# ============================================================================== #
#Definicao de parametros de onda

#python
hs_py = py[:,1]
h10_py = py[:,2]
hmax_py = py[:,3]
tmed_py = py[:,4]
thmax_py = py[:,5]
hm0_py = py[:,6]
tp_py = py[:,7]
dirtp_py = py[:,8]

#axys
hm0_ax = ax[:,10]
tp_ax = ax[:,8] #qual periodo usar?
tmed_ax = ax[:,15]
th10_ax = ax[:,14]
dirtp_ax = ax[:,11]
hmax_ax = ax[:,5]
hs_ax = ax[:,6]
h10_ax = ax[:,13]

#site
hs_st = site[:,5]
hmax_st = site[:,6]
tp_st = site[:,7]
dirm_st = site[:,8]

# ========================================================================== #
#Correcao dos dados (para facilitar na visualizacao dos graficos
#*pois tem valores de hs de 1200 no site)

hs_st[(np.where(hs_st>30))] = np.nan

# ========================================================================== #

#Graficos

# #hm0 
# pl.figure()
# pl.plot_date(datam_py,hm0_py,'bo')
# pl.plot_date(datam_ax,hm0_ax,'go',alpha=0.5)
# pl.title('Hm0 - Rio_Grande_do_Sul')
# pl.ylabel('metros')
# pl.legend(('python','axys'))

# #hs
# pl.figure()
# pl.plot_date(datam_py,hs_py,'bo')
# pl.plot_date(datam_ax,hs_ax,'go',alpha=0.6)
# pl.plot_date(datam_st,hs_st,'ro',alpha=0.5)
# pl.title('Hs - Rio_Grande_do_Sul')
# pl.ylabel('meters')
# pl.legend(('python','axys','site'))

# #h 1/10
# pl.figure()
# pl.plot_date(datam_py,h10_py,'bo')
# pl.plot_date(datam_ax,h10_ax,'go',alpha=0.5)
# pl.title('H 1/10 - Rio_Grande_do_Sul')
# pl.ylabel('metros')
# pl.legend(('python','axys'))

# #hmax
# pl.figure()
# pl.plot_date(datam_py,hmax_py,'bo')
# pl.plot_date(datam_ax,hmax_ax,'go',alpha=0.6)
# pl.plot_date(datam_st,hmax_st,'ro',alpha=0.5)
# pl.ylabel('metros')
# pl.title('Hmax - Rio_Grande_do_Sul')
# pl.legend(('python','axys','site'))

# #tp
# pl.figure()
# pl.plot_date(datam_py,tp_py,'bo')
# pl.plot_date(datam_ax,tp_ax,'go',alpha=0.6)
# pl.plot_date(datam_st,tp_st,'ro',alpha=0.5)
# pl.ylabel('segundos')
# pl.title('Tp - Rio_Grande_do_Sul')
# pl.legend(('python','axys','site'))

# #tmed
# pl.figure()
# pl.plot_date(datam_py,tmed_py,'bo')
# pl.plot_date(datam_ax,tmed_ax,'go',alpha=0.5)
# pl.title('tmed')
# pl.legend(('python','axys'))

# #t hmax
# pl.figure()
# pl.plot_date(datam_py,thmax_py,'bo')
# pl.plot_date(datam_ax,th10_ax,'go',alpha=0.6)
# pl.title('t hmax')
# pl.legend(('python','axys'))

# #dirtp
# pl.figure()
# pl.plot_date(datam_py,dirtp_py,'bo')
# pl.plot_date(datam_ax,dirtp_ax,'go',alpha=0.6)
# pl.plot_date(datam_st,dirm_st,'ro',alpha=0.5)
# pl.title('Dirtp - Rio_Grande_do_Sul')
# pl.ylabel('graus')
# pl.legend(('python','axys','site'))

#subplot do periodo de dez 09
pl.figure()
pl.subplot(3,1,1)
pl.plot_date(datam_py,hs_py,'bo')
pl.plot_date(datam_ax,hs_ax,'go',alpha=0.6)
pl.plot_date(datam_st,hs_st,'ro',alpha=0.5)
pl.axis([datam_py[0],datam_py[-1],0,10])
pl.title(local)
pl.ylabel('Hs - metros')
pl.legend(('lioc','axys','site'))
pl.xticks(rotation=70)
pl.subplot(3,1,2)
pl.plot_date(datam_py,tp_py,'bo')
pl.plot_date(datam_ax,tp_ax,'go',alpha=0.6)
pl.plot_date(datam_st,tp_st,'ro',alpha=0.5)
pl.axis([datam_py[0],datam_py[-1],0,20])
pl.ylabel('Tp - segundos')
# pl.legend(('lioc','axys','site'))
pl.subplot(3,1,3)
pl.plot_date(datam_py,dirtp_py,'bo')
pl.plot_date(datam_ax,dirtp_ax,'go',alpha=0.6)
pl.plot_date(datam_st,dirm_st,'ro',alpha=0.5)
pl.axis([datam_py[0],datam_py[-1],0,360])
pl.ylabel('Dp - graus')
# pl.legend(('lioc','axys','site'))

pl.show()