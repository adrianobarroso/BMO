# -*- coding: utf-8 -*-
#
#consistencia dos espectros dos dados brutos de boias meteo-oceanograficas
#
# Autores: 
# Henrique P. P. Pereira
# Izabel C. M. Nogueira
# Ricardo M. Campos
# Carlos E. Parente
# Fabio Nascimento
#
# Data da ultima modificacao: 05/02/2014
#
# Testes:
# 1 - Validade da mensagem recebida (nome do arquivo)
# 2 - Comprimento da serie 
# 3 - Gap
# 4 - Spike
# 5 - Flat
# 6 - Consecutivos nulos
# 7 - Consecutivos iguais
# 8 - Range grosseiro
# 9 - Range regional
#
# ================================================================================== #
#importa bibliotecas

import numpy as np
import pylab as pl
import copy as cp


# ================================================================================== #

def freq_range(fp,iminf,imaxf,lminf,lmaxf,flag):
    
    '''

    FAIXA DE FREQUENCIA OPERACIONAL
    * Verifica se a frequencia de pico esta nos limites aceitaveis
    
    Dados de entrada: fp - frequencia de pico
                      iminf - freq. minima do instrumento
                      imaxf - freq. maxima do instrumento
                      lminf - freq. minima local
                      lmaxf - freq. maxima local
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Suspeito  : flag = '3'
    Reprovado : flag = '4'
    
    '''

    if fp > imaxf or fp < iminf:

        flag = flag + '4'

    elif fp > lmaxf or fp < lminf:

        flag = flag + '3'

    else:

        flag = flag + '1'

    return flag


# ================================================================================== #

def checkratio(h,k,sn,snx,sny,flag):
    
    '''

    CHECKRATIO
    * Compara numero de onda medido e teorico
    
    Dados de entrada: h - profundidade
                      k - numero de onda da teoria linear
                      snx - auto-espec de dspx
                      sny - auto-espec de dspy
    * ver descricao das matrizes em 'espec.py'
    
    Dados de saida: flag = vetor de flag preenchido
                    kf = numero de onda medido
                    rf = vetor de checkratio
                    rf_med = valor medio do ckeckratio

    Aprovado  : flag = '1'
    Reprovado : flag = '3'
    
    '''
	
    f = sn[:,0] #vetor de frequencia
    c11 = sn[:,2] #auto-espec de heave
    c22 = snx[:,2] #auto-espec de dspx
    c33 = sny[:,2] #auto-espec de dspy

    #numero de onda do instrumento (medido)
    kf = np.real(np.sqrt(c11 / (c22+c33)))

    #check-ratio
    rf = (1 / (np.tanh(k) * h) ) * kf

    #valor medio de check-ratio na frequencia de energia
    rf_med = np.mean([rf[1:12]])

    if rf_med < 0.9 or rf_med > 1.1:

        flag[0] = flag[0] + '3'
        flag[1] = flag[1] + '3'
        flag[2] = flag[2] + '3'

    else:

        flag[0] = flag[0] + '1'
        flag[1] = flag[1] + '1'
        flag[2] = flag[2] + '1'
        
    return flag, kf, rf, rf_med


# ================================================================================== #

#espectro de fase