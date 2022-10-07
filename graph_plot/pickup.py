import csv, os, sys, datetime, shutil,copy
from graph_plot import data_processing as dp
import numpy as np

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
    cnfg['stmpath'] = p.stmpath
    cnfg['copyfile'] = p.copyfile

    return cnfg

def get_datalist(dl_cnfg,rfr):
    for i in range(len(dl_cnfg)):
        with open(dl_cnfg[i][0]) as f: data = [row for row in csv.reader(f)]
        for j in range(len(rfr[i])):
            de = np.array(dp.datafilter(copy.deepcopy(data), rfr[i][j][0]))
            dle = np.empty((de.shape[0], 3))#data list element
            if de.shape[0] == 0: print('there are no data in fixeddata');sys.exit()
            dle[:,0] = de[:,dl_cnfg[i][1]]
            dle[:,1] = de[:,dl_cnfg[i][2]]
            dle[:,2] = de[:,rfr[i][j][1]]
            if 'dl' in locals(): dl = np.hstack((dl, dle[:,2][:,np.newaxis]))
            else: dl = dle

    np.savetxt('datalist.csv',dl, delimiter=",")
    return dl

def pickup(data,pk_cnfg):
    pl = []; count = {}; cnt = 0 #pickup list
    for d in data:
        for i, c in enumerate(pk_cnfg):
            if str(d[i+2]) == 'nan' :break
            if not eval(str(d[i+2]) + c): break

            if  i == len(pk_cnfg)-1:
                if not d[0] in count: count[d[0]] = 1
                pl.append([d[0],d[1]]); cnt += 1

    pl = np.array([[len(count), cnt]] + pl)
    np.savetxt('pickup.csv',pl,delimiter=',')
    return pl

def pickup_image(stmpath, copyfile, pupath):
    pu = np.loadtxt(pupath,delimiter=',')
    pu = pu.tolist()

    dir =os.path.dirname(pupath) + '/puimg_'+copyfile.split('.')[0]
    if not os.path.exists(dir): os.makedirs(dir)

    if pu == [0,0]: print('there are no pickup model.'); sys.exit()
    del pu[0]
    for rl in pu:
        orname = stmpath + '/' + str(int(rl[0])) + '/' + str(int(rl[1])) + '.pth/' + copyfile
        cpname = dir + '/' + str(int(rl[0])) + '_' + str(int(rl[1])) + os.path.splitext(copyfile)[-1]
        shutil.copyfile(orname, cpname)

if __name__ == '__main__':
    cnfg = get_config()
    dl = get_datalist(cnfg['dl_cnfg'],cnfg['rfr'])
    pl = pickup(dl,cnfg['pk_cnfg'])

    dir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if not os.path.exists(dir): os.mkdir(dir)
    shutil.copyfile('config/config.py', dir + '/config.py')
    os.rename('datalist.csv', dir + '/datalist.csv')
    os.rename('pickup.csv', dir + '/pickup.csv')

    pupath = dir + '/pickup.csv'
    stmpath = '../result/net0/st0_ln20_li0_imsw2_read_list.txt'
    copyfile = 'test_14y_0.jpg'

    pu = np.loadtxt(pupath, delimiter = ',')
    pickup_image(stmpath, copyfile, pupath)