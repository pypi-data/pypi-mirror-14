#!/usr/bin/env python

__AUTHOR__ = 'Long-Gang Pang'
__EMAIL__ = 'lgpang@qq.com'

import _gubser
import numpy as np

class Gubser():
    def __init__(self, L, tau, lam1, etaos=0.08):
        '''gubser solution for 2nd order viscous hydro
        Params:
            :param L: typical size of the system, radius of ds3 space
            :param tau: proper time
            :param lam1: lam1 = \hat{\varepsilon}/\hat{\pi^{\mu\nu}}
            :param etaos: shear viscosity over entropy density'''
        self.L = L
        self.tau = tau
        self.lam1 = lam1
        self.etaos = etaos

    def set_range(self, x0, x1, nx, y0=0.0, y1=0.0, ny=1):
        ''' set lattice for gubser solution output
            Params:
                :param x0, x1, nx: lower bound, upper bound, num of x points
                :param y0, y1, ny: lower bound, upper bound, num of y points
                '''
        self.nx, self.ny = nx, ny
        self.x = np.linspace(x0, x1, nx)
        self.y = np.linspace(y0, y1, ny)

    def velocity(self, along='x'):
        '''fluid velocity on the lattice in gubser solution '''
        result = np.zeros((self.nx, self.ny))
        func = None
        if along == 'x': func = _gubser.lib.vx
        if along == 'y': func = _gubser.lib.vy
        if along == 'eta': return result

        for i, x in enumerate(self.x):
            for j, y in enumerate(self.y):
                result[i,j] = func(x, y, self.tau, self.L, self.lam1)
        return result 


    def energy_density(self):
        '''energy density on the lattice in gubser solution '''
        ed = np.empty((self.nx, self.ny))
        func = _gubser.lib.eps
        for i, x in enumerate(self.x):
            for j, y in enumerate(self.y):
                ed[i,j] = func(x, y, self.tau, self.L, self.lam1)
        return ed

    def pimn(self, mu=0, nu=0):
        '''pimn on the lattice in gubser solution '''
        results = np.zeros((self.nx, self.ny))
        func = None
        if mu == 0 and nu == 0: func = _gubser.lib.pitt
        if mu == 0 and nu == 1: func = _gubser.lib.pitx
        if mu == 0 and nu == 2: func = _gubser.lib.pity
        if mu == 1 and nu == 1: func = _gubser.lib.pixx
        if mu == 1 and nu == 2: func = _gubser.lib.pixy
        if mu == 2 and nu == 2: func = _gubser.lib.piyy
        if mu == 3 and nu == 3: func = _gubser.lib.pizz

        # pi^{tau eta}, pi^{x eta}, pi^{y eta} = 0.0
        if mu == 0 and nu == 3: return results
        if mu == 1 and nu == 3: return results
        if mu == 2 and nu == 3: return results

        for i, x in enumerate(self.x):
            for j, y in enumerate(self.y):
                results[i,j] = func(x, y, self.tau, self.L, self.lam1)
        return results



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    solution = Gubser(L=1, tau=3.0, lam1=-10)
    solution.set_range(x0=-10, x1=10, nx=400, y0=-10, y1=10, ny=400)
    
    pixx = solution.pimn(1, 1)
    
    plt.imshow(pixx.T)
    
    plt.show()
