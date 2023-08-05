from pytem import PyTem

infilename = './pytem_demo2.tm'
outfilename = './PYTEM_demo2.out'
pyfile = True
debug = 0x0100


with open(infilename,'r') as f:
  intext = f.read()

pt = PyTem( pyfile=pyfile, debug=debug )

s = pt.expandString( intext, infilename, {'sally': "Salty"}, dick="Dick Tracy")

with open(outfilename,'w') as f:
  f.write(s)
