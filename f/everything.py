import tqdm
import os
import logplotter
import numpy as np
# from units import units

Ts = np.linspace(1, 3., 5)
num_Ts = len(Ts)
Ds = np.zeros(num_Ts)
eqTs = np.zeros_like(Ts)


def aberror(t, msd):
    a, b = np.polyfit(t, msd, 1)
    error = np.sum(np.abs(a * t + b - msd))
    return a, b, error


for i, T in enumerate(tqdm.tqdm(Ts, desc="Temperatures:".ljust(20))):
    os.system("make data/log.msd_%g > /dev/null" % T)
    data = logplotter.find_data("data/log.msd_%g" % T)
    msd = np.array(data["c_msd[4]"])
    t = np.array(data["Time"])
    res = np.array([t, msd]).transpose()
    np.savetxt("data/msd_%g.dat" % T, res)
    eqTs[i] = np.mean(data["Temp"])
    a, b, error0 = aberror(t, msd)
    error = 2 * error0
    num_values = len(t)
    j = 1
    while error > 0.01 * error0:
        assert j < 0.9 * num_values, "Need more data for T = %g" % T
        a, b, error = aberror(t[j:], msd[j:])
        j += 1
    print(j / num_values)
    Ds[i] = a / 6

res = np.array([eqTs, Ds]).transpose()
np.savetxt("data/D.dat", res)
