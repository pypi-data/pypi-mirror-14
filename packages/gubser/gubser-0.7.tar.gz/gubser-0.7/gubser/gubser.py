#!/usr/bin/env python

__AUTHOR__ = 'Long-Gang Pang'
__EMAIL__ = 'lgpang@qq.com'

import _gubser
import numpy as np

class Gubser():
    def __init__(self, L=5.0, tau=1.0, lam1=-10.0, etaos=0.08,
            x=(-10.0, 10.0, 101), y=(-10.0, 10.0, 101)):
        '''gubser solution for 2nd order viscous hydro
        Params:
            :param L: typical size of the system, radius of ds3 space
            :param tau: proper time
            :param lam1: lam1 = \\hat{\\varepsilon}/\\hat{\\pi^{\\mu\\nu}}
            :param etaos: shear viscosity over entropy density
            :param x: (xlow, xhigh, num_of_x)
            :param y: (ylow, yhigh, num_of_y)
        Example:
            example 1, save the gubser solution with default arguments:
                gu = Gubser()
                gu.save_data()

            example 2, get the energy density of  gubser solution
                     with default arguments:

                gu = Gubser(L=1.0, tau=1.0, lam1=-10, etaos=0.08,
                            x=(-10, 10, 400), y=(-10, 10, 400))

                ed = gu.energy_density()
               '''
        self.L = L
        self.tau = tau
        self.lam1 = lam1
        self.etaos = etaos
        self.set_range(x0=x[0], x1=x[1], nx=x[2], y0=y[0], y1=y[1], ny=y[2])

    def set_tau(self, tau):
        '''Set proper time to get the solution at time tau'''
        self.tau = tau

    def set_range(self, x0=-10, x1=10, nx=101, y0=0.0, y1=0.0, ny=1):
        ''' set lattice for gubser solution output
            Params:
                :param x0, x1, nx: lower bound, upper bound, num of x points
                :param y0, y1, ny: lower bound, upper bound, num of y points
                '''
        self.nx, self.ny = nx, ny
        self.x = np.linspace(x0, x1, nx, endpoint=True)
        self.y = np.linspace(y0, y1, ny, endpoint=True)

    def velocity(self, along='x'):
        '''fluid velocity on the lattice in gubser solution '''
        result = np.zeros((self.nx, self.ny))
        func = None
        if along == 'x': func = _gubser.lib.ux
        if along == 'y': func = _gubser.lib.uy
        if along == 'eta': return result

        for i, x in enumerate(self.x):
            for j, y in enumerate(self.y):
                utau = _gubser.lib.ut(x, y, self.tau, self.L)
                result[i,j] = func(x, y, self.tau, self.L)/utau
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

    def save_data(self, tau=None):
        ''' save the initial condition to harddisk for further usage
        Params:
            :param tau: the proper time'''
        if tau is not None: self.set_tau(tau)
        result = []
        x, y = np.meshgrid(self.x, self.y, indexing='ij')
        ed = self.energy_density().flatten()
        vx = self.velocity(along='x').flatten()
        vy = self.velocity(along='y').flatten()

        result.append(x.flatten())
        result.append(y.flatten())
        result.append(ed)
        result.append(vx)
        result.append(vy)
        for mu in range(4):
            for nu in range(mu, 4):
                if (mu==0 or mu==1 or mu==2) and nu==3: continue
                result.append(self.pimn(mu, nu).flatten())

        params = 'L={L}, tau={tau}, lam1={lam1}, etaos={etaos}'.format(
                L=self.L, tau=self.tau, lam1=self.lam1, etaos=self.etaos)

        fname = ('gubser_tau%s'%self.tau).replace('.', 'p') + '.dat'

        np.savetxt(fname, np.array(result).T, fmt='%.6e',
                header = 'x, y, ed, vx, vy, pi00, pi01, pi02, pi11, pi12, pi22, pi33 %s'%params)
        

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    solution = Gubser(L=1, tau=3.0, lam1=-10)
    solution.set_range(x0=-10, x1=10, nx=400, y0=-10, y1=10, ny=400)
    solution.save_data()
