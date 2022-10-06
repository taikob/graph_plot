dl_cnfg = []; rfr = []

# data1
path = '../result/stat_stater.csv'
lrn = 5
frm = 6
dl_cnfg.append([path ,lrn ,frm])

# para1
rfrd =[]
fixpara = [[0, 0], [4, 2], [7, 15]]
row = 8
rfrd.append([fixpara, row])

rfr.append(rfrd)

# pickup
pk_cnfg = []
c1 = '>4e-1'
pk_cnfg.append(c1)