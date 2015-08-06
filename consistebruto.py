# -*- coding: utf-8 -*-
#
#consistencia dos dados brutos de boias meteo-oceanograficas
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
# Teste 1

def msg(arq,flag):
    
    '''

    VALIDADE DA MENSAGEM RECEBIDA  (Boias Axys)
    * Ex: 200905101100.HNE
    * Verifica se os minutos estao igual a '00'
    * Para dados programados para serem enviados em hora cheia (min=00)
    
    Dados de entrada: arq - nome do arquivo
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 0
    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
		
    if arq[10:12] <> '00':

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
        
    return flag

# ================================================================================== #
# Teste 2

def comp(serie,cs,flag): #modificar a entrada para entrar com qlq tamanho de vetor, devido aos tbm dados meteorologicos
    
    '''

    COMPRIMENTO DA SERIE
    * Verifica se o comprimento da serie eh menor que 1313
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Posicao (indice) em 'lista_flag' : 1
    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
    
    #2- verifica comprimento do vetor
    if len(serie) < cs:

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
        
    return flag

# ================================================================================== #
# Teste 3

def gap(serie,N,flag):
    
    '''

    TESTE DE GAP
    * Verifica valores consecutivos faltando
    
    Dados de entrada: serie - (ex: elevacao, deslocamento ..)
                      N - numero de valores consecutivos aceitaveis para estar
                      faltando
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
    
    for i in range(len(serie)-N):
        
        if np.isnan(serie[i:i+N]).all() == True:

            flag = flag + '4'
            
            #se achou um gap, para o teste
            break

    if flag <> '4':

        flag = flag + '1'

    return flag


# ================================================================================== #
# Teste 4

def spike(serie,med,dp,N,M,P,flag):
    
    '''

    TESTE DE SPIKE
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      med - média da série
                      dp - desvio padrão da série
                      N% - limite total de spikes
                      M - multiplicador do dp
                      P - numero de iteracoes
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''

    #retira o primeiro e ultimo valor, caso o spike ocorra nessas
    #posicoes, nao sera editado, pois da erro (melhorar)
    vetc = cp.copy(serie)

    #M1 = 0
    #M2 = 0
    #quantidade maxima de spikes
    N = len(serie) * N / 100 #transforma em %

    #procura valores na serie maior do que o limite
    sp = pl.find(np.abs(serie) > (M * dp) )
    
    #verifica quantidade total de spikes
    M1 = len(sp)

    #valor inicial para numero de spikes (caso tenha spikes sera incrementada durante o programa)
    M2 = 0

    # ----------------#
    # Realiza edicoes #

    #se a quantidade de spikes for maior que zero
    if M1 > 0:

        #numero de vezes que serao realizadas edicoes (retirada de spikes)
        for j in range(P):

            #recalcula o numero de spikes
            sp = pl.find(np.abs(vetc[1:-1]) > (M * dp) )

            #coloca o valor medio no lugar do spike
            for i in range(len(sp)):

                vetc[sp[i]] = np.mean([ vetc[sp[i]-1] , vetc[sp[i]+1] ])

        #verifica se ainda permaneceu com spikes depois das iteracoes
        #Quantidade total de spikes depois das P iteracoes  
        M2 = len(sp)

    if M1 > N or M2 > 0:
    
        flag = flag + '4'
    
    else:
    
        flag = flag + '1'

    return flag, vetc
    
# ================================================================================== #
# Teste 5

def nulos(serie,ncn,flag):
    
    '''

    VERIFICA VALORES CONSECUTIVOS NULOS
    * Verifica valores consecutivos nulos
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      ncn - numero de valores consecutivos nulos testados
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''
    
    for i in range(len(serie)-ncn):

        if (serie[i:i+ncn] == 0).all():

            flag = flag + '4'
            break

        else:

            flag = flag + '1'
            break

    return flag
            

# ================================================================================== #
# Teste 6


def flat(serie,lmin,lmax,flag):
    
    '''

    VALORES FLAT (PROXIMOS DE ZERO)
    * Verifica variacoes menores que 20 cm
    * Verifica se todos os valores de eta sao muito proximos de zero
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    Aprovado  : flag = '1'
    Reprovado : flag = '4'
    
    '''

    if ( (serie > lmin).all() and (serie < lmax).all() ):

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
        
    return flag


# ================================================================================== #
# Teste 7

def iguais(serie,nci,flag):
    
    '''

    VERIFICA VALORES CONSECUTIVOS IGUAIS
    * Verifica valores consecutivos iguais
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      nci - numero de valores consecutivos iguais testados
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    
    '''
    
    for i in range(len(serie)-(nci+1)):
        
        if (serie[i:i+nci] == serie[i+1:i+1+nci]).all():

            flag = flag + '4'
            
            break
        
        else:
            
            flag = flag + '1'
            
            break
            
    return flag
            

# ================================================================================== #
# Teste 8

def faixa(serie,imin,imax,flag):
    
    '''

    VERIFICA VALORES QUE EXCEDEM LIMITE DE RANGE
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      imin - limite inferior grosseiro
                      imax - limite superior grosseiro
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    '''
    
    if ( (serie > imax).any() and (serie < imin).any() ):

        flag = flag + '4'
        
    else:
        
        flag = flag + '1'
    
    return flag    
    

# ================================================================================== #
# Teste 9

def shift(serie,m,n,P,flag):
    
    '''

    VERIFICA DESLOCAMENTO DAS MEDIAS DOS SEGMENTOS
    
    Dados de entrada: serie - (eta, dspx, dspy)
                      m - comprimento do segmento (length(serie)/8)
                      n - numero de segmentos (UNESCO = 8)
                      P - deslocamento maximo das medias dos segmentos (UNESCO = 0.20 m)
                      flag - vetor de flags a ser preenchido
    
    Dados de saida: flag = vetor de flag preenchido

    '''

    dmed = []
    a = 0

    for i in range(n-1):

        m1 = np.mean(serie[a:(a+m)])

        m2 = np.mean(serie[(a+m):(a+2*m)])

        dmed.append(m1 - m2)

        a += m

    if abs(max(dmed)) > P:

        flag = flag + '4'

    else:
        
        flag = flag + '1'
    
    return flag    

# ================================================================================== #
