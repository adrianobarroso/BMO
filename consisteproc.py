# -*- coding: utf-8 -*-
#
# Consistencia de parametros meteo-oceanograficos processados
#
# Autores: 
# Henrique P. P. Pereira
# Izabel Nogueira
# Ricardo M. Campos
# Carlos E. Parente
# Fabio Nascimento

# Data da ultima modificacao: 05/02/2014
#
# Testes:
# 1 - Range
# 2 - Spike

# ================================================================================== #
#importa bibliotecas

from numpy import *
import numpy as np
from pylab import *
import pylab as pl
from scipy.stats import nanmean, nanstd

import numeronda

# ================================================================================== #

### a) Consitencia dos parâmetros de ondas (Hs, Tp, Dp, ...)

# ================================================================================== #


def faixa(var,imin,imax,lmin,lmax,flag):
    
    '''
    
    TESTE DE FAIXA (RANGE)
    
    Dados de entrada: var - variavel sem consistencia
                      var1 - variavel editada
                      linf - limite inferior
                      lsup - limite superior
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: 'A'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    for i in range(len(var)):

      if np.isnan(var[i]):

          flag[i] = flag[i] + '9'

      # A condicao eh realizada na serie bruta
      elif var[i] < imin or var[i] > imax:

          flag[i] = flag[i] + '4'

          #o valor do dado inconsistente editado recebe 'nan'
          # var1[i] = np.nan

      # A condicao eh realizada na serie bruta
      elif var[i] < lmin or var[i] > lmax:

          flag[i] = flag[i] + '3'

          #o valor do dado inconsistente editado recebe 'nan'
          # var1[i] = np.nan

      else:

          flag[i] = flag[i] + '1'


    return flag


# ================================================================================== #

def variab(var,lag,lim,flag):
    
    '''
    
    TESTE DE VARIABILDADE TEMPORAL
    
    Dados de entrada: var - variavel
                      var1 - variavel editada
                      lag - delta tempo para o teste (indicado ser de 0 a 3 horas)
                      lim - variacao temporal maxima (para o lag escolhido)
                      flag - matriz de flags
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - data + flag
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: 'B'
         Dados 'consistentes' recebem flag = '0'
    
    '''
    
    #calcula a derivada de acordo com o lag (horas)
    der = var[lag:] - var[:-lag]
    
    for i in range(len(der)):

        if np.isnan(var[i]):

          flag[i] = flag[i] + '9'
                             
        elif der[i] > lim or der[i] < -lim:
            
            flag[i] = flag[i] + '4'
            
            #o valor do dado inconsistente recebe 'nan'
            # var1[i] = np.nan
            
        else:
        
            flag[i] = flag[i] + '1'


    # Coloca flag = '1' nos utlimos dados (nao foram verificados)
    flag[-lag:] = [flag[-i] + '2' for i in range(1,lag+1)]
    # var1[-lag:] = np.nan
                
    return flag
    
    
## ================================================================================== #

def iguais(var,nci,flag):
    
    '''
    
    TESTE VALORES CONSECUTIVOS IGUAIS
    
    Dados de entrada: var - variavel
                      var1 - variavel editada
                      nci - numero de valores consecutivos iguais
                      flag - matriz de flags
                          
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag                    
       
    Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
         O flag utilizado para o teste de range eh: 'C'
         Dados 'consistentes' recebem flag = '0'
    
    '''

    for i in range(len(var)-nci):

        if np.isnan(var[i]):

          flag[i] = flag[i] + '9'
                        
        elif (var[i:i+nci] == var[i+1:i+nci+1]).all():
            
            flag[i] = flag[i] + '4'
            
            #o valor do dado inconsistente recebe 'nan'
            # var1[i] = np.nan
            
        else:
            
            flag[i] = flag[i] + '1'


    # Coloca flag = '2' nos dados que nao foram verificados
    flag[-nci:] = [flag[i] + '2' for i in range(-nci,0)]

                
    return flag

# ================================================================================== #
    
def meddp(var,p,N,flag):
    
    '''
    
    TESTE DE MEDIA E DESVIO PADRAO
    
    Dados de entrada: var - variavel
                      p - periodo em que sera calculada a media e desvio padrao
                      N - multiplicador do desvio padrao
                      flag - matriz de flags
    
    Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
                    flag - parametro + flag
       
    Obs:
    '''

    for i in range(len(var)):

        med = np.nanmean(var[i:i+p])
        dp = np.nanstd(var[i:i+p])

        if np.isnan(var[i]):

          flag[i] = flag[i] + '9'

        elif var[i] < med - N * dp or var[i] > med + N * dp:

            flag[i] = flag[i] + '3'

        else:

            flag[i] = flag[i] + '1'

    # Coloca flag = '2' nos dados que nao foram verificados
    # flag[-p:] = [flag[i] + '2' for i in range(-p,0)]

    return flag

# # ================================================================================== #
    
# def t2(var,var1,M,hh,flag):
    
#     '''
    
#     TESTE SPIKE UTILIZANDO MEDIA MOVEL
    
#     Dados de entrada: var - variavel
#                       var1 - variavel editada
#                       M - multiplicador do desvio padrao
#                       despad - desvio padrao da serie
#                       hh - tempo em horas para a media movel
#                       flag - matriz de flags
    
#     Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
#                     flag - parametro + flag
       
#     Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
#          O flag utilizado para o teste de range eh: '1'
#          Dados 'consistentes' recebem flag = '0'
    
#     '''

#     for i in range(len(var)):
        
#         if var[i] < nanmean(var[i-int(hh/2):i+int(hh/2)])-M*nanstd(var[i-int(hh/2):i+int(hh/2)]) or var[i] > nanmean(var[i-hh/2:i+hh/2])+M*nanmean(var[i-int(hh/2):i+int(hh/2)]):
            
#             flag[i] = flag[i] + '1'
            
#             #o valor do dado inconsistente recebe 'nan'
#             var1[i] = nan
            
#         else:
            
#             flag[i] = flag[i] + '0'
            
#     return var1,flag
    
    
# # ================================================================================== #


### ** fazer o teste de consistencia dos parametros processados, indicando se exedeu limite superior ou inferior
# def t6(serie,linf,lsup,flag):
    
#     '''

#     VERIFICA VALORES QUE EXCEDEM LIMITE GROSSEIRO
#     * Verifica valores que excedem limites grosseiros
    
#     Dados de entrada: serie - (eta, dspx, dspy)
#                       linf - limite inferior
#                       lsup - limite superior
#                       flag - vetor de flags a ser preenchido
    
#     Dados de saida: flag = vetor de flag preenchido

#     Posicao (indice) em 'lista_flag' : 6
#     Aprovado  : flag = '0'
#     Reprovado : flag = 'a' - above limit
#                 flag = 'b' - below limit
#                 flag = 'c' - above and below limit
    
#     '''
    
#     if ( (serie > lsup).any() and (serie > lsup).any() ):

#         flag = flag + 'c'

#     elif (serie > lsup).any():

#         flag = flag + 'a'

#     elif (serie < linf).any():
        
#         flag = flag + 'b'
        
#     else:
        
#         flag = flag + '0'
    
#     return flag    
#     


# ================================================================================== #

# def t2(var,med,dp,M,flag):

#     '''

#     TESTE DE SPIKE
    
#     Dados de entrada: var - variavel sem consistencia
#                       med - media da serie
#                       dp - desvio padrão da série
#                       M - multiplicador do dp
#                       flag - vetor de flags a ser preenchido
    
#     Dados de saida: flag = vetor de flag preenchido

#     Aprovado  : flag = '0'
#     Reprovado : flag = '1'
    
#     '''

#     var1 = np.copy(var)

#     for i in range(len(var)):

#         if np.abs(var[i]) > (med + M*dp):

#             var1[i] = np.nan

#             flag[i] = flag[i] + '1'

#         else:

#             flag[i] = flag[i] + '0'

#     return var1,flag


## ================================================================================== #

# def t4(var,var1,hmax,hs,flag):

    
#     '''
    
#     TESTE DE LIMITE DE FREAK-WAVE
    
#     Dados de entrada: var - variavel
#                       var1 - variavel editada
#                       hmax - altura maxima
#                       hs - altura significativa
                          
#     Dados de saida: var1 - variavel consistente (com NaN no lugar do dado espúrio)
#                     flag - parametro + flag                    
       
#     Obs: A saida 'flag' cria uma lista com o valor do parametro e o flag
#          O flag utilizado para o teste de freakwave eh: 'D'
#          Dados 'consistentes' recebem flag = '0'
    
#     '''


#     for i in range(len(var)):

#       if hmax[i] / hs[i] >= 2.1:

#         flag = flag + 'D'

#         #o valor do dado inconsistente recebe 'nan'
#         var1[i] = nan

#       else:

#         flag = flag + '0'

      #flag[-nvc:] = [flag[-i]+'n' for i in range(1,nvc+1)]


    # return var1,flag



