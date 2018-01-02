import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime

price_pad = pd.DataFrame()
price_pad['SP500'] = web.DataReader('^GSPC', 'yahoo', datetime.datetime(2012, 1, 1),
                                    datetime.datetime(2017, 4, 13))['Adj Close']
price_pad['RTY'] = web.DataReader('^RUT', 'yahoo', datetime.datetime(2012, 1, 1),
                                    datetime.datetime(2017, 4, 13))['Adj Close']
returns = np.log(price_pad / price_pad.shift(1))
returns.fillna(0, inplace=True)

returns = returns.tail(1000)
CORR = returns.corr().as_matrix()
MEAN = returns.mean().tolist()
COV = returns.cov().as_matrix() * 252
# COV[0][0] *= 1.04 ** 2 sensitivity
# COV[1][1] *= 1.04 ** 2 sensitivity
SGM = np.sqrt(COV)
rho = CORR[1][0] # * 1.04 sensitivity

rf_maturity = 1.916255255 / 100 # * 1.04 sensitivity
rf6 = 0.9439800 / 100


T = 5.275
steps = 1926
dt = T / steps

th_SPX = 1863.16
th_RTY = 1076.195

P12 = []

for j in range(12):
    Price = []
    for _ in range(10000):
        X1 = np.random.normal(0, 1, steps + 1)
        X2 = np.random.normal(0, 1, steps + 1)
        S_SPX = [2328.95]
        S_RTY = [1345.244]

        for i in range(1, steps + 1):
            SPX = S_SPX[i - 1] * np.exp((rf_maturity - .5 * COV[0][0]) * dt
                                        + SGM[0][0] * X1[i] * np.sqrt(dt))
            RTY = S_RTY[i - 1] * np.exp((rf_maturity - .5 * COV[1][1]) * dt
                                        + SGM[1][1] * X1[i] * rho * np.sqrt(dt)
                                        + SGM[1][1] * X2[i] * np.sqrt(1 - rho ** 2) * np.sqrt(dt))
            S_SPX.append(SPX)
            S_RTY.append(RTY)
        final_SPX = np.average(S_SPX[-95:-5])
        final_RTY = np.average(S_RTY[-95:-5])
        if final_SPX >= th_SPX and final_RTY >= th_RTY:
            PMT = 10 + 4.310
        else:
            PMT = 10 * (min(final_RTY / S_RTY[0], final_SPX / S_SPX[0]) + .2)

        V = PMT * np.exp(-T * rf_maturity)
        # for i in range(1, steps + 1):
        #     V.append(V[i - 1] * np.exp(-dt * rf_maturity))

        Price.append(V * np.exp(6 / 365 * rf6))
    P12.append(np.average(Price))
    print P12[-1]

print np.average(P12)
