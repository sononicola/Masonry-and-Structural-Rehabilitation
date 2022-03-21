from scipy.interpolate import interp2d
import numpy as np
"""
interp2d è buggato se si usano gli np.NaN, è stato usato 0 al loro posto
"""

x = [0, 0.5, 1.0, 1.5, 2.0]
y = [0., 5., 10., 15., 20.]
z = np.array([
        [1.00, 0.74, 0.59, 0.44, 0.33],
        [0.97, 0.71, 0.55, 0.39, 0.27],
        [0.86, 0.61, 0.45, 0.27, 0.16],
        [0.69, 0.48, 0.32, 0.17, 0.00],
        [0.53, 0.36, 0.23, 0.00, 0.00]
    ])
tab_4_5_iii_temp = interp2d(x, y, z, kind="linear", bounds_error=True) 
def tab_4_5_iii(m:float, lamb:float) -> float:
    return tab_4_5_iii_temp(m, lamb)[0]

x = [15, 10, 5, 2.5]
y = [2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0, 40.0]
z = np.array([
        [1.2, 1.2, 1.2, 1.2],
        [2.2, 2.2, 2.2, 2.0],
        [3.5, 3.4, 3.3, 3.0],
        [5.0, 4.5, 4.1, 3.5],
        [6.2, 5.3, 4.7, 4.1],
        [8.2, 6.7, 6.0, 5.1],
        [9.7, 8.0, 7.0, 6.1],
        [12.0, 10.0, 8.6, 7.2],
        [14.3, 12.0, 10.4, 0],

    ])
tab_11_10_vi_temp = interp2d(x, y, z, kind="linear", bounds_error=True)
def tab_11_10_vi(malta:int, f_bk:float) -> float:
    return tab_11_10_vi_temp(malta, f_bk)[0]

x = [15, 10, 5, 2.5]
y = [2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0, 40.0]
z = np.array([
        [1.0, 1.0, 1.0, 1.0],
        [2.2, 2.2, 2.2, 2.0],
        [3.5, 3.4, 3.3, 3.0],
        [5.0, 4.5, 4.1, 3.5],
        [6.2, 5.3, 4.7, 4.1],
        [8.2, 6.7, 6.0, 5.1],
        [9.7, 8.0, 7.0, 6.1],
        [12.0, 10.0, 8.6, 7.2],
        [14.3, 12.0, 10.4, 0],

    ])
tab_11_10_vii_temp = interp2d(x, y, z, kind="linear", bounds_error=True)
def tab_11_10_vii(malta:int, f_bk:float) -> float:
    return tab_11_10_vii_temp(malta, f_bk)[0]