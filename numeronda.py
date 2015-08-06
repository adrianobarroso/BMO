### CALCULA O NUMERO DE ONDA (K)
# ================================================================================== #
# Dados de entrada: h - profundidade
#	  			    deltaf - vetor de frequencia
#				    reg - comprimento do vetor de frequencia
#
# Dados de saida: k - vetor numero de onda
# ================================================================================== #

from numpy import arange, cosh,tanh, pi

def numeronda(h,deltaf,reg):

	'''
	# ================================================================================== #
	#
	# Calcula o numero de onda (k)
	#
	# Dados de entrada: h - profundidade
	#	  			    deltaf - vetor de frequencia
	#				    reg - comprimento do vetor de frequencia
	#
	# Dados de saida: k - vetor numero de onda
	#
	# ================================================================================== #
	'''

	#gravidade
	g = 9.8

	#vetor numero de onda a ser criado
	k = []

	#k anterior
	kant = 0.001

	#k posterior
	kpos = 0.0011

	for j in range(reg):
		sigma = (2*pi*deltaf[j])**2
		while abs(kpos - kant) > 0.001:
			kant = kpos
			dfk = g*kant*h*(1/cosh(kant*h))**2+g+tanh(kant*h)
			fk = g*kant*tanh(kant*h) - sigma
			kpos = kant - fk/dfk
		kant = kpos - 0.002
		k.append(kpos)
	return k