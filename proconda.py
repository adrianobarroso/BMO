### CALCULA PARAMETROS DE ONDA NO DOMINIO DO TEMPO E FREQUENCIA ###
# Desenvolvido por: Henrique P. P. Pereira - pereira.henriquep@gmail.com
# Data da ultima modificacao: 20/05/2014
# ================================================================================== #
# Funcao 'ondat': Processamento de dados de onda no dominio do tempo
# Funcao 'ondaf': Processamento de dados de onda no dominio da frequencia
# ================================================================================== #

import numpy as np
import espec
import numeronda

reload(espec)
# reload(numeronda)

def numeronda(h,deltaf,reg):

	'''
	# ================================================================================== #
	
	Calcula o numero de onda (k)
	
	Dados de entrada: h - profundidade
		  			    deltaf - vetor de frequencia
					    reg - comprimento do vetor de frequencia
	
	Dados de saida: k - vetor numero de onda
	
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
		sigma = (2*np.pi*deltaf[j])**2
		while abs(kpos - kant) > 0.001:
			kant = kpos
			dfk = g*kant*h*(1/np.cosh(kant*h))**2+g+np.tanh(kant*h)
			fk = g*kant*np.tanh(kant*h) - sigma
			kpos = kant - fk/dfk
		kant = kpos - 0.002
		k.append(kpos)
	return k


#Processamento no dominio do tempo
def ondat(t,eta,h):

	'''
	#======================================================================#
	
	Calcula parametros de onda no dominio do tempo
	
	Dados de entrada: t - vetor de tempo  
	                  eta - vetor de elevacao
	                  h - profundidade
	
	Dados de saida: pondat = [Hs,H10,Hmax,THmax,Tmed,]
					  Hs - altura significativa
	                H10 - altura de 1/10 das maiores
	                Hmax - altura maxima
	                THmax - periodo associado a altura maxima
	                Tmed - periodo medio
	
	#======================================================================#
	'''

	#retira a media
	eta = eta - np.mean(eta)

	#criando os vetores H(altura),Cr(crista),Ca(cavado),T (periodo)
	Cr = []
	Ca = []
	H = []
	T = []

	#acha os indices que cruzam o zero
	z = np.where(np.diff(np.sign(eta)))[0]

	#zeros ascendentes e descendentes
	zas=z[0::2]
	zde=z[1::2]

	#calcula ondas individuas
	for i in range(0,len(zas)-1):
	    onda = eta[zas[i]:(zas[i+1])+1]
	    cr = np.max(onda)
	    Cr.append(cr)
	    ca = np.min(onda)
	    Ca.append(ca)
	    H.append(cr + np.abs(ca))
	    T.append(((zas[i+1])+1) - zas[i])

	#coloca as alturas em ordem crescente
	Hss = np.sort(H)
	Hss = np.flipud(Hss)

	#calcula a altura significativa (H 1/3)
	div = len(Hss) / 3
	Hs = np.mean(Hss[0:div+1])
	
	#calcula a altura das 1/10 maiores (H 1/10)
	div1 = len(Hss) / 10
	H10 = np.mean(Hss[0:div1+1]) #altura da media das um decimo maiores
	
	#altura maxima
	Hmax = np.max(H)
	
	#periodo medio
	Tmed = np.mean(T)
	
	#calcula periodo associado a altura maxima
	ind = np.where(H == Hmax)[0][0]
	THmax = T[ind]

	#parametros de onda no tempo
	pondat = np.array([Hs,H10,Hmax,Tmed,THmax])

	return Hs,H10,Hmax,Tmed,THmax

#Processamento no dominio da frequencia
def ondaf(eta,etax,etay,h,nfft,fs):

	"""
	#======================================================================#
	
	Calcula parametros de onda no dominio da frequencia
	
	Dados de entrada: eta - vetor de elevacao
	                  etax - vetor de deslocamento em x
	                  etay - vetor de deslocamento em y
						h - profundidade
						nfft - Numero de pontos utilizado para o calculo da FFT
	                  fs - frequencia de amostragem
	
	Dados de saida: pondaf = [hm0 tp dp]	
	
	#======================================================================#
	"""

	#espectro simples
	sn = espec.espec1(eta,nfft,fs)
	snx = espec.espec1(etax,nfft,fs)
	sny = espec.espec1(etay,nfft,fs)

	#espectros cruzados
	snn = espec.espec2(eta,eta,nfft,fs)
	snnx = espec.espec2(eta,etax,nfft,fs)
	snny = espec.espec2(eta,etay,nfft,fs)
	snxny = espec.espec2(etax,etay,nfft,fs)
	snxnx = espec.espec2(etax,etax,nfft,fs)
	snyny = espec.espec2(etay,etay,nfft,fs)

	#vetor de frequencia
	f = sn[:,0]

	#deltaf
	df = f[1] - f[0]

	#calculo do numero de onda
	k = numeronda(h,f,len(f))
	k = np.array(k)

	#calculo dos coeficientes de fourier - NDBC 96_01 e Steele (1992)
	c = snx[:,1] + sny[:,1]
	cc = np.sqrt(sn[:,1] * (c))

	a1 = snnx[:,3] / cc
	b1 = snny[:,3] / cc

	a2 = (snx[:,1] - sny[:,1]) / c
	b2 = 2 * snxny[:,2] / c

	#calcula direcao de onda
	#mean direction
	dire1 = np.array([np.angle(np.complex(b1[i],a1[i]),deg=True) for i in range(len(a1))])

	#principal direction
	dire2 = 0.5 * np.array([np.angle(np.complex(b2[i],a2[i]),deg=True) for i in range(len(a2))])

	#condicao para valores maiores que 360 e menores que 0
	dire1[np.where(dire1 < 0)] = dire1[np.where(dire1 < 0)] + 360
	dire1[np.where(dire1 > 360)] = dire1[np.where(dire1 > 360)] - 360

	dire2[np.where(dire2 < 0)] = dire2[np.where(dire2 < 0)] + 360
	dire2[np.where(dire2 > 360)] = dire2[np.where(dire2 > 360)] - 360

	#acha o indice da frequencia de pico
	ind = np.where(sn[:,1] == np.max(sn[:,1]))[0]

	#periodo de pico
	tp = (1. / f[ind])[0]

	#momento espectral de ordem zero total - m0
	m0 = np.sum(sn[:,1]) * df

	#calculo da altura significativa
	hm0 = 4.01 * np.sqrt(m0)

	#direcao do periodo de pico
	dp = dire1[ind][0]

	#Espalhamento direcional
	#Formula do sigma1 do livro Tucker&Pitt(2001) "Waves in Ocean Engineering" pags 196-198
	c1 = np.sqrt(a1 ** 2 + b1 **2)
	c2 = np.sqrt(a2 ** 2 + b2 ** 2)
	
	s1 = c1 / (1-c1)
	s2 = (1 + 3 * c2 + np.sqrt(1 + 14 * c2 + c2 ** 2)) / (2 * (1 - c2))
	
	sigma1 = np.sqrt(2 - 2 * c1) * 180 / np.pi
	sigma2 = np.sqrt((1 - c2) / 2) * 180 / np.pi

	sigma1p = np.real(sigma1[ind])[0]
	sigma2p = np.real(sigma2[ind])[0]

	# pondaf = np.array([hm0, tp, dp, sigma1p, sigma2p])

	return hm0, tp, dp, sigma1, sigma2, sigma1p, sigma2p, f, df, k, sn, snx, sny, snn, snnx, snny, snxny, snxnx, snyny, a1, b1, a2, b2, dire1, dire2

def ondap(hm0,tp,dp,sn,dire1,df):

	'''

	#======================================================================#
	Programa para calcular parametros
	de onda nas particoes de sea e swell
	
	desenvolvido para 32 gl
	
	divide o espectro em 2 partes: 
	parte 1 - 8.33 a 50 seg
	parte 2 - 1.56 a 7.14 seg
	
	calcula o periodo de pico de cada particao, e despreza o
	pico 2 (menos energetico) se a energia for inferior a 15% da
	energia do pico 1 (mais energetico)
	#======================================================================#

	'''

	#vetor de frequencia e energia
	f,s = sn[:,[0,1]].T

	# seleciona os picos espectrais - considera somente 2 picos
	g1=np.diff(s)
	g1=np.sign(g1)
	g1=np.diff(g1)
	g1=np.concatenate(([0],g1))
	g2=np.where(g1==-2)[0]
	picos=1 # a principio e unimodal
	l=np.size(g2)

	# inicializar considerando ser unimodal
	hm02 = np.nan #9999
	tp2 = np.nan #9999
	dp2 = np.nan #9999
	hm01 = hm0
	tp1 = tp 
	dp1 = dp 

	if l > 1: #verificando espacamento entre picos (espacamento maior que 4 df)
		fr=np.argsort(s[g2])[::-1] #frequencia decrescente
		er=np.sort(s[g2])[::-1] # energia decrescente

		if (f[g2[fr[1]]]-f[g2[fr[0]]]) > 4*(f[1]-f[0]) and (er[1]/er[0] >= 0.15): #adota criterio de 4*deltaf
			picos=2
	    
	    # calcular o Hs dos picos pegando a cava e dividindo em pico 1 e pico 2
		if picos == 2:
			n1=g2[0] #pico mais energetico
			n2=g2[1] #pico menos energetico
			nc=np.where(g1[n1:n2]==2) #indice da cava

			#particao do swell e sea
			swell = range(n1+nc+1)
			sea = range(n1+nc+1,len(s))

			#maxima energia do swell
			esw = max(s[swell])

			#maxima energia do sea
			ese = max(s[sea])

			#indice do pico do swell
			isw = np.where(s==esw)[0][0]

			#indice do pico do sea
			ise = np.where(s==ese)[0][0]

			#altura sig. do swell
			hm0sw = 4.01 * np.sqrt(sum(s[swell]) * df)

			#altura sig. do sea
			hm0se = 4.01 * np.sqrt(sum(s[sea]) * df)

			#periodo de pico do swell
			tpsw = 1./f[isw]

			#periodo de pico do sea
			tpse = 1./f[ise]

			#direcao do swell
			dpsw = dire1[isw]

			#direcao do sea
			dpse = dire1[ise]

			
			#deixa o pico 1 como swell e pico 2 como sea
			en1 = esw ; en2 = ese
			hm01 = hm0sw ; hm02 = hm0se
			tp1 = tpsw ; tp2 = tpse
			dp1 = dpsw ; dp2 = dpse
		
			#seleciona pico 1 como mais energetico
			# e pico 2 com o menos energetico
			# if esw > ese:
			# 	en1 = esw ; en2 = ese
			# 	hm01 = hm0sw ; hm02 = hm0se
			# 	tp1 = tpsw ; tp2 = tpse
			# 	dp1 = dpsw ; dp2 = dpse
			# else:
			# 	en1 = ese ; en2 = esw
			# 	hm01 = hm0se ; hm02 = hm0sw
			# 	tp1 = tpse ; tp2 = tpsw
			# 	dp1 = dpse ; dp2 = dpsw

	# pondaf1 = np.array([hm01, tp1, dp1, hm02, tp2, dp2])

	return hm01, tp1, dp1, hm02, tp2, dp2 #pondaf1


# def spread(en,a1,b1):

# 	'''
# 	#======================================================================#
# 	Programa para calcular o espelhamento
# 	angular
# 	Kuik et al 1988
	
# 	Entrada:
# 	en - espectro 1D
# 	a1 - coef de fourier de 1 ordem
# 	b1 - conef de fourir de 1 ordem 

# 	Saida:
# 	spr - valor do espalhamento angular para cada
# 	frequencia
# 	#======================================================================#
# 	'''

# 	#esplhamento com vetor complexo - radianos?
# 	sprc = (2 * (1 - ( (a1**2 + b1**2) / (en**2) ) **0.5) **0.5)

# 	#soma a parte real e imag e coloca em graus
# 	spr = (np.real(sprc) + np.imag(sprc)) * 180 / np.pi

# 	#parece que aparece na parte real onde tem energia no espectro
# 	sprr = np.real(sprc)

# 	#diminui 360 nos maiores que 360
# 	# spr[np.where(spr>360)[0]] = spr[np.where(spr>360)[0]] - 360

# 	#coloca zeros nos valores muito altos
# 	# spr[np.where(spr>360)[0]] = 0

# 	return sprc, spr, sprr