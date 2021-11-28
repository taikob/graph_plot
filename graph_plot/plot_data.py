import sys, os, csv, argparse, shutil
from data_prcs import get as g
from color import convert as c
import data_processing as d
import matplotlib.pyplot as plt
import numpy as np
import datetime

def plot(configpath=None,dataname=None,rename=None,fixparam=None, xline=None,yline=None):
    if configpath is None or configpath is '':
        print('Please set config file!')
        import set_config as sc
        sc.main()
        sys.exit()
    elif not os.path.exists('config/'+configpath+'.py'):
        print('config file is not here! ', 'config/'+configpath+'.py')
        sys.exit()

    sys.path.append(os.getcwd()+'/config')
    exec('import ' + configpath + ' as p')

    #param
    if xline == None:
        if hasattr(p, 'xline'):
            xline = p.xline
    if yline == None:
        if hasattr(p, 'yline'):
            yline = p.yline


    tt="x"+str(p.xnum)+"_y"+str(p.ynum)
    if p.lnum is not None and p.ap==1:
        tt+="_z"+str(p.znum)+"_l"+str(p.lnum)
    elif p.znum is not None: tt+="_z"+str(p.znum)
    if   p.addt is not None: tt+=p.addt

    #prepare graph data
    if dataname == None:
        dataname = p.dataname
    with open(dataname) as f:
        reader = csv.reader(f)
        data = [row for row in reader]

    if p.exceptnum is not None:
        data=d.dataexcept(data, p.exceptnum, p.exceptval, p.exceptreq, p.ynum)

    if p.fixparam is not None:
        fixparam = p.fixparam
    if fixparam != None:
        data=d.datafilter(data, fixparam)

    sysparam, nump=g.get_sysparam(data,p.paramrow)
    data=d.make_graphdata(data,sysparam,nump,p.xnum,p.ynum,p.znum,p.lnum)

    if p.xmin is not None or p.xmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, p.xnum, p.xmin, p.xmax,0)
    if p.zmin is not None or p.zmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, p.znum, p.zmin, p.zmax,1)
    if p.lmin is not None or p.lmax is not None:
        data, sysparam, nump = d.rangelimit(data, sysparam, nump, p.lnum, p.lmin, p.lmax,2)

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

    if hasattr(p, 'fntsize'):
        plt.rcParams["font.size"] = p.fntsize
    if p.lnum is not None and p.ap==1:
        if hasattr(p, 'lineplot'):
            fig = plt.figure(figsize=(0.1*float(len(sysparam[p.xnum])),16))
        else:
            fig = plt.figure(figsize=(6,4))
        pltt=  range(nump[p.lnum])# plot table
        pltn=[0]
        if hasattr(p, 'xtitle') and hasattr(p, 'ytitle'):
            plt.gcf().text(0.04, 0.75, p.ytitle, rotation=90)
            plt.gcf().text(0.47, 0.18, p.xtitle)
    else:
        pltn = [0]
        if p.lnum is not None and p.ap==0:
            pltn = range(nump[p.lnum])
            tmptt=tt

    if type(xline) != list:
        tmp=xline
        xline=[]
        for n in pltt:
            xline.append(tmp)
    if type(yline) != list:
        tmp=yline
        yline=[]
        for n in pltt:
            yline.append(tmp)

    for n in pltn:
        if p.lnum is None or p.ap==0: pltt = [n]
        for l in pltt:
            if p.lnum is not None and p.ap==1:
                if hasattr(p, 'lineplot'):
                    plt.subplot(len(pltt), 1, l+1)
                else:
                    plt.subplot(5, 3, l+1)
            else:
                if hasattr(p, 'hsize') and hasattr(p, 'vsize'):
                    fig = plt.figure(figsize=(p.hsize, p.vsize))
                else:
                    fig = plt.figure(figsize=(1.89, 0.7))
                if hasattr(p, 'xtitle') and hasattr(p, 'ytitle'):
                    plt.subplot(111,xlabel=p.xtitle,ylabel=p.ytitle)

            if hasattr(p, 'xlog'):
                if p.xlog is not None: plt.xscale("log")
            if hasattr(p, 'ylog'):
                if p.ylog is not None: plt.yscale("log")
            if not hasattr(p, 'nogrid'):
                plt.grid(linewidth = 0.2)
            if hasattr(p, 'xlm'):
                plt.xlim(p.xlm[0], p.xlm[1])
            if hasattr(p, 'xmal'):
                plt.gca().xaxis.set_major_locator(plt.MultipleLocator(p.xmal))
            if hasattr(p, 'xmil'):
                plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(p.xmil))
            if hasattr(p, 'ylm'):
                plt.ylim(p.ylm[0], p.ylm[1])
            if hasattr(p, 'ymal'):
                plt.gca().yaxis.set_major_locator(plt.MultipleLocator(p.ymal))
            if hasattr(p, 'ymil'):
                plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(p.ymil))
            if xline is not None:
                plt.hlines([xline[l]], p.xlm[0], p.xlm[1], "black", linewidth=0.7)  # hlines
            if yline is not None:
                plt.vlines([yline[l]], p.ylm[0], p.ylm[1], "black", linewidth=0.7)  # hlines
            if hasattr(p, 'mksize'): mksize=p.mksize
            else: mksize=3
            if hasattr(p, 'lnsize'): lnsize=p.lnsize
            else: lnsize=0.5

            plt.subplots_adjust(wspace=0.8/8, hspace=0.8/3)
            #plt.xticks(color="None")
            #plt.yticks(color="None")

            if p.lnum is not None and p.ap==1:
                if p.tc==1:
                    plt.title(str(sysparam[p.lnum][l]),color=c.get_colorcode(int(sysparam[p.lnum][l])))
                else:
                    #plt.title(str(sysparam[p.lnum][l]),x=0.5,y=0.9)
                    print('skip title')
            else:
                lb=None
                cl='black'

            ydata = data[:,:,l]
            for yn in range(0, data.shape[1]):
                if p.znum is not None and not hasattr(p, 'cl'):
                    lb = str(sysparam[p.znum][yn])
                    if p.pc == 1:
                        if p.lnum is None:
                            cl = c.get_colorcode(int(sysparam[p.znum][yn]))
                        else:
                            cl = c.get_colorcode(int(sysparam[p.lnum][l]))
                    else:
                        cl = c.get_colorcode(int(360/data.shape[1]*yn))
                elif hasattr(p, 'cl'):
                    lb=str(sysparam[p.znum][yn])
                    if p.cl is not None:
                        cl=c.get_colorcode(int(p.cl))
                else:
                    lb=None
                    cl='black'

                xdata=sysparam[p.xnum]

                if hasattr(p, 'gl'): gl=p.gl
                else: gl='-o'

                if p.znum is not None:
                    if nump[p.znum] == 2 and yn == 1:
                        #plt.plot(xdata, ydata[:, yn], '--', label=lb, color='black',dashes=[2,1], linewidth=1, markersize=3)
                        plt.plot(xdata, ydata[:, yn], '-o', label=lb, color='red', linewidth=1, markersize=3)
                    else:
                        if hasattr(p, 'dashline'):
                            if yn==0:
                                plt.plot(xdata, ydata[:, yn], '--', label=lb, color='black', linewidth=lnsize+1, markersize=mksize)
                            else:
                                plt.plot(xdata, ydata[:, yn], gl, label=lb, color=cl, linewidth=lnsize, markersize=mksize)
                        else:
                            plt.plot(xdata, ydata[:, yn], gl, label=lb, color=cl, linewidth=lnsize, markersize=mksize)
                else:
                    plt.plot(xdata, ydata[:, yn], gl, label=lb, color=cl, linewidth=lnsize, markersize=mksize, mec='k', mew=0.5)

        if hasattr(p, 'fitdata'):
            if p.fitdata is not None:
                fitdata=np.loadtxt(p.fitdata, delimiter=',')
                plt.plot(fitdata[:,0], fitdata[:,1], ls='--', color='black',dashes=[2,1] , linewidth=1)


        # save files
        if p.lnum is not None and p.ap==0:tt=tmptt+"_l"+str(n)
        fig.savefig(tt+'_output.pdf',transparent = True, bbox_inches='tight')
        if lb is not None:
            plt.legend().get_frame().set_alpha(1)
            fig.savefig(tt+"_legend.pdf",transparent = True, bbox_inches='tight')
        plt.close()

        d.save_graph_data(tt + '_graph.csv', data, sysparam, p.xnum, p.znum, p.lnum)

        if rename==None and hasattr(p, 'rename'):
            rename=p.rename
        elif rename==None and not hasattr(p, 'rename'):
            rename=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        os.mkdir(rename)
        os.rename(tt + '_graph.csv' ,rename+'_'+tt + '_graph.csv')
        os.rename(tt + '_output.pdf',rename+'_'+tt + '_output.pdf')
        if os.path.exists(tt + '_legend.pdf'):
            os.rename(tt + '_legend.pdf',rename+'_'+tt + '_legend.pdf')
        shutil.copyfile('config/'+configpath+'.py', configpath + '_' + rename + '.py')

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='plot_data')
    parser.add_argument('--path', '-p', default='', type=str, help='config')
    parser.set_defaults(test=False)
    args = parser.parse_args()
    plot(args.path)