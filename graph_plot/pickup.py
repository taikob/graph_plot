from graph_plot import data_processing as dp
import numpy as np
import csv, os, sys, datetime, shutil

def get_config():
    if not os.path.exists('config/config.py'):
        print('config file is not here! ', 'config/config_pickup.py')
        sys.exit()

    sys.path.append(os.getcwd()+'/config')
    import config_pickup as p

    cnfg = {}
    cnfg['rfr'] = p.rfr
    cnfg['dl_cnfg'] = p.dl_cnfg
    cnfg['pk_cnfg'] = p.pk_cnfg

    return cnfg

def get_datalist(dl_cnfg,rfr):
    for i in range(len(dl_cnfg)):
        with open(dl_cnfg[i][0]) as f: data = [row for row in csv.reader(f)]
        for j in range(len(rfr[i])):
            de = np.array(dp.datafilter(data, rfr[i][j][0]))
            dle = np.empty((de.shape[0], 3))#data list element
            dle[:,0] = de[:,dl_cnfg[i][1]]
            dle[:,1] = de[:,dl_cnfg[i][2]]
            dle[:,2] = de[:,rfr[i][j][1]]
            if 'dl' in locals(): dl = np.hstack((dl, dle[:,2]))
            else: dl = dle

    np.savetxt('datalist.csv',dl, delimiter=",")
    return dl

def pickup(data,pk_cnfg):
    pl = []; count = {}; cnt = 0 #pickup list
    for d in data:
        for i, c in enumerate(pk_cnfg):
            if eval(str(d[i+2]) + c):
                if not d[i] in count: count[d[i]] = 1
                pl.append([d[0],d[1]]); cnt += 1

    pl = np.array([[len(count), cnt]] + pl)
    np.savetxt('pickup.csv',pl,delimiter=',')
    return pl

if __name__ == '__main__':
    cnfg = get_config()
    dl = get_datalist(cnfg['dl_cnfg'],cnfg['rfr'])
    pl = pickup(dl,cnfg['pk_cnfg'])

    dir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if not os.path.exists(dir): os.mkdir(dir)
    shutil.copyfile('config/config.py', dir + '/config.py')
    os.rename('datalist.csv', dir + '/datalist.csv')
    os.rename('pickup.csv', dir + '/pickup.csv')
