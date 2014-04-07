import sys

initname = raw_input('Which domain would you like to load? cl or ch1?\n')
filename=initname+'_sasa.dat'

if filename[0:2]=='ch': domain=['H', 123]
elif filename[0:2]=='cl': domain=['L', 112]
else:
  print 'FATAL ERROR: the format of input file name is not defined!'
  sys.exit()

with open(filename) as f:
    array = [i.split() for i in f.readlines()]

del array[0:1] # delete heading of dat file

# /* area of whole amino acid */ His --> Hsd
amino_acid=['Cys' , 'Phe' , 'Leu' , 'Trp' , 'Val' , 'Ile' , 'Met' , 'Hsd' , 'Tyr' , 'Ala' , \
'Gly' , 'Pro' , 'Asn' , 'Thr' , 'Ser' , 'Arg' , 'Gln' , 'Asp' , 'Lys' , 'Glu']

amino_acid.extend([140., 218., 180., 259., 160., 182, 204., 194., 229., 113., \
85., 143., 158., 146., 122., 241., 189., 151., 211., 183.])

# hydrophobic (Cys, Phe, Ile, Leu, Trp, Val, Met, Tyr and Ala) 
# polar (Gly, Pro, Asn, Thr, Ser, Gln and His) His --> Hsd
# positively charged (Arg and Lys)
# negatively charged (Asp and Glu).
type=[]
type.append(['Cys', 'Phe', 'Ile','Leu', 'Trp', 'Val', 'Met', 'Tyr', 'Ala'])
type.append(['Gly', 'Pro', 'Asn', 'Thr', 'Ser', 'Gln', 'Hsd']) 
type.append(['Arg', 'Lys'])
type.append(['Asp', 'Glu'])

type_sign=['1','2','+','-']

# laod original pdb file to find secondary structure

load_pdb = open('1fh5.pdb', "r")
read_pdb = load_pdb.read()
sec_list = []

for line in read_pdb.splitlines():
    if "HELIX" in line: sec_list.append(line.split()[0:9])
    if "SHEET" in line: sec_list.append(line.split()[0:10])
# !print sec_list

# CH1 domain of Igg residues 123 - 215
# CL domain of Igg residues 112 - 214
helix=[]; sheet=[];  k=1; h=0
# loading HELIX
for i in xrange(len(sec_list)):
    if sec_list[i][0]=="HELIX":
       if sec_list[i][7]==domain[0]:
          if int(sec_list[i][5])>domain[1] and int(sec_list[i][8])>domain[1]:
#!            print int(sec_list[i][5])-domain[1], sec_list[i][5], int(sec_list[i][8])-domain[1], sec_list[i][8]
            lower=int(sec_list[i][5])-domain[1]
            upper=int(sec_list[i][8])-domain[1]
            for j in xrange(upper-lower+1): helix.append([lower+j, 'H%d'%k])
            k=k+1

# loading SHEET
k=1;
for i in xrange(len(sec_list)):
    if sec_list[i][0]=="SHEET":
       if sec_list[i][8]==domain[0]:
          if int(sec_list[i][6])>domain[1] and int(sec_list[i][9])>domain[1]:
#!            print int(sec_list[i][6])-domain[1], sec_list[i][6], int(sec_list[i][9])-domain[1], sec_list[i][9]
            lower=int(sec_list[i][6])-domain[1]
            upper=int(sec_list[i][9])-domain[1]
            for j in xrange(upper-lower+1): sheet.append([lower+j, 'S%d'%k])
            k=k+1

#! print helix, sheet
# claculations and finilazing
s=0;
outputfile=open(initname + '_sasa_complete.dat', 'w')
template="{0:10} {1:10} {2:10} {3:10} {4:11} {5:10} {6:5} {7:10}"
print template.format('Index', 'SASA', 'Resname', 'X value', 'Gly_res_Gly', 'R', 'Type', 'Sec Struc')
print >> outputfile, template.format('Index', 'SASA', 'Resname', 'X value', 'Gly_res_Gly', 'R', 'Type', 'Sec Struc')


for i in xrange(len(array)):
     restype=''; j=0
     index=array[i][0]; sasa=round(float(array[i][1]),3); resname=array[i][2]; r=array[i][3]
     x=amino_acid[amino_acid.index(resname.capitalize())+20]
     while restype=='':
        try: restype=type[j].index(resname.capitalize())
        except ValueError: j=j+1
     gly_x_gly=round(sasa/x,3)
     sec_id='0'
     if h < len(helix): 
        if i==int(helix[h][0])-1: sec_id=helix[h][1]; h=h+1
     if s < len(sheet):
        if i==int(sheet[s][0])-1: sec_id=sheet[s][1]; s=s+1       
     print template.format(str(index), str(sasa), resname, str(x), str(gly_x_gly), str(r), type_sign[j], sec_id)
     print >> outputfile, template.format(str(index), str(sasa), resname, str(x), str(gly_x_gly), str(r), type_sign[j], sec_id)
