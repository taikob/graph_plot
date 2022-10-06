import os, sys

def set_config():
    with open('config.py','w:') as f:
        f.write('#import numpy as np\n')
        f.write('#dataname:\n')
        f.write('#fitdata:\n')
        f.write('#paramrow:\n')
        f.write('#xnum:\n')
        f.write('#ynum:\n')
        f.write('#znum:\n')
        f.write('#lnum:\n')
        f.write('#fixparam:\n')
        f.write('#addt:\n')
        f.write('#ap:\n')
        f.write('#tc:\n')
        f.write('#pc:\n')
        f.write('#minus:\n')
        f.write('#xmin:\n')
        f.write('#xmax:\n')
        f.write('#zmin:\n')
        f.write('#zmax:\n')
        f.write('#lmin:\n')
        f.write('#lmax:\n')
        f.write('#exceptnum:\n')
        f.write('#exceptval:\n')
        f.write('#exceptreq:\n')
        f.write('#Hfnum:\n')
        f.write('#Hlnum:\n')
        f.write('#ofnum:\n')
        f.write('#x_change:\n')
        f.write('#xlm:\n')
        f.write('#xmal:\n')
        f.write('#xmil:\n')
        f.write('#ylm:\n')
        f.write('#ymal:\n')
        f.write('#ymil:\n')
        f.write('#xlog:\n')
        f.write('#xline:\n')
        f.write('#yline:\n')
        f.write('#xtitle:\n')
        f.write('#ytitle:\n')
        f.write('#cl:\n')
        f.write('#nogrid:')

def get_config(cwd,configpath,fixparaml=None):

    if configpath is None or configpath is '':
        print('Please set config file!')
        set_config(); sys.exit()
    elif not os.path.exists('config/'+configpath+'.py'):
        print('config file is not here! ', 'config/'+configpath+'.py')
        sys.exit()

    sys.path.append(cwd+'/config')
    exec('import ' + configpath + ' as p')

    cnfg = {}
    cnfg['dataname'] = p.dataname
    cnfg['fixparam'] = fixparaml
    cnfg['exceptnum'] = p.exceptnum
    cnfg['exceptval'] = p.exceptval
    cnfg['exceptreq'] = p.exceptreq
    cnfg['paramrow'] = p.paramrow
    cnfg['xnum'] = p.xnum
    cnfg['ynum'] = p.ynum
    cnfg['znum'] = p.znum
    cnfg['lnum'] = p.lnum
    cnfg['xmin'] = p.xmin
    cnfg['xmax'] = p.xmax
    cnfg['zmin'] = p.zmin
    cnfg['zmax'] = p.zmax
    cnfg['lmin'] = p.lmin
    cnfg['lmax'] = p.lmax
    cnfg['tc'] = p.tc
    cnfg['cl'] = p.cl
    cnfg['gl'] = '-o'
    cnfg['pc'] = p.pc
    cnfg['addt'] = p.addt
    cnfg['lineplot'] = None
    cnfg['xtitle'] = p.xtitle
    cnfg['ytitle'] = p.ytitle
    cnfg['hsize'] = 1.89
    cnfg['vsize'] = 0.7
    cnfg['xlog'] = p.xlog
    cnfg['ylog'] = p.ylog
    cnfg['nogrid'] = p.nogrid
    cnfg['xlm'] = p.xlm
    cnfg['xmal'] = p.xmal
    cnfg['xmil'] = p.xmil
    cnfg['ylm'] = p.ylm
    cnfg['ymal'] = p.ymal
    cnfg['ymil'] = p.ymil
    cnfg['xtick'] = p.xtick
    cnfg['ytick'] = p.ytick
    cnfg['xline'] = p.xline
    cnfg['yline'] = p.yline
    cnfg['mksize'] = 3
    cnfg['lnsize'] = 0.5
    cnfg['dashline'] = None
    cnfg['fitdata'] = None
    cnfg['xplotnum'] = p.xplotnum
    cnfg['yplotnum'] = p.yplotnum
    cnfg['wspace'] = p.wspace
    cnfg['hspace'] = p.hspace
    cnfg['title'] = p.title


    if hasattr(p,'lineplot'): cnfg['lineplot']=p.lineplot
    if hasattr(p,'hsize' ): cnfg['hsize']=p.hsize
    if hasattr(p,'vsize' ): cnfg['vsize']=p.vsize
    if hasattr(p,'mksize'): cnfg['mksize']=p.mksize
    if hasattr(p,'lnsize'): cnfg['lnsize']=p.lnsize
    if hasattr(p, 'gl'): cnfg['gl'] = p.gl
    if fixparaml == None: cnfg['fixparam'] = p.fixparam

    return cnfg