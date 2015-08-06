'''
PLEDS (Parente's Diagram)

- Desenvolido por Parente (1999)
- Adaptado para Python por Henrique Pereira

Programa para plotagem da evolucao do espectro direcional
Plotting the Evolution of Directional Spectrum

Carlos Eduardo Parente
Henrique P P Pereira
Izabel C M Nogueira
Ricardo M Campos

Funcoes:
- pledstriaxys - plota os dados mensais das boias triaxys
- pledsSWAN - plota a previsao de 1 semana da saida espectral
do SWAN


Ultima modificacao: 28/07/2015
'''

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle

plt.close('all')

def pleds(espe1,dire1,ws1,wd1):


	ad = np.array(['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])


	fig = plt.figure(figsize=(8,8))
	ax = fig.add_subplot(111)


	a = 0
	plt.plot(a,'w')
	plt.axis([-0.1,20.2,0,300])

	v6 = np.hanning(15)
	v61 = np.hanning(11)

	ad1 = np.array([31,29,31,30,31,30,31,31,30,31,30,31]) #???

	plt.axis('off')

	# arq2 = np.array(([ [1,0.00,0],
	# 				   [1,0.00,0],
	# 				   [1,0.55,0],
	# 				   [1,0.55,0],
	# 				   [1,1.00,0],
	# 				   [1,1.00,0],
	# 				   [0,1.00,0],
	# 				   [0,1.00,0] ]))

	col = np.array([0.7,0.7,0.7])

	ax.set_position([0,0,1,1]) # set a new position

	# #codigo de cores para faixas de periodos
	# x = np.array([0.5,3,3,0.5]) + 0.5
	# y = np.array([1,1,12,12]) - 3.5


	ax.add_patch(Rectangle((0,3), 3.3, 8,alpha=0.8,facecolor='r'))
	ax.text(0.5,4.5, "21.3-16.0 s")

	ax.add_patch(Rectangle((3.3, 3), 3.3, 8,alpha=0.8,facecolor='y'))
	ax.text(3.8,4.5, "12.8-8.0 s")

	ax.add_patch(Rectangle((6.6, 3), 3.3, 8,alpha=0.8,facecolor='g'))
	ax.text(7.1,4.5, "7.1-4.0 s")

	ax.add_patch(Rectangle((9.9, 3), 3.3, 8,alpha=0.8,facecolor='b'))
	ax.text(10.4,4.5, "3.7-1.5 s")

	ax.add_patch(Rectangle((13.2, 3), 3.3, 8,alpha=0.8,facecolor='w'))
	ax.text(13.5,4.5, "5 div=10 m/s")

	ax.add_patch(Rectangle((16.5, 3), 3.3, 8,alpha=0.8,facecolor='w'))
	ax.text(16.8,4.5, "5 div=0.1 m2")

	plt.draw()

	#linhas verticais
	y = np.array([20,283])
	for i in range(1,20):
		x = [i,i]
		pl.plot(x,y,'k',alpha=0.2)

	#linhas horizontais (dias)
	x = np.array([0.9,19.1])
	dia = 0
	for i in range(20,260+8,8):
		dia += 1
		y = [i,i]
		pl.plot(x,y,'k',alpha=0.3)
		pl.text(0.3,y[0],str(dia))
		pl.text(19.3,y[0],str(dia))

	#linhas horizontais (3 horas)
	x = np.array([1,19])
	for i in range(20,284,2):
		y = [i,i]
		pl.plot(x,y,'k',alpha=0.2)

	pl.text(1.13,286,'DIRECTIONAL WAVE SPECTRUM - Rio Grande/RS 2009/05 - PNBOIA (AXYS)')


	#plotagem do espectro direcional a cada dia por faixa de periodos
	#plota de cima para baixo (de 31 para 1)

	#eixo horizontal de direcao
	a = np.arange(310,720,20)
	a[pl.find(a>360)] = a[pl.find(a>360)] - 360

	for i in range(1,19):
		pl.text(i+0.15,15,str(a[i-1]),color='red',fontsize=11)


	ld = np.array(['NW','N ','NE','E ','SE','S ','SW','W ','SW','W '])

	k = 1.55;
	d = np.arange(1.75,13,2.25)

	for i in range(8):
		pl.text(k,20.8,ld[i],weight='bold')
		k=k+2.25;
	 
	pl.text(1.15,80,'days in a month',rotation=90)

	#w=[[1;6] [2;7] [3;8] [4;9]];
	#bb = np.array([0.3]*10) #utilizado para montar o triangulo??

	for t in range(dire1.shape[1]-1,-1,-1):

		#define os vetores de direcao e espectro (energia)
		s1 = dire1[:,t]
		s2 = espe1[:,t]

		#varia as 4 faixas
		cor = -1
		for i in [0,2,4,6]:

			# arq5 = arq2[i,:] #cor - fazer com 'r', 'b', ... ??

			cor += 1
			arq5 = ['r','y','g','b']

			s11 = s1[i] #valor da direcao no tempo i
			s12 = s2[i] #valor do espectro no tempo i

			b1 = s11 / 20 #direcao (correcao para o eixo??)
			b2 = s12 / 2  #espectro

			if b1 > 0:
				b1 = b1 + 3 #ajuste da direcao

				if b1 > 18:
					b1 = b1 - 18

				b1 = b1 + 1 #o zero comecaem 111 (ou 11??)
				n1 = t + 9 + 10 #shift na escala vertical

				#monta um triangulo (x)
				v7 = np.linspace(b1-0.3,b1+0.3,len(v61))
				x = np.array(list(v7) + list(np.flipud(v7)))

				#cria un hanning
				y = np.array( list(n1+v61*b2) + list(n1*np.ones(len(v61))))

				# ??
				z1 = 1
				z2 = 1

				if b2 * b1 > 0:

					pl.fill(x,y,arq5[cor])



	#####################################################
	#vento (u e v)

	for t in np.arange(dire1.shape[1]-1,-1,-1):

		s1 = ws1[t]
		s2 = wd1[t]

		if s1 > 0:

			s2 = s2/20
			st = t+9+10
			s2 = s2 + 3

			if s2 > 18:

				s2 = s2 - 18

			s2 = s2 + 1

        	#s1 eh a velocidade do vento, colocada na escala certa
        	#1 divisao=2m/s
        	#s2 eha direcao em caixas de 18 graus
        	#st eh a posicao de plotagem ao logo da vertical

        	x = [s2-0.05,s2+0.05,s2+0.05,s2-0.05]
        	y = [st,st,st+s1,st+s1]

        	if s2 < 2:

        		x = np.nan
        		y = np.nan

        	if s2 > 18:

        		x = np.nan
        		y = np.nan

        	if s1 > 0:

        		pl.fill(x,y,'w')

        	if s1 > 10:

        		pl.fill(x,y,'y')

        	if s1 >20:

        		pl.fill(x,y,'g')




	pl.savefig('pledspy.png')

	plt.show()

	return


def pledsSWAN(espe1,dire1,tit,dia):


	ad = np.array(['Jan','Fev','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])


	fig = plt.figure(figsize=(8,8))
	ax = fig.add_subplot(111)


	a = 0
	plt.plot(a,'w')
	plt.axis([-0.1,20.2,0,300])

	v6 = np.hanning(15)
	v61 = np.hanning(11)

	ad1 = np.array([31,29,31,30,31,30,31,31,30,31,30,31]) #???

	plt.axis('off')

	# arq2 = np.array(([ [1,0.00,0],
	# 				   [1,0.00,0],
	# 				   [1,0.55,0],
	# 				   [1,0.55,0],
	# 				   [1,1.00,0],
	# 				   [1,1.00,0],
	# 				   [0,1.00,0],
	# 				   [0,1.00,0] ]))

	col = np.array([0.7,0.7,0.7])

	ax.set_position([0,0,1,1]) # set a new position

	# #codigo de cores para faixas de periodos
	# x = np.array([0.5,3,3,0.5]) + 0.5
	# y = np.array([1,1,12,12]) - 3.5


	ax.add_patch(Rectangle((0,3), 3.3, 8,alpha=0.8,facecolor='r'))
	ax.text(0.5,4.5, "25.0-13.1 s")

	ax.add_patch(Rectangle((3.3, 3), 3.3, 8,alpha=0.8,facecolor='y'))
	ax.text(3.8,4.5, "11.8-08.5 s")

	ax.add_patch(Rectangle((6.6, 3), 3.3, 8,alpha=0.8,facecolor='g'))
	ax.text(7.1,4.5, "07.7-05.0 s")

	ax.add_patch(Rectangle((9.9, 3), 3.3, 8,alpha=0.8,facecolor='b'))
	ax.text(10.4,4.5, "04.5-01.0 s")

	ax.add_patch(Rectangle((13.2, 3), 3.3, 8,alpha=0.8,facecolor='w'))
	ax.text(13.5,4.5, "5 div=10 m/s")

	ax.add_patch(Rectangle((16.5, 3), 3.3, 8,alpha=0.8,facecolor='w'))
	ax.text(16.8,4.5, "5 div=0.1 m2")

	plt.draw()

	#linhas verticais
	y = np.array([20,284])
	for i in np.arange(1,20):
		x = [i,i]
		pl.plot(x,y,'k',alpha=0.2)

	#linhas horizontais (dias)
	x = np.array([0.9,19.1])
	#dia = 0
	for i in np.arange(20,284,37):
		dia += 1
		y = [i,i]
		pl.plot(x,y,'k',alpha=0.3)
		pl.text(0.3,y[0],str(dia))
		pl.text(19.3,y[0],str(dia))


	#linhas horizontais (1 hora)
	x = np.array([1,19])
	for i in np.arange(20,284,1.5416):
		y = [i,i]
		pl.plot(x,y,'k',alpha=0.2)


	#pl.text(1.13,286,'DIRECTIONAL WAVE SPECTRUM - Previsao - ADCP Vale')
	pl.text(1.13,286,tit)


	#plotagem do espectro direcional a cada dia por faixa de periodos
	#plota de cima para baixo (de 31 para 1)

	#eixo horizontal de direcao
	a = np.arange(310,720,20)
	a[pl.find(a>360)] = a[pl.find(a>360)] - 360

	for i in range(1,19):
		pl.text(i+0.15,15,str(a[i-1]),color='red',fontsize=11)


	ld = np.array(['NW','N ','NE','E ','SE','S ','SW','W ','SW','W '])

	k = 1.55;
	d = np.arange(1.75,13,2.25)

	for i in range(8):
		pl.text(k,20.8,ld[i],weight='bold')
		k=k+2.25;
	 
	pl.text(1.15,80,'days in a month',rotation=90)

	#w=[[1;6] [2;7] [3;8] [4;9]];
	#bb = np.array([0.3]*10) #utilizado para montar o triangulo??

	#for t in range(dire1.shape[1]-1,-1,-1):
	t = dire1.shape[1]
	for tt in np.arange(278,20-1.542/2,-1.542):
		t -= 1
		print t
		print tt

		#define os vetores de direcao e espectro (energia)
		s1 = dire1[:,t]
		s2 = espe1[:,t]

		#varia as 4 faixas
		cor = -1
		for i in [0,2,4,6]:

			# arq5 = arq2[i,:] #cor - fazer com 'r', 'b', ... ??

			cor += 1
			arq5 = ['r','y','g','b']

			s11 = s1[i] #valor da direcao no tempo i
			s12 = s2[i] #valor do espectro no tempo i

			b1 = s11 / 20 #direcao (correcao para o eixo??)
			b2 = s12 / 2  #espectro

			if b1 > 0:
				b1 = b1 + 3 #ajuste da direcao

				if b1 > 18:
					b1 = b1 - 18

				b1 = b1 + 1 #o zero comecaem 111 (ou 11??)
				n1 = tt #shift na escala vertical

				#monta um triangulo (x)
				v7 = np.linspace(b1-0.3,b1+0.3,len(v61))
				x = np.array(list(v7) + list(np.flipud(v7)))

				#cria un hanning
				y = np.array( list(n1+v61*b2) + list(n1*np.ones(len(v61))))
				

				# ??
				z1 = 1
				z2 = 1

				if b2 * b1 > 0:

					pl.fill(x,y,arq5[cor],alpha=.9)



	pl.savefig('pledspy_SWAN.png')

	plt.show()

	return

