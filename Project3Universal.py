import numpy as np
import pandas as pd


def monte_carlo(CORR, COV, rfm, rfs, steps, trails):
    SGM = np.sqrt(COV) * np.sqrt(365)
    T = 5.275
    dt = 1.0 * T / steps
    th_SPX = 1863.16
    th_RTY = 1076.195
    for j in range(12):
        for _ in range(trails):
            X1 = np.random.normal(0, 1, steps + 1)
            X2 = np.random.normal(0, 1, steps + 1)
            S_SPX = [2328.95]
            S_RTY = [1345.244]

            for i in range(1, steps + 1):
                SPX = S_SPX[i - 1] * np.exp((rfm - .5 * COV[1][1]) * dt
                                            + SGM[1][1] * X[i][1] * np.sqrt(dt))
                RTY = S_RTY[i - 1] * np.exp((rfs - .5 * COV[0][0]) * dt
                                            + SGM[0][0] * X[i][1] * np.sqrt(dt))
                S_SPX.append(SPX)
                S_RTY.append(RTY)
            final_SPX = np.average(S_SPX[-90:])
            final_RTY = np.average(S_RTY[-90:])
            if final_SPX >= th_SPX and final_RTY >= th_RTY:
                PMT = 10 + 4.310
            else:
                PMT = 10 * (min(final_RTY / S_RTY[0], final_SPX / S_SPX[0]) - 1 + .2)

            V = PMT * np.exp(-T * rfm)
            # for i in range(1, steps + 1):
            #     V.append(V[i - 1] * np.exp(-dt * rf_maturity))

            Price.append(V * np.exp(6 / 365 * rfs))
        P12.append(np.average(Price))
        print P12[-1]
    return np.mean(P12)


returns = pd.read_csv('returns.csv')
CORR = returns.corr().as_matrix()
MEAN = returns.mean().tolist()
COV = returns.cov().as_matrix()
SGM = np.sqrt(COV) * np.sqrt(365)

rf_maturity = 1.916255255 / 100
rf6 = 0.9439800 / 100


T = 5.275
steps = 1926
dt = T / steps

th_SPX = 1863.16
th_RTY = 1076.195

Price = []
P12 = []

for j in range(12):
    for _ in range(10000):
        X = np.random.multivariate_normal([0, 0], CORR, steps + 1)
        S_SPX = [2328.95]
        S_RTY = [1345.244]

        for i in range(1, steps + 1):
            SPX = S_SPX[i - 1] * np.exp((rf_maturity - .5 * COV[1][1]) * dt
                                        + SGM[1][1] * X[i][1] * np.sqrt(dt))
            RTY = S_RTY[i - 1] * np.exp((rf_maturity - .5 * COV[0][0]) * dt
                                        + SGM[0][0] * X[i][1] * np.sqrt(dt))
            S_SPX.append(SPX)
            S_RTY.append(RTY)
        final_SPX = np.average(S_SPX[-90:])
        final_RTY = np.average(S_RTY[-90:])
        if final_SPX >= th_SPX and final_RTY >= th_RTY:
            PMT = 10 + 4.310
        else:
            PMT = 10 * (min(final_RTY / S_RTY[0], final_SPX / S_SPX[0]) - 1 + .2)

        V = PMT * np.exp(-T * rf_maturity)
        # for i in range(1, steps + 1):
        #     V.append(V[i - 1] * np.exp(-dt * rf_maturity))

        Price.append(V * np.exp(6 / 365 * rf6))
    P12.append(np.average(Price))
    print P12[-1]

print np.average(P12)