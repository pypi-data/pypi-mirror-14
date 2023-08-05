import sys
from pytem import PyTem

infilename = './pytem_demo_in.txt'

pt = PyTem( search_path=['.'], debug=0xC000 )

print(">>>>> Expand %r, first time." % infilename)
s = pt.expandFile( infilename, {'tom': "Tom Thumb"}, dick="Dick Tracy")
with open('./pytem_demo_out1.txt','w') as outfile:
  outfile.write(s)

print(">>>>> Expand %r, second time, different environment." % infilename)
s = pt.expandFile( infilename, {'tom': "The Bug Tom", 'dick': "Richard Nixon"})
with open('./pytem_demo_out2.txt','w') as outfile:
  outfile.write(s)


tem_string =  "<%   tom + '--' + dick %> <%tom.upper()%> ..."
print(">>>>> Expand string, %r." % tem_string)
s = pt.expandString(tem_string, "my-string", dict(tom="Thumb"),  dick="Tracy")
print(s)

sys.exit(0)