#!/bin/bash

if [ ! -d "monte_carlo" ]; then
  python -m venv monte_carlo
fi
  
source monte_carlo/bin/activate
if [ $# -eq 0 ]; then
  python3 Simulation.py -h
  exit 1
fi

python3 Simulation.py $1 $2 $3
