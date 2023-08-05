import sys
from pytem import PyTem

infilename = './pytem_demo1.tm'
outfilename = './pytem_demo1.out'
pyfile = True


pt = PyTem( pyfile=pyfile, search_path=['.'], debug=0x0100 )

s = pt.expandFile( infilename, {'tom': "Tom Thumb"}, dick="Dick Tracy")
#print( s)
with open(outfilename,'w') as f:
  f.write(s)

sys.exit(0)