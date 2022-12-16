import copy
import os, datetime, csv
import sys

from graph_plot import data_processing as d
from graph_plot import set_config as sc
import matplotlib.pyplot as plt
from data_prcs import get as g
import numpy as np

def plot_paraset():

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['axes.linewidth'] = 0.5
    plt.rcParams['xtick.major.width'] = 0.5
    plt.rcParams['ytick.major.width'] = 0.5
    plt.rcParams['xtick.minor.width'] = 0.5
    plt.rcParams['ytick.minor.width'] = 0.5
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["font.size"] = 10

def graph_paraset(cnfg):
    xlog = cnfg['xlog']; ylog = cnfg['ylog']
    nogrid = cnfg['nogrid']
    xlm = cnfg['xlm']; xmal = cnfg['xmal']; xmil = cnfg['xmil']
    ylm = cnfg['ylm']; ymal = cnfg['ymal']; ymil = cnfg['ymil']
    xtick = cnfg['xtick']; ytick = cnfg['ytick']

    if xlog is not None: plt.xscale("log")
    if ylog is not None: plt.yscale("log")
    if nogrid == 1:      plt.grid(linewidth=0.2)
    if xlm  is not None: plt.xlim(xlm[0], xlm[1])
    if xmal is not None: plt.gca().xaxis.set_major_locator(plt.MultipleLocator(xmal))
    if xmil is not None: plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(xmil))
    if ylm  is not None: plt.ylim(ylm[0], ylm[1])
    if ymal is not None: plt.gca().yaxis.set_major_locator(plt.MultipleLocator(ymal))
    if ymil is not None: plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(ymil))
    if xtick is not None: plt.xticks(color="None")
    if ytick is not None: plt.yticks(color="None")

def pickupdata(data,pickuppath,refd):
    with open(pickuppath) as f: picklist = [row for row in csv.reader(f)]
    pickdata = np.copy(data)
    pickdata[:,3] = np.nan

    del picklist[0]
    for i in range(pickdata.shape[0]):
        for j in reversed(range(len(picklist))):
            if  pickdata[i, refd[1]] == float(picklist[j][1]) and pickdata[i, refd[0]] == float(picklist[j][0]):
                pickdata[i,3] = data[i,3]
        if len(picklist)==0: break

    return pickdata

def plot(data,cnfg,sysparam=None,nump=None):
    xline = cnfg['xline']; yline = cnfg['yline']
    hsize = cnfg['hsize']; vsize = cnfg['vsize']
    xlm = cnfg['xlm']; ylm = cnfg['ylm']; gl = cnfg['gl']
    xplotnum = cnfg['xplotnum']; yplotnum = cnfg['yplotnum']
    wspace = cnfg['wspace']; hspace = cnfg['hspace']; title = cnfg['title']
    lnsize = cnfg['lnsize']; mksize = cnfg['mksize']
    pickuppath = cnfg['pickuppath']; refd = cnfg['refd']
    if sysparam is None or nump is None:
        sysparam, nump=g.get_sysparam(data,range(0,3))
        data = d.make_graphdata(data, sysparam, nump, 0, 3, 1, 2)

    if pickuppath is not None: pickup = d.make_graphdata(pickupdata(data,pickuppath,refd),sysparam,nump,0,3,1,2)
    plot_paraset()
    fig = plt.figure(figsize=(hsize*xplotnum,vsize*yplotnum))

    if type(xline) != list: xline=[xline]*nump[2]
    if type(yline) != list: yline=[yline]*nump[2]
    for l in range(nump[2]):
        plt.subplot(yplotnum, xplotnum, l+1)
        plt.subplots_adjust(wspace=wspace, hspace=hspace)
        graph_paraset(cnfg)

        if xline is not None: plt.hlines([xline[l]], xlm[0], xlm[1], "black", linewidth=0.7)  # hlines
        if yline is not None: plt.vlines([yline[l]], ylm[0], ylm[1], "black", linewidth=0.7)  # hlines
        if title is not None: plt.title(str(sysparam[2][l]),x=0.5,y=0.9)

        for yn in range(0, data.shape[1]):
            plt.plot(sysparam[0], data[:,yn,l], gl, label=str(sysparam[1][yn]), linewidth=lnsize, markersize=mksize)
            if pickuppath is not None:
                plt.plot(sysparam[0], pickup[:,yn,l], 'o', label=str(sysparam[1][yn]), markersize=float(mksize*1.1), color='red')

    # save files
    plt.close()
    dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fig.savefig('output_'+dt+'.pdf', transparent=True, bbox_inches='tight')
    fig.legend().get_frame().set_alpha(1)
    fig.savefig('legend_'+dt+'.pdf', transparent=True, bbox_inches='tight')

    return dt

if __name__== "__main__":
    configpath='config'
    datapath='20221006180502/x6_y14_z1_l5.csv'

    cnfg = sc.get_config(configpath)
    dt = plot(np.loadtxt(datapath,delimiter=','),cnfg)
    os.rename('output_'+dt+'.pdf', os.path.dirname(datapath)+'/output_'+dt+'.pdf')
    os.rename('legend_'+dt+'.pdf', os.path.dirname(datapath)+'/legend_'+dt+'.pdf')