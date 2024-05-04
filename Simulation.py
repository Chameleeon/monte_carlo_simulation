from MonteCarloCalculator import MonteCarlo
import tkinter as tk
try:
    import argparse
except ImportError:
    print("Argparse is not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "argparse"])
    import argparse

def main():
    parser = argparse.ArgumentParser(description="Estimate Pi usnig Monte Carlo method")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', type=int, metavar='iterations', help='Estimate PI by generating the provided amount of random numbers. Requires number of random numbers to be generated to be provided.' )
    group.add_argument('-p', type=int, metavar='decimals', help='Estimateas PI to the provided decimal. Requires the desired decimal to be provided.')
    parser.add_argument('-f', '--fast', action='store_true', help='Enables fast mode, which does not sleep the thread in order to visually show the dots being placed in a nice way.')
    args = parser.parse_args()

    window = (1920, 1080)
    mc = MonteCarlo(window, "count", 300)
    if args.c:
        mc.sim_type="count"
        mc.points = args.c
    elif args.p:
        mc.sim_type="precise"
        mc.precision = args.p
        
    if args.fast:
        mc.fast_mode = True
    mc.loop()

if __name__ == "__main__":
    main()
