import sys, os, datetime
import matplotlib.pyplot as plt
import data_processing as d
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

def graph_paraset():

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

def plot(data, configpath):
    if configpath is None or configpath is '':
        print('Please set config file!')
        import set_config as sc
        sc.main(); sys.exit()
    elif not os.path.exists('config/'+configpath+'.py'):
        print('config file is not here! ', 'config/'+configpath+'.py')
        sys.exit()

    sys.path.append(os.getcwd()+'/config')
    exec('import ' + configpath + ' as p')

    global tc, cl, gl, pc, addt,wspace,hspace, xline,yline,xtitle,ytitle, xtick, ytick, hsize, vsize,xlog,ylog,nogrid,xlm
    global xmal,xmil,ylm,ymal,ymil,xplotnum,yplotnum,title,mksize,lnsize,dashline,fitdata
    tc=p.tc; cl=p.cl; gl='-o'; pc=p.pc; addt=p.addt; wspace = p.wspace; hspace = p.hspace; vsize=0.7; xlog=p.xlog; ylog=p.ylog
    xline=p.xline; yline=p.yline; xtitle=p.xtitle; ytitle=p.ytitle; xtick=p.xtick; ytick=p.ytick; hsize=1.89; nogrid=p.nogrid
    xlm = p.xlm; xmal = p.xmal; xmil=p.xmil; ylm =p.ylm; ymal=p.ymal; ymil=p.ymil; xplotnum=p.xplotnum; yplotnum=p.yplotnum
    title = p.title; mksize=3; lnsize=0.5; dashline=None; fitdata=None

    if hasattr(p,'hsize' ): hsize=p.hsize
    if hasattr(p,'vsize' ): vsize=p.vsize
    if hasattr(p,'mksize'): mksize=p.mksize
    if hasattr(p,'lnsize'): lnsize=p.lnsize
    if hasattr(p, 'gl'): gl = p.gl

    sysparam, nump=g.get_sysparam(data,range(0,3))
    data=d.make_graphdata(data,sysparam,nump,0,3,1,2)

    plot_paraset()
    graph_paraset()
    fig = plt.figure(figsize=(hsize*xplotnum,vsize*yplotnum))

    xdata=sysparam[0]
    pltt=  range(nump[2])# plot table

    if type(xline) != list: xline=[xline]*len(pltt)
    if type(yline) != list: yline=[yline]*len(pltt)

    for l in pltt:
        plt.subplot(xplotnum, yplotnum, l+1)
        graph_paraset()

        if xline is not None: plt.hlines([xline[l]], xlm[0], xlm[1], "black", linewidth=0.7)  # hlines
        if yline is not None: plt.vlines([yline[l]], ylm[0], ylm[1], "black", linewidth=0.7)  # hlines

        plt.subplots_adjust(wspace=wspace, hspace=hspace)
        if title is not None: plt.title(str(sysparam[2][l]),x=0.5,y=0.9)

        for yn in range(0, data.shape[1]):
            plt.plot(xdata, data[:,yn,l], gl, label=str(sysparam[1][yn]), linewidth=lnsize, markersize=mksize)

    # save files
    plt.close()
    dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fig.savefig('output_'+dt+'.pdf', transparent=True, bbox_inches='tight')
    fig.legend().get_frame().set_alpha(1)
    fig.savefig('legend_'+dt+'.pdf', transparent=True, bbox_inches='tight')

    return dt

if __name__== "__main__":
    configpath='config_0'
    datapath='20221005163545/x6_y14_z1_l5.csv'

    dt = plot(np.loadtxt(datapath,delimiter=','),configpath)
    os.rename('output_'+dt+'.pdf', os.path.dirname(datapath)+'/output_'+dt+'.pdf')
    os.rename('legend_'+dt+'.pdf', os.path.dirname(datapath)+'/legend_'+dt+'.pdf')