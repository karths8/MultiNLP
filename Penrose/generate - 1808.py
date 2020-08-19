import re
import string
inp = '''A is a set.
A, B, C are sets.
B is contained in A. 
C is contained in B.
C is a set.
C is contained in A.
P is a point.
P is contained in A.
P is not contained in C.
X is a vectorspace.
U is a vector.
V is a vector.
U and V belong to the vectorspace X.
X is the vectorspace to which U and V belong.
U and V are orthogonal vectors.
U and V are equal vectors.
U and V have equal lengths.
U and V make an angle of 45 degrees with each other.
W=U+V.
W is equal to the sum of U and V.
W is the dot product of U and V.
P is a point.
P,Q,R,S are points.
A is a segment.
A,B,C,D are segments.
T is an angle.
T,U,V are angles.
T is a triangle.
W is a ray.
W is a bisector to T.
W is a perpendicular bisector to A.
A and B are sets.
C and D are sets.
P and Q are sets.
F is a function.
F,G,H are functions.
F is an injective function from A to B.
G is a surjective function from C to D.
H is a bijective function from P to Q.
F is an injective function from A to B.
G is a surjective function from B to C.
H is a bijective function from C to D.
S is a square.
R is a rectangle.
K is a right angled triangle.
K is a triangle with angles 60,40,80.'''
strs = inp.split('\n')
ent_keys=['set','sets','vector','vectorspace','point','points','segment','segments','angle','angles'
,'triangle','ray','function','functions','square','rectangle']
oper = ['dot product','sum','+','=','equal','orthogonal','right angled','angle of 45 degrees with each other','injective','bijective','surjective']

for idx,st in enumerate(strs):
  g= open(str(idx+1)+".txt", mode='w', encoding='utf-8')
  g.write(st)
  st_sub = re.sub(r"[,.;@#?!&$]+", ' ', st)
  f = open(str(idx+1)+".ann", mode='w', encoding='utf-8')
  t_count=1
  for obj in re.finditer('[0-9A-Z]+',st_sub):
    f.write('T'+str(t_count)+'\t'+'VAR'+' '+str(obj.start())+' '+str(obj.end())+'\t'+obj.group()+'\n')
    t_count+=1
  for ent in ent_keys:
    for obj in re.finditer(ent,st_sub):
      f.write('T'+str(t_count)+'\t'+'ATTR'+' '+str(obj.start())+' '+str(obj.end())+'\t'+ent+'\n')
      t_count+=1
  for op in oper:
    for obj in re.finditer(re.escape(op),st_sub):
      f.write('T'+str(t_count)+'\t'+'OPER'+' '+str(obj.start())+' '+str(obj.end())+'\t'+op+'\n')
      t_count+=1
f.close()
g.close()   
  