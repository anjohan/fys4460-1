import numpy as np

with open("data/fcc.data", "r") as infile,\
        open("data/uniformvelocity.data", "w") as outfile:
    for line in infile:
        if "Velocities" not in line:
            outfile.write(line)
        else:
            break
    outfile.write(line + infile.readline())
    for line in infile:
        id, vx, vy, vz = line.split()
        vx, vy, vz = np.random.uniform(-5, 5, size=3)
        outfile.write("%s %g %g %g\n" % (id, vx, vy, vz))
