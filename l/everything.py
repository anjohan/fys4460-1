import tqdm
import subprocess
import logplotter
import numpy as np
# from units import units

Ts = np.linspace(2200, 3200, 201)
np.savetxt("data/Ts.dat", Ts)
num_Ts = len(Ts)
Ds = np.zeros(num_Ts)
eqTs = np.zeros_like(Ts)


def aberror(t, msd):
    a, b = np.polyfit(t, msd, 1)
    error = np.sum(np.abs(a * t + b - msd))
    return a, b, error


num_threads = 4
threads = []
for i, T in enumerate(tqdm.tqdm(Ts, desc="Simulating:".ljust(20))):
    p = subprocess.Popen(
        ("make data/log.msd_%g" % T).split(), stdout=subprocess.DEVNULL)
    threads.append(p)
    if (i % num_threads == 0 and i > 0) or i == num_Ts - 1:
        for j in range(i):
            threads[j].wait()

for i, T in enumerate(tqdm.tqdm(Ts, desc="Analysing:".ljust(20))):
    data = logplotter.find_data("data/log.msd_%g" % T)
    msd = np.array(data["c_msd[4]"])
    t = np.array(data["v_mytime"])
    N = len(t)

    res = np.array([t, msd]).transpose()
    np.savetxt("data/msd_%g.dat" % T, res)

    eqTs[i] = np.mean(data["Temp"])
    a, b, error0 = aberror(t[N // 2:], msd[N // 2:])
    Ds[i] = a / 6

res = np.array([eqTs, Ds]).transpose()
np.savetxt("data/D.dat", res)

np.savetxt("data/eqTs.dat", eqTs)
