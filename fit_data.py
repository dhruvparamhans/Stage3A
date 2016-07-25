from clean_data import *
from scipy.special import erfc, wofz
from scipy.optimize import fmin, leastsq
from datetime import datetime
from utils import *


def single_profile(T, freq_center, line_strength, deg, freqs, L = 15e-2):
	profile = []
	temp = []
	u = np.sqrt(2*k_B*T/m)
	ku = k*u
	ku /= 1e9
	pre_factor = np.sqrt(np.pi/4)*d**2/(h_bar*epsilon_0*u*deg)
	N = atomic_density(T,vapor_pressure(T)[1])
	for freq in freqs:
		det = 2*np.pi*freq/ku
		a = Gamma/ku
		s_y = (wofz(1j*a+(det-(2*np.pi*freq_center/ku)))+wofz(1j*a-(det-(2*np.pi*freq_center/ku)))).real*pre_factor*N/2
		alpha = s_y*line_strength
		profile.append(np.exp(-alpha*L))
		temp.append(alpha)
	return np.asarray(profile), np.asarray(temp)

def multiple_profile(T,freq_centers, freqs, line_strengths=line_strengths, degs=degs,  L=15e-2, nb_profiles=4):
	profiles = []
	alphas = []
	weights = [0.28, 0.72, 0.72, 0.28]
	for i in range(nb_profiles):
		temp_profile, temp_alpha = single_profile(T,freq_centers[i], line_strengths[i], degs[i],freqs)
		profiles.append(weights[i]*temp_profile)
		alphas.append(weights[i]*temp_alpha)
	profiles = np.asarray(profiles)
	alphas = np.asarray(alphas)
	alpha_sum = np.sum(alphas, axis = 0)
	return np.exp(-alpha_sum*L), alpha_sum

def residual(x, *args):
	"""
	Computes the residual between the voigt profile
	and the raw spectrum data. This function is then passed
	for optimization of the Nelder-Mead algorithm used below.

	The arguments are the raw spectrum data and other parameters
	which would not be optimized (typically the temperature)

	x contains the parameters which we want to fit for. They should be provided
	in the order

	N1 = density for the transition1 Rb87 F=2 -> F=1,2,3
	N2 = density for transition 2 Rb85 F=3 -> F=2,3,4
	N3 = density for transition 3 Rb85 F=2 -> F=1,2,3
	N4 = density for transition 4 Rb87 F=1 -> F=0,1,2

	freq1 = frequency of transition 1
	freq2 = frequency of transition 2
	freq3 = frequency of transition 3
	freq4 = frequency of transition 4

	"""

	spectrum_exp = normalize(args[0])
	T = x[0]
	densities = args[1]
	# freq_centers = args[2]
	freq_centers = x[1:] #Use freq centers as a parameter of fit
	line_strengths = args[2]
	degs = args[3]
	freqs = args[4]
	y_predicted = multiple_profile(T,4,densities,freq_centers,line_strengths, degs, freqs)[0]
	y_experimental = np.asarray(spectrum_exp)
	return np.sum((y_predicted-y_experimental)**2)
	# return y_experimental - y_predicted

def fit(filename,x0, *args):
	"""
	Fits the experimental data to the voigt profile defined in multiple profile
	using the Nelder-Mead algorithm.
	The profile computed using the fitted parameters is written to the file filename.
	The parameters of the fit are logged to the file fit_log.out
	"""
	result,fopt,iter,funcalls, warnflag= fmin(residual, x0, args,full_output=True, disp=False, maxiter=100, maxfun = 200)
	T = result[0]
	freq_centers = result[1:]

	# result, conv = leastsq(residual,x0, args)
	print "Temperature: {}".format(T)
	print "Frequency centers {}".format(freq_centers)
	# print "Densities : {}".format(result[:4])
	# print "Frequency centers : {}".format(result[4:])
	# print "Final Residue : {}".format(fopt)
	# print "Number of Iterations : {} ".format(iter)
	# print "Function Calls : {}".format(funcalls)
	densities = args[1]
	# freq_centers = args[2]
	line_strengths = args[2]
	degs = args[3]
	freqs = args[4]
	# if args[5] != None:
	# 	extra_params = args[5]

	y_experimental = np.asarray(args[0])

	profile_fit, alpha_fit = multiple_profile(result[0],4,densities, freq_centers, line_strengths, degs, freqs)
	final_residue = np.sum((y_experimental - profile_fit)**2)
	write2file(filename, np.asarray(freqs), profile_fit, alpha_fit, y_experimental)

	print "Final_residue : {}".format(final_residue)
	# logfile = DATA_PATH+'/Test/fit_log.out'
	with open(logfile, 'a') as f:
		f.write("Time: {}\n".format(str(datetime.now())))
		# f.write("Initial Densities: {}\n".format(x0[:4]))
		# f.write("Initial Frequency: {}\n".format(x0[4:]))
		# f.write("Extra Parameters: {}\n".format(extra_params))
		f.write("Parameters for fit \n")
		f.write("T: {}\t".format(result))
		f.write("Line strengths :{}\n".format(line_strengths))
		# f.write("Function iterations: {}\n".format(iter))
		f.write("Final residue: {}\n".format(final_residue))
		# f.write("N1: {}\t N2: {}\t N3: {}\t N4: {}\n".format(result[0], result[1], result[2], result[3]))
		f.write("freq1: {}\t freq2: {}\t freq3: {}\t freq4: {}\n".format(result[1], result[2], result[3], result[4]))
		f.write("\n\n\n\n")
	print "Fit parameters logged to: {}\n".format(logfile)
	return result,final_residue
