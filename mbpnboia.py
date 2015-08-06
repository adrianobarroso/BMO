'''
PNBOIA MB
Programa principal para baixar e processsar
os dados do PNBOIA enviado via sistema argos
e disponibilizado no site da marinha
mar.mil/dados/pnboia

Os dados estao em .xls

corrige a declinacao magnetica

'''

import numpy as np
import matplotlib
matplotlib.use('Agg') #necessario para salvar figura no crontab
import matplotlib.pylab as pl
import os
import xlrd
from datetime import datetime
import datetime as dt
import consisteproc
import getpnboia #baixa dados
reload(consisteproc)
reload(getpnboia)

pl.close('all')

data = dt.datetime.strftime(dt.datetime.now(),'%Y%m%d%H')

#declinacao magnetica para as boias
#rio grande, florian, santos
dmag = [-16.8,-19.3,-21.5]

#escolhe se baixa o dado
baixadados = 1

#local de onde estao os dados em xls baixados do site da marinha
pathname = os.environ['HOME'] + '/Dropbox/pnboia/dados/'
pathnameout = os.environ['HOME'] + '/Dropbox/pnboia/reports/'


boias = ["B69153",
         "B69152",
         "B69150"]

local = ["Rio Grande/RS",
         "Florianopolis/SC",
         "Santos/SP"]


if baixadados == 1:

	dirout = os.environ['HOME'] + '/Dropbox/pnboia/dados/'

	#BMOs
	boiasmb = ['69007_PortoSeguro'  ,
			   '69008_Recife'       ,
			   '69009_Guanabara'    ,
			   '69150_Santos'       ,
			   '69152_SantaCatarina',
			   '69153_RioGrande'    ,]
			   

	boiasgoosbrasil = ['B69007',  #porto seguro
				 	   'B69008',  #recife
				       'B69009',  #baia guanabara
				       'B69150',  #santos
				       'B69152',  #florianopolis
				       'B69153'] #rio grande

	boiassiodoc = 'Monthly_Data.csv'

	getpnboia.mb(boiasmb,dirout)
	getpnboia.siodoc(boiassiodoc,dirout)
	getpnboia.goosbrasil(boiasgoosbrasil,dirout)


pl.figure(figsize=(24,12))

ff = 0
for boia in boias:
	ff += 1

	#lista os arquivos
	arqs = np.sort(os.listdir(pathname + boia))

	#lista o ultima arquivo em .xls
	arq = arqs[-1]
	#arq = boia + '_2015073123.xls' #processa dado xls especifico
		
	print 'Processando: ' + arq

	workbook = xlrd.open_workbook(pathname + boia + '/' + arq)

	#seleciona planilha por indice (pode ser por nome tbm)
	sheet_0 = workbook.sheet_by_index(0) #planilha 1 - status + vento
	sheet_1 = workbook.sheet_by_index(1) #planilha 2 - meteo + onda

	#pega os valores das celulas selecionadas

	#legenda
	leg0 = np.array([[sheet_0.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_0.ncols)]).T
	leg1 = np.array([[sheet_1.cell_value(r,c) for r in range(3,4)] for c in range(0,sheet_1.ncols)]).T

	#dados - inverte - flipud
	dd0 = np.flipud(np.array([[sheet_0.cell_value(r,c) for r in range(4,sheet_0.nrows)] for c in range(sheet_0.ncols)]).T)
	dd1 = np.flipud(np.array([[sheet_1.cell_value(r,c) for r in range(4,sheet_1.nrows)] for c in range(sheet_1.ncols)]).T)

	#substitui 'xxxx' por nan
	dd0[np.where(dd0=='xxxx')] = np.nan
	dd1[np.where(dd1=='xxxx')] = np.nan
	dd0[np.where(dd0=='xxx')] = np.nan
	dd1[np.where(dd1=='xxx')] = np.nan
	dd0[np.where(dd0=='')] = np.nan
	dd1[np.where(dd1=='')] = np.nan

	#data com datetime (nao sao iguais as datas das duas planilhas- deveria ser..)
	if boia == "B69153":
		dd1 = dd1[:-8,:]
		
	dt0 = np.array([ datetime.strptime(dd0[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd0)) ])
	dt1 = np.array([ datetime.strptime(dd1[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd1)) ])

	#data em numero inteiro
	dt0i = np.array([datetime.strftime(dt0[i],'%Y%m%d%H%M') for i in range(len(dt0)) ]).astype(int)
	dt1i = np.array([datetime.strftime(dt1[i],'%Y%m%d%H%M') for i in range(len(dt1)) ]).astype(int)

	#dados da planilha 1 - dd1
	# 7     8   9  10
	# hs, hmax, tp dp

	#define parametros
	hs, hmax, tp, dp = np.array(dd1[:,[7,8,9,10]].T).astype(float)
	dp = dp + dmag[ff-1] #corrige a declinacao magnetica para cada boia

	ws1, wd1, ws2, wd2 = np.array(dd0[:,[5,7,8,10]].T).astype(float)
	wd1 = wd1 + dmag[ff-1] #corrige a declinacao magnetica para cada boia
	wd2 = wd2 + dmag[ff-1]

	#corrige valores menores que zero
	dp[pl.find(dp<0)] = dp[pl.find(dp<0)] + 360
	wd1[pl.find(wd1<0)] = wd1[pl.find(wd1<0)] + 360
	wd2[pl.find(wd2<0)] = wd2[pl.find(wd2<0)] + 360
	
	dp[pl.find(dp>360)] = dp[pl.find(dp>360)] - 360
	wd1[pl.find(wd1>360)] = wd1[pl.find(wd1>360)] - 360
	wd2[pl.find(wd2>360)] = wd2[pl.find(wd2>360)] - 360



	#cria vetores de flags das series processadas (depende das qtdade de variaveis a serem consistidas + data) 
	flagp = np.zeros((len(hs),4+1),dtype='|S32')
	flagp[:,0] = [datetime.strftime(dt1[i],'%Y%m%d%H%M') for i in range(len(dt1))]

	# ================================================================================== #  
	# Testes de consistencia dos dados processados

	#Teste 1 - faixa
	flagp[:,1] = consisteproc.faixa(hs,0,10,0.25,8,flagp[:,1])
	flagp[:,2] = consisteproc.faixa(tp,3,30,4,18,flagp[:,2])
	flagp[:,3] = consisteproc.faixa(dp,0,360,0,360,flagp[:,3])
	flagp[:,4] = consisteproc.faixa(hmax,0,10,0.5,20,flagp[:,4])

	#Teste 2 - Variabilidade temporal
	flagp[:,1] = consisteproc.variab(hs,1,2.5,flagp[:,1])
	flagp[:,2] = consisteproc.variab(tp,1,20,flagp[:,2])
	flagp[:,3] = consisteproc.variab(dp,1,360,flagp[:,3])
	flagp[:,4] = consisteproc.variab(hmax,1,5,flagp[:,4])

	#fazer consistencia dos parametros meteorologicos

	# ================================================================================== #  
	# Coloca nan nos dados reprovados

	onda = np.array(zip(hs,tp,dp,hmax))
	for c in range(0,onda.shape[1]):
	    for i in range(onda.shape[0]):
	        if '4' in flagp[i,c+1]:
	            onda[i,c] = np.nan

	#define parametros de onda consistentes
	hs, tp, dp, hmax = onda.T

	# #matriz com dados para ser concatenado a matriz com dados mais antigos
	matvento = zip(dt0i,ws1,wd1,ws2,wd2)
	matonda = zip(dt1i,hs,tp,dp,hmax)

	#abre o arquivo com todos os dados para incluir os arquivos novos
	ddvento = np.loadtxt(pathname + 'LIOc/' + boia + '_vento.out',delimiter=',')
	ddonda = np.loadtxt(pathname + 'LIOc/' + boia + '_onda.out',delimiter=',')
	
	#concatena os dados baixados com os dados anteriores
	concatvento1 = np.concatenate((ddvento,np.array(matvento)),axis=0)
	concatonda1 = np.concatenate((ddonda,np.array(matonda)),axis=0)
	
	#retira os dados repetidos (b sao os indices sem repeticao) - utiliza a data (coluna 0)
	a,b = np.unique(concatonda1[:,0],return_index=True)
	concatonda = concatonda1[b,:]

	a,b = np.unique(concatvento1[:,0],return_index=True)
	concatvento = concatvento1[b,:]

	#salva o arquivo do mes concatenado (mudar para 'concat' para 'mat' quando for para salvar algum arquivo)
	np.savetxt(pathname + 'LIOc/' + boia + '_vento.out',concatvento,fmt=['%i']+4*['%.2f'],delimiter=',',
		header='data,ws1,wd1,ws2,wd2')

	np.savetxt(pathname + 'LIOc/' + boia + '_onda.out',concatonda,fmt=['%i']+4*['%.2f'],delimiter=',',
		header='data,hs,tp,dp,hmax')


	#cria variaveis com os parametros concatenados
	timev, ws1, wd1, ws2, wd2 = concatvento.T #vento
	timeo, hs, tp, dp, hmax = concatonda.T  #onda
	
	dt0 = np.array([datetime.strptime(str(int(timev[i])), '%Y%m%d%H%M') for i in range(len(timev))]) #vento
	dt1 = np.array([datetime.strptime(str(int(timeo[i])), '%Y%m%d%H%M') for i in range(len(timeo))]) #onda

	
	#data onda/vento mensal (comentar para concatenar)
	#dataaux, hs, tp, dp, hmax = np.array(matonda).T
	#dataaux, ws1, wd1, ws2, wd2 = np.array(matvento).T
	#dt0 = np.array([ datetime.strptime(dd0[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd0)) ])
	#dt1 = np.array([ datetime.strptime(dd1[i,1],'%Y/%m/%d %H:%M:%S') for i in range(len(dd1)) ])


	#tamanho da janela em horas para plotagem	
	tj = 7 * 24 #dia x hora
	#tj = len(matonda) #mes
	#tj = len(dt1)

	
	#figuras das boias de rg, fl, st
	pl.subplot(3,3,ff)
	pl.title('PNBOIA - ' + boia + '\n '+ local[ff-1])
	pl.plot(dt1,hs,'b',dt1,hmax,'--r')
	pl.xticks(visible=False), pl.grid()
	pl.xlim(dt1[-tj],dt1[-1]), pl.ylim(0,10)
	if ff == 1:
		pl.ylabel('Hs, Hmax (m)')
	ax = pl.twinx()
	ax.plot(dt0,ws1,'.g',dt0,ws2,'.y',markersize=5,alpha=0.9)
	pl.xlim(dt1[-tj],dt1[-1])
	ax.set_ylim(0,20)
	if ff == 3:
		ax.set_ylabel('WS (m/s)')

	pl.subplot(3,3,ff+3)
	pl.plot(dt1,tp,'ob')
	pl.xticks(visible=False), pl.grid()
	pl.xlim(dt1[-tj],dt1[-1]), pl.ylim(0,20)
	if ff == 1:
		pl.ylabel('Tp (s)')
	
	pl.subplot(3,3,ff+6)
	pl.plot(dt1,dp,'ob')
	pl.plot(dt0,wd1,'.g',dt0,wd2,'.y',markersize=8,alpha=0.9)
	pl.xticks(rotation=30,visible=True), pl.grid()
	pl.xlim(dt1[-tj],dt1[-1])
	pl.yticks(np.arange(0,361,45))
	pl.ylim(0,360)
	if ff == 1:
		pl.ylabel('Dp, WD (deg)')


pl.savefig(pathnameout + 'report_' + data)


pl.show()
