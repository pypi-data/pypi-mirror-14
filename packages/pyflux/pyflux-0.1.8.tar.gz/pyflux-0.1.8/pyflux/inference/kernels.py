import numpy as np

class SquaredExponential(object):

	def __init__(self, X, l, tau):

		self.X = X
		self.l = l
		self.tau = tau

	def K(self):
		K = np.zeros((X.shape[0],X.shape[0]))

		for i in xrange(0,self.X.shape[0]):
			for j in xrange(0,self.X.shape[0]):
				K[i,j] = self.tau*np.exp((X.transpose()[i] - X.transpose()[j])/self.l**2)

		return K