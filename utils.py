from scipy.special import erfc, wofz
from scipy.optimize import fmin, leastsq
from datetime import datetime
import numpy as np

## Constants
logfile = 'fit_log.out'
## Wavelength
Lambda = 780.241e-9
## Wavevector
k = 2*np.pi/(Lambda)
## Electric charge
e = 1.602e-19
## Bohr Radius
a_0 = 0.529e-10
## Dipole strength for D2 transition
d = 5.177*e*a_0
## Degeneracy Rb-85
deg_85 = 12.
## Degeneracy Rb-87
deg_87 = 8.
## Reduced Planck's constant
h_bar = 1.504e-34
##Permittivity
epsilon_0 = 8.854e-12
## Boltzmann constant
k_B = 1.380e-23
## Mass
m = 1.409e-25
## Natural Linewidth
Gamma = 2*np.pi*6.066e-3
## Self Broadening
self_broad = 2*np.pi*1.10e-13

## line strengths
cf_1 = 1./18 + 5./18 + 7./9
cf_2 = 1./3 + 35./81 + 28./81
cf_3 = 10./81+ 35./81 + 1.
cf_4 = 1./9 + 5./18 + 5./18

line_strengths = [cf_1, cf_2, cf_3, cf_4]
degs = [deg_87, deg_85, deg_85, deg_87]


def normalize(data):
    data -= np.min(np.asarray(data))
    data /= np.max(np.asarray(data))
    return np.asarray(data)

def vapor_pressure(T):
    # logp = 15.88253 - (4529.635/T) + 0.00058663*T - 2.99138*(np.log10(T))
    logp = 15.88253 - (4529.635/T) + 0.00058663*T
    return logp, pow(10,logp)
def atomic_density(T,p):
    return 133.323*p/(k_B*T)

def get_data(filename):
    with open(filename, 'r') as f:
        data_list = [line.split() for line in f]
    for i in range(len(data_list)):
        temp = data_list[i]
        temp = [float(element) for element in temp]
        data_list[i] = temp
    spectra = np.asarray(data_list)
    return spectra[:,0], spectra[:,1]


def gnuplot(filename,xlabel, ylabel,title,picname):
    import subprocess
    proc = subprocess.Popen(['gnuplot','-p'],
                        shell=True,
                        stdin=subprocess.PIPE,
                        )
#     proc.stdin.write('set autorange\n')
    proc.stdin.write('set style data lines\n')
    proc.stdin.write('set xlabel "{}"\n'.format(xlabel))
    proc.stdin.write('set ylabel "{}"\n'.format(ylabel))
    proc.stdin.write('set title "{}"\n'.format(title))
    proc.stdin.write('set key right bottom\n')
    proc.stdin.write('set term png\n')
    proc.stdin.write('set output "{}"\n'.format(picname))
    proc.stdin.write('plot "{}" u 1:2 t "Fit", "{}" u 1:4 t "Exp"\n'.format(filename, filename))
    proc.stdin.write('quit\n')