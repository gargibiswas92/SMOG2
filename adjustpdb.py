import sys

path = '/home_b/gargi/project_1/test_on_PTS/smog/new_str_2/new_smog/'                    
pdbtraj = open('/home_b/gargi/project_1/test_on_PTS/smog/new_str_2/new_smog/input_new.pdb','r')
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

s1 = '   CA'
s2 = '   C1'

newfile = open("/home_b/gargi/project_1/test_on_PTS/smog/new_str_2/new_smog/calpha.pdb", "w")
        
for i in range(count):
    if at_name[i] == s1 or at_name[i] == s2:
        p = [atomtype[i], res_num[i], at_name[i], res_name[i], res_num[i], cord_x[i], cord_y[i], cord_z[i], occu[i], temp_fact[i], element[i], "\n"]
        newfile.writelines(p)
    else:
        continue

newfile.close()
pdbtraj.close()
    
