print('A plain first line.')
#
# Two lines of python comments.
steve="beisner"
mel="palacio"
print('Expand "steve" and "mel":')
#
print('    steve first: '+str(eval('steve'))+', then mel: '+str(eval(' mel ')))
print('Expand "tom" and "dick":')
print('    tom: '+str(eval('  tom  ')))
print('    dick: '+str(eval('dick')))
print()
tom = tom.upper()
mel = mel.upper()
print('This is fancy '+str(eval(' "%s/%s/%s" % ("2016", "02", "25") ')))
for ii in range(1,4):
  print('    Loop count is '+str(eval(' ii '))+', friend.')
  if ii % 2 == 0:
    print('tom is '+str(eval(' tom '))+', dick is '+str(eval('dick'))+'.')
    print('steve is '+str(eval(' steve '))+', mel is '+str(eval(' mel '))+'.')
  else:
    print('dick is '+str(eval('dick'))+', tom is '+str(eval(' tom '))+'.')
    print('mel is '+str(eval(' mel '))+', steve is '+str(eval(' steve '))+'.')


print(str(eval("include_template('pytem_demo1_incl.tm', sally='Ride')")))
print('Line with a numeric expr: '+str(eval('100 * 123'))+". That's what!")
print('% escaped line, not python')
print('line with <% an escaped %>'+' hole.')
print('This is the last line.')
