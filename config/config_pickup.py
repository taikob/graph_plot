dl_cnfg = []; rfr = []

# data1
path = '../exp2/result/stat_statof.csv'
lrn = 5
frm = 6
dl_cnfg.append([path ,lrn ,frm])

rfrd =[]
# para1
fixpara = [[0, 2],[1,2], [4, 0], [7, 15]]
row = 15
rfrd.append([fixpara, row])
# para2
fixpara = [[0, 2],[1,2], [4, 0], [7, 15]]
row = 17
rfrd.append([fixpara, row])
# para3
fixpara = [[0, 2],[1,2], [4, 0], [7, 15]]
row = 17
rfrd.append([fixpara, row])
# para4
fixpara = [[0, 2],[1,1], [4, 0], [7, 15]]
row = 15
rfrd.append([fixpara, row])
# para5
fixpara = [[0, 2],[1,1], [4, 0], [7, 15]]
row = 17
rfrd.append([fixpara, row])
# para6
fixpara = [[0, 2],[1,1], [4, 0], [7, 15]]
row = 17
rfrd.append([fixpara, row])

rfr.append(rfrd)

# pickup
pk_cnfg = []
c1 = '>1e-3'
c2 = '>30e0'
c3 = '<150e0'
c4 = '>1e-3'
c5 = '>30e0'
c6 = '<150e0'
pk_cnfg+=[c1,c2,c3,c4,c5,c6]

#pickupimg
stmpath = '../result/net2/st2_ln5_li15_imsw0_read_list.txt'
copyfile = 'result_lk_15.jpg'