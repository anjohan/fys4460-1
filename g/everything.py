import tqdm
import ovito
from ovito.modifiers import CoordinationNumberModifier
import os
import logplotter
import numpy as np

Ts = np.array([0.2, 2, 5, 10])
np.savetxt("data/Ts.dat", Ts)
num_Ts = len(Ts)
eqTs = np.zeros_like(Ts)

for i, T in enumerate(tqdm.tqdm(Ts)):
    os.system("make data/log.%g > /dev/null" % T)
    data = logplotter.find_data("data/log.%g" % T)
    t = np.array(data["Time"])
    num_values = len(t)
    pipeline = ovito.io.import_file("data/dump.%g" % T, multiple_frames=True)
    num_frames = pipeline.source.num_frames
    rdfcalculator = CoordinationNumberModifier(cutoff=6, number_of_bins=400)
    pipeline.modifiers.append(rdfcalculator)
    if i == 0:
        pipeline.compute(0)
        np.savetxt("data/fccrdf.dat", rdfcalculator.rdf)
    temp = np.array(data["Temp"])
    # Find equilibrium temperature and time
    max_deviation = np.max(np.abs(temp - temp[-1]))
    j = len(temp) - 1
    while abs(temp[j] - temp[-1]) < 0.2 * max_deviation:
        j -= 1
    equilibrium_index = j
    assert equilibrium_index < 0.9 * len(temp),\
        "More data needed for T=%g, %g" % (T, equilibrium_index/len(temp))
    equilibrium_step = data["Step"][equilibrium_index]
    eqTs[i] = np.mean(temp[equilibrium_index:])
    step = 0
    j = 0
    while step < equilibrium_step:
        step = pipeline.compute(j).attributes["Timestep"]
        j += 1
    rdf = np.zeros_like(rdfcalculator.rdf)
    num_rdfs = 0
    while j < num_frames:
        pipeline.compute(j)
        rdf += rdfcalculator.rdf
        j += 1
        num_rdfs += 1
    rdf /= num_rdfs
    np.savetxt("data/rdf_%g.dat" % T, rdf)
np.savetxt("data/eqTs.dat", eqTs)
