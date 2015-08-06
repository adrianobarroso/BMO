### CARREGA DADOS DE ONDAS DA BOIA AXYS ###
# Desenvolvido por: Henrique P. P. Pereira e Carlos E. Parente
# pereira.henriquep@gmail.com
# Data da ultima modificacao: 09/04/13
# ================================================================================== #
# Funcao 'lista_hne': Cria uma lista com o nome dos arquivos com extensao HNE que estao
# dentro do diretorio 'pathname' indicado.
# Funcao 'dados_hne': Atribui os dados dos arquivos a variavel 'data' com o tempo, e 
# 'dados' com elevacao e deslocamentos norte e leste 
# ================================================================================== #

import numpy as np
import os

#======================================================================#

#Entrada: pathname - diretorio que estao os arquivos
#
#Saida: arq - variavel com o nome dos arquivos

def lista_hne(pathname):

	''' Lista arquivos com extensao .HNE 
	que estao dentro do diretorio 'pathname' '''

	lista = []
	# Lista arquivos do diretorio atual
	for f in os.listdir(pathname):
		if f.endswith('.HNE'):
			lista.append(f)
	lista=np.sort(lista)

	return lista


#======================================================================#

#Entrada: nome do arquivo com extensao -exemplo: 200907060200.HNE
#
#Saida: t - tempo
#		eta - elevacao
#		dspy - deslocamento norte
#		dspx - deslocamento leste
#		data - ano, mes, dia, hora, minuto

def dados_hne(pathname,arq):

	''' Retorna os dados de tempo, elevacao e
	deslocamentos norte e leste '''

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
