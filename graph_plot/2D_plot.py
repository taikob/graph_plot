import sys, os, csv, argparse
from data_prcs import get as g
from color import convert as c
import data_processing as d
import matplotlib.pyplot as plt
import numpy as np

import os

def plot(configpath):

    sys.path.append(os.getcwd()+'/config')
    exec('import ' + configpath + ' as p')

    print(p.dataname)
    data=np.loadtxt(p.dataname)

    print(data[:,1:3])

    fig = plt.figure(figsize=(10, 10))
    plt.imshow(data[:,1:3])
    plt.title("Plot 2D array")
    plt.colorbar()
    plt.show()


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='plot_data')
    parser.add_argument('--path', '-p', default='', type=str, help='config')
    parser.set_defaults(test=False)
    args = parser.parse_args()

    plot(args.path)