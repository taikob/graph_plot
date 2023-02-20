import csv, os, sys, datetime, shutil,copy
from graph_plot import data_processing as dp
import numpy as np

def get_config():
    if not os.path.exists('config/config.py'):
        print('config file is not here! ', 'config/config_pickup.py')
        sys.exit()

    sys.path.append(os.getcwd()+'/config')
    import config_datalist as d
    import config_pickup as p

    cnfg = {}
    if hasattr(p,     'rfr'): cnfg[     'rfr'] = d.rfr
    if hasattr(p, 'dl_cnfg'): cnfg[ 'dl_cnfg'] = d.dl_cnfg
    if hasattr(p, 'dl_path'): cnfg[ 'dl_path'] = p.dl_path
    if hasattr(p, 'pk_cnfg'): cnfg[ 'pk_cnfg'] = p.pk_cnfg
    if hasattr(p, 'stmpath'): cnfg[ 'stmpath'] = p.stmpath
    if hasattr(p,'copyfile'): cnfg['copyfile'] = p.copyfile

    return cnfg

def add_dl(dla,dl):
    nda = dla.shape[1]
    for i in range(dl.shape[1]-2): dla = np.insert(dla, dla.shape[1], 0, axis=1)

    for i in range(dla.shape[0]):
        for j in range(dl.shape[0]):
            if dla[i,0]==dl[j,0] and dla[i,1]==dl[j,1]: dla[i,nda:] = dl[j,2:]
    return dla

def get_datalist(dl_cnfg,rfr):
    for i in range(len(dl_cnfg)):
        with open(dl_cnfg[i][0]) as f: data = [row for row in csv.reader(f)]
        for j in range(len(rfr[i])):
            print('data: ',dl_cnfg[i][0],', reference: ',rfr[i][j])
            #data filtering
            de, data = dp.datafilter(data, rfr[i][j][0])
            if len(de) == 0: print('there are no data in fixeddata');sys.exit()
            if 'dl' in locals():
                if len(de)!=dl.shape[0]:
                    print('mismatch of number of lerning model: putdata = ' + str(len(de)) + ', datalist = ' + str(len(data)))
                    sys.exit()

            #making datalist
            de = np.array(de, dtype='float128')
            dle = np.empty((de.shape[0], 2+len(rfr[i][j][1])), dtype='float128')#dle: data list element
            for k in range(len(rfr[i][j][1])): dle[:,2+k] = de[:,rfr[i][j][1][k]]
            if 'dl' in locals(): dl = np.hstack((dl, dle[:,2:]))
            else:
                dle[:,0] = de[:,dl_cnfg[i][1]]
                dle[:,1] = de[:,dl_cnfg[i][2]]
                dl = dle
        if 'dla' in locals(): dla = add_dl(dla,dl)
        else: dla = dl
        del dl

    dla=dla.tolist()
    with open('datalist.csv', 'w') as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(dla)
    return dla

def pickup(data, pk_cnfg):
    #pickup
    pl = []; count = {}; cnt = 0  # pickup list
    for d in data:
        for i, c in enumerate(pk_cnfg):
            if str(d[c[0]]) == 'nan': break
            if not eval(str(d[c[0]]) + c[1]): break

            if i == len(pk_cnfg) - 1:
                if not d[0] in count: count[d[0]] = 1
                pl.append(list(d)); cnt += 1

    #save pickup data
    if len(pl)==0: pl = np.array([[len(count), cnt]])
    else: pl = np.array([[len(count), cnt] + [0] * (len(pl[0]) - 2)] + pl)
    np.savetxt('pickup.csv', pl, delimiter=',')

    print('number of pickuped learning: ' + str(len(count)) + ', model: ' + str(cnt))
    return pl

def pickup_image(stmpath, copyfile, pupath):
    pu = np.loadtxt(pupath,delimiter=',')
    pu = pu.tolist()

    dir =os.path.dirname(pupath) + '/puimg_'+copyfile.split('.')[0]
    if not os.path.exists(dir): os.makedirs(dir)

    if pu == [0,0]: print('there are no pickup model.'); sys.exit()
    del pu[0]
    for rl in pu:
        if len(str(rl[0]))!=14:
            rln = str(int(rl[0]))[:14];tmp=str(int(float(rl[0])))[14:]
            while len(tmp)>0: rln +='_'+str(int(float(tmp[:3])));tmp=tmp[3:]
        else: rln=str(int(rl[0]))
        orname = stmpath + '/' + rln + '/' + str(int(rl[1])) + '.pth/' + copyfile
        cpname = dir + '/' + rln + '_' + str(int(rl[1])) + os.path.splitext(copyfile)[-1]
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