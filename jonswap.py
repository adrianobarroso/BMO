'''
Espectro de JONSWAP

- Calculo do GAMMA
- Ajusta o Espectro
'''

import numpy as np
from numpy import (inf, atleast_1d, newaxis, any, minimum, maximum, array, #@UnresolvedImport
    asarray, exp, log, sqrt, where, pi, arange, linspace, sin, cos, abs, sinh, #@UnresolvedImport
    isfinite, mod, expm1, tanh, cosh, finfo, ones, ones_like, isnan, #@UnresolvedImport
    zeros_like, flatnonzero, sinc, hstack, vstack, real, flipud, clip) #@UnresolvedImport


def jonswap_peakfact(Hm0, Tp):
    ''' Jonswap peakedness factor, gamma, given Hm0 and Tp

    Parameters
    ----------
    Hm0 : significant wave height [m].
    Tp  : peak period [s]

    Returns
    -------
    gamma : Peakedness parameter of the JONSWAP spectrum

    Details
    -------
    A standard value for GAMMA is 3.3. However, a more correct approach is
    to relate GAMMA to Hm0 and Tp:
         D = 0.036-0.0056*Tp/sqrt(Hm0)
        gamma = exp(3.484*(1-0.1975*D*Tp**4/(Hm0**2)))
    This parameterization is based on qualitative considerations of deep water
    wave data from the North Sea, see Torsethaugen et. al. (1984)
    Here GAMMA is limited to 1..7.

    NOTE: The size of GAMMA is the common shape of Hm0 and Tp.

    Examples
    --------
    import pylab as plb
    Tp,Hs = plb.meshgrid(range(4,8),range(2,6))
    gam = jonswap_peakfact(Hs,Tp)

    Hm0 = plb.linspace(1,20)
    Tp = Hm0
    [T,H] = plb.meshgrid(Tp,Hm0)
    gam = jonswap_peakfact(H,T)
    v = plb.arange(0,8)
    h = plb.contourf(Tp,Hm0,gam,v);h=plb.colorbar()

    Hm0 = plb.arange(1,11)
    Tp  = plb.linspace(2,16)
    T,H = plb.meshgrid(Tp,Hm0)
    gam = jonswap_peakfact(H,T)
    h = plb.plot(Tp,gam.T)
    h = plb.xlabel('Tp [s]')
    h = plb.ylabel('Peakedness parameter')

    >>> plb.close('all')

    See also
    --------
    jonswap
    '''
    Hm0, Tp = atleast_1d(Hm0, Tp)

    x = Tp / sqrt(Hm0)

    gam = ones_like(x)

    k1 = flatnonzero(x <= 5.14285714285714)
    if k1.size > 0: # #limiting gamma to [1 7]
        xk = x.take(k1)
        D = 0.036 - 0.0056 * xk # # approx 5.061*Hm0**2/Tp**4*(1-0.287*log(gam))
        gam.put(k1, minimum(exp(3.484 * (1.0 - 0.1975 * D * xk ** 4.0)), 7.0)) # # gamma

    return gam

def gamma(tp):
	'''
	calculo do parametro gamma
	TEO/CENPES
	'''

	gam = 6.4 * ( tp ** (-0.491) )

	return gam

def spec(hs,tp,f,gam):
	'''
	ajuste do espectro de JONSWAP
	'''

	#frequencia de pico
	fp = 1./tp

	s_js = np.zeros(len(f))

	for i in range(len(f)):

		if f[i] <= fp:

			sigm = 0.07

			s_js[i] = (5./16) * (hs**2) * tp * (fp/f[i])**5 * (1-0.287*np.log(gam)) * np.exp(-1.25*(f[i]/fp)**(-4)) * gam ** ( np.exp(-(f[i]-fp)**2/(2*sigm**2*fp**2)) )

		elif f[i] > fp:

			sigm = 0.09


			s_js[i] = (5./16) * (hs**2) * tp * (fp/f[i])**5 * (1-0.287*np.log(gam)) * np.exp(-1.25*(f[i]/fp)**(-4)) * gam ** ( np.exp(-(f[i]-fp)**2/(2*sigm**2*fp**2)) )

	return s_js
