dl_cnfg = []; rfr = []

# data1
path = 'stat_statof_converted.csv'
lrn = 8
frm = 9
dl_cnfg.append([path ,lrn ,frm])
rfrd =[]

#mov and flash y0y0 17 color
id =[[0,0],[2,0],[3,16],[5, 0],[7, 0], [10,17], [11,0]]
fixpara = id
row = [1,19]
rfrd.append([fixpara, row])

# flash y0y0 18 color
id =[[0,0],[2,0],[3,16],[5, 0],[7, 0], [10,18], [11,0]]
fixpara = id
row = [19]
rfrd.append([fixpara, row])

rfr.append(rfrd)