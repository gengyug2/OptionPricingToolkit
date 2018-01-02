import numpy as np
import time
# import pandas as pd
#
# returns = pd.read_csv('returns.csv')
# CORR = returns.corr().as_matrix()
# MEAN = returns.mean().tolist()
# COV = returns.cov().as_matrix()
# SGM = np.sqrt(COV) * np.sqrt(365)
#
# rf_maturity = 1.808304 / 100
#
# T = 5.275
# steps = 1926
# dt = T / steps
#
# X = np.random.multivariate_normal([0, 0], CORR, steps +1)
# S_SPX = [2328.95]
# S_RTY = [1345.244]
# for i in range(1, steps + 1):
#     SPX = S_SPX[i - 1] * np.exp((rf_maturity - .5 * COV[1][1]) * dt
#                                 + SGM[1][1] * X[i][1] * np.sqrt(dt))
#     RTY = S_RTY[i - 1] * np.exp((rf_maturity - .5 * COV[0][0]) * dt
#                                 + SGM[0][0] * X[i][0] * np.sqrt(dt))
#     S_SPX.append(SPX)
#     S_RTY.append(RTY)
# # print CORR
# # print MEAN
# # print COV[1][1]
# # print SGM
# print S_SPX
# print S_RTY
# print SPX
# print RTY
#
# # from datetime import date
# # AVR_dates = date (2022 , 7 , 7) - date (2022 , 4 , 8)
# principal = 10
# coupon = 4.31
# SPX_thres = 1863.16
# RTY_thres = 1076.195
# if np.average( SPX[-90:] ) > SPX_thres & np.average( RTY[-90:] ) > RTY_thres:
#     VT = principal + coupon

def cal_rate(steps=60, trials=5000, loans_number=20, rho=.3, m0=.8):
    defaults = []
    COV = np.identity(loans_number) * (1 - rho) + rho
    for i in range(loans_number):
        COV[i][i] = 1
    print COV

    for _ in range(trials):
        m = [m0, ] * loans_number
        dft = 0
        rdm = np.random.multivariate_normal(np.zeros(loans_number), COV, steps)
        for i in range(loans_number):
            for j in range(steps):
                m[i] = m[i] + np.sqrt(1.0 / steps) * rdm[j][i]
                if m[i] < 0:
                    dft += 1
                    break
        defaults.append(dft)

    rate = 0
    for i in defaults:
        if i == 0:
            rate += 1.0 / trials

    return rate
start = time.time()
print cal_rate(100, 10000, 20, .3, .8)
end = time.time()
print str(end - start)