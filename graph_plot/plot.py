import datetime, shutil, os
import data_processing as d
import set_config as sc
import plot_data as p

dir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

cnfg = sc.get_config()
data, sysparam, nump = d.prepare_data(cnfg)
path = d.save_graph_data(data, sysparam, cnfg)
dt = p.plot(data,cnfg,sysparam=sysparam,nump=nump)

if not os.path.exists(dir): os.mkdir(dir)
shutil.copyfile('config/config.py', dir + '/config.py')
os.rename(path, dir + '/' +path)
os.rename('output_'+dt+'.pdf', dir+'/output_'+dt+'.pdf')
os.rename('legend_'+dt+'.pdf', dir+'/legend_'+dt+'.pdf')