#!/usr/bin/env python
''' Analyticall solution for 1D Riemann problem'''

__AUTHOR__ = 'Long-Gang Pang'
__EMAIL__ = 'lgpang@qq.com'

import numpy as np
import math
import _riemann

class Riemann(object):
    def __init__(self, z, pressure_left=5):
        '''Params:
            :param z: numpy array for z coordinates
            :param pressure_left: pressure in the z<0 region
            pressure_right: always equals to 0
           Example:
            z = np.linspace(-10, 10, 101)
            sol = Riemann(z)
            print(sol.energy_density(t=0.1))
        '''
        self.pressure_left = pressure_left
        self.pressure_right = 0.0
        self.z = z
        self.cs2 = 1.0/3.0
        self.cs = math.sqrt(self.cs2)
        self.ed0 = self.pressure_left/self.cs2

    def pressure(self, t):
        '''Params:
            :param t: time for the solution
        Return: Eq. (53) of http://arxiv.org/pdf/nucl-th/9504018.pdf
            pressure array with the shape of self.z
        '''
        pre = np.zeros_like(self.z)
        for i, zi in enumerate(self.z):
            pre[i] = _riemann.lib.pressure(t, zi, self.pressure_left,
                                      self.pressure_right)
        return pre

    def energy_density(self, t):
        '''Return: Eq. (53) of http://arxiv.org/pdf/nucl-th/9504018.pdf
           energy density array with the shape of self.z'''
        return self.pressure(t)/self.cs2
            
    def fluid_velocity(self, t):
        '''Return: Eq. (51) of http://arxiv.org/pdf/nucl-th/9504018.pdf
            fluid velocity array with the shape of self.z'''
        ed = self.energy_density(t)
        cs, cs2 = self.cs, self.cs2
        tmp = np.power(ed/self.ed0, 2*cs/(1+cs2))
        return (1 - tmp)/(1 + tmp)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    z = np.linspace(-10, 10, 401)
    sol = Riemann(z, pressure_left=1.0)
    for t in range(10):
        pr = sol.pressure(t)
        vl = sol.fluid_velocity(t)
        label1, label2 = None, None
        if t == 0:
            label1 = r'$pressure$'
            label2 = r'$fluid\ velocity$'

        plt.plot(z, pr, 'r-', label=label1)
        plt.plot(z, vl, 'b--', label=label2)
    plt.ylim(-0.5, 1.5)
    plt.xlabel(r'$z\ [fm]$')
    plt.ylabel(r'$pr\ and\ vz$')
    plt.legend(loc='best')
    plt.show()
