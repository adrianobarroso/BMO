### PROGRAMA QUE CALCULA O ESPECTRO SIMPLES E CRUZADO DE SERIER REAIS ###
# Desenvolvido por: Henrique P. P. Pereira - pereira.henriquep@gmail.com
# Data da ultima modificacao: 20/06/2014
# ================================================================================== #
#Funcao espec1: calcula o espectro simples de uma serie real
#Funcao espec2: calculo o espectro cruzado entre duas series reais
# ================================================================================== #

from matplotlib import mlab
import numpy as np

#Espectro simples
def espec1(x,nfft,fs):

	"""
	#======================================================================#
	#
	# Calcula o espectro simples de uma serie real
	#
	# Dados de entrada: x = serie real
	#                   nfft - Numero de pontos utilizado para o calculo da FFT
	#                   fs - frequencia de amostragem
	#
	# Dados de saida: [aa] - col 0: vetor de frequencia
	#                        col 1: autoespectro
	#                        col 2: intervalo de confianca inferior
	#                        col 3: intervalo de confianca superior
	#
	# Infos:	detrend - mean
	#			window - hanning
	#			noverlap (welch) - 50%
	#
	#======================================================================#
	"""

	#calculo do espectro
	sp = mlab.psd(x,NFFT=nfft,Fs=fs,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=nfft/2)
	f, sp = sp[1][1:],sp[0][1:]

	#graus de liberdade
	gl = len(x) / nfft * 2

	#intervalo de confianca 95%
	ici = sp * gl / 26.12
	ics = sp * gl / 5.63

	aa = np.array([f,sp,ici,ics]).T

	return aa

#Espectro cruzado
def espec2(x,y,nfft,fs):

	"""
	# ================================================================================== #
	#
	# Calcula o espectro cruzado entre duas series reais
	#
	# Dados de entrada: x = serie real 1 (potencia de 2)
	#                   y = serie real 2 (potencia de 2)
	#                   nfft - Numero de pontos utilizado para o calculo da FFT
	#                   fs - frequencia de amostragem
	#
	# Dados de saida: [aa2] - col 0: vetor de frequencia
	#                         col 1: amplitude do espectro cruzado
	#                         col 2: co-espectro
	#                         col 3: quad-espectro
	#                         col 4: espectro de fase
	#                         col 5: espectro de coerencia
	#                         col 6: intervalo de confianca inferior do espectro cruzado
	#                         col 7: intervalo de confianca superior do espectro cruzado
	#                         col 8: intervalo de confianca da coerencia
	#
	# Infos:	detrend - mean
	#			window - hanning
	#			noverlap - 50%
	#
	# ================================================================================== #
	"""

	#cross-spectral density - welch method (complex valued)
	sp = mlab.csd(x,y,NFFT=nfft,Fs=fs,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=nfft/2)
	f = sp[1][1:]
	sp2 = sp[0][1:]

	#co e quad espectro (real e imag) - verificar com parente
	co = np.real(sp2)
	qd = np.imag(sp2)

	#phase (angle function)
	ph = np.angle(sp2,deg=True)

	#ecoherence between x and y (0-1)
	coer = mlab.cohere(x,y,NFFT=nfft,Fs=fs,detrend=mlab.detrend_mean,window=mlab.window_hanning,noverlap=nfft/2)
	coer = coer[0][1:]

	#intervalo de confianca para a amplitude do espectro cruzado - 95%
	ici = sp2 * 14 /26.12
	ics = sp2 * 14 /5.63

	#intervalo de confianca para coerencia
	icc = np.zeros(len(sp2))
	icc[:] = 1 - (0.05 ** (1 / (14 / 2.0 - 1)))

	aa2 = np.array([f,sp2,co,qd,ph,coer,ici,ics,icc]).T

	return aa2