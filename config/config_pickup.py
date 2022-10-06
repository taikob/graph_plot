dl_cnfg = []; rfr = []

# data1
path = 'stat_statof.csv'
lrn = 5
frm = 6
dl_cnfg.append([path ,lrn ,frm])

# para1
rfrd =[]
fixpara = [[0, 0],[1,2], [4, 0], [7, 15]]
row = 15
rfrd.append([fixpara, row])
# para2
fixpara = [[0, 0],[1,2], [4, 0], [7, 15]]
row = 17
rfrd.append([fixpara, row])

rfr.append(rfrd)

# pickup
pk_cnfg = []
c1 = '>5e-3'
c2 = '>10e0'
pk_cnfg+=[c1,c2]