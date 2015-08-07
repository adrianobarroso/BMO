'''
================================================================================== #
PROGRAMA PRINCIPAL PARA PROCESSAMENTO DE DADOS DA BOIA AXYS
================================================================================== #

Autores: 
Henrique P. P. Pereira
Izabel C. M. Nogueira
Ricardo M. Campos
Carlos E. Parente
Fabio Nascimento

Laboratorio de Instrumentacao Oceanografica - COPPE/UFRJ

Data da ultima modificacao: 06/12/2014

================================================================================== #
### Descricao
================================================================================== #
    
Cria uma variavel 'lista' com os arquivos HNE que estao dentro do 'pathname', 
le e processa cada arquivo HNE listado. Passa por uma consitencia, onde sao 
listados os arquivos incosistentes e consistentes atribuindo um flag. Processa
os arquivos consistentes. Chama o modulo 'proc_onda' para processamento dos
dados no dominio do tempo e frequencia. Cria uma variavel 'mat_onda' contendo
os parametros calculados. Cria uma tabela 'saida.txt' com os parametros. Cria
graficos dos parametros.
- Calcula Tp1 (mais energetico) e Tp2
- Calcula Spreading (Tucker) - cos2s?? 

para processar apenas 1 ou poucos arquivos, verificar se o teste de variabildade 
e consecutivos iguais no 'consisteproc.py' estao habilitados, pois pode dar erro

#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
        
'''

# ================================================================================== #
# Modulos utilizados
# ================================================================================== #

from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import os
import sys
import numpy as np
import pylab as pl
import time
from datetime import datetime
import proconda
import consistebruto
import consisteespec
import consisteproc
import relatorio
#import graficos_axys
# import jonswap_wafo #calculo do gamma
import jonswap
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.stats import norm
import matplotlib.mlab as mlab

reload(proconda)
reload(consistebruto)
reload(consisteespec)
reload(consisteproc)
reload(relatorio)
reload(jonswap)

pl.close('all')


#habilita a daat
#import daat


# ================================================================================== #
# Contador inicial de tempo de execucao

tic = time.clock()

# ================================================================================== #
#### Dados de entrada
# ================================================================================== #

#localizacao (habilite um para processar)

local = 'Recife/PE' # relatorio
local1 = 'recife' #nome do arquivo salvo
latlon = '-8.149 / -34.56' #relatorio
idargos = '69154'
idwmo = '31052'

# local = 'Santos/SP'
# local1 = 'santos'
# latlon = '-25.28334 / -44.93334'
# idargos = '69151'
# idwmo = '31051'

# local = 'Florianpolis/SC'
# local1 = 'florianopolis'
# latlon = '-28.50000 / -47.36667'
# idargos = '69150'
# idwmo = '31374'

#local = 'Rio Grande/RS'
#local1 = 'rio_grande'
#latlon = '-31.56667 / -49.86667'
#idargos = '69153'
#idwmo = '31053'

# local = 'Porto Seguro/BA' #nao tem dados validos
# local1 = 'porto_seguro'
# latlon = '-18.151 / -37.94367'
# idargos = '69007'
# idwmo = '31260'

print 'Processamento em... ' + local
#opcoes de plotagem (1=plota , 0=nao)
plotfig = 0
figtese = 0

#corrige a dmag na plotagem (1=sim , 0=nao)
mdp = 1 


#caminho onde estao os arquivos .HNE
# pathname = os.environ['HOME'] + '/Dropbox/lioc/dados/pnboia/axys/ondas/preproc/' + local1 + '/hne_' + local1 + '/'
pathname = os.environ['HOME'] + '/Dropbox/lioc/dados/pnboia/triaxys/' + local1 + '/HNE/'
pathnameout = os.environ['HOME'] + '/Dropbox/pnboia/out/'


#para processar todos os arquivos (comentao o p0 e p1 abaixo)
# p0 = 2500
# p1 = 2600

#escolhe a data inicial e final para ser processada (opcional, no 'p0' e 'p1')
z0 = '200905090600.HNE'
z1 = '200905090600.HNE'

#z0 = '200907241900.HNE' #freakwave 1
#z1 = z0

# # z0 = '200910051100.HNE' #freakwave 2
# # z1 = z0

#z0 = '201203281400.HNE' #freakwave 3
#z1 = z0

# # z0 = '201210161000.HNE' #freakwave 4
# # z1 = z0

#evento de 13 de dez - maior hs
#z0 = '200912130600.HNE' #maior hs
#z1 = z0

h = 200 #profundidade 
nfft = 82 #numero de dados para a fft (p/ nlin=1312: 32gl;nfft=82, 16gl;nfft=164, 8gl;nfft=328)
fs = 1.28 #freq de amostragem
nlin = 1312 #comprimento da serie temporal a ser processada
gl = (nlin/nfft) * 2

#numero de testes habilitados
ntb = 9 #brutos
#nte = 3 #espectro
ntp = 3 #processado

#numero de parametros a serem calculados
npa = 19


#define funcoes
#======================================================================#

def lista_hne(pathname):

    ''' Lista arquivos com extensao .HNE 
    que estao dentro do diretorio 'pathname' 

    Entrada: pathname - diretorio que estao os arquivos
    Saida: arq - variavel com o nome dos arquivos

    '''

    lista = []
    # Lista arquivos do diretorio atual
    for f in os.listdir(pathname):
        if f.endswith('.HNE'):
            lista.append(f)
    lista=np.sort(lista)

    return lista

def dados_hne(pathname,arq):

    ''' Retorna os dados de tempo, elevacao e
    deslocamentos norte e leste

    Entrada: nome do arquivo com extensao -exemplo: 200907060200.HNE

    Saida: t - tempo
           eta - elevacao
           dspy - deslocamento norte
           dspx - deslocamento leste
           data - ano, mes, dia, hora, minuto
 '''

    #le os dados a partir da 11 linha que sao numeros
    dados=np.loadtxt(pathname+arq, skiprows = 11)

    ano = arq[0:4]
    mes = arq[4:6]
    dia = arq[6:8]
    hora = arq[8:10]
    minuto = arq[10:12]

    data = [ano, mes, dia, hora, minuto]

    return dados,data

#======================================================================#


#cria variavel 'lista' com nome dos arquivos HNE
lista = np.array(lista_hne(pathname))

#numero dos arq para processar (modificar p0=0 e p1=len(lista) para todos)
#p0 = np.where(lista == z0)[0][0]
#p1 = np.where(lista == z1)[0][0]

#processar todos os arquivos
p0 = 0
p1 = len(lista)


# ================================================================================== #
#### Incicializacao do programa
# ================================================================================== #

#lista dos arquivos que serao processados
listap = lista[p0:p1+1] 
listap = [listap[i][0:-4] for i in range(len(listap))]

#numero de arquivos a serem processados
ncol = len(listap)

#cria vetores de flags das series brutas
flagb = np.zeros((len(listap),4),dtype='|S32')
flagb[:,0] = listap

#cria vetores de flags dos parametros espectrais
flage = np.zeros((1,4),dtype='S32')
flage1 = np.copy(flage)

#parametros criados no processamento em batelada
matondab = [] #matriz com parametros de onda
listac = [] #lista de arquivos consistentes
listai = [] #lista de arquivos inconsistentes

# ================================================================================== #
#### Processamento em batelada
# ================================================================================== #

# ================================================================================== #
#DAAT

# espe1, energ, dire1 = daat.daat1(pathname,listap,nfft,fs,ncol,p0,p1)

# ================================================================================== #

#contador
cont = -1
eta_mat = []
eta_med = []
eta_dp = []
fase_nnx = [] #valor do espec de fase para a fp
fase_nny = [] #valor do espec de fase para a fp
fase_nxny = [] #valor do espec de fase para a fp
coer_nnx = [] #valor do espec de coerencia para a fp
coer_nny = [] #valor do espec de coerencia para a fp
coer_nxny = [] #valor do espec de coerencia para a fp

for i in range(len(listap)):

    plt.close('all')

    print 'LH: ' + str(i+1)   

    cont = cont + 1

    #carrega dados e data
    dados, data = dados_hne(pathname,listap[i]+'.HNE')

    #define variaveis
    t = dados[:,0]
    eta = dados[:,1]
    etay = dados[:,2]
    etax = dados[:,3]

    # ================================================================================== #  
    # Testes de consistencia dos dados processados
    
    #Teste 1 - validade da mensagem (apenas axys *.HNE) -  validade do nome do arquivo (ind=0)
    flagb[i,1] = consistebruto.msg(listap[i],flagb[i,1])
    flagb[i,2] = consistebruto.msg(listap[i],flagb[i,2])
    flagb[i,3] = consistebruto.msg(listap[i],flagb[i,3])
    
    #Teste 2 - comprimento do vetor (ind=1)
    flagb[i,1] = consistebruto.comp(eta,1312,flagb[i,1])
    flagb[i,2] = consistebruto.comp(etax,1312,flagb[i,2])
    flagb[i,3] = consistebruto.comp(etay,1312,flagb[i,3])

    #Teste 3 - gap (lacuna)
    flagb[i,1] = consistebruto.gap(eta,10,flagb[i,1])
    flagb[i,2] = consistebruto.gap(etax,10,flagb[i,2])
    flagb[i,3] = consistebruto.gap(etay,10,flagb[i,3])

    #Teste 4 - spike
    flagb[i,1], vet_etai = consistebruto.spike(eta,np.mean(eta),np.std(eta),10,5,2,flagb[i,1])
    flagb[i,2], vet_etaxi = consistebruto.spike(etax,np.mean(etax),np.std(etax),10,5,2,flagb[i,2])
    flagb[i,3], vet_etayi = consistebruto.spike(etay,np.mean(etay),np.std(etay),10,5,2,flagb[i,3])
    
    #Teste 5 - valores flat
    flagb[i,1] = consistebruto.flat(eta,-0.15,0.15,flagb[i,1])
    flagb[i,2] = consistebruto.flat(etax,-0.15,0.15,flagb[i,2])
    flagb[i,3] = consistebruto.flat(etay,-0.15,0.15,flagb[i,3])
    
    #Teste 6 - valores consecutivos nulos
    flagb[i,1] = consistebruto.nulos(eta,10,flagb[i,1])
    flagb[i,2] = consistebruto.nulos(etax,10,flagb[i,2])
    flagb[i,3] = consistebruto.nulos(etay,10,flagb[i,3])
    
    #Teste 7 -valores consecutivos iguais
    flagb[i,1] = consistebruto.iguais(eta,10,flagb[i,1])
    flagb[i,2] = consistebruto.iguais(etax,10,flagb[i,2])
    flagb[i,3] = consistebruto.iguais(etay,10,flagb[i,3])
 
    #Teste 8 -valores que excedem limites de faixa
    flagb[i,1] = consistebruto.faixa(eta,-20,20,flagb[i,1])
    flagb[i,2] = consistebruto.faixa(etax,-20,20,flagb[i,2])
    flagb[i,3] = consistebruto.faixa(etay,-20,20,flagb[i,3])

    #Teste 9 -deslocamento da media (shift)
    flagb[i,1] = consistebruto.shift(eta,164,8,0.3,flagb[i,1])
    flagb[i,2] = consistebruto.shift(etax,164,8,0.3,flagb[i,2])
    flagb[i,3] = consistebruto.shift(etay,164,8,0.3,flagb[i,3])

    # ================================================================================== #
    # Condicao para dados aprovados na consistencia dos dados brutos
    
    if (flagb[i,1:] == [ntb*'1',ntb*'1',ntb*'1']).all():

        t = t[0:nlin]
        eta = eta[0:nlin]
        etax = etax[0:nlin]
        etay = etay[0:nlin]

        #cria matriz com serie de heave (para o calculo do multiplicador do desvio padrao)
        eta_mat.append(eta)
        eta_med.append(np.mean(eta))
        eta_dp.append(np.std(eta))

        #lista nome dos arquivos consistentes 
        listac.append(listap[cont])

        #processamento no dominio do tempo
        hs,h10,hmax,tmed,thmax = proconda.ondat(t,eta,h)

        #processamento no dominio da frequencia
        hm0, tp, dp, sigma1, sigma2, sigma1p, sigma2p, freq, df, k, sn, snx,sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2 = proconda.ondaf(
            eta,etax,etay,h,nfft,fs)

        #calcula o espectro de fase (fase e coerencia)
        #acha o indice da fp
        indfp = pl.find(sn[:,0]==sn[sn[:,1]==max(sn[:,1]),0])

        fase_nnx.append(np.real(snnx[indfp,4])[0]) #fase de heave e dspx
        fase_nny.append(np.real(snny[indfp,4])[0]) #fase de heave e dspx
        fase_nxny.append(np.real(snxny[indfp,4])[0]) #fase de heave e dspx

        coer_nnx.append(np.real(snnx[indfp,5])[0]) #coerencia de heave e dspx
        coer_nny.append(np.real(snny[indfp,5])[0]) #coerencia de heave e dspx
        coer_nxny.append(np.real(snxny[indfp,5])[0]) #coerencia de heave e dspx

        # #parametros de ondas instantaneos
        # Hm0 = pondaf[0]
        # Tp = pondaf[1]
        # Dp = pondaf[2]

        #plota o espectro
        # pl.figure()
        # pl.plot(f,sn[:,1])
        # pl.title(listac[-1])

        #processamento no dominio da frequencia particionado (sea e swell)
        hm01, tp1, dp1, hm02, tp2, dp2 = proconda.ondap(hm0,tp,dp,sn,dire1,df)

        #calcula o espalhamento angular (kuik et al 1988)
        #sprc - vetor de spread complexo
        #spr - vetor de spread
        # sprc, spr, sprr = proconda.spread(sn[:,1],a1,b1)

        #calculo do parametro gamma - WAFO
        # gam = jonswap.jonswap_peakfact(hm0,tp)
        # gam1 = jonswap.jonswap_peakfact(hm01,tp1)
        # gam2 = jonswap.jonswap_peakfact(hm02,tp2)

        #calculo do parametro gamma - LIOc
        gam = jonswap.gamma(tp)
        gam1 = jonswap.gamma(tp1)
        gam2 = jonswap.gamma(tp2)

        #espectro de jonswap
        s_js = jonswap.spec(hm0,tp,freq,gam)
        s_js2 = jonswap.spec(hm02,tp2,freq,gam2)

        # pl.figure()
        # pl.plot(freq,sn[:,1],freq,s_js,freq,s_js2)
        # pl.legend(['LIOc','JS-1','JS-2'])
        # pl.title('Espectro de Energia - LIOc')
        # pl.xlabel('Frequencia (Hz)')
        # pl.ylabel('m^2/Hz')
        # pl.grid()
        
        #espectro direcional
        if plotfig == 1:

            [freqs,dires] = np.meshgrid(np.linspace(0,max(freq),100),np.linspace(0,360,100),sparse=False,copy=False)
            en = sn[:,1] * np.real(sigma1)

            #interpola a energia
            sp2 = mpl.mlab.griddata(freq,dire1,en/max(np.real(sigma2)),freqs,dires,interp='linear') #a interp linear e a nn ficaram praticamente iguais

            #coloca zeros no lugar de nan
            sp2.data[np.where(np.isnan(sp2.data)==True)] = 0

            #surface
            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            # ax.plot_surface(freqs, dires, sp2)
            # surf = ax.plot_surface(freqs, dires, sp2.data, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
            # ax.zaxis.set_major_locator(LinearLocator(10))
            # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
            # fig.colorbar(surf, shrink=0.5, aspect=5)

            #contourf
            plt.figure()
            plt.subplot(211)
            plt.title(local + ' - ' + str(int(listac[-1])) + ' -- Hs=%.2f, Tp=%.2f, Dp=%.2f' %(hm0, tp, dp))
            plt.plot(t,eta), plt.axis('tight')
            plt.ylabel('metros'), plt.xlabel('segundos')
            plt.subplot(223)
            plt.plot(freq,sn[:,1],'b')
            plt.xlabel('Freq. (Hz)'), plt.ylabel('m2/Hz')
            # plt.twinx()
            # plt.plot(freq,sigma1,'r'), plt.legend('spread'), plt.ylabel('graus')
            plt.subplot(224)
            # cs = plt.pcolormesh(freqs,dires,sp2,shading='flat',cmap=plt.cm.jet) #,vmin=np.nanmin(sp2),vmax=np.nanmax(sp2))
            cs = plt.contourf(freqs,dires,sp2.data,shading='flat',cmap=plt.cm.jet,\
                levels=np.arange(0,np.nanmax(sp2.data),0.25),vmin=np.nanmin(sp2.data),vmax=np.nanmax(sp2.data))
            plt.xlabel('Freq. (Hz)'), plt.ylabel('graus')
            plt.colorbar()
            
            # plt.show()
            # plt.savefig('/media/hp/MOSKOWITZ/documentos/pnboia/espec2d/' + local1 + '/' + local1 + '_espec2d_' + str(int(listac[-1])))

            # plt.close('all')

        # ================================================================================== #
        # Consistencia dos parametros espectrais
        
    #     #coloca data na primeira coluna do flage
    #     flage[-1,0] = listac[-1]

        # ================================================================================== #
        # Testes de consistencia dos parametros espectrais

    #     #Teste 1 - check-ratio (coloca flag em heave, dspx e dspy)
    #     flage[-1,[1,2,3]], kf, rf, rf_med = consiste_espec.checkratio(h,k,snn,snxnx,snyny,flage[-1,[1,2,3]])

    #     #Teste 2 - faixa de frequencia operacional
    #     flage[-1,1] = consiste_espec.freq_range(1/Tp,1,0.333,1,0.1,flage[-1,1])

        # ================================================================================== #

    #     #monta vetor de flag na iteracao
    #     flage = np.concatenate((flage,flage1))

        # ================================================================================== #  
        # Condicao para dados aprovados na consistencia dos parametros espectrais

    #     if (flage[-2,1:] == [nte*'1',nte*'1',nte*'1']).all():

        #         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
        #header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')
        # * no caso de utilizar a consiste_espec, remover uma identacao no 'matonda'
        matondab.append(np.concatenate([([int(listac[-1])]),[hs,h10,hmax,tmed,thmax,hm0,tp,dp,sigma1p,sigma2p,hm01,tp1,dp1,hm02,tp2,dp2,gam,gam1,gam2]]))

    #Condicao para dado inconsistentes
    else:

        #lista nome dos arquivos inconsistentes 
        listai.append(listap[i])

        #coloca NaN nos dados reprovados na consistencia dos dados brutos e espectrais
        matondab.append(np.concatenate([([int(listai[-1])]),npa * [np.nan]]))


# ================================================================================== #  
#### Finalizacao do processamento em batelada
# ================================================================================== #  

#retira a ultima linha do flage
# flage = flage[:-1,:]

# ================================================================================== #  
# Realiza a consistencia dos dados processados

if len(listac) > 0:

    #deixa coluna de dados em string
    # matonda[:,0].astype(int)
    
    #cria array das listas criadas
    matondab = np.array(matondab)
    listac = np.array(listac)
    listaip = np.copy(listai)
    listai = np.array(listai)

    #cria vetor dos parametros calculados
    datap = matondab[:,0]
    hs = matondab[:,1] 
    h10 = matondab[:,2] 
    hmax = matondab[:,3]
    tmed = matondab[:,4] 
    thmax = matondab[:,5] 
    hm0 = matondab[:,6] 
    tp = matondab[:,7] 
    dp = matondab[:,8] 
    sigma1p = matondab[:,9] 
    sigma2p = matondab[:,10] 
    hm01 = matondab[:,11] 
    tp1 = matondab[:,12]
    dp1 = matondab[:,13]
    hm02 = matondab[:,14]
    tp2 = matondab[:,15] 
    dp2 = matondab[:,16]
    gam = matondab[:,17]
    gam1 = matondab[:,18]
    gam2 = matondab[:,19]

    #cria vetores de flags das series processadas (depende das qtdade de variaveis a serem consistidas + data) 
    flagp = np.zeros((len(listap),npa+1),dtype='|S32')
    flagp[:,0] = listap[:]
    
    # ================================================================================== #  
    # Testes de consistencia dos dados processados

    #Teste 1 - faixa
    flagp[:,1] = consisteproc.faixa(hs,0,20,0.25,8,flagp[:,1])
    flagp[:,2] = consisteproc.faixa(h10,0,20,0.25,8,flagp[:,2])
    flagp[:,3] = consisteproc.faixa(hmax,0,35,0.5,20,flagp[:,3])
    flagp[:,4] = consisteproc.faixa(tmed,3,30,4,18,flagp[:,4])
    flagp[:,5] = consisteproc.faixa(thmax,3,30,4,18,flagp[:,5])
    flagp[:,6] = consisteproc.faixa(hm0,0,20,0.25,8,flagp[:,6])
    flagp[:,7] = consisteproc.faixa(tp,3,30,4,18,flagp[:,7])
    flagp[:,8] = consisteproc.faixa(dp,0,360,0,360,flagp[:,8])
    flagp[:,9] = consisteproc.faixa(sigma1p,0,360,0,360,flagp[:,9])
    flagp[:,10] = consisteproc.faixa(sigma2p,0,360,0,360,flagp[:,10])
    flagp[:,11] = consisteproc.faixa(hm01,0,20,0.25,8,flagp[:,11])
    flagp[:,12] = consisteproc.faixa(tp1,3,30,4,18,flagp[:,12])
    flagp[:,13] = consisteproc.faixa(dp1,0,360,0,360,flagp[:,13])
    flagp[:,14] = consisteproc.faixa(hm02,0,20,0.25,8,flagp[:,14])
    flagp[:,15] = consisteproc.faixa(tp2,3,30,4,18,flagp[:,15])
    flagp[:,16] = consisteproc.faixa(dp2,0,360,0,360,flagp[:,16])

    #Teste 2 - Variabilidade temporal
    flagp[:,1] = consisteproc.variab(hs,1,5,flagp[:,1])
    flagp[:,2] = consisteproc.variab(h10,1,5,flagp[:,2])
    flagp[:,3] = consisteproc.variab(hmax,1,5,flagp[:,3])
    flagp[:,4] = consisteproc.variab(tmed,1,20,flagp[:,4])
    flagp[:,5] = consisteproc.variab(thmax,1,20,flagp[:,5])
    flagp[:,6] = consisteproc.variab(hm0,1,5,flagp[:,6])
    flagp[:,7] = consisteproc.variab(tp,1,20,flagp[:,7])
    flagp[:,8] = consisteproc.variab(dp,1,360,flagp[:,8])
    flagp[:,9] = consisteproc.variab(hm01,1,5,flagp[:,9])
    flagp[:,10] = consisteproc.variab(sigma1p,1,360,flagp[:,10])
    flagp[:,11] = consisteproc.variab(sigma2p,1,360,flagp[:,11])
    flagp[:,12] = consisteproc.variab(tp1,1,20,flagp[:,12])
    flagp[:,13] = consisteproc.variab(dp1,1,360,flagp[:,13])
    flagp[:,14] = consisteproc.variab(hm02,1,5,flagp[:,14])
    flagp[:,15] = consisteproc.variab(tp2,1,20,flagp[:,15])
    flagp[:,16] = consisteproc.variab(dp2,1,360,flagp[:,16])

    #Teste 3 - Valores consecutivos iguais 
    flagp[:,1] = consisteproc.iguais(hs,5,flagp[:,1])
    flagp[:,2] = consisteproc.iguais(h10,5,flagp[:,2])
    flagp[:,3] = consisteproc.iguais(hmax,5,flagp[:,3])
    flagp[:,4] = consisteproc.iguais(tmed,20,flagp[:,4])
    flagp[:,5] = consisteproc.iguais(thmax,20,flagp[:,5])
    flagp[:,6] = consisteproc.iguais(hm0,5,flagp[:,6])
    flagp[:,7] = consisteproc.iguais(tp,20,flagp[:,7])
    flagp[:,8] = consisteproc.iguais(dp,20,flagp[:,8])
    flagp[:,9] = consisteproc.iguais(sigma1p,20,flagp[:,9])
    flagp[:,10] = consisteproc.iguais(sigma2p,20,flagp[:,10])
    flagp[:,11] = consisteproc.iguais(hm01,5,flagp[:,11])
    flagp[:,12] = consisteproc.iguais(tp1,20,flagp[:,12])
    flagp[:,13] = consisteproc.iguais(dp1,20,flagp[:,13])
    flagp[:,14] = consisteproc.iguais(hm02,5,flagp[:,14])
    flagp[:,15] = consisteproc.iguais(tp2,20,flagp[:,15])
    flagp[:,16] = consisteproc.iguais(dp2,20,flagp[:,16])


    # ================================================================================== #  
    # Coloca nan nos dados reprovados
    
    matondap = np.copy(matondab)

    for c in range(1,flagp.shape[1]):

        for i in range(len(flagp)):

            if '4' in flagp[i,c]:

                matondap[i,c] = np.nan


    # ================================================================================== #  

    #parametros de ondas processados
    # matondap = np.array([datap,hsc,h10c,hmaxc,tmedc,thmaxc,hm0c, tpc, dpc, sigma1pc,
    # sigma2pc, hm01c, tp1c, dp1c, hm02c, tp2c, dp2c]).T

    # ================================================================================== #  
    # Imprime relatorio de controle de qualidade

    # salva relatorio em txt
    # f = open('saida/'+'consistencia_'+str(gl)+'-'+local1+'.out','w')
    # fflagb, fflagp = relatorio.axys(f,lista,listap,listac,listai,flagb,flagp,h,local,latlon,idargos,idwmo)
    




    # ================================================================================== #  
    # ================================================================================== #  
    # Cria saida de dados com savetxt

    #parametros de ondas com cq apenas nos dados brutos
    np.savetxt(pathnameout+'/B'+str(idargos)+'_Wave_DB'+str(gl)+'.out',matondab,delimiter=',',fmt=['%i']+npa*['%.2f'],
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

    #parametros de ondas com cq nos dados brutos e processados
    np.savetxt(pathnameout+'/B'+str(idargos)+'_Wave_DP'+str(gl)+'.out',matondap,delimiter=',',fmt=['%i']+npa*['%.2f'],
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

    #flags aplicados nos dados brutos
    np.savetxt(pathnameout+'/B'+str(idargos)+'_Flags_DB'+str(gl)+'.out',flagb,delimiter=',',fmt='%s',
        header='date,eta,etax,etay')

    #flags aplicados nos dados processados
    np.savetxt(pathnameout+'/B'+str(idargos)+'_Flags_DP'+str(gl)+'.out',flagp,delimiter=',',fmt='%s',
        header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2')

    #lista de dados aprovados no cq bruto
    #np.savetxt(pathnameout+'/B'+str(idargos)+'_DB'+str(gl)+'_LIOc.out',listac,fmt='%s') #lista de dados aprovados no cq bruto

    #lista de dados reprovados no cq bruto
    #np.savetxt('out/'+'listaib_'+str(gl)+'-'+local1+'.out',listai,fmt='%s') #lista de dados reprovados no cq bruto



else:

    print('Todos os arquivos reprovaram em algum teste de Controle de Qualidade' '\n' '\n')

#data com datetime
datat = np.array([datetime.strptime(str(int(matondap[i,0])), '%Y%m%d%H%M') for i in range(len(matondap))])
datatcb = np.array([datetime.strptime(str(int(listac[i])), '%Y%m%d%H%M') for i in range(len(listac))])


#         0   1   2   3    4     5    6   7   8     9       10       11   12   13   14    15   16   17    18   19
#header='data,hs,h10,hmax,tmed,thmax,hm0, tp, dp, sigma1p, sigma2p, hm01, tp1, dp1, hm02, tp2, dp2, gam, gam1, gam2')

if figtese == 1:

    ###########################################################################
    #verifica multiplicador do desvio padrao

    #verifica multiplicador do desvio padrao
    if mdp == 1:
        eta_mat = np.array(eta_mat)
        M = np.zeros((eta_mat.shape[0],eta_mat.shape[1]))
        #matriz com elevacao
        for cc in range(np.size(eta_mat)/nlin):
            for ii in range(eta_mat.shape[1]):
                M[cc,ii] = ( eta_mat[cc,ii] - eta_med[cc] ) / eta_dp[cc]


        eta_mat = eta_mat.reshape(np.size(eta_mat),1)
        M = M.reshape(np.size(eta_mat),1)



        #plot da serie de heave, hs e hmax
        pl.figure()
        pl.subplot(211)
        pl.plot(eta_mat)
        pl.axis('tight')
        pl.ylim(-7,7)
        pl.ylabel(r'$Heave\ (m)$')
        pl.xticks([])
        pl.subplot(212)
        pl.plot(datat,matondap[:,1],'b',label='Hs')
        pl.plot(datat,matondap[:,3],'r',label='Hmax')
        pl.ylabel(r'$Hs\ e\ Hmax\ (m)$')
        pl.legend(loc=0,fontsize=10)
        pl.ylim(0,13)

        #histograma do multiplicador do dp de heave 
        pl.figure()
        p98 = np.percentile(M,98)
        (mu, sigma) = norm.fit(M) #ajusta a melhor curva para os dados #media e despad?
        n, bins, patches = pl.hist(M,50,normed=1,facecolor='blue',alpha=0.75)
        y = mlab.normpdf( bins, mu, sigma)
        l = pl.plot(bins, y, 'r--',linewidth=3)
        pl.title(r'$\mathrm{}\ Max=%.2f,\ Min=%.2f,\ \sigma=%.2f,\ P98=%.2f$' %(M.max(), M.min(), sigma, p98 ))
        pl.xlabel(r'$M$'), pl.ylabel(r'$Probabilidade$')
        pl.axis('tight'), pl.grid()
        pl.xlim(-5,5)


        #plotagem da serie temporal e espectro
        pl.figure()
        t1 = t - t[0]
        pl.subplot(2,1,1)
        pl.plot(t1,eta)
        pl.plot([t1[0],t1[-1]],[5*np.std(eta),5*np.std(eta)],'r-.',linewidth=3)
        pl.plot([t1[0],t1[-1]],[4*np.std(eta),4*np.std(eta)],'r-.',linewidth=3)
        pl.plot([t1[0],t1[-1]],[-5*np.std(eta),-5*np.std(eta)],'r-.',linewidth=3)
        pl.plot([t1[0],t1[-1]],[-4*np.std(eta),-4*np.std(eta)],'r-.',linewidth=3)
        pl.title(datat.astype(str)[0]+'\n Hs=%.1f' %matondap[0,1]+' m, Hmax=%.1f' %matondap[0,3]+' m, Hmax/Hs=%.1f' %(matondap[0,3]/matondap[0,1])+' m, Tp=%.1f' %matondap[0,7]+' s, Dp=%i' %(matondap[0,8]-17)+u' \u00b0')
        pl.axis('tight')
        pl.xlabel(r'$Tempo\ (s)$')
        pl.ylabel(r'$Elevac\c{}a\~o\ (m)$')
        pl.grid()
        pl.yticks([-8,-6,-4,-2,0,2,4,6,8])
        pl.ylim(-9,9)


        dmag = -17
        pl.subplot(2,2,3)
        pl.plot(sn[:,0],dire1+dmag)
        pl.axis('tight')
        pl.yticks([0,45,90,135,180,225,270,315,360])
        pl.plot([1/tp,1/tp],[0,360],'k--')
        pl.xlabel(r'$Freque\^ncia\ (Hz)$')
        pl.ylabel(r'$Direc\c{}a\~o\ $'+u'(\u00b0)')
        pl.grid()

        # pl.plot(t1,eta)
        # pl.plot([t1[0],t1[-1]],[5*np.std(eta),5*np.std(eta)],'r-.',linewidth=3)
        # pl.plot([t1[0],t1[-1]],[4*np.std(eta),4*np.std(eta)],'r-.',linewidth=3)
        # pl.plot([t1[0],t1[-1]],[-5*np.std(eta),-5*np.std(eta)],'r-.',linewidth=3)
        # pl.plot([t1[0],t1[-1]],[-4*np.std(eta),-4*np.std(eta)],'r-.',linewidth=3)
        # pl.ylim(-7.5,7.5)
        # pl.xlabel(r'$Tempo\ (s)$')
        # pl.ylabel(r'$Elevac\c{}a\~o\ (m)$')
        # pl.grid()

        pl.subplot(2,2,4)
        pl.plot(sn[:,0],sn[:,1])
        pl.axis('tight')
        pl.xlabel(r'$Freque\^ncia\ (Hz)$')
        pl.ylabel(r'$m^{2}/Hz$')
        pl.grid()



        #serie com espectros de fase e coerencia
        pl.figure()
        pl.subplot(211)
        pl.plot(datatcb[0:-1:3],fase_nnx[0:-1:3],'b',label='nnx')
        pl.plot(datatcb[0:-1:3],fase_nny[0:-1:3],'r-',label='nny')
        pl.plot(datatcb[0:-1:3],fase_nxny[0:-1:3],'g-',label='nxny')
        pl.ylim(-180,180)
        pl.ylabel(r'$Fase\ $'u'(\u00b0)')
        pl.grid()
        pl.legend(loc=0,fontsize=15,ncol=3)
        pl.xticks([])
        pl.subplot(212)
        pl.plot(datatcb[0:-1:3],coer_nnx[0:-1:3],'b-',label='nnx')
        pl.plot(datatcb[0:-1:3],coer_nny[0:-1:3],'r-',label='nny')
        pl.plot(datatcb[0:-1:3],coer_nxny[0:-1:3],'g-',label='nxny')
        pl.plot([datatcb[0],datatcb[-1]],[0.393,0.393],'k--',linewidth=4,label='nxny')
        # pl.ylim(-180,180)
        pl.ylabel(r'$Coere\^encia$')
        pl.grid()

        pl.figure()
        pl.subplot(311)
        pl.plot(datat,matondap[:,6],'b')
        pl.ylabel(r'$Hs\ (m)$')
        pl.xticks(visible=False)
        pl.grid()
        pl.subplot(312)
        pl.plot(datat,matondap[:,7],'bo')
        pl.ylabel(r'$Tp\ (s)$')
        pl.xticks(visible=False)
        pl.grid()
        pl.subplot(313)
        pl.plot(datat,matondap[:,8],'bo')
        pl.ylabel(r'$Dp\ $'+u'(\u00b0)')
        pl.grid()


    ######################################################################
        #check ratio


        f = sn[:,0] #vetor de frequencia
        c11 = sn[:,1] #auto-espec de heave
        c22 = snnx[:,1] #auto-espec de dspx
        c33 = snny[:,1] #auto-espec de dspy

        #numero de onda do instrumento (medido)
        kf = np.sqrt( c11 / (c22+c33) )

        #check-ratio
        rf = (1 / (np.tanh(k) * h) ) * kf

        #valor medio de check-ratio na frequencia de energia
        rf_med = np.mean([rf[1:12]])


        pl.figure()
        pl.subplot(2,1,1)
        pl.title(datat.astype(str)[0]+'\n Hs=%.1f' %matondap[0,1]+' m, Hmax=%.1f' %matondap[0,3]+' m, Hmax/Hs=%.1f' %(matondap[0,3]/matondap[0,1])+' m, Tp=%.1f' %matondap[0,7]+' s, Dp=%i' %(matondap[0,8]-17)+u' \u00b0')
        pl.plot(t1[120:220],eta[120:220],'b',label=r'$heave$')
        pl.plot(t1[120:220],etax[120:220],'r',label=r'$dsp.x$')
        pl.plot(t1[120:220],etay[120:220],'g',label=r'$dsp.y$')
        pl.axis('tight')
        pl.xlabel(r'$Tempo\ (s)$')
        pl.ylabel(r'$Deslocamentos\ (m)$')
        pl.grid()
        pl.subplot(2,2,3)
        pl.plot(sn[:,0],sn[:,1])
        pl.axis('tight')
        pl.xlabel(r'$Freque\^ncia\ (Hz)$')
        pl.ylabel(r'$m^{2}/Hz$')
        pl.grid()
        pl.subplot(2,2,4)
        pl.plot(f,k,label=r'$k-teor.$')
        pl.plot(f,kf,label=r'$k-inst.$')
        pl.xlabel(r'$Freque\^ncia\ (Hz)$')
        pl.ylabel(r'$Nu\'mero\ de\ Onda\ (k)$')
        pl.grid(), pl.axis('tight')
        pl.legend(loc=2,fontsize=10)


        #serie e espectro - ww3es
        pl.figure(figsize=(12,6))
        pl.subplot(121)
        pl.plot(t[:500]-t[0],eta[:500])
        pl.grid()
        pl.axis('tight')
        pl.xlabel(r'$Tempo\ (s)$',fontsize=17)
        pl.ylabel(r'$Elevac\c{}a\~o\ (m)$',fontsize=17)
        pl.subplot(122)
        pl.plot(sn[:,0],sn[:,1])
        pl.grid()
        pl.xlabel(r'$Freque\^ncia\ (Hz)$',fontsize=17)
        pl.ylabel(r'$m^{2}/Hz$',fontsize=17)

        # pl.savefig('fig/serieespec.png', dpi=1200, facecolor='w', edgecolor='w',
        # orientation='portrait',format='png') 

        # pl.savefig('fig/serieespec.eps', dpi=1200, facecolor='w', edgecolor='w',
        # orientation='portrait',format='eps') 


# ================================================================================== #  
# Salva saida da daat (espe e dire)

# np.savetxt('saida/'+'espe1.out',espe1,delimiter=',',fmt='%.1f')
# np.savetxt('saida/'+'dire1.out',dire1,delimiter=',',fmt='%.1f')
# np.savetxt('saida/'+'energ.out',energ,delimiter=',',fmt='%.1f')

# ================================================================================== #  
# Tempo de execucao da rotina

#contador inicial de tempo de execucao
toc = time.clock()

#tempo de execucao
texec = toc - tic

print 'Tempo de execucao pp_proc + daat_oc (s): ',texec

# ================================================================================== #  
# Graficos

# graficos_axys.graf(mat_onda,eta_mat_cons,dspx_mat_cons,dspy_mat_cons,reg_fw,Hmax_fw,Hs_fw,THmax_fw,rel_fw,ind_fw)


# ================================================================================== #  
# Fim

# [freqs,dires] = np.meshgrid(np.linspace(0,max(freq),100),np.linspace(0,360,100),sparse=False,copy=False)
# sn[:,1] = ( sn[:,1] * np.real(sigma1) ) / sigma1
# #interpola a energia
# sp2 = mpl.mlab.griddata(freq,dire1,sn[:,1],freqs,dires,interp='nn') #a interp linear e a nn ficaram praticamente iguais
# fig, ax = plt.subplots()
# cs = plt.pcolormesh(freqs,dires,sp2,shading='flat',cmap=plt.cm.jet,vmin=np.nanmin(sp2),vmax=np.nanmax(sp2))
# cs = plt.contourf(freqs,dires,sp2,shading='flat',cmap=plt.cm.jet,vmin=np.nanmin(sp2),vmax=np.nanmax(sp2))
# plt.colorbar()
# plt.savetxt('sp2d_' + str(int(listac[i])))

# mostra figuras


#salva matriz com espectro e direcao
# a=np.concatenate((sn[:,[0,1]],np.array([dire1]).T,np.array([real(sigma1)]).T),axis=1)


pl.show()
