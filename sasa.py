with open('ch1-sasa.dat') as f:
    array = [i.split() for i in f.readlines()]

del array[0:1]
# /* area of whole amino acid */ His --> Hsd

amino_acid=['Cys' , 'Phe' , 'Leu' , 'Trp' , 'Val' , 'Ile' , 'Met' , 'Hsd' , 'Tyr' , 'Ala' , \
'Gly' , 'Pro' , 'Asn' , 'Thr' , 'Ser' , 'Arg' , 'Gln' , 'Asp' , 'Lys' , 'Glu']

amino_acid.extend([140., 218., 180., 259., 160., 182, 204., 194., 229., 113., \
85., 143., 158., 146., 122., 241., 189., 151., 211., 183.])

# hydrophobic (Cys, Phe, Ile,Leu, Trp, Val, Met, Tyr and Ala) 
# polar (Gly, Pro, Asn, Thr, Ser, Gln and His) His --> Hsd
# positively charged (Arg and Lys)
# negatively charged (Asp and Glu).

type=[]
type.append(['Cys', 'Phe', 'Ile','Leu', 'Trp', 'Val', 'Met', 'Tyr', 'Ala'])
type.append(['Gly', 'Pro', 'Asn', 'Thr', 'Ser', 'Gln', 'Hsd']) 
type.append(['Arg', 'Lys'])
type.append(['Asp', 'Glu'])

type_sign=['0','1','+','-']

print type[0].index('Leu')

for i in xrange(len(array)):
     check=''; j=0
     index=array[i][0]; sasa=round(float(array[i][1]),3); resname=array[i][2]

     x=amino_acid[amino_acid.index(resname.capitalize())+20]
     while check=='':
        try: check=type[j].index(resname.capitalize())
        except ValueError: j=j+1
     gly_x_gly=round(sasa/x,3)
     template = "{0:3}|{1:10}| {2:6}|{3:7}"    
     print template.format(index, sasa, resname, x, gly_x_gly)

# whatever       
# gly_x_gly(array[i][2]) 

#template = "{0:8}{1:10}{2:15}{3:7}" # column widths: 8, 10, 15, 7, 10

# print template.format("Index", "SASA", "Type", "R") # header

#for rec in array: 
#    print template.format(*rec)

print amino_acid[5], amino_acid[25]
#print amino_acids.index('Gly'), amino_acids[amino_acids.index('Gly')+20]
