import ovito
from ovito.modifiers import CoordinationNumberModifier
import os
import logplotter
import numpy as np

Ts = np.array([0.2, 1, 1.5, 2])
np.savetxt("data/Ts.dat", Ts)
num_Ts = len(Ts)
eqTs = np.zeros_like(Ts)

for i, T in enumerate(Ts):
    os.system("make data/log.%g" % T)
    data = logplotter.find_data("data/log.%g" % T)
    t = np.array(data["Time"])
    num_values = len(t)
    pipeline = ovito.io.import_file("data/dump.%g" % T, multiple_frames=True)
    num_frames = pipeline.source.num_frames
    rdfcalculator = CoordinationNumberModifier(cutoff=10, number_of_bins=200)
    pipeline.modifiers.append(rdfcalculator)
    if i == 0:
        pipeline.compute(0)
        np.savetxt("data/fccrdf.dat", rdfcalculator.rdf)
    temp = np.array(data["Temp"])
    # Find equilibrium temperature and time
    max_deviation = np.max(np.abs(temp - temp[-1]))
    j = len(temp) - 1
    while abs(temp[j] - temp[-1]) < 0.5 * max_deviation:
        j -= 1
    equilibrium_index = 3 * j
    assert equilibrium_index < 0.9 * len(temp),\
        "More data needed for T=%g, %g" % (T, equilibrium_index/len(temp))
    equilibrium_step = data["Step"][equilibrium_index]
    eqTs[i] = np.mean(temp[equilibrium_index:])
