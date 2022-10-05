import data_processing as d
import plot_data as p
import datetime, shutil, os, sys
import numpy as np

def get_config(configpath,fixparaml=None):

    if configpath is None or configpath is '':
        print('Please set config file!')
        import set_config as sc
        sc.main(); sys.exit()
    elif not os.path.exists('config/'+configpath+'.py'):
        print('config file is not here! ', 'config/'+configpath+'.py')
        sys.exit()

    sys.path.append(os.getcwd()+'/config')
    exec('import ' + configpath + ' as p')

    global dataname; dataname = p.dataname
    global fixparam; fixparam = fixparaml
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
    global tc;       tc=p.tc
    global cl;       cl=p.cl
    global gl;       gl='-o'
    global pc;       pc=p.pc
    global addt;     addt=p.addt
    global lineplot; lineplot=None
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
    global xtick;   xtick=p.xtick
    global ytick;   ytick=p.ytick
    global mksize; mksize=3
    global lnsize; lnsize=0.5
    global dashline; dashline=None
    global fitdata; fitdata=None

    if hasattr(p,'lineplot'): lineplot=p.lineplot
    if hasattr(p,'hsize' ): hsize=p.hsize
    if hasattr(p,'vsize' ): vsize=p.vsize
    if hasattr(p,'mksize'): mksize=p.mksize
    if hasattr(p,'lnsize'): lnsize=p.lnsize
    if hasattr(p, 'gl'): gl = p.gl
    if fixparam == None: fixparam = p.fixparam

configpath ='config_0'
get_config(configpath)
dir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
data, sysparam, nump = d.prepare_data(dataname, paramrow, xnum, ynum, lnum, fixparam)
datapath = d.save_graph_data(dir, data, sysparam, xnum, ynum, znum, lnum)
shutil.copyfile('config/' + configpath + '.py', dir + '/config.py')

dt = p.plot(np.loadtxt(datapath,delimiter=','),configpath)
os.rename('output_'+dt+'.pdf', dir+'/output_'+dt+'.pdf')
os.rename('legend_'+dt+'.pdf', dir+'/legend_'+dt+'.pdf')