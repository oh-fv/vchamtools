#!/usr/bin/env python3

# disable JIT to see the difference it makes ...
# import os
# os.environ['NUMBA_DISABLE_JIT'] = '1'

import numpy as np
from vchamtools.vcham import vcham, err_nstate, mctdh
from vchamtools.vcham.plot import plot_model
from vchamtools import sqlitedb

np.set_printoptions(threshold=np.nan, linewidth=200)

# database path
db_path = '../data.sqlite'

# point group
pg = 'c2v'

# total number of vibrational degrees of freedom
n_vibrational_modes = 30

# vertical excitation energies
E = {'a1': [0., 4.74412327642684, 6.75995802149102, 7.98600046338684],
     'a2': [6.15547861028794],
     'b1': [6.43537288149314],
     'b2': [6.11882230057693, 6.66745869109101, 7.76702176293909]}

# harmonic vibrational frequencies
w = {'a1': [276.28, 323.97], # 276.28, 323.97, 457.14, 691.44, 1067.22, 1188.17, 1347.50, 1357.08, 1555.37, 1673.97, 3257.74
     'a2': [144.23, 365.18], # 144.23, 365.18, 487.15, 572.90, 922.85
     'b1': [], # 155.89, 295.01, 606.46, 815.81
     'b2': []} # 282.30, 487.41, 609.52, 753.74, 998.96, 1262.73, 1284.14, 1555.48, 1673.21, 3244.40

# mode numbers in Mulliken notation
modes = [11, 10, 16, 15]

# set up the model
H = vcham.VCHAM(w, E, pg)
H.modes = modes

# disable some additional couplings, here goes careful consideration of the problem at hand
H.disable_coupling([[1,4], [1,7], [1,9], [2,7], [2,9], [4,7], [4,9]])
H.disable_coupling([[3,6], [3,8], [6,8], [7,9]], disable_linear=False)

# model coefficients from previous fit
H.c_kappa[0] = np.array([0.00226097, 0.00730952, 0.        , 0.        ])
H.c_kappa[1] = np.array([-0.00585934,  0.02845974,  0.        ,  0.        ])
H.c_kappa[2] = np.array([0.00526791, 0.01066038, 0.        , 0.        ])
H.c_kappa[3] = np.array([-0.03903281,  0.08634507,  0.        ,  0.        ])
H.c_kappa[4] = np.array([-0.00296215,  0.05681293,  0.        ,  0.        ])
H.c_kappa[5] = np.array([-0.00920856,  0.02148043,  0.        ,  0.        ])
H.c_kappa[6] = np.array([0.0126099 , 0.01094113, 0.        , 0.        ])
H.c_kappa[7] = np.array([0.00016505, 0.02257473, 0.        , 0.        ])
H.c_kappa[8] = np.array([-0.00581672,  0.03210484,  0.        ,  0.        ])
H.c_gamma[0] = np.array([[-0.00157829, -0.00200896,  0.        ,  0.        ],
       [ 0.        ,  0.00166973,  0.        ,  0.        ],
       [ 0.        ,  0.        ,  0.00139532,  0.00541158],
       [ 0.        ,  0.        ,  0.        ,  0.00550469]])
H.c_gamma[1] = np.array([[-0.00201454, -0.00086337,  0.        ,  0.        ],
       [ 0.        , -0.00280972,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.00955719,  0.00064187],
       [ 0.        ,  0.        ,  0.        ,  0.00121664]])
H.c_gamma[2] = np.array([[-0.00079799,  0.00093688,  0.        ,  0.        ],
       [ 0.        , -0.00114346,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.01434947,  0.0074392 ],
       [ 0.        ,  0.        ,  0.        , -0.00529021]])
H.c_gamma[3] = np.array([[-0.00592336,  0.00192414,  0.        ,  0.        ],
       [ 0.        , -0.00300896,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.00748816,  0.0046616 ],
       [ 0.        ,  0.        ,  0.        , -0.00425541]])
H.c_gamma[4] = np.array([[-0.00555582, -0.00020799,  0.        ,  0.        ],
       [ 0.        , -0.00506918,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.00515772,  0.00751671],
       [ 0.        ,  0.        ,  0.        , -0.01023613]])
H.c_gamma[5] = np.array([[-0.00136829, -0.00432615,  0.        ,  0.        ],
       [ 0.        , -0.00073048,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.00374493, -0.00360623],
       [ 0.        ,  0.        ,  0.        , -0.02086767]])
H.c_gamma[6] = np.array([[-0.00074253, -0.00101934,  0.        ,  0.        ],
       [ 0.        , -0.00319582,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.00604365,  0.0021358 ],
       [ 0.        ,  0.        ,  0.        , -0.0233736 ]])
H.c_gamma[7] = np.array([[-0.00371194, -0.00043699,  0.        ,  0.        ],
       [ 0.        , -0.00110189,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.01545724,  0.00404402],
       [ 0.        ,  0.        ,  0.        , -0.0288508 ]])
H.c_gamma[8] = np.array([[-0.00347471, -0.00291253,  0.        ,  0.        ],
       [ 0.        , -0.00243418,  0.        ,  0.        ],
       [ 0.        ,  0.        , -0.00907362, -0.00271997],
       [ 0.        ,  0.        ,  0.        , -0.02478213]])
H.c_rho[0] = np.array([[-4.66590261e-04,  1.15676889e-04,  7.32843558e-04, -1.92738777e-04],
       [ 1.51057649e-03, -3.05338521e-05, -6.23807911e-04,  4.42897751e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[1] = np.array([[-5.25477125e-04,  1.65954285e-04,  6.09484534e-04, -5.76920262e-05],
       [ 1.56680672e-03, -6.98414711e-05, -3.16720148e-04,  2.26334058e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[2] = np.array([[-5.50327441e-04,  3.50680577e-04,  1.16322664e-03,  8.21368531e-04],
       [ 1.74115617e-03, -5.53326827e-05, -4.97287039e-04,  5.18709063e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[3] = np.array([[-3.34927442e-04,  1.53455208e-04,  7.53644392e-04,  1.50813870e-04],
       [ 1.29868922e-03, -3.66510745e-05, -3.23340773e-04, -5.11467460e-06],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[4] = np.array([[-4.10035173e-04,  1.27632853e-04,  3.11021858e-04, -6.36397369e-04],
       [ 1.38319191e-03, -5.45855409e-05, -7.61890196e-04, -2.54256632e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[5] = np.array([[-4.69255420e-04,  1.04373452e-05,  9.88739354e-04,  2.29868781e-04],
       [ 1.55727119e-03, -6.50464477e-05, -6.71717065e-04,  1.24392497e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[6] = np.array([[-4.50817629e-04,  3.71143989e-05,  1.05394424e-03,  7.04866601e-05],
       [ 1.65897592e-03, -2.33261906e-04, -7.03366664e-04,  5.37294328e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[7] = np.array([[-4.92081173e-04,  8.79675872e-05,  8.39749258e-04, -2.67817437e-04],
       [ 1.43295348e-03, -1.42390593e-05, -5.25866476e-04,  3.63300606e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_rho[8] = np.array([[-4.63311441e-04,  2.17470411e-04,  9.10814233e-04,  3.98065667e-04],
       [ 1.53612714e-03, -5.56804007e-05, -5.58978469e-04,  4.15266819e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_sigma[0] = np.array([[9.29700001e-05, 1.03655400e-04, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 2.06616862e-05, 7.02046525e-06],
       [0., 0., 0., 7.02867921e-06]])
H.c_sigma[1] = np.array([[8.74559015e-05, 8.19351704e-05, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 2.49613030e-05, 4.40910147e-05],
       [0., 0., 0., 0.]])
H.c_sigma[2] = np.array([[9.88433839e-05, 1.08113868e-04, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 3.42406136e-05, 4.57371977e-05],
       [0., 0., 0., 1.45996596e-08]])
H.c_sigma[3] = np.array([[7.22532167e-05, 7.66480655e-05, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 2.10384329e-05, 2.49548662e-05],
       [0., 0., 0., 0.]])
H.c_sigma[4] = np.array([[7.54836162e-05, 8.11315922e-05, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 1.93206189e-05, 3.21762219e-05],
       [0., 0., 0., 4.37836712e-08]])
H.c_sigma[5] = np.array([[8.59540553e-05, 9.05662596e-05, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 2.08339020e-05, 6.37802159e-05],
       [0., 0., 0., 7.96227906e-06]])
H.c_sigma[6] = np.array([[8.88138526e-05, 1.26668613e-04, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 2.61053990e-05, 5.25567055e-05],
       [0., 0., 0., 4.96372785e-05]])
H.c_sigma[7] = np.array([[8.93331497e-05, 8.40651615e-05, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 4.49912884e-05, 5.32068080e-05],
       [0., 0., 0., 6.68826413e-05]])
H.c_sigma[8] = np.array([[9.03397953e-05, 9.27718895e-05, 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 2.29724062e-05, 2.32802062e-05],
       [0., 0., 0., 5.75662446e-05]])
H.c_lambda[0] = np.array([0.00354033, 0.0955053 , 0.        , 0.        ])
H.c_lambda[9] = np.array([ 0.        ,  0.        , -0.02860516,  0.20504545])
H.c_lambda[16] = np.array([ 0.        ,  0.        , -0.03463296,  0.11456855])
H.c_lambda[17] = np.array([ 0.00847989, -0.01071734,  0.        ,  0.        ])
H.c_lambda[19] = np.array([0.03712925, 0.00056384, 0.        , 0.        ])
H.c_lambda[26] = np.array([0.        , 0.        , 0.00162421, 0.0481036 ])
H.c_lambda[28] = np.array([0.        , 0.        , 0.00166358, 0.0422065 ])
H.c_lambda[31] = np.array([-0.01141688,  0.0157547 ,  0.        ,  0.        ])
H.c_lambda[34] = np.array([0.03427663, 0.02852346, 0.        , 0.        ])
H.c_eta[0] = np.array([[ 2.75820932e-04, -2.75388768e-04, -2.91361692e-04, -4.20146328e-04],
       [ 3.11874986e-04, -2.02325533e-05, -7.14505091e-04, -4.92015854e-04],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
H.c_eta[9] = np.array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [-1.71261690e-04,  2.25360678e-04, -3.45122551e-05,  1.23574680e-04],
       [-1.14333329e-04, -1.04952285e-04, -3.19881701e-04, -5.61238888e-04]])
H.c_eta[16] = np.array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [-4.30948425e-04, -2.78158265e-05,  1.55298226e-05,  1.24164981e-04],
       [-1.07719804e-04,  4.61040438e-05, -2.21298302e-05, -4.80361996e-04]])
H.c_eta[26] = np.array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [-5.48155828e-05, -2.84052243e-05,  4.35909742e-06,  6.85113226e-05],
       [-1.45522065e-04, -1.11947423e-04, -1.31322426e-04, -6.98560902e-05]])
H.c_eta[28] = np.array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [-1.15641831e-04, -1.15205688e-05,  2.37123456e-06, -8.67606788e-06],
       [-6.28651352e-04, -1.01321897e-04, -8.38999481e-05, -6.51335716e-05]])


# read data
scan_no, Q, V = sqlitedb.load_scans(db_path, H, n_vibrational_modes)

# do the fit
# see the Scipy documentation for documentation of all options
fit = vcham.fit_coefficients(H, err_nstate.err_weighted, Q, V, jac=err_nstate.err_weighted_jacobian,
       loss='soft_l1', f_scale=0.25, method='trf', x_scale='jac', tr_solver='lsmr', bounds=H.params_bounds,
       ftol=1e-6, xtol=1e-6, verbose=2)

# print result and goodness of fit statistics
print()
print(H)

try:
    if fit:
        print()
        print('time elapsed:', fit['t_fit'], 's')
        print('termination message:', fit['message'])
        print('number of function calls:', fit['nfev'])
        print('R^2 =', fit['r2'])
        print('Adj. R^2 =', fit['adj_r2'])
        print('RMSE =', fit['rmse'], 'eV')
except: pass

# plot results
x_axis_limits_fixed = (-15, 20)
y_axis_limits = (4.3, 10)
plot_points = 200

plot_model(H, Q, V, scan_no, err_nstate, x_axis_limits_fixed, y_axis_limits, plot_points)
