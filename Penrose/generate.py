import re
with open('train.txt','r',encoding = 'utf-8') as k:
  full_text=k.read()	
strs = full_text.split('\n')
ent_keys=['set','vector','vectorspace','point','segment','angle','triangle','ray','function','square','rectangle']
oper = ['dot product','sum','+','=','equal','orthogonal','perpendicular','bisector','angle of 45 degrees with each other','contained','not contained']
types = ['injective','bijective','surjective','right angled']
rel_dict = {
    'SET':['set'],
    'VEC':['vector'],
    'VECSP':['vectorspace'],
    'PNT':['point'],
    'SEG':['segment'],
    'ANGL':['angle'],
    'TRI':['triangle'],
    'RAY':['ray'],
    'FUNC':['function'],
    'SQR':['square'],
    'RECT':['rectangle'],
    'DOT':['dot product'],
    'SUM':['sum','+'],
    'ASSIGN':['equal','='],
    'ORTH':['orthogonal','perpendicular'],
    'FNCTYPE':['injective','bijective','surjective']
}

def append_attr(count,tag,obj,f):
  f.write('T{}\t{} {} {}\t{}\n'.format(count,tag,obj.start(),obj.end(),obj.group()))
  count+=1
  return count

def write_entities():
  for idx,st in enumerate(strs):
    t_count=1
    f = open(str(idx+1)+".ann", mode='w', encoding='utf-8')
    with open(str(idx+1)+".txt", mode='w', encoding='utf-8') as g:
      g.write(st)
    for obj in re.finditer('[0-9A-Z]+',st):
      t_count = append_attr(t_count,'VAR',obj,f)
    for ent in ent_keys:
      plural=False
      for obj in re.finditer(ent+'s',st):
        plural=True
        t_count = append_attr(t_count,'ATTR',obj,f)
      if plural==False:
        for obj in re.finditer(ent,st):
          t_count = append_attr(t_count,'ATTR',obj,f)
    for op in oper:
      for obj in re.finditer(re.escape(op),st):
        t_count = append_attr(t_count,'OPER',obj,f)
    for t in types:
      for obj in re.finditer(t,st):
        t_count = append_attr(t_count,'TYP',obj,f)
    f_count=idx+2
  f.close()
  return f_count

def list_update(attr_list,var_list,op_list,type_list,item):
  tag=item[1]
  if tag=='ATTR':
      attr_list.append(item)
  elif tag=='VAR':
    var_list.append(item)
  elif tag=='OPER':
    op_list.append(item)
  elif tag=='TYP':
    type_list.append(item)
  return attr_list,var_list,op_list,type_list

def write_to_file(count,key,arg1,arg2,i):
  with open(str(i)+".ann",'a',encoding = 'utf-8') as g:
    g.write('R{}\t{} Arg1:{} Arg2:{}\n'.format(count,key,arg1,arg2))
  count+=1
  return count

def append_rel(itr_list,count,key,i,arg=None,rel_type='var'):
  if rel_type=='op':
    for idx,var in enumerate(itr_list):
      if idx==0:
        prev=var
      else:
        count = write_to_file(count,key,prev[0],var[0],i)
        prev=var
  else:
    for item in itr_list:
      count = write_to_file(count,key,arg,item[0],i)
  return count
    
def write_rels(f_count):
  for i in range(1,f_count):
    str_list,attr_list,var_list,op_list,type_list = ([] for _ in range(5))
    rel_count=1
    with open(str(i)+".ann",'r',encoding = 'utf-8') as f:
      text = f.read()
    strs = text.split('\n')
    for st in strs:
      str_list.append(st.replace('\t',' ').split(' '))
    for item in str_list:
      if item[0]!='':
        attr_list,var_list,op_list,type_list = list_update(attr_list,var_list,op_list,type_list,item)
    for key in rel_dict:
      for attr in attr_list:
          if attr[-1][:-1] in rel_dict[key]:
            rel_count = append_rel(var_list,rel_count,key,i,attr[0])
          elif attr[-1] in rel_dict[key] :
            rel_count = append_rel(var_list,rel_count,key,i,attr[0])
      for op in op_list:
          if op[-1] in rel_dict[key]:
            rel_count = append_rel(var_list,rel_count,key,i,rel_type='op')
      for typ in type_list:
          if typ[-1] in rel_dict[key]:
            rel_count = append_rel(attr_list,rel_count,key,i,typ[0])

def main():
  count = write_entities()
  write_rels(count)

if __name__=='__main__':
  main()