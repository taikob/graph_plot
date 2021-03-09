import sys, os, csv, argparse
from data_prcs import get as g
from color import convert as c
import data_processing as d
import matplotlib.pyplot as plt

def plot(configpath):
    sys.path.append(os.getcwd()+'/config')
    exec('import ' + configpath + ' as p')

    tt="x"+str(p.xnum)+"_y"+str(p.ynum)
    if p.lnum is not None and p.ap==1:
        tt+="_z"+str(p.znum)+"_l"+str(p.lnum)
    elif p.znum is not None: tt+="_z"+str(p.znum)
    if   p.addt is not None: tt+=p.addt

    #prepare graph data
    with open(p.dataname) as f:
        reader = csv.reader(f)
        data = [row for row in reader]

    if p.exceptnum is not None:
        data=d.dataexcept(data, p.exceptnum, p.exceptval, p.exceptreq, p.ynum)

    if p.fixparam is not None:
        data=d.datafilter(data, p.fixparam)

    sysparam, nump=g.get_sysparam(data,p.paramrow)
    data=d.make_graphdata(data,sysparam,nump,p.xnum,p.ynum,p.znum,p.lnum)
    print(sysparam)
    print(nump)

    if p.xmin is not None or p.xmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, p.xnum, p.xmin, p.xmax,0)
    if p.zmin is not None or p.zmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, p.znum, p.zmin, p.zmax,1)
    if p.lmin is not None or p.lmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, p.lnum, p.lmin, p.lmax,2)

    if p.lnum is not None and p.ap==1:
        fig = plt.figure(figsize=(30,20))
        pltt=  range(nump[p.lnum])# plot table
        pltn=[0]
    else:
        pltn = [0]
        if p.lnum is not None and p.ap==0:
            pltn = range(nump[p.lnum])
            tmptt=tt

    for n in pltn:
        if p.lnum is None or p.ap==0: pltt = [n]
        for l in pltt:
            if p.lnum is not None and p.ap==1:
                plt.subplot(5, 3, l+1)
            else:
                fig = plt.figure(figsize=(8, 3))
                plt.subplot(111)

            plt.grid()
            if p.xlm is not None: plt.xlim(p.xlm[0], p.xlm[1])
            if p.xtc is not None: plt.xticks(p.xtc)
            if p.ylm is not None: plt.ylim(p.ylm[0], p.ylm[1])
            if p.xlog is not None: plt.xscale("log")
            if p.ylog is not None: plt.yscale("log")

            if p.lnum is not None and p.ap==1:
                if p.tc==1:
                  plt.title(str(sysparam[p.lnum][l]),color=c.get_colorcode(int(sysparam[p.lnum][l])))
                else:
                  plt.title(str(sysparam[p.lnum][l]))
            else:
                lb=None
                cl='black'

            ydata = data[:,:,l]
            for yn in range(0, data.shape[1]):
                if p.znum is not None:
                    lb = str(sysparam[p.znum][yn])
                    if p.pc == 1:
                        cl = c.get_colorcode(int(sysparam[p.znum][yn]))
                    else:
                        cl = c.get_colorcode(int(360/data.shape[1]*yn))

                xdata=sysparam[p.xnum]
                plt.plot(xdata, ydata[:, yn], '-o', label=lb, color=cl, linewidth=0.5, markersize=6)

        if p.lnum is not None and p.ap==0:tt=tmptt+"_l"+str(n)
        fig.savefig(tt+'_output.png',transparent = True, bbox_inches='tight')
        if lb is not None:
            plt.legend().get_frame().set_alpha(1)
            fig.savefig(tt+"_legend.png",transparent = True, bbox_inches='tight')
        plt.close()

        d.save_graph_data(tt + '_graph.csv', data, sysparam, p.xnum, p.znum, p.lnum)

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='plot_data')
    parser.add_argument('--path', '-p', default='', type=str, help='config')
    parser.set_defaults(test=False)
    args = parser.parse_args()

    plot(args.path)