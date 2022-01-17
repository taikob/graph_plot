import sys, os, csv, argparse, shutil
from data_prcs import get as g
from color import convert as c
import data_processing as d
import matplotlib.pyplot as plt
import numpy as np
import datetime

def get_config(configpath,dataname,rename,fixparam, xline, yline):

    if configpath is None or configpath is '':
        print('Please set config file!')
        import set_config as sc
        sc.main(); sys.exit()
    elif not os.path.exists('config/'+configpath+'.py'):
        print('config file is not here! ', 'config/'+configpath+'.py')
        sys.exit()

    sys.path.append(os.getcwd()+'/config')
    exec('import ' + configpath + ' as p')

    global exceptnum;exceptnum=p.exceptnum
    global exceptval;exceptval=p.exceptval
    global exceptreq;exceptreq=p.exceptreq
    global paramrow ;paramrow=p.paramrow
    global xnum;     xnum=p.xnum
    global ynum;     ynum=p.ynum
    global znum;     znum=p.znum
    global lnum;     lnum=p.lnum
    global xmin;     xmin=p.xmin
    global xmax;     xmax=p.xmax
    global zmin;     zmin=p.zmin
    global zmax;     zmax=p.zmax
    global lmin;     lmin=p.lmin
    global lmax;     lmax=p.lmax
    global ap;       ap=p.ap
    global tc;       tc=p.tc
    global cl;       cl=p.cl
    global gl;       gl='-o'
    global pc;       pc=p.pc
    global addt;     addt=p.addt
    global lineplot
    global xtitle;   xtitle=p.xtitle
    global ytitle;   ytitle=p.ytitle
    global hsize; hsize=1.89
    global vsize; vsize=0.7
    global xlog;   xlog=p.xlog
    global ylog;   ylog=p.ylog
    global nogrid; nogrid=p.nogrid
    global xlm;    xlm =p.xlm
    global xmal;   xmal=p.xmal
    global xmil;   xmil=p.xmil
    global ylm;    ylm =p.ylm
    global ymal;   ymal=p.ymal
    global ymil;   ymil=p.ymil
    global mksize; mksize=None
    global lnsize; lnsize=None
    global dashline; dashline=None
    global fitdata; fitdata=None


    if hasattr(p,'lineplot'): lineplot=p.lineplot
    if hasattr(p,'hsize' ): hsize=p.hsize
    if hasattr(p,'vsize' ): vsize=p.vsize
    if hasattr(p,'mksize'): mksize=p.mksize
    if hasattr(p,'lnsize'): lnsize=p.lnsize
    if hasattr(p, 'gl'): gl = p.gl

    if xline == None:
        if hasattr(p, 'xline'): xline = p.xline
    if yline == None:
        if hasattr(p, 'yline'): yline = p.yline

    if dataname == None: dataname = p.dataname
    if fixparam == None: fixparam = p.fixparam

    return dataname,rename,fixparam, xline, yline

def prepare_data(dataname,fixparam):

    with open(dataname) as f:
        reader = csv.reader(f)
        data = [row for row in reader]


    if exceptnum is not None:
        data=d.dataexcept(data, exceptnum, exceptval, exceptreq, ynum)

    if fixparam != None:
        data=d.datafilter(data, fixparam)

    sysparam, nump=g.get_sysparam(data,paramrow)
    data=d.make_graphdata(data,sysparam,nump,xnum,ynum,znum,lnum)

    if xmin is not None or xmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, xnum, xmin, xmax,0)
    if zmin is not None or zmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, znum, zmin, zmax,1)
    if lmin is not None or lmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, lnum, lmin, lmax,2)

    return data, sysparam, nump

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

def graph_paraset(xline,yline,l):

    if xlog is not None: plt.xscale("log")
    if ylog is not None: plt.yscale("log")
    if nogrid == 1:      plt.grid(linewidth=0.2)
    if xlm  is not None: plt.xlim(xlm[0], xlm[1])
    if xmal is not None: plt.gca().xaxis.set_major_locator(plt.MultipleLocator(xmal))
    if xmil is not None: plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(xmil))
    if ylm  is not None: plt.ylim(ylm[0], ylm[1])
    if ymal is not None: plt.gca().yaxis.set_major_locator(plt.MultipleLocator(ymal))
    if ymil is not None: plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(ymil))
    if xline is not None: plt.hlines([xline[l]], xlm[0], xlm[1], "black", linewidth=0.7)  # hlines
    if yline is not None: plt.vlines([yline[l]], ylm[0], ylm[1], "black", linewidth=0.7)  # hlines
    if mksize is None: global mksize; mksize = 3
    if lnsize is None: global lnsize; lnsize = 0.5

def save(data, sysparam,configpath, rename, fig, lb, n):
    tt = "x" + str(xnum) + "_y" + str(ynum) + "_z" + str(znum) + "_l" + str(lnum) + '_' + str(n)
    if addt is not None: tt += addt

    d.save_graph_data(tt + '_graph.csv', data, sysparam, xnum, znum, lnum)

    fig.savefig(tt + '_output.pdf', transparent=True, bbox_inches='tight')
    if lb is not None:
        plt.legend().get_frame().set_alpha(1)
        fig.savefig(tt + "_legend.pdf", transparent=True, bbox_inches='tight')

    if rename == None:
        rename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if not os.path.exists('graph'):
        os.mkdir('graph')
    os.rename(tt + '_graph.csv', 'graph/' + rename + '_' + tt + '_graph.csv')
    os.rename(tt + '_output.pdf', 'graph/' + rename + '_' + tt + '_output.pdf')
    if os.path.exists(tt + '_legend.pdf'):
        os.rename(tt + '_legend.pdf', 'graph/' + rename + '_' + tt + '_legend.pdf')
    shutil.copyfile('config/' + configpath + '.py', 'graph/' + configpath + '_' + rename + '.py')

def plot(configpath=None,dataname=None,rename=None,fixparam=None, xline=None,yline=None):

    dataname,rename,fixparam, xline, yline=get_config(configpath,dataname,rename,fixparam, xline, yline)
    data, sysparam, nump = prepare_data(dataname,fixparam)
    plot_paraset()

    pltn = [0]
    if lnum is not None and ap==1:
        if lineplot==1: fig = plt.figure(figsize=(0.1*float(len(sysparam[xnum])),16))
        else:           fig = plt.figure(figsize=(6,4))
        pltt=  range(nump[lnum])# plot table
        plt.gcf().text(0.04, 0.75, ytitle, rotation=90)
        plt.gcf().text(0.47, 0.18, xtitle)
    else:
        pltt=  [0]
        if lnum is not None and ap==0:
            pltn = range(nump[lnum])

    if type(xline) != list: xline=[xline]*len(pltt)
    if type(yline) != list: yline=[yline]*len(pltt)

    for n in pltn:
        if lnum is None or ap==0: pltt = [n]
        for l in pltt:
            if lnum is not None and ap==1:
                if lineplot==1: plt.subplot(len(pltt), 1, l+1)
                else:           plt.subplot(5, 3, l+1)
            else:
                fig = plt.figure(figsize=(hsize, vsize))
                plt.subplot(111,xlabel=xtitle,ylabel=ytitle)

            graph_paraset(xline, yline, l)

            plt.subplots_adjust(wspace=0.8/8, hspace=0.8/3)
            #plt.xticks(color="None")
            #plt.yticks(color="None")

            if lnum is not None and ap==1:
                if tc==1:
                    plt.title(str(sysparam[lnum][l]),color=c.get_colorcode(int(sysparam[lnum][l])))
                else:
                    #plt.title(str(sysparam[p.lnum][l]),x=0.5,y=0.9)
                    print('skip title')
            else:
                lb=None
                clg='black'

            ydata = data[:,:,l]
            for yn in range(0, data.shape[1]):
                if znum is not None and cl is None :
                    lb = str(sysparam[znum][yn])
                    if pc == 1:
                        if lnum is None:
                            clg = c.get_colorcode(int(sysparam[znum][yn]))
                        else:
                            clg = c.get_colorcode(int(sysparam[lnum][l]))
                    else:
                        clg = c.get_colorcode(int(360/data.shape[1]*yn))
                elif cl is not None:
                    lb=str(sysparam[znum][yn])
                    if clg is not None:
                        clg=c.get_colorcode(int(cl))
                else:
                    lb=None
                    clg='black'

                xdata=sysparam[xnum]

                if znum is not None:
                    if nump[znum] == 2 and yn == 1:
                        plt.plot(xdata, ydata[:, yn], '-o', label=lb, color='black', linewidth=1, markersize=3)
                        #plt.plot(xdata, ydata[:, yn], '--', label=lb, color='black',dashes=[2,1], linewidth=1, markersize=3)
                        #plt.plot(xdata, ydata[:, yn], '-o', label=lb, color='red', linewidth=1, markersize=3)
                    else:
                        if dashline is not None:
                            if yn==0: plt.plot(xdata, ydata[:, yn], '--', label=lb, color='black', linewidth=lnsize+1, markersize=mksize)
                            else:     plt.plot(xdata, ydata[:, yn], gl, label=lb, color=clg, linewidth=lnsize, markersize=mksize)
                        else:         plt.plot(xdata, ydata[:, yn], gl, label=lb, color=clg, linewidth=lnsize, markersize=mksize)
                else:
                    plt.plot(xdata, ydata[:, yn], gl, label=lb, color=clg, linewidth=lnsize, markersize=mksize, mec='k', mew=0.5)

        if fitdata is not None:
            fdata=np.loadtxt(fdata, delimiter=',')
            plt.plot(fdata[:,0], fdata[:,1], ls='--', color='black',dashes=[2,1] , linewidth=1)

        # save files
        plt.close()
        save(data, sysparam,configpath, rename, fig, lb, n)

def plot2D(configpath=None,dataname=None,rename=None,fixparam=None, xline=None,yline=None):

    dataname,rename,fixparam, xline, yline=get_config(configpath,dataname,rename,fixparam, xline, yline)
    data, sysparam, nump = prepare_data(dataname,fixparam)
    plot_paraset()

    if type(xline) != list: xline=[xline]
    if type(yline) != list: yline=[yline]
    gd = d.save_graph_data('graph.csv', data, sysparam, xnum, znum, lnum)
    fig = plt.figure(figsize=(hsize+0.3, hsize))
    graph_paraset(xline, yline, 0)
    plt.scatter(gd[:,0], gd[:,1], s=10, c=gd[:,2], cmap='seismic', vmin=-2.2, vmax=2.2)
    plt.colorbar()


    # save files
    plt.close()
    save(data, sysparam,configpath, rename, fig, 'g', 0)

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='plot_data')
    parser.add_argument('--path', '-p', default='', type=str, help='config')
    parser.add_argument('--dimension', '-d', default=None, type=str, help='config')
    parser.set_defaults(test=False)
    args = parser.parse_args()
    if args.dimension!=None: plot2D(args.path)
    else: plot(args.path)