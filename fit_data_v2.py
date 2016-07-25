from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
from utils import *
from fit_data import single_profile, multiple_profile
import numpy as np

# The parameters of the fit are Temperature, Frequency centers and densities.

detunings, transmission = get_data('data/p1.9mw_det.gpt')
transmission -= np.min(transmission)
transmission /= np.max(transmission)
# detunings = np.asarray(detunings)/1e3
T = 155.5+273.15
freq_centers = [-0.819325124033,-0.130162753488, 3.39728856186, 6.576]
line_strengths = [cf_1, cf_2, cf_3, cf_4]
degs = [deg_87, deg_85, deg_85, deg_87]

# x,y = multiple_profile(T, freq_centers, np.asarray(detunings)/1e3)

# import matplotlib.pyplot as plt
# print len(detunings)
# print len(x)
# plt.plot(detunings, x)
# # plt.plot(detunings, transmission, 'r')
# plt.show()

def residue(params, x, data):
	temperature = params['T']
	centers = [params['f1'], params['f2'], params['f3'], params['f4']]
	model, _ = multiple_profile(temperature, centers, np.asarray(x)/1e3)

	return model - data


## Test

params = Parameters()
params.add('T', value = 384.252, vary = True)
params.add('f1', value = freq_centers[0], vary=True)
params.add('f2', value = freq_centers[1], vary=True)
params.add('diff1', value = 3.035, vary = False)
params.add('diff2', value = 6.834, vary = False)
params.add('f3', value = freq_centers[2], vary=True)
params.add('f4', value = freq_centers[3], vary=True)

print detunings

minner = Minimizer(residue, params, fcn_args=(np.asarray(detunings)/1e3, transmission))

kws = {'options': {'maxiter':10}}
result = minner.minimize()

final = transmission+result.residual

report_fit(result)

try:
	import pylab
	pylab.plot(detunings, transmission, 'k+')
	pylab.plot(detunings, final, 'r')
	pylab.show()
except:
	pass
