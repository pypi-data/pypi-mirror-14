from pytem import PyTem

pt = PyTem()
s = pt.expandFile('pytem_demo4.tm', {'greeting': 'Hello',  'name': 'George'})
print(s)
