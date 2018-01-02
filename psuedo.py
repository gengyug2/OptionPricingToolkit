import numpy as np
import pandas as pd

returns = pd.read_csv('returns.csv')
CORR = returns.corr().as_matrix()
MEAN = returns.mean().tolist()

rf_maturity = 1.916255255 / 100
rf6 = 0.9439800 / 100


T = 5.275
steps = 1926
dt = T / steps

th_SPX = 1863.16
th_RTY = 1076.195


Price = []

for _ in range(10000):
    R = np.random.multivariate_normal([0, 0], CORR, steps + 1)
    R = R.T
    S_SPX = [2328.95]
    S_RTY = [1345.244]
    for i in range(1, steps + 1):
        SPX = S_SPX[i - 1] * np.exp(R[1][i])
        RTY = S_RTY[i - 1] * np.exp(R[0][i])
        S_SPX.append(SPX)
        S_RTY.append(RTY)
    final_SPX = np.average(S_SPX[-90:])
    final_RTY = np.average(S_RTY[-90:])
    if final_SPX >= th_SPX and final_RTY >= th_RTY:
        PMT = 10 + 4.310
    else:
        PMT = 10 * (min(final_RTY / S_RTY[0], final_SPX / S_SPX[0]) + .2)

    V = PMT * np.exp(-T * rf_maturity)
    # for i in range(1, steps + 1):
    #     V.append(V[i - 1] * np.exp(-dt * rf_maturity))

    Price.append(V * np.exp(6 / 365 * rf6))


print np.average(Price)