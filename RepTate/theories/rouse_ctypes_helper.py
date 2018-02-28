"""
Define the C-variables and functions from the C-files that are needed in Python
"""
import numpy as np
from ctypes import c_double, c_int, CDLL
import sys

lib_path = 'theories/rouse_lib_%s.so' % (sys.platform)
try:
    rouse_lib = CDLL(lib_path)
except:
    print('OS %s not recognized' % (sys.platform))

continuous_rouse_freq = rouse_lib.continuous_rouse_freq
continuous_rouse_freq.restype = None

continuous_rouse_time = rouse_lib.continuous_rouse_time
continuous_rouse_time.restype = None


def approx_rouse_frequency(params):
    G0, tau0, N, w = params
    n = len(w)

    w_arr = (c_double * n)()
    gp_arr = (c_double * n)()
    gpp_arr = (c_double * n)()
    w_arr[:] = w[:]
    gp_arr[:] = np.zeros(n)[:]
    gpp_arr[:] = np.zeros(n)[:]
    continuous_rouse_freq(
        c_int(n), c_double(G0), c_double(tau0), c_int(N), w_arr, gp_arr,
        gpp_arr)
    return(np.asarray(gp_arr[:]), np.asarray(gpp_arr[:]))

def approx_rouse_time(params):
    G0, tau0, N, t = params
    n = len(t)

    t_arr = (c_double * n)()
    gt_arr = (c_double * n)()
    t_arr[:] = t[:]
    gt_arr[:] = np.zeros(n)[:]

    continuous_rouse_time(
        c_int(n), c_double(G0), c_double(tau0), c_int(N), t_arr, gt_arr)
    return(np.asarray(gt_arr[:]))