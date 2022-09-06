import sys

path = '/home_b/gargi/project_1/pts480/'                    
pdbtraj = open('/home_b/gargi/project_1/pts480/structure_3.hetatoms.pdb','r')
trajlines = pdbtraj.readlines()
atomtype = []
at_num = []
at_name = []
res_name = []
res_num = []
cord_x = []
cord_y = []
cord_z = []
occu = []
temp_fact = []
element = []
count = 0
for line in trajlines:
    if line.startswith(("ATOM", "HETATM")):
        a = line[0:6]
        atomtype.append(a)
        b = line[6:11]
        at_num.append(b)
        c = line[11:16]
        at_name.append(c)
        d = line[16:21]
        res_name.append(d)
        e = line[21:26]
        res_num.append(e)
        f = line[26:38]
        cord_x.append(f)
        g = line[38:46]
        cord_y.append(g)
        h = line[46:54]
        cord_z.append(h)
        m = line[54:60]
        occu.append(m)
        n = line[60:66]
        temp_fact.append(n)
        p = line[66:78]
        element.append(p)
        count = count + 1
        

newfile = open("/home_b/gargi/project_1/pts480/hetats3.pdb", "w")
at_num_int = []
res_num_int = []
at_num2 = []
res_num2 = []
for i in range(count):
    abc = int(at_num[i])+2982
    bcd = int(res_num[i])+356
    at_num_int.append(abc)
    res_num_int.append(bcd)
    cde = str(at_num_int[i])
    dep = str(res_num_int[i])
    at_num2.append(cde)
    res_num2.append(dep)
    p = [atomtype[i], ' ', at_num2[i], at_name[i], res_name[i],'  ', res_num2[i], cord_x[i], cord_y[i], cord_z[i], occu[i], temp_fact[i], element[i], "\n"]        
    newfile.writelines(p)

newfile.close()
pdbtraj.close()
