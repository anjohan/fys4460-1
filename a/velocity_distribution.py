import ovito
from units import units

import numpy as np
import re

with open("in.simulation", "r") as infile:
    lammpsscript = infile.read()

dt = float(re.findall(r"timestep (\S+)", lammpsscript)[0]) * units.t0

pipeline = ovito.io.import_file(
    "data/simulation.in.bin",
    multiple_frames=True,
    columns=[
        "id", "type", "Position.X", "Position.Y", "Position.Z", "vx", "vy",
        "vz"
    ])

time_between_frames = dt * (pipeline.compute(1).attributes["Timestep"] -
                            pipeline.compute(0).attributes["Timestep"])

num_frames = pipeline.source.num_frames
t = np.arange(0, num_frames) * time_between_frames
dims = ["x", "y", "z"]

vmax = 0
for i in range(num_frames):
    data = pipeline.compute(i)
    for dim in dims:
        v = data.particle_properties["v" + dim]
        vmax = max(vmax, np.ndarray.max(np.abs(v)))
print(vmax)

vz_final = v * units.v0
data_final = pipeline.compute(num_frames - 1)
vx_final = data_final.particle_properties["vx"] * units.v0
vy_final = data_final.particle_properties["vy"] * units.v0

vmax *= units.v0
num_bins = 100
bin_edges = np.linspace(-vmax, vmax, num_bins + 1)
hist_final = np.zeros(num_bins)

for dim in dims:
    hist_final += np.histogram(eval("v%s_final" % dim), bin_edges)[0]
hist_final /= 3 * np.linalg.norm(hist_final)

correlation = np.zeros(num_frames)

bin_mids = 0.5 * (bin_edges[:-1] + bin_edges[1:])
num_plots = 0

for i in range(num_frames):
    data = pipeline.compute(i)
    hist = np.zeros(num_bins)
    for dim in dims:
        v = data.particle_properties["v" + dim] * units.v0
        hist += np.histogram(v, bin_edges)[0]
    hist /= 3
    norm = np.linalg.norm(hist)
    correlation[i] = np.dot(hist / norm, hist_final)
    if i == 0 or i == num_frames // 2 or i == num_frames - 1:
        num_plots += 1
        np.savetxt("data/velocity_distribution%d.dat" % num_plots,
                   np.array([bin_mids, hist]).transpose())

np.savetxt("data/velocity_correlation.dat",
           np.array([t, correlation]).transpose())
