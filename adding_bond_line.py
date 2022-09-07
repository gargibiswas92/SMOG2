import sys

path = '/home_b/gargi/project_1/pts480/'                    
pdbtraj = open('/home_b/gargi/project_1/pts480/structure_3.link.pdb','r')
newfile = open("/home_b/gargi/project_1/pts480/bond3.pdb", "w")
trajlines = pdbtraj.readlines()
res_num1 = []
res_num2 = []
chain1 = []
chain2 = []
resi1 = []
resi2 = []
chain1s = []
chain2s = []
resi1s = []
resi2s = []
count = 0
p = 1
for line in trajlines:
    if line.startswith("LINK"):
        a = line[23:26]
        res_num1.append(a)
        b = line[53:56]
        res_num2.append(b)
        count = count + 1
for i in range(count):
    c = int(res_num1[i]) + 286
    d = int(res_num2[i]) + 356
    q = int(res_num2[i]) - 123
    
    resi1.append(c)
    chain1.append(p)
    resi2.append(d)
    chain2.append(q)
    
    re1 = str(resi1[i])
    resi1s.append(re1)
    re2 = str(resi2[i])
    resi2s.append(re2)
    ch1 = str(chain1[i])
    chain1s.append(ch1)
    ch2 = str(chain2[i])
    chain2s.append(ch2)
    
    pq = [ 'BOND'," ", chain1s[i], " ", resi1s[i], " ", chain2s[i], " ", resi2s[i], " " 'bb', "\n"]
    newfile.writelines(pq)

newfile.close()
pdbtraj.close()
