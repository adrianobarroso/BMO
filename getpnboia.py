'''
Programa para baixar os dados
de boias do PNBOIA

funcoes:
getpnboiaxls - site da MB (tabela em excel)
getpnboiaopendap - site do GOOS/BRASIL ()
'''


import numpy as np
import datetime as dt
import urllib
import urllib2	
import csv
import os

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


def mb(boias,dirout):

	data = dt.datetime.strftime(dt.datetime.now(),'%Y%m%d%H')
	meses = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
	mes = meses[int(data[4:6])-1]

	#baixa os dados
	for boia in boias:

		site_adress = "https://www.mar.mil.br/dhn/chm/meteo/prev/dados/pnboia/"+mes+"_ARGOS_"+boia+".xls"
		site = urllib.urlretrieve(site_adress,dirout+"B"+boia[0:5]+"/B"+boia[0:5]+"_"+data+".xls")
		print 'Baixando dado da MB: B'+ boia[0:5]

	return


def goosbrasil(boias,dirout):

	'''
	Baixa dados das boias do pnboia em netCDF
	atraves do openDAP do site do GOOS/BRASIL

	Henrique P P Pereira
	LIOC - COPPE/UFRJ

	Ultima atualizacao 21/07/2015 
	'''

	data = dt.datetime.strftime(dt.datetime.now(),'%Y%m%d%H')

	for boia in boias:

		print 'Baixando dado do GOOS/BRASIL: ' + boia
		urllib.urlretrieve("http://opendap.saltambiental.com.br/pnboia/"+boia+"_argos.nc", \
			dirout+boia+"/"+boia+"_"+data+".nc")

	return


def siodoc(boias,dirout):

	'''
	Entra com o endereco de onde baixa o dado da boia
	'''

	data = dt.datetime.strftime(dt.datetime.now(),'%Y%m%d%H')
	site = urllib2.urlopen("http://metocean.fugrogeos.com/marinha/Member/"+boiassiodoc)
	print 'Baixando dado do SIODOC'

	#datefile = '%02d%02d%02d' %(y,m,d)
	filename = "SIODOC_"+data+".csv"
	
	#create .csv file
	csv = open(dirout+'SIODOC/'+filename,"w")	
	csv.write(site.read())
	csv.close()

	return


#baixa od dados
# mb(boiasmb,dirout)
# siodoc(boiassiodoc,dirout)
# goosbrasil(boiasgoosbrasil,dirout)
