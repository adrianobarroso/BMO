## Cria relatorio para ser impresso no terminal

from numpy import *
from pylab import *

def axys(f,lista,listap,listac,listai,flagb,flagp,h,local,latlon,idargos,idwmo):


    # ================================================================================== #
    # Quantifica dados reprovados por teste
    # cria matriz de flags por variavel
    # ================================================================================== #


    # ================================================================================== #
    # flags dos dados brutos

    #heave
    feta = [] ; [feta.append(list(flagb[i,1])) for i in range(len(flagb))]
    feta = np.array(feta)
    #dsp.EO
    fetax = [] ; [fetax.append(list(flagb[i,2])) for i in range(len(flagb))]
    fetax = np.array(fetax)

    #dsp.NS
    fetay = [] ; [fetay.append(list(flagb[i,3])) for i in range(len(flagb))]
    fetay = np.array(fetay)

    # ================================================================================== #
    # quantifica flags dos dados brutos

    #eta
    etaa = np.zeros(feta.shape[1])
    etar = np.zeros(feta.shape[1])
    etas = np.zeros(feta.shape[1])

    #etax
    etaxa = np.zeros(fetax.shape[1])
    etaxr = np.zeros(fetax.shape[1])
    etaxs = np.zeros(fetax.shape[1])

    #etay
    etaya = np.zeros(fetay.shape[1])
    etayr = np.zeros(fetay.shape[1])
    etays = np.zeros(fetay.shape[1])

    #varia quantidade de testes
    for i in range(feta.shape[1]):

        #aprovados
        etaa[i] = len(np.where(feta[:,i] == '1')[0])
        etaxa[i] = len(np.where(fetax[:,i] == '1')[0])
        etaya[i] = len(np.where(fetay[:,i] == '1')[0])
        
        #suspeitos
        etas[i] = len(np.where(feta[:,i] == '3')[0])
        etaxs[i] = len(np.where(fetax[:,i] == '3')[0])
        etays[i] = len(np.where(fetay[:,i] == '3')[0])
        
        #reprovados
        etar[i] = len(np.where(feta[:,i] == '4')[0])
        etaxr[i] = len(np.where(fetax[:,i] == '4')[0])
        etayr[i] = len(np.where(fetay[:,i] == '4')[0])


    # ================================================================================== #
    # flags dados processados

    #hs
    fhs = [] ; [fhs.append(list(flagp[i,1])) for i in range(len(flagp))]
    fhs = np.array(fhs)

    #h10
    fh10 = [] ; [fh10.append(list(flagp[i,2])) for i in range(len(flagp))]
    fh10 = np.array(fh10)

    #hmax
    fhmax = [] ; [fhmax.append(list(flagp[i,3])) for i in range(len(flagp))]
    fhmax = np.array(fhmax)

    #tmed
    ftmed = [] ; [ftmed.append(list(flagp[i,4])) for i in range(len(flagp))]
    ftmed = np.array(ftmed)

    #thmax
    fthmax = [] ; [fthmax.append(list(flagp[i,5])) for i in range(len(flagp))]
    fthmax = np.array(fthmax)

    #hm0
    fhm0 = [] ; [fhm0.append(list(flagp[i,6])) for i in range(len(flagp))]
    fhm0 = np.array(fhm0)

    #tp
    ftp = [] ; [ftp.append(list(flagp[i,7])) for i in range(len(flagp))]
    ftp = np.array(ftp)

    #dp
    fdp = [] ; [fdp.append(list(flagp[i,8])) for i in range(len(flagp))]
    fdp = np.array(fdp)

    #sigma1p
    fsigma1p = [] ; [fsigma1p.append(list(flagp[i,9])) for i in range(len(flagp))]
    fsigma1p = np.array(fsigma1p)

    #sigma2p
    fsigma2p = [] ; [fsigma2p.append(list(flagp[i,10])) for i in range(len(flagp))]
    fsigma2p = np.array(fsigma2p)

    #hm01
    fhm01 = [] ; [fhm01.append(list(flagp[i,11])) for i in range(len(flagp))]
    fhm01 = np.array(fhm01)

    #tp1
    ftp1 = [] ; [ftp1.append(list(flagp[i,12])) for i in range(len(flagp))]
    ftp1 = np.array(ftp1)

    #tp1
    fdp1 = [] ; [fdp1.append(list(flagp[i,13])) for i in range(len(flagp))]
    fdp1 = np.array(fdp1)

    #hm02
    fhm02 = [] ; [fhm02.append(list(flagp[i,14])) for i in range(len(flagp))]
    fhm02 = np.array(fhm02)
    
    #tp1
    ftp2 = [] ; [ftp2.append(list(flagp[i,15])) for i in range(len(flagp))]
    ftp2 = np.array(ftp2)

    #dp1
    fdp2 = [] ; [fdp2.append(list(flagp[i,16])) for i in range(len(flagp))]
    fdp2 = np.array(fdp2)


    # ================================================================================== #
    # quantifica flags dos dados processados

    # aprovados
    hsa = np.zeros(fhs.shape[1])
    h10a = np.zeros(fh10.shape[1])
    hmaxa = np.zeros(fhmax.shape[1])
    tmeda = np.zeros(ftmed.shape[1])
    thmaxa = np.zeros(fthmax.shape[1])
    hm0a = np.zeros(fhm0.shape[1])
    tpa = np.zeros(ftp.shape[1])
    dpa = np.zeros(fdp.shape[1])
    sigma1pa = np.zeros(fsigma1p.shape[1])
    sigma2pa = np.zeros(fsigma2p.shape[1])
    hm01a = np.zeros(fhm01.shape[1])
    tp1a = np.zeros(ftp1.shape[1])
    dp1a = np.zeros(fdp1.shape[1])
    hm02a = np.zeros(fhm02.shape[1])
    tp2a = np.zeros(ftp2.shape[1])
    dp2a = np.zeros(fdp2.shape[1])

    #nao avaliado
    hsn = np.zeros(fhs.shape[1])
    h10n = np.zeros(fh10.shape[1])
    hmaxn = np.zeros(fhmax.shape[1])
    tmedn = np.zeros(ftmed.shape[1])
    thmaxn = np.zeros(fthmax.shape[1])
    hm0n = np.zeros(fhm0.shape[1])
    tpn = np.zeros(ftp.shape[1])
    dpn = np.zeros(fdp.shape[1])
    sigma1pn = np.zeros(fsigma1p.shape[1])
    sigma2pn = np.zeros(fsigma2p.shape[1])
    hm01n = np.zeros(fhm01.shape[1])
    tp1n = np.zeros(ftp1.shape[1])
    dp1n = np.zeros(fdp1.shape[1])
    hm02n = np.zeros(fhm02.shape[1])
    tp2n = np.zeros(ftp2.shape[1])
    dp2n = np.zeros(fdp2.shape[1])

    #suspeito
    hss = np.zeros(fhs.shape[1])
    h10s = np.zeros(fh10.shape[1])
    hmaxs = np.zeros(fhmax.shape[1])
    tmeds = np.zeros(ftmed.shape[1])
    thmaxs = np.zeros(fthmax.shape[1])
    hm0s = np.zeros(fhm0.shape[1])
    tps = np.zeros(ftp.shape[1])
    dps = np.zeros(fdp.shape[1])
    sigma1ps = np.zeros(fsigma1p.shape[1])
    sigma2ps = np.zeros(fsigma2p.shape[1])
    hm01s = np.zeros(fhm01.shape[1])
    tp1s = np.zeros(ftp1.shape[1])
    dp1s = np.zeros(fdp1.shape[1])
    hm02s = np.zeros(fhm02.shape[1])
    tp2s = np.zeros(ftp2.shape[1])
    dp2s = np.zeros(fdp2.shape[1])

    #reprovados
    hsr = np.zeros(fhs.shape[1])
    h10r = np.zeros(fh10.shape[1])
    hmaxr = np.zeros(fhmax.shape[1])
    tmedr = np.zeros(ftmed.shape[1])
    thmaxr = np.zeros(fthmax.shape[1])
    hm0r = np.zeros(fhm0.shape[1])
    tpr = np.zeros(ftp.shape[1])
    dpr = np.zeros(fdp.shape[1])
    sigma1pr = np.zeros(fsigma1p.shape[1])
    sigma2pr = np.zeros(fsigma2p.shape[1])
    hm01r = np.zeros(fhm01.shape[1])
    tp1r = np.zeros(ftp1.shape[1])
    dp1r = np.zeros(fdp1.shape[1])
    hm02r = np.zeros(fhm02.shape[1])
    tp2r = np.zeros(ftp2.shape[1])
    dp2r = np.zeros(fdp2.shape[1])

    #valor faltando
    hsf = np.zeros(fhs.shape[1])
    h10f = np.zeros(fh10.shape[1])
    hmaxf = np.zeros(fhmax.shape[1])
    tmedf = np.zeros(ftmed.shape[1])
    thmaxf = np.zeros(fthmax.shape[1])
    hm0f = np.zeros(fhm0.shape[1])
    tpf = np.zeros(ftp.shape[1])
    dpf = np.zeros(fdp.shape[1])
    sigma1pf = np.zeros(fsigma1p.shape[1])
    sigma2pf = np.zeros(fsigma2p.shape[1])
    hm01f = np.zeros(fhm01.shape[1])
    tp1f = np.zeros(ftp1.shape[1])
    dp1f = np.zeros(fdp1.shape[1])
    hm02f = np.zeros(fhm02.shape[1])
    tp2f = np.zeros(ftp2.shape[1])
    dp2f = np.zeros(fdp2.shape[1])

    #varia a quantidade de testes
    for i in range(fhs.shape[1]):

        #aprovados
        hsa[i] = len(np.where(fhs[:,i] == '1')[0])
        h10a[i] = len(np.where(fh10[:,i] == '1')[0])
        hmaxa[i] = len(np.where(fhmax[:,i] == '1')[0])
        tmeda[i] = len(np.where(ftmed[:,i] == '1')[0])
        thmaxa[i] = len(np.where(fthmax[:,i] == '1')[0])
        hm0a[i] = len(np.where(fhm0[:,i] == '1')[0])
        tpa[i] = len(np.where(ftp[:,i] == '1')[0])
        dpa[i] = len(np.where(fdp[:,i] == '1')[0])
        sigma1pa[i] = len(np.where(fsigma1p[:,i] == '1')[0])
        sigma2pa[i] = len(np.where(fsigma2p[:,i] == '1')[0])
        hm01a[i] = len(np.where(fhm01[:,i] == '1')[0])
        tp1a[i] = len(np.where(ftp1[:,i] == '1')[0])
        dp1a[i] = len(np.where(fdp1[:,i] == '1')[0])
        hm02a[i] = len(np.where(fhm02[:,i] == '1')[0])
        tp2a[i] = len(np.where(ftp2[:,i] == '1')[0])
        dp2a[i] = len(np.where(fdp2[:,i] == '1')[0])

        #nao avaliado
        hsn[i] = len(np.where(fhs[:,i] == '2')[0])
        h10n[i] = len(np.where(fh10[:,i] == '2')[0])
        hmaxn[i] = len(np.where(fhmax[:,i] == '2')[0])
        tmedn[i] = len(np.where(ftmed[:,i] == '2')[0])
        thmaxn[i] = len(np.where(fthmax[:,i] == '2')[0])
        hm0n[i] = len(np.where(fhm0[:,i] == '2')[0])
        tpn[i] = len(np.where(ftp[:,i] == '2')[0])
        dpn[i] = len(np.where(fdp[:,i] == '2')[0])
        sigma1pn[i] = len(np.where(fsigma1p[:,i] == '2')[0])
        sigma2pn[i] = len(np.where(fsigma2p[:,i] == '2')[0])
        hm01n[i] = len(np.where(fhm01[:,i] == '2')[0])
        tp1n[i] = len(np.where(ftp1[:,i] == '2')[0])
        dp1n[i] = len(np.where(fdp1[:,i] == '2')[0])
        hm02n[i] = len(np.where(fhm02[:,i] == '2')[0])
        tp2n[i] = len(np.where(ftp2[:,i] == '2')[0])
        dp2n[i] = len(np.where(fdp2[:,i] == '2')[0])

        #suspeitos
        hss[i] = len(np.where(fhs[:,i] == '3')[0])
        h10s[i] = len(np.where(fh10[:,i] == '3')[0])
        hmaxs[i] = len(np.where(fhmax[:,i] == '3')[0])
        tmeds[i] = len(np.where(ftmed[:,i] == '3')[0])
        thmaxs[i] = len(np.where(fthmax[:,i] == '3')[0])
        hm0s[i] = len(np.where(fhm0[:,i] == '3')[0])
        tps[i] = len(np.where(ftp[:,i] == '3')[0])
        dps[i] = len(np.where(fdp[:,i] == '3')[0])
        sigma1ps[i] = len(np.where(fsigma1p[:,i] == '3')[0])
        sigma2ps[i] = len(np.where(fsigma2p[:,i] == '3')[0])
        hm01s[i] = len(np.where(fhm01[:,i] == '3')[0])
        tp1s[i] = len(np.where(ftp1[:,i] == '3')[0])
        dp1s[i] = len(np.where(fdp1[:,i] == '3')[0])
        hm02s[i] = len(np.where(fhm02[:,i] == '3')[0])
        tp2s[i] = len(np.where(ftp2[:,i] == '3')[0])
        dp2s[i] = len(np.where(fdp2[:,i] == '3')[0])

        #dado reprovado
        hsr[i] = len(np.where(fhs[:,i] == '4')[0])
        h10r[i] = len(np.where(fh10[:,i] == '4')[0])
        hmaxr[i] = len(np.where(fhmax[:,i] == '4')[0])
        tmedr[i] = len(np.where(ftmed[:,i] == '4')[0])
        thmaxr[i] = len(np.where(fthmax[:,i] == '4')[0])
        hm0r[i] = len(np.where(fhm0[:,i] == '4')[0])
        tpr[i] = len(np.where(ftp[:,i] == '4')[0])
        dpr[i] = len(np.where(fdp[:,i] == '4')[0])
        sigma1pr[i] = len(np.where(fsigma1p[:,i] == '4')[0])
        sigma2pr[i] = len(np.where(fsigma2p[:,i] == '4')[0])
        hm01r[i] = len(np.where(fhm01[:,i] == '4')[0])
        tp1r[i] = len(np.where(ftp1[:,i] == '4')[0])
        dp1r[i] = len(np.where(fdp1[:,i] == '4')[0])
        hm02r[i] = len(np.where(fhm02[:,i] == '4')[0])
        tp2r[i] = len(np.where(ftp2[:,i] == '4')[0])
        dp2r[i] = len(np.where(fdp2[:,i] == '4')[0])


        #dado faltando
        hsf[i] = len(np.where(fhs[:,i] == '9')[0])
        h10f[i] = len(np.where(fh10[:,i] == '9')[0])
        hmaxf[i] = len(np.where(fhmax[:,i] == '9')[0])
        tmedf[i] = len(np.where(ftmed[:,i] == '9')[0])
        thmaxf[i] = len(np.where(fthmax[:,i] == '9')[0])
        hm0f[i] = len(np.where(fhm0[:,i] == '9')[0])
        tpf[i] = len(np.where(ftp[:,i] == '9')[0])
        dpf[i] = len(np.where(fdp[:,i] == '9')[0])
        sigma1pf[i] = len(np.where(fsigma1p[:,i] == '9')[0])
        sigma2pf[i] = len(np.where(fsigma2p[:,i] == '9')[0])
        hm01f[i] = len(np.where(fhm01[:,i] == '9')[0])
        tp1f[i] = len(np.where(ftp1[:,i] == '9')[0])
        dp1f[i] = len(np.where(fdp1[:,i] == '9')[0])
        hm02f[i] = len(np.where(fhm02[:,i] == '9')[0])
        tp2f[i] = len(np.where(ftp2[:,i] == '9')[0])
        dp2f[i] = len(np.where(fdp2[:,i] == '9')[0])


    # ================================================================================== #
    # Cria e salva relatorio

    regua1 = 50 * '-'
    regua2 = 50 * '='


    #salva relatorio
    print >> f, (

        'Relatorio de Controle de Qualidade de dados de Ondas \n'
        'Laboratorio de Instrumentacao Oceanografica - LIOc \n'
        'COPPE/UFRJ \n \n'

        'Boia Axys - PNBOIA/MB \n'
        'ID Argos: ' + str(idargos) + '\n'
        'ID WMO: ' + str(idwmo) + '\n'
        'Localizacao: ' + local + '\n'
        'Lat/Lon: ' + latlon + '\n'
        'Profundidade: ' + str(h) + ' m \n'
        'Data inicial: ' + listap[0][6:8]+'/'+listap[0][4:6]+'/'+listap[0][0:4]+' - '+listap[0][8:10]+':'+listap[0][10:12] + '\n'
        'Data final: '   + listap[-1][6:8]+'/'+listap[-1][4:6]+'/'+listap[-1][0:4]+' - '+listap[-1][8:10]+':'+listap[-1][10:12] + '\n \n'

        'Numero de arquivos listados no diretorio: ' + str(len(lista)) + '\n'
        'Numero de series analisadas: '              + str(len(listap)) + '\n'
        'Numero de series aprovadas no CQ de Curto-Termo: '          + str(len(listac)) + '\n'
        'Numero de series reprovadas no CQ de Curto-Termo: '          + str(len(listai)) + '\n \n'

        'Numero de Testes de CQ:' '\n'
        '- Brutos: '      + str(len(flagb[0][1])) + '\n'
        '- Processados: ' + str(len(flagp[0][1])) + '\n'


        # ================================================================================== #


        '\n' + regua2 + '\n'
        'Consistencia dos dados brutos'
        '\n' + regua2 + '\n'

        '\n' + regua1 + '\n'
        '** Teste 1 - Mensagem recebida **' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[0])) + '\n'
        'Suspeito: ' + str(int(etas[0])) + '\n'
        'Reprovado: ' + str(int(etar[0])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[0])) + '\n'
        'Suspeito: ' + str(int(etaxs[0])) + '\n'
        'Reprovado: ' + str(int(etaxr[0])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[0])) + '\n'
        'Suspeito: ' + str(int(etays[0])) + '\n'
        'Reprovado: ' + str(int(etayr[0])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 2 - Comprimento da serie ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[1])) + '\n'
        'Suspeito: ' + str(int(etas[1])) + '\n'
        'Reprovado: ' + str(int(etar[1])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[1])) + '\n'
        'Suspeito: ' + str(int(etaxs[1])) + '\n'
        'Reprovado: ' + str(int(etaxr[1])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[1])) + '\n'
        'Suspeito: ' + str(int(etays[1])) + '\n'
        'Reprovado: ' + str(int(etayr[1])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 3 - Lacuna (Gap) ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[2])) + '\n'
        'Suspeito: ' + str(int(etas[2])) + '\n'
        'Reprovado: ' + str(int(etar[2])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[2])) + '\n'
        'Suspeito: ' + str(int(etaxs[2])) + '\n'
        'Reprovado: ' + str(int(etaxr[2])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[2])) + '\n'
        'Suspeito: ' + str(int(etays[2])) + '\n'
        'Reprovado: ' + str(int(etayr[2])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 4 - Spike ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[3])) + '\n'
        'Suspeito: ' + str(int(etas[3])) + '\n'
        'Reprovado: ' + str(int(etar[3])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[3])) + '\n'
        'Suspeito: ' + str(int(etaxs[3])) + '\n'
        'Reprovado: ' + str(int(etaxr[3])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[3])) + '\n'
        'Suspeito: ' + str(int(etays[3])) + '\n'
        'Reprovado: ' + str(int(etayr[3])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 5 - Flat ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[4])) + '\n'
        'Suspeito: ' + str(int(etas[4])) + '\n'
        'Reprovado: ' + str(int(etar[4])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[4])) + '\n'
        'Suspeito: ' + str(int(etaxs[4])) + '\n'
        'Reprovado: ' + str(int(etaxr[4])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[4])) + '\n'
        'Suspeito: ' + str(int(etays[4])) + '\n'
        'Reprovado: ' + str(int(etayr[4])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 6 - Consec. Nulos ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[5])) + '\n'
        'Suspeito: ' + str(int(etas[5])) + '\n'
        'Reprovado: ' + str(int(etar[5])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[5])) + '\n'
        'Suspeito: ' + str(int(etaxs[5])) + '\n'
        'Reprovado: ' + str(int(etaxr[5])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[5])) + '\n'
        'Suspeito: ' + str(int(etays[5])) + '\n'
        'Reprovado: ' + str(int(etayr[1])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 7 - Consec. Iguais ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[6])) + '\n'
        'Suspeito: ' + str(int(etas[6])) + '\n'
        'Reprovado: ' + str(int(etar[6])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[6])) + '\n'
        'Suspeito: ' + str(int(etaxs[6])) + '\n'
        'Reprovado: ' + str(int(etaxr[6])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[6])) + '\n'
        'Suspeito: ' + str(int(etays[6])) + '\n'
        'Reprovado: ' + str(int(etayr[6])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 8 - Faixa ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[7])) + '\n'
        'Suspeito: ' + str(int(etas[7])) + '\n'
        'Reprovado: ' + str(int(etar[7])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[7])) + '\n'
        'Suspeito: ' + str(int(etaxs[7])) + '\n'
        'Reprovado: ' + str(int(etaxr[7])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[7])) + '\n'
        'Suspeito: ' + str(int(etays[7])) + '\n'
        'Reprovado: ' + str(int(etayr[7])) + '\n \n'

        '\n' + regua1 + '\n'
        '** Teste 9 - Shift ** ' '\n \n'

        '-- Eta --' '\n'
        'Aprovado: ' + str(int(etaa[8])) + '\n'
        'Suspeito: ' + str(int(etas[8])) + '\n'
        'Reprovado: ' + str(int(etar[8])) + '\n \n'

        '-- Dsp.EO --' '\n'
        'Aprovado: ' + str(int(etaxa[8])) + '\n'
        'Suspeito: ' + str(int(etaxs[8])) + '\n'
        'Reprovado: ' + str(int(etaxr[8])) + '\n \n'

        '-- Dsp.NS --' '\n'
        'Aprovado: ' + str(int(etaya[8])) + '\n'
        'Suspeito: ' + str(int(etays[8])) + '\n'
        'Reprovado: ' + str(int(etayr[8])) + '\n \n'


        # ================================================================================== #

        '\n' + regua2 + '\n'
        'Consistencia dos dados processados'
        '\n' + regua2 + '\n'


        '\n' + regua1 + '\n'
        '** Teste 1 - Faixa **' '\n \n'

        '-- Hs --' '\n'
        'Aprovado: ' + str(int(hsa[0])) + '\n'
        'Faltando: ' + str(int(hsf[0])) + '\n'
        'Suspeito: ' + str(int(hss[0])) + '\n'
        'Reprovado: ' + str(int(hsr[0])) + '\n'
        'Nao avaliado: ' + str(int(hsn[0])) + '\n \n'

        '-- H1/10 --' '\n'
        'Aprovado: ' + str(int(h10a[0])) + '\n'
        'Faltando: ' + str(int(h10f[0])) + '\n'
        'Suspeito: ' + str(int(h10s[0])) + '\n'
        'Reprovado: ' + str(int(h10r[0])) + '\n'
        'Nao avaliado: ' + str(int(h10n[0])) + '\n \n'

        '-- Hmax --' '\n'
        'Aprovado: ' + str(int(hmaxa[0])) + '\n'
        'Faltando: ' + str(int(hmaxf[0])) + '\n'
        'Suspeito: ' + str(int(hmaxs[0])) + '\n'
        'Reprovado: ' + str(int(hmaxr[0])) + '\n'
        'Nao avaliado: ' + str(int(hmaxn[0])) + '\n \n'

        '-- Tmed --' '\n'
        'Aprovado: ' + str(int(tmeda[0])) + '\n'
        'Faltando: ' + str(int(tmedf[0])) + '\n'
        'Suspeito: ' + str(int(tmeds[0])) + '\n'
        'Reprovado: ' + str(int(tmedr[0])) + '\n'
        'Nao avaliado: ' + str(int(tmedn[0])) + '\n \n'

        '-- THmax --' '\n'
        'Aprovado: ' + str(int(thmaxa[0])) + '\n'
        'Faltando: ' + str(int(thmaxf[0])) + '\n'
        'Suspeito: ' + str(int(thmaxs[0])) + '\n'
        'Reprovado: ' + str(int(thmaxr[0])) + '\n'
        'Nao avaliado: ' + str(int(thmaxn[0])) + '\n \n'

        '-- Hm0 --' '\n'
        'Aprovado: ' + str(int(hm0a[0])) + '\n'
        'Faltando: ' + str(int(hm0f[0])) + '\n'
        'Suspeito: ' + str(int(hm0s[0])) + '\n'
        'Reprovado: ' + str(int(hm0r[0])) + '\n'
        'Nao avaliado: ' + str(int(hm0n[0])) + '\n \n'

        '-- Tp --' '\n'
        'Aprovado: ' + str(int(tpa[0])) + '\n'
        'Faltando: ' + str(int(tpf[0])) + '\n'
        'Suspeito: ' + str(int(tps[0])) + '\n'
        'Reprovado: ' + str(int(tpr[0])) + '\n'
        'Nao avaliado: ' + str(int(tpn[0])) + '\n \n'

        '-- Dp --' '\n'
        'Aprovado: ' + str(int(dpa[0])) + '\n'
        'Faltando: ' + str(int(dpf[0])) + '\n'
        'Suspeito: ' + str(int(dps[0])) + '\n'
        'Reprovado: ' + str(int(dpr[0])) + '\n'
        'Nao avaliado: ' + str(int(dpn[0])) + '\n \n'

        '-- Sigma1p --' '\n'
        'Aprovado: ' + str(int(sigma1pa[0])) + '\n'
        'Faltando: ' + str(int(sigma1pf[0])) + '\n'
        'Suspeito: ' + str(int(sigma1ps[0])) + '\n'
        'Reprovado: ' + str(int(sigma1pr[0])) + '\n'
        'Nao avaliado: ' + str(int(sigma1pn[0])) + '\n \n'

        '-- Sigma2p --' '\n'
        'Aprovado: ' + str(int(sigma2pa[0])) + '\n'
        'Faltando: ' + str(int(sigma2pf[0])) + '\n'
        'Suspeito: ' + str(int(sigma2ps[0])) + '\n'
        'Reprovado: ' + str(int(sigma2pr[0])) + '\n'
        'Nao avaliado: ' + str(int(sigma2pn[0])) + '\n \n'

        '-- Hm01 / Hm02 --' '\n'
        'Aprovado: ' + str(int(hm01a[0])) + '\n'
        'Faltando: ' + str(int(hm01f[0])) + '\n'
        'Suspeito: ' + str(int(hm01s[0])) + '\n'
        'Reprovado: ' + str(int(hm01r[0])) + '\n'
        'Nao avaliado: ' + str(int(hm01n[0])) + '\n \n'

        '-- Tp1 / Tp2 --' '\n'
        'Aprovado: ' + str(int(tp1a[0])) + '\n'
        'Faltando: ' + str(int(tp1f[0])) + '\n'
        'Suspeito: ' + str(int(tp1s[0])) + '\n'
        'Reprovado: ' + str(int(tp1r[0])) + '\n'
        'Nao avaliado: ' + str(int(tp1n[0])) + '\n \n'

        '-- Dp1 / Dp2 --' '\n'
        'Aprovado: ' + str(int(dp1a[0])) + '\n'
        'Faltando: ' + str(int(dp1f[0])) + '\n'
        'Suspeito: ' + str(int(dp1s[0])) + '\n'
        'Reprovado: ' + str(int(dp1r[0])) + '\n'
        'Nao avaliado: ' + str(int(dp1n[0])) + '\n \n'

        # '-- Hm02 --' '\n'
        # 'Aprovado: ' + str(int(hm02a[0])) + '\n'
        # 'Faltando: ' + str(int(hm02f[0])) + '\n'
        # 'Suspeito: ' + str(int(hm02s[0])) + '\n'
        # 'Reprovado: ' + str(int(hm02r[0])) + '\n'
        # 'Nao avaliado: ' + str(int(hm02n[0])) + '\n \n'

        # '-- Tp2 --' '\n'
        # 'Aprovado: ' + str(int(tp2a[0])) + '\n'
        # 'Faltando: ' + str(int(tp2f[0])) + '\n'
        # 'Suspeito: ' + str(int(tp2s[0])) + '\n'
        # 'Reprovado: ' + str(int(tp2r[0])) + '\n'
        # 'Nao avaliado: ' + str(int(tp2n[0])) + '\n \n'

        # '-- Dp2 --' '\n'
        # 'Aprovado: ' + str(int(dp2a[0])) + '\n'
        # 'Faltando: ' + str(int(dp2f[0])) + '\n'
        # 'Suspeito: ' + str(int(dp2s[0])) + '\n'
        # 'Reprovado: ' + str(int(dp2r[0])) + '\n'
        # 'Nao avaliado: ' + str(int(dp2n[0])) + '\n \n'


        # ================================================================================== #

        '\n' + regua1 + '\n'
        '** Teste 2 - Variabilidade Temporal ** ' '\n \n'


        '-- Hs --' '\n'
        'Aprovado: ' + str(int(hsa[1])) + '\n'
        'Faltando: ' + str(int(hsf[1])) + '\n'
        'Suspeito: ' + str(int(hss[1])) + '\n'
        'Reprovado: ' + str(int(hsr[1])) + '\n'
        'Nao avaliado: ' + str(int(hsn[1])) + '\n \n'

        '-- H1/10 --' '\n'
        'Aprovado: ' + str(int(h10a[1])) + '\n'
        'Faltando: ' + str(int(h10f[1])) + '\n'
        'Suspeito: ' + str(int(h10s[1])) + '\n'
        'Reprovado: ' + str(int(h10r[1])) + '\n'
        'Nao avaliado: ' + str(int(h10n[1])) + '\n \n'

        '-- Hmax --' '\n'
        'Aprovado: ' + str(int(hmaxa[1])) + '\n'
        'Faltando: ' + str(int(hmaxf[1])) + '\n'
        'Suspeito: ' + str(int(hmaxs[1])) + '\n'
        'Reprovado: ' + str(int(hmaxr[1])) + '\n'
        'Nao avaliado: ' + str(int(hmaxn[1])) + '\n \n'

        '-- Tmed --' '\n'
        'Aprovado: ' + str(int(tmeda[1])) + '\n'
        'Faltando: ' + str(int(tmedf[1])) + '\n'
        'Suspeito: ' + str(int(tmeds[1])) + '\n'
        'Reprovado: ' + str(int(tmedr[1])) + '\n'
        'Nao avaliado: ' + str(int(tmedn[1])) + '\n \n'

        '-- THmax --' '\n'
        'Aprovado: ' + str(int(thmaxa[1])) + '\n'
        'Faltando: ' + str(int(thmaxf[1])) + '\n'
        'Suspeito: ' + str(int(thmaxs[1])) + '\n'
        'Reprovado: ' + str(int(thmaxr[1])) + '\n'
        'Nao avaliado: ' + str(int(thmaxn[1])) + '\n \n'

        '-- Hm0 --' '\n'
        'Aprovado: ' + str(int(hm0a[1])) + '\n'
        'Faltando: ' + str(int(hm0f[1])) + '\n'
        'Suspeito: ' + str(int(hm0s[1])) + '\n'
        'Reprovado: ' + str(int(hm0r[1])) + '\n'
        'Nao avaliado: ' + str(int(hm0n[1])) + '\n \n'

        '-- Tp --' '\n'
        'Aprovado: ' + str(int(tpa[1])) + '\n'
        'Faltando: ' + str(int(tpf[1])) + '\n'
        'Suspeito: ' + str(int(tps[1])) + '\n'
        'Reprovado: ' + str(int(tpr[1])) + '\n'
        'Nao avaliado: ' + str(int(tpn[1])) + '\n \n'

        '-- Dp --' '\n'
        'Aprovado: ' + str(int(dpa[1])) + '\n'
        'Faltando: ' + str(int(dpf[1])) + '\n'
        'Suspeito: ' + str(int(dps[1])) + '\n'
        'Reprovado: ' + str(int(dpr[1])) + '\n'
        'Nao avaliado: ' + str(int(dpn[1])) + '\n \n'

        '-- Sigma1p --' '\n'
        'Aprovado: ' + str(int(sigma1pa[1])) + '\n'
        'Faltando: ' + str(int(sigma1pf[1])) + '\n'
        'Suspeito: ' + str(int(sigma1ps[1])) + '\n'
        'Reprovado: ' + str(int(sigma1pr[1])) + '\n'
        'Nao avaliado: ' + str(int(sigma1pn[1])) + '\n \n'

        '-- Sigma2p --' '\n'
        'Aprovado: ' + str(int(sigma2pa[1])) + '\n'
        'Faltando: ' + str(int(sigma2pf[1])) + '\n'
        'Suspeito: ' + str(int(sigma2ps[1])) + '\n'
        'Reprovado: ' + str(int(sigma2pr[1])) + '\n'
        'Nao avaliado: ' + str(int(sigma2pn[1])) + '\n \n'

        '-- Hm01 / Hm02 --' '\n'
        'Aprovado: ' + str(int(hm01a[1])) + '\n'
        'Faltando: ' + str(int(hm01f[1])) + '\n'
        'Suspeito: ' + str(int(hm01s[1])) + '\n'
        'Reprovado: ' + str(int(hm01r[1])) + '\n'
        'Nao avaliado: ' + str(int(hm01n[1])) + '\n \n'

        '-- Tp1 / Tp2 --' '\n'
        'Aprovado: ' + str(int(tp1a[1])) + '\n'
        'Faltando: ' + str(int(tp1f[1])) + '\n'
        'Suspeito: ' + str(int(tp1s[1])) + '\n'
        'Reprovado: ' + str(int(tp1r[1])) + '\n'
        'Nao avaliado: ' + str(int(tp1n[1])) + '\n \n'

        '-- Dp1 / Dp2 --' '\n'
        'Aprovado: ' + str(int(dp1a[1])) + '\n'
        'Faltando: ' + str(int(dp1f[1])) + '\n'
        'Suspeito: ' + str(int(dp1s[1])) + '\n'
        'Reprovado: ' + str(int(dp1r[1])) + '\n'
        'Nao avaliado: ' + str(int(dp1n[1])) + '\n \n'


        # '-- Hm02 --' '\n'
        # 'Aprovado: ' + str(int(hm02a[1])) + '\n'
        # 'Faltando: ' + str(int(hm02f[1])) + '\n'
        # 'Suspeito: ' + str(int(hm02s[1])) + '\n'
        # 'Reprovado: ' + str(int(hm02r[1])) + '\n'
        # 'Nao avaliado: ' + str(int(hm02n[1])) + '\n \n'

        # '-- Tp2 --' '\n'
        # 'Aprovado: ' + str(int(tp2a[1])) + '\n'
        # 'Faltando: ' + str(int(tp2f[1])) + '\n'
        # 'Suspeito: ' + str(int(tp2s[1])) + '\n'
        # 'Reprovado: ' + str(int(tp2r[1])) + '\n'
        # 'Nao avaliado: ' + str(int(tp2n[1])) + '\n \n'

        # '-- Dp2 --' '\n'
        # 'Aprovado: ' + str(int(dp2a[1])) + '\n'
        # 'Faltando: ' + str(int(dp2f[1])) + '\n'
        # 'Suspeito: ' + str(int(dp2s[1])) + '\n'
        # 'Reprovado: ' + str(int(dp2r[1])) + '\n'
        # 'Nao avaliado: ' + str(int(dp2n[1])) + '\n \n'


        # ================================================================================== #

        '\n' + regua1 + '\n'
        '** Teste 3 - Conec. Iguais **' '\n \n'


        '-- Hs --' '\n'
        'Aprovado: ' + str(int(hsa[2])) + '\n'
        'Faltando: ' + str(int(hsf[2])) + '\n'
        'Suspeito: ' + str(int(hss[2])) + '\n'
        'Reprovado: ' + str(int(hsr[2])) + '\n'
        'Nao avaliado: ' + str(int(hsn[2])) + '\n \n'

        '-- H1/10 --' '\n'
        'Aprovado: ' + str(int(h10a[2])) + '\n'
        'Faltando: ' + str(int(h10f[2])) + '\n'
        'Suspeito: ' + str(int(h10s[2])) + '\n'
        'Reprovado: ' + str(int(h10r[2])) + '\n'
        'Nao avaliado: ' + str(int(h10n[2])) + '\n \n'

        '-- Hmax --' '\n'
        'Aprovado: ' + str(int(hmaxa[2])) + '\n'
        'Faltando: ' + str(int(hmaxf[2])) + '\n'
        'Suspeito: ' + str(int(hmaxs[2])) + '\n'
        'Reprovado: ' + str(int(hmaxr[2])) + '\n'
        'Nao avaliado: ' + str(int(hmaxn[2])) + '\n \n'

        '-- Tmed --' '\n'
        'Aprovado: ' + str(int(tmeda[2])) + '\n'
        'Faltando: ' + str(int(tmedf[2])) + '\n'
        'Suspeito: ' + str(int(tmeds[2])) + '\n'
        'Reprovado: ' + str(int(tmedr[2])) + '\n'
        'Nao avaliado: ' + str(int(tmedn[2])) + '\n \n'

        '-- THmax --' '\n'
        'Aprovado: ' + str(int(thmaxa[2])) + '\n'
        'Faltando: ' + str(int(thmaxf[2])) + '\n'
        'Suspeito: ' + str(int(thmaxs[2])) + '\n'
        'Reprovado: ' + str(int(thmaxr[2])) + '\n'
        'Nao avaliado: ' + str(int(thmaxn[2])) + '\n \n'

        '-- Hm0 --' '\n'
        'Aprovado: ' + str(int(hm0a[2])) + '\n'
        'Faltando: ' + str(int(hm0f[2])) + '\n'
        'Suspeito: ' + str(int(hm0s[2])) + '\n'
        'Reprovado: ' + str(int(hm0r[2])) + '\n'
        'Nao avaliado: ' + str(int(hm0n[2])) + '\n \n'

        '-- Tp --' '\n'
        'Aprovado: ' + str(int(tpa[2])) + '\n'
        'Faltando: ' + str(int(tpf[2])) + '\n'
        'Suspeito: ' + str(int(tps[2])) + '\n'
        'Reprovado: ' + str(int(tpr[2])) + '\n'
        'Nao avaliado: ' + str(int(tpn[2])) + '\n \n'

        '-- Dp --' '\n'
        'Aprovado: ' + str(int(dpa[2])) + '\n'
        'Faltando: ' + str(int(dpf[2])) + '\n'
        'Suspeito: ' + str(int(dps[2])) + '\n'
        'Reprovado: ' + str(int(dpr[2])) + '\n'
        'Nao avaliado: ' + str(int(dpn[2])) + '\n \n'

        '-- Sigma1p --' '\n'
        'Aprovado: ' + str(int(sigma1pa[2])) + '\n'
        'Faltando: ' + str(int(sigma1pf[2])) + '\n'
        'Suspeito: ' + str(int(sigma1ps[2])) + '\n'
        'Reprovado: ' + str(int(sigma1pr[2])) + '\n'
        'Nao avaliado: ' + str(int(sigma1pn[2])) + '\n \n'

        '-- Sigma2p --' '\n'
        'Aprovado: ' + str(int(sigma2pa[2])) + '\n'
        'Faltando: ' + str(int(sigma2pf[2])) + '\n'
        'Suspeito: ' + str(int(sigma2ps[2])) + '\n'
        'Reprovado: ' + str(int(sigma2pr[2])) + '\n'
        'Nao avaliado: ' + str(int(sigma2pn[2])) + '\n \n'

        '-- Hm01 / Hm02--' '\n'
        'Aprovado: ' + str(int(hm01a[2])) + '\n'
        'Faltando: ' + str(int(hm01f[2])) + '\n'
        'Suspeito: ' + str(int(hm01s[2])) + '\n'
        'Reprovado: ' + str(int(hm01r[2])) + '\n'
        'Nao avaliado: ' + str(int(hm01n[2])) + '\n \n'

        '-- Tp1 / Tp2 --' '\n'
        'Aprovado: ' + str(int(tp1a[2])) + '\n'
        'Faltando: ' + str(int(tp1f[2])) + '\n'
        'Suspeito: ' + str(int(tp1s[2])) + '\n'
        'Reprovado: ' + str(int(tp1r[2])) + '\n'
        'Nao avaliado: ' + str(int(tp1n[2])) + '\n \n'

        '-- Dp1 / Dp1 --' '\n'
        'Aprovado: ' + str(int(dp1a[2])) + '\n'
        'Faltando: ' + str(int(dp1f[2])) + '\n'
        'Suspeito: ' + str(int(dp1s[2])) + '\n'
        'Reprovado: ' + str(int(dp1r[2])) + '\n'
        'Nao avaliado: ' + str(int(dp1n[2])) + '\n \n'

        # '-- Hm02 --' '\n'
        # 'Aprovado: ' + str(int(hm02a[2])) + '\n'
        # 'Faltando: ' + str(int(hm02f[2])) + '\n'
        # 'Suspeito: ' + str(int(hm02s[2])) + '\n'
        # 'Reprovado: ' + str(int(hm02r[2])) + '\n'
        # 'Nao avaliado: ' + str(int(hm02n[2])) + '\n \n'

        # '-- Tp2 --' '\n'
        # 'Aprovado: ' + str(int(tp2a[2])) + '\n'
        # 'Faltando: ' + str(int(tp2f[2])) + '\n'
        # 'Suspeito: ' + str(int(tp2s[2])) + '\n'
        # 'Reprovado: ' + str(int(tp2r[2])) + '\n'
        # 'Nao avaliado: ' + str(int(tp2n[2])) + '\n \n'

        # '-- Dp2 --' '\n'
        # 'Aprovado: ' + str(int(dp2a[2])) + '\n'
        # 'Faltando: ' + str(int(dp2f[2])) + '\n'
        # 'Suspeito: ' + str(int(dp2s[2])) + '\n'
        # 'Reprovado: ' + str(int(dp2r[2])) + '\n'
        # 'Nao avaliado: ' + str(int(dp2n[2])) + '\n \n'


        # ================================================================================== #

    )
    f.close()

    # flag com resltado da quantidade de flags (9x9 -- linha=variaveis (ex:l1 = etaa, l2=etas ..) x coluna=testes (ex:c1=t2, c2=t2 ..))
    fflagb = np.concatenate([(etaa, etas, etar, etaxa, etaxs, etaxr, etaya, etays, etayr)])
    fflagp = np.concatenate([(fhs,fh10,fhmax,ftmed,fthmax,fhm0,ftp,fdp,fsigma1p,fsigma2p,fhm01,ftp1,fdp1,fhm02,ftp2,fdp2)])

    return fflagb, fflagp