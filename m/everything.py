import ovito
from ovito.modifiers import CoordinationNumberModifier,\
    SelectTypeModifier, DeleteSelectedModifier
import tqdm
import subprocess
import logplotter
import numpy as np
# from units import units

Ts = np.linspace(100, 400, 301)
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
        ("make data/log.%g" % T).split(), stdout=subprocess.DEVNULL)
    threads.append(p)
    if ((i + 1) % num_threads == 0) or i == num_Ts - 1:
        for j in range((i+1)):
            threads[j].wait()

for i, T in enumerate(tqdm.tqdm(Ts, desc="MSD:".ljust(20))):
    data = logplotter.find_data("data/log.%g" % T)
    msd = np.array(data["c_msd[4]"])
    t = np.array(data["v_mytime"])
    N = len(t)

    res = np.array([t, msd]).transpose()
    np.savetxt("data/msd_%g.dat" % T, res)

    eqTs[i] = np.mean(data["Temp"])
    a, b, error0 = aberror(t[N // 2:], msd[N // 2:])
    Ds[i] = a / 6

num_rdfs = min(3, num_Ts)
indices = list(range(0, num_Ts, max(1, num_Ts // num_rdfs)))
for i in tqdm.tqdm(indices, desc="RDF:".ljust(20)):
    pipeline = ovito.io.import_file(
        "data/dump.%g" % Ts[i], multiple_frames=True)
    num_frames = pipeline.source.num_frames
    num_bins = 400
    oxygenchooser = SelectTypeModifier(types={"Type 2"})
    hydrogendeleter = DeleteSelectedModifier()
    pipeline.modifiers.append(oxygenchooser)
    pipeline.modifiers.append(hydrogendeleter)
    rdfcalculator = CoordinationNumberModifier(
        cutoff=20, number_of_bins=num_bins)
    pipeline.modifiers.append(rdfcalculator)

    rdf = np.zeros((num_bins, 2))
    for j in range(num_frames // 2, num_frames):
        pipeline.compute(j)
        rdf += rdfcalculator.rdf
    rdf /= num_frames // 2
    np.savetxt("data/rdf_%g.dat" % Ts[i], rdf)

res = np.array([eqTs, Ds]).transpose()
np.savetxt("data/D.dat", res)

np.savetxt("data/eqTs.dat", eqTs)

np.savetxt("data/rdfindices.dat", indices, fmt="%d")
