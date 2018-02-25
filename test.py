import os
import re
files = os.listdir("f/data/")
for file in files:
    searchres = re.findall(r"msd_(.+).dat", file)
    print(file)
    print(searchres)
    if len(searchres) != 0:
        T = searchres[0]
        print(r"\addplot table {f/data/msd_%s.dat};" % T)
        print(r"\addlegendentry{\(T/T_0 = %s\)};" % T)
