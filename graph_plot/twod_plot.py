import sys, os, csv, argparse
import matplotlib.pyplot as plt
import numpy as np

import os

def plot(configpath):

    sys.path.append(os.getcwd()+'/config')
    exec('import ' + configpath + ' as p')

    data=np.loadtxt(p.dataname)
    ext=os.path.splitext(os.path.basename(p.dataname))[-1]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(data,aspect='auto', extent=[p.ymin,p.ymax,p.xmax,p.xmin])
    plt.colorbar(cax)
    plt.savefig(p.dataname.replace(ext,'.png'), transparent=True, bbox_inches='tight')


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='plot_data')
    parser.add_argument('--path', '-p', default='', type=str, help='config')
    parser.set_defaults(test=False)
    args = parser.parse_args()

    plot(args.path)