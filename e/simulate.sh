#!/usr/bin/bash
set -e -x

for rho in $(seq 0.005 0.001 0.025)
do
    for T in $(seq 1.0 0.1 3.0)
    do
        make data/log.${rho}_${T}
    done
done
