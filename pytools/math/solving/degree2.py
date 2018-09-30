# -*- coding: utf-8 -*-
"""
Created on Sat May 19 11:52:26 2018

@author: Eric
"""
import numpy as np

def solve(a, b, c, precision=1e-7):
    """
    Solve the equation : a.x^2 + b.x + c = 0 with real coeficients
    <a>, <b>, <c> are coeficients of the equation
    <precision> define the zero-level
    
    Return the list of roots
    """
    delta = np.square(b)-4*a*c
    if delta > precision: # 2 real roots
        return [-b+np.sqrt(delta)/(2*a), -b-np.sqrt(delta)/(2*a)]
    elif np.abs(delta)<=precision:
        return [-b/(2*a)] # only one real root
    else:                 # 2 complex roots
        return [-b/(2*a)+np.sqrt(-delta)/(2*a)*1j, -b/(2*a)-np.sqrt(-delta)/(2*a)*1j]
    