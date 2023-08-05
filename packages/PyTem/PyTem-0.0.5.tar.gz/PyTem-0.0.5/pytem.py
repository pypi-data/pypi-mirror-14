'''
PyTem is a simple implementation of the Python Server Pages style
of templating.
'''

import sys, re, os
from io import StringIO

__all__ = [ 'PyTem' ]

DBG_CACHE             = 0x8000    # Trace caching of compiled templates.
DBG_CODE              = 0x4000    # Dump intermediate (python source for template) to stderr.
debug_mask = 0
def dbg( bits, msg):
  if debug_mask & bits:
    errout( msg)  
def errout(msg):
  print(">>> "+msg, file=sys.stderr)


def build_env(*kv_dicts, **kv_vars):  
    env = {}
    for m in kv_dicts:
      env.update(m)
    env.update(kv_vars)
    return env


class PyTem:
    def __init__(self, search_path = ['.'], debug = 0):
        global debug_mask
        debug_mask = debug
        self.search_path = (search_path 
                              if '.' in search_path
                              else search_path + ['.'])
        self.compiled_cache = {}


    def _get_input_path_and_file(self, infilename):
      '''
      infilename is one of 
        '<stdin>'                 
              returns ('<stdin>', sys.stdin)
        An absolute-file-path     
              returns (absolute-file-path,  file-object) 
        A relative-file-path
              returns (absolute-file-path,  file-object) 
      '''
      if infilename == '<stdin>':
        return ('<stdin>', sys.stdin)
      if infilename[0] == '/':
        return (infilename, open(infilename,'r'))           

      for p in self.search_path:
          ftry = os.path.join(p, infilename)
          #errout("_get_file_name trying %r" % ftry)
          if os.path.isfile(ftry):
            try:
              return (ftry, open(ftry, 'r'))
            except FileNotFoundError:
              continue
      raise RuntimeError( "_get_input_path_and_file: %r not found" % infilename )


    def compileString(self, text, infilename='<string>'):
      '''
      text            The lines of the template to be compiled.
      infilename      An identifier for the string being compiled.
                      If text came originally from a file, then the
                      file name would be appropriate.
      Returns a code_object (compiled python code).
      '''
      inlines = text.rstrip().split('\n')
      outlines = []
      indent = 0
      line_num = 0
      dbg(DBG_CODE, ("Intermediate code for template %r" % infilename))
      for line in inlines:
        line_num += 1

        if line.startswith('%'):
          line = line[1:].strip()
          while True:     # break target, not a loop!
            mo = re.match( r'^end$', line)
            if mo:                        # python block 'end' statement 
              if indent < 2:
                raise RuntimeError("Unexpected python block 'end' statement.")
              indent -= 2
              outlines.append('\n')
              break

            mo = re.match( r'^(else:)|(elif.*:)$', line)
            if mo:                        # python block 'else' or 'elif' statement 
              if indent < 2:
                raise RuntimeError("Unexpected 'else' or elif statement.")
              outlines.append(' '*(indent-2) + line + '\n')
              break

            if len(line):                 # other python statement
              outlines.append(' '*indent + line + '\n')
              if line[-1]==':':
                indent = indent + 2
              break

            else:                         # python block empty statement
              outlines.append('\n')
              break

        else:
          linelist = [ "print(" ]
          while True:
            mo = re.search( r'^(.*?)<%(.*?)%>(.*)$', line)
            if mo==None:
              #errout("no more holes")
              break
            #errout(pre: %r then hole: %r" % (mo.group(1),mo.group(2)))
            linelist.append( "%r+str(eval(%r))+" % (mo.group(1),mo.group(2)))
            #linelist.append( "%r+str(eval(%r,globals(),locals()))+" % (mo.group(1),mo.group(2)))
            line = mo.group(3)

          linelist.append( "%r)\n" % line)
          line = str.join('', linelist)
          outlines.append( ' '*indent + line)

        dbg(DBG_CODE, ("%4d %s" %  (line_num, outlines[-1].rstrip())))

      return compile( str.join('',outlines), infilename, 'exec')

    def compileFile(self,infilename):
      '''
      infilename is one of:
        '<stdin>'             Compile lines from standard input.
        Absolute file path    Compile lines from the specified file.
        Relative file path    Compile lines from the file located relative
                              to the directories in search_path.
      Returns a code_object (compiled python code).
      '''
      if infilename in self.compiled_cache:
        dbg(DBG_CACHE, "Using cached template for %r" % infilename)
        return self.compiled_cache[infilename]
      (input_path, infile) = self._get_input_path_and_file(infilename)
      text = infile.read()
      infile.close()
      code_object = self.compileString(text, input_path)
      self.compiled_cache[infilename] = code_object
      return code_object


    def expand(self, code_object, *kv_dicts, **kv_vars):
      '''
      Expand the compiled template (code_object) using environment built from:
          kv_dicts      0 or more dictionaries of key/values (variable/values).
          kv_vars       0 or more individual key/values (variable/values).
      '''
      env = build_env( *kv_dicts, **kv_vars)
      #errout("expand env is %r" % (env,))
      def include_template( infilename, **arg_kv_vars):
        #errout("include_template env is %r" % (env,))
        return self.expandFile(infilename, env, **arg_kv_vars).rstrip()
      env['include_template'] = include_template


      save_stdout = sys.stdout
      sys.stdout = StringIO()
      exec(code_object, env)
      s = sys.stdout.getvalue()
      sys.stdout = save_stdout
      return s


    def expandFile(self, infilename, *kv_dicts, **kv_vars):
      "Convenience function: combines compileFile and expand."
      code_object = self.compileFile(infilename)
      return self.expand( code_object, *kv_dicts, **kv_vars)


    def expandString(self, 
        template_string,   #[ infilename,]
        *kv_dicts,         **kv_vars):
      '''
      Convenience function: combines compileString and expand. 
      NOTE: The infilename argument is optional !!!
      '''
      kv_dicts = list(kv_dicts)
      if kv_dicts and isinstance(kv_dicts[0],str):
          infilename = kv_dicts.pop(0)
      else:
          infilename = "<string>"
      code_object = self.compileString(template_string, infilename)
      return self.expand( code_object, *kv_dicts, **kv_vars)


def usage(msg=''):
  '''
  Help for command line usage.
  '''
  if(msg):
    sys.stderr.write(msg+'\n')
  sys.stderr.write("Usage:  python pytem.py [options]\n")
  sys.stderr.write("Options\n")
  sys.stderr.write("  (-s | --search_path)  path1,path2,...\n")
  sys.stderr.write("  (-d | --debug)        debug mask bits\n")
  sys.stderr.write("                        0x8000  Trace caching, compiled templates\n")
  sys.stderr.write("                        0x4000  Show python source\n")
  sys.stderr.write("                                for compiled templates.\n")
  sys.stderr.write("  (-e | --env)          Env file name\n")
  sys.stderr.write("                        File contains a python dictionary\n")
  sys.stderr.write("  (-i | --in)           In file name\n")
  sys.stderr.write("  (-o | --out)          Out file name. Defaults to '<stdout>'\n")
  sys.exit(1)
    
def run():
  '''
  Command line use.  Get options from sys.argv.
  '''
  args = sys.argv
  args.pop(0)
  errout("args list is %r" % (args,))


  debug = 0
  search_path = ['.']
  infilename = '<stdin>'
  outfilename = '<stdout>'

  if( len(args) == 0):
    usage()

  while len(args):
    arg = args.pop(0)
    if arg == '-h' or arg == '--help' or arg == 'help':
      usage()
    elif arg == '-s' or arg == '--search_path':
        search_path = re.split(r' *, *', args.pop())
    elif arg == '-d' or arg == '--debug':
        debug = int(args.pop(0),0)
    elif arg == '-e' or arg == '--env':
        envfilename = args.pop(0)
    elif arg == '-i' or arg == '--in':
        infilename = args.pop(0)
    elif arg == '-o' or arg == '--out':
        outfilename = args.pop(0)
    else:
        usage("Unrecognized command line argument, %r" % (arg,))


  with open(envfilename,'r') as f:
    s = f.read()
  env = eval(s)
  errout("env is %r", env)

  outfile = ( sys.stdout
              if outfilename == '<stdout>'
              else open(outfilename, 'w'))

  pt = PyTem( search_path, debug )
  s = pt.expandFile( infilename, env)
  outfile.write(s)
  outfile.close()

if __name__ == '__main__':
    run();
    sys.exit(0)
