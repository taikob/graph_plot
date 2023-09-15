import csv,os,datetime,shutil,copy
from graph_plot import set_config as sc
from data_prcs import get as g
import numpy as np

def datafilter(data, fixparam):
    newdata = copy.deepcopy(data)
    deldata = []
    for param in fixparam:
        for i in reversed(range(len(newdata))):
            if np.float128(newdata[i][param[0]])!=np.float128(param[1]):
                deldata.append(newdata[i])
                del newdata[i]
    deldata.reverse()
    return newdata,deldata

def dataexcept(data, exceptnum, exceptval, exceptreq, ynum):
    for i in range(len(data)):
        if len(data[i][exceptnum]) != 0:
            for y in ynum:
                if exceptreq == 1:
                    if float(data[i][exceptnum]) >= exceptval:
                        data[i][y] = 0
                if exceptreq ==-1:
                    if float(data[i][exceptnum]) <= exceptval:
                        data[i][y] = 0
                if exceptreq == 0:
                    if float(data[i][exceptnum]) == exceptval:
                        data[i][y] = 0
    return data

def make_graphdata(data,sysparam,nump,xnum,ynum,znum,lnum):

    aldata=np.zeros([nump[0],nump[1],nump[2],len(ynum)])
    aldata[:,:]=None
    xpara = sysparam[0];zpara = sysparam[1];lpara = sysparam[2]

    for li, l in enumerate(lpara):
        if lnum is not None:
            ldata=np.ndarray([0,len(data[0])],dtype='float128')
            ldata[:,:]=None
            for d in data:
                if np.float128(d[lnum])==l: ldata=np.vstack((ldata, d))
        else: ldata=data

        for zi, z in enumerate(zpara):
            if znum is not None:
                zdata=np.ndarray([0,len(data[0])],dtype='float128')
                zdata[:,:]=None
                for d in ldata:
                    if np.float128(d[znum]) == z: zdata=np.vstack((zdata, d))
            else: zdata=ldata

            for xi, x in enumerate(xpara):
                for d in zdata:
                    if np.float128(d[xnum]) == x:
                        for y in range(len(ynum)): aldata[xi][zi][li][y] = d[ynum[y]]

    return aldata

def rangelimit(data, sysparam, nump, xnum, xmin, xmax,ax):
    sspr = list(map((lambda x: float(x)), sysparam[xnum]))

    for i in reversed(range(len(sspr))):
        if xmin is not None:
            if sspr[i] < xmin:
                nump[xnum]-=1
                data=np.delete(data, i, ax)
                sysparam[xnum]=np.delete(sysparam[xnum], i)
        if xmax is not None:
            if sspr[i] > xmax:
                nump[xnum]-=1
                data=np.delete(data, i, ax)
                sysparam[xnum]=np.delete(sysparam[xnum], i)

    return data, sysparam, nump

def save_graph_data(data,sysparam,cnfg):
    xnum = cnfg['xnum']; ynum = cnfg['ynum']; znum = cnfg['znum']; lnum = cnfg['lnum']

    xdata=sysparam[0]
    if znum is not None: zdata=sysparam[1]
    if lnum is not None: ldata=sysparam[2]

    tmpd=data.copy()#tmpdata

    if znum==None and lnum!=None: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],3))
    elif znum==None: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],1))
    elif lnum==None: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],2))
    else: pdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],3))
    sdata=np.empty((tmpd.shape[0]* tmpd.shape[1]*tmpd.shape[2],len(ynum)))

    nz=0
    for l in range(tmpd.shape[2]):
        for z in range(tmpd.shape[1]):
            for y in range(len(ynum)):
                sdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), y]=tmpd[:,z,l,y]
            pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 0]=xdata
            if znum is not None: pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 1] = zdata[z]
            if lnum is not None: pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 2] = ldata[l]
            if lnum is not None and znum is None: pdata[tmpd.shape[0] * nz : tmpd.shape[0] * (nz + 1), 1] = 0
            nz+=1

    yname=''
    for y in ynum:yname+=str(y)+'_'
    yname=yname.rstrip('_')

    dir = 'x' + str(xnum) + '_y' + str(yname) + '_z' + str(znum) + '_l' + str(lnum) + '.csv'
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
    if fixparam != None: data,_=datafilter(data, fixparam)

    sysparam, nump=g.get_sysparam(data,[xnum,znum,lnum])
    data=make_graphdata(data,sysparam,nump,xnum,ynum,znum,lnum)

    if xmin is not None or xmax is not None: data, sysparam, nump = rangelimit(data, sysparam, nump, 0, xmin, xmax,0)
    if zmin is not None or zmax is not None: data, sysparam, nump = rangelimit(data, sysparam, nump, 1, zmin, zmax,1)
    if lmin is not None or lmax is not None: data, sysparam, nump = rangelimit(data, sysparam, nump, 2, lmin, lmax,2)

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