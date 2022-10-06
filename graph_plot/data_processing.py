import csv,os,datetime,shutil
from graph_plot import set_config as sc
from data_prcs import get as g
import numpy as np

def datafilter(data, fixparam):

  for param in fixparam:
    for i in reversed(range(len(data))):
      if float(data[i][param[0]])!=float(param[1]):
        del data[i]

  return data

def dataexcept(data, exceptnum, exceptval, exceptreq, ynum):
    for i in range(len(data)):
        if len(data[i][exceptnum]) != 0:
            if exceptreq == 1:
                if float(data[i][exceptnum]) >= exceptval:
                    data[i][ynum] = 0
            if exceptreq ==-1:
                if float(data[i][exceptnum]) <= exceptval:
                    data[i][ynum] = 0
            if exceptreq == 0:
                if float(data[i][exceptnum]) == exceptval:
                    data[i][ynum] = 0
    return data

def make_graphdata(data,sysparam,nump,xnum,ynum,znum,lnum,fixparam=None):

    if lnum is not None and znum is None:
        aldata=np.zeros([nump[xnum],1,nump[lnum]])
        lpara=sysparam[lnum]
        zpara=[0]
    elif lnum is not None:
        aldata=np.zeros([nump[xnum],nump[znum],nump[lnum]])
        lpara=sysparam[lnum]
        zpara=sysparam[znum]
    elif znum is not None:
        aldata=np.zeros([nump[xnum],nump[znum], 1])
        lpara=[0]
        zpara=sysparam[znum]
    else:
        aldata=np.zeros([nump[xnum],1,1])
        lpara=[0]
        zpara=[0]

    xpara = sysparam[xnum]

    for li, l in enumerate(lpara):
        if lnum is not None:
            ldata=np.ndarray([0,len(data[0])])
            for d in data:
                if float(d[lnum])==l:
                    ldata=np.vstack((ldata, d))
        else:
            ldata=data

        for zi, z in enumerate(zpara):
            if znum is not None:
                zdata=np.ndarray([0,len(data[0])])
                for d in ldata:
                    if float(d[znum])==z:
                        zdata=np.vstack((zdata, d))
            else:
                zdata=ldata


            for xi, x in enumerate(xpara):
                for d in zdata:
                    if float(d[xnum]) == x:
                        aldata[xi][zi][li] = d[ynum]

    return aldata

def rangelimit(data, sysparam, nump, xnum, xmin, xmax,ax):
    sspr = map((lambda x: float(x)), sysparam[xnum])

    if xmin is not None:
        for i in reversed(range(len(sspr))):
            if sspr[i] < xmin:
                nump[xnum]-=1
                data=np.delete(data, i, ax)
                del sysparam[xnum][i]
    if xmax is not None:
        for i in reversed(range(len(sspr))):
            if sspr[i] > xmax:
                nump[xnum]-=1
                data=np.delete(data, i, ax)
                del sysparam[xnum][i]

    return data, sysparam, nump

def save_graph_data(data,sysparam,cnfg):
    xnum = cnfg['xnum']; ynum = cnfg['ynum']; znum = cnfg['znum']; lnum = cnfg['lnum']

    xdata=sysparam[xnum]
    if znum is not None: zdata=sysparam[znum]
    if lnum is not None: ldata=sysparam[lnum]

    tmpd=data.copy()#tmpdata

    if znum==None and lnum!=None: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],3))
    elif znum==None: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],1))
    elif lnum==None: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],2))
    else: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],3))
    sdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],1))

    nz=0
    for l in range(tmpd.shape[2]):
        for z in range(tmpd.shape[1]):
            sdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 0]=tmpd[:,z,l]
            pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 0]=xdata
            if znum is not None: pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 1] = zdata[z]
            if lnum is not None: pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 2] = ldata[l]
            if lnum is not None and znum is None: pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 1] = 0
            nz+=1

    dir = 'x' + str(xnum) + '_y' + str(ynum) + '_z' + str(znum) + '_l' + str(lnum) + '.csv'
    np.savetxt(dir,np.hstack([pdata,sdata]), delimiter=",")
    return dir

def prepare_data(cnfg):
    dataname = cnfg['dataname'];  exceptnum = cnfg['exceptnum']
    exceptval = cnfg['exceptval'];exceptreq = cnfg['exceptreq']
    fixparam = cnfg['fixparam'];  paramrow = cnfg['paramrow']
    xnum = cnfg['xnum'];xmin = cnfg['xmin'];xmax = cnfg['xmax']
    ynum = cnfg['ynum']
    znum = cnfg['znum'];zmin = cnfg['zmin'];zmax = cnfg['zmax']
    lnum = cnfg['lnum'];lmin = cnfg['lmin'];lmax = cnfg['lmax']

    with open(dataname) as f: data = [row for row in csv.reader(f)]

    if exceptnum is not None: data=dataexcept(data, exceptnum, exceptval, exceptreq, ynum)
    if fixparam != None: data=datafilter(data, fixparam)

    sysparam, nump=g.get_sysparam(data,paramrow)
    data=make_graphdata(data,sysparam,nump,xnum,ynum,znum,lnum)

    if xmin is not None or xmax is not None: data, sysparam, nump = rangelimit(data, sysparam, nump, xnum, xmin, xmax,0)
    if zmin is not None or zmax is not None: data, sysparam, nump = rangelimit(data, sysparam, nump, znum, zmin, zmax,1)
    if lmin is not None or lmax is not None: data, sysparam, nump = rangelimit(data, sysparam, nump, lnum, lmin, lmax,2)

    return data, sysparam, nump

if __name__ == '__main__':

    configpath='config_0'

    cnfg = sc.get_config(configpath)
    dir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data, sysparam, nump = prepare_data(cnfg)
    path = save_graph_data(data, sysparam, cnfg)

    if not os.path.exists(dir): os.mkdir(dir)
    shutil.copyfile('config/' + configpath + '.py', dir + '/config.py')
    os.rename(path, dir + '/' +path)