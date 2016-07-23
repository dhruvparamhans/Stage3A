import numpy as np 
from scipy import linalg, special 


class Loop:
	radius = 0.1
	position = [0,0,0]
	direction = [0,0,1]

	def __init__(self, name):

		self.name = name

	def base_vectors(self):
		n = self.direction/(np.asarray(self.direction)**2).sum(axis=-1)

		if np.abs(n[0]) == 1:
			l = np.r_[n[2],0,-n[0]]
		else:
			l = np.r_[0,n[2], -n[1]]

		l /= (l**2).sum(axis=-1)
		m = np.cross(n,l)
		return n,l,m

	def mk_B_field(self, nb_turns=1, I=1, mu=4*np.pi*1e-7):
		"""
		returns the magnetic field for the current loop calculated 
		from eqns (1) and (2) in Phys Rev A Vol. 35, N 4, pp. 1535-1546; 1987. 

		return: 
			B is a vector for the B field at point r in inverse units of 
		(mu I) / (2 pi d) 
		for I in amps and d in meters and mu = 4 pi * 10^-7 we get Tesla 
		"""
		### Translate the coordinates in the coil's frame
		n, l, m = self.base_vectors()
		R       = self.radius
		r0      = self.position
		r       = np.c_[np.ravel(self.app.X), np.ravel(self.app.Y),
												np.ravel(self.app.Z)]

		# transformation matrix coil frame to lab frame
		trans = np.vstack((l, m, n))

		r -= r0	  #point location from center of coil
		r = np.dot(r, linalg.inv(trans) ) 	    #transform vector to coil frame 

		#### calculate field

		# express the coordinates in polar form
		x = r[:, 0]
		y = r[:, 1]
		z = r[:, 2]
		rho = np.sqrt(x**2 + y**2)
		theta = np.arctan(x/y)

		E = special.ellipe((4 * R * rho)/( (R + rho)**2 + z**2))
		K = special.ellipk((4 * R * rho)/( (R + rho)**2 + z**2))
		Bz =  1/np.sqrt((R + rho)**2 + z**2) * ( 
					K 
				  + E * (R**2 - rho**2 - z**2)/((R - rho)**2 + z**2) 
				)
		Brho = z/(rho*np.sqrt((R + rho)**2 + z**2)) * ( 
				-K 
				+ E * (R**2 + rho**2 + z**2)/((R - rho)**2 + z**2) 
				)
		# On the axis of the coil we get a divided by zero here. This returns a
		# NaN, where the field is actually zero :
		Brho[np.isnan(Brho)] = 0

		B = np.c_[np.cos(theta)*Brho, np.sin(theta)*Brho, Bz ]

		# Rotate the field back in the lab's frame
		B = np.dot(B, trans)

		Bx, By, Bz = B.T
		Bx = np.reshape(Bx, self.app.X.shape)
		By = np.reshape(By, self.app.X.shape)
		Bz = np.reshape(Bz, self.app.X.shape)

		Bnorm = np.sqrt(Bx**2 + By**2 + Bz**2)

		# We need to threshold ourselves, rather than with VTK, to be able 
		# to use an ImageData
		Bmax = 10 * np.median(Bnorm)

		Bx[Bnorm > Bmax] = np.NAN 
		By[Bnorm > Bmax] = np.NAN
		Bz[Bnorm > Bmax] = np.NAN
		Bnorm[Bnorm > Bmax] = np.NAN

		prefactor = mu*I*nb_turns/(2*np.pi)
		self.Bx = prefactor*Bx
		self.By = prefactor*By
		self.Bz = prefactor*Bz
		self.Bnorm = Bnorm

test = Loop(1)

print test.base_vectors()
test.mk_B_field()

print test.Bx.shape


