import numpy as np, time, os, pdb
import math, sys, cPickle, re 
import numpy.random as random

b_ = dict(g=0.9e-10, r=1.2e-10) #band softening parameter
f0 = 3631.0 #Jy

@np.vectorize
def convert_to_flux(mag, band = 'g'): #Converts a Luptitude to an SDSS flux

	return math.sinh(math.log(10.0)/-2.5*mag-math.log(b_[band]))*2*b_[band]*f0

@np.vectorize
def convert_errors(err, flux, band = 'g'): #Converts a Luptitude error to SDSS flux error

	return err*math.log(10)/2.5*2*b_[band]*math.sqrt(1+(flux/(2*b_[band]*f0))**2)*f0 

def getCarmaModel(time, flux, flux_err, p = 2, q = 1, pmax = None):

	model = cmcmc.CarmaModel(time, flux, flux_err, p=2, q=1)
	if pmax is not None: MLE, pqlist, AICc_list = model.choose_order(pmax)
	sample = model.run_mcmc(50000)
	return sample

def convert_time(time, z): #Converts a cadence to the rest frame

	t = np.empty((len(time),), dtype = 'f4')
	t[0] = 0
	for i in xrange(1,len(time)):t[i] = (time[i] - time[i-1])/(1+z) + t[i-1]

	return t

def get_psd(f, sigma, ar_coefs, ma_coefs, percentile):
	numSamples = ma_coefs.shape[0]

	lower = (100.0 - percentile)/2.0
	upper = (100.0 - lower)

	psd = np.empty((numSamples, f.shape[0]))
	K = m.pi*2*frequencies*1j
	for i in xrange(nfreq):
		ma = (ma_coefs[:,1]*K[i]+ma_coefs[:,0])
		ar = (K[i]**2+ar_coefs[:,1]*K[i] + ar_coefs[:,2])
		ma = abs(ma)**2
		ar = abs(ar)**2
		psd[:,i] = (sigma[:,0]**2)*ma/ar
	psd_mid = np.median(psd,axis=0)
	psd_high = np.percentile(psd,upper,axis=0)
	psd_low = np.percentile(psd,lower,axis=0)
	return (psd_low,psd_high,psd_mid,f)

def get_greens_func(time, ar_roots, percentile):

	g_func = np.empty((time.shape[0], ar_roots.shape[0]), dtype = np.complex64)	
	lower = (100.0 - percentile)/2.0
	upper = (100.0 - lower)
	t = time.reshape(1,time.shape[0]).T
	g_func[:] = (np.exp(ar_roots[:,0]*t) - np.exp(ar_roots[:,1]*t))/(ar_roots[:,0] - ar_roots[:,1])

	gfunc_mid = np.median(g_func[:].real, axis = 1)
	gfunc_high = np.percentile(g_func[:].real, upper, axis = 1)
	gfunc_low = np.percentile(g_func[:].real, lower, axis = 1)

	return gfunc_low, gfunc_high, gfunc_mid, time

