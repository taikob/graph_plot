import datetime, shutil, os
import data_processing as d
import set_config as sc
import plot_data as p
import numpy as np

configpath ='config_0'
dir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

cnfg = sc.get_config(configpath)
data, sysparam, nump = d.prepare_data(cnfg)
path = d.save_graph_data(data, sysparam, cnfg)
dt = p.plot(np.loadtxt(path,delimiter=','),cnfg)

if not os.path.exists(dir): os.mkdir(dir)
shutil.copyfile('config/' + configpath + '.py', dir + '/config.py')
os.rename(path, dir + '/' +path)
os.rename('output_'+dt+'.pdf', dir+'/output_'+dt+'.pdf')
os.rename('legend_'+dt+'.pdf', dir+'/legend_'+dt+'.pdf')