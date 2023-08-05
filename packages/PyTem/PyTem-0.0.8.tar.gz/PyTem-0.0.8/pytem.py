'''
PyTem is a simple implementation of the Python Server Pages style
of templating.
'''

import sys, re, os
from io import StringIO

__all__ = [ 'PyTem' ]

DBG_CODE              = 0x4000    # Dump intermediate (python source for template) to stderr.
DBG_BASE              = 0x0100    # Minor messages.
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
    def __init__(self, search_path = ['.'], debug = 0, pyfile = False,  env={}):
        global debug_mask
        debug_mask = debug
        self.search_path = (search_path 
                              if '.' in search_path
                              else search_path + ['.'])
        self.pyfile = pyfile

        self.compiled_cache = {}

        self.env = {}
        self.env.update(env)

        dbg(DBG_BASE, "search_path %r, pyfile %r, debug 0x%04x, env %r" % 
                      (self.search_path, self.pyfile, debug_mask, self.env))



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
          line_pieces = []
          while True:
            mo = re.search( r'^(.*?)<%(.*?)%>(.*)$', line)
            if mo==None:
              #errout("no more holes")
              break
            if mo.group(1): line_pieces.append( repr(mo.group(1)) )
            line_pieces.append( 'str(eval(%r))' % (mo.group(2),))
            line = mo.group(3)

          if line: line_pieces.append( repr(line) )
          line = str.join('+', line_pieces)
          outlines.append( ' '*indent + 'print(' + line + ')\n')

        dbg(DBG_CODE, ("%4d %s" %  (line_num, outlines[-1].rstrip())))

      py = str.join('',outlines)
      if self.pyfile:
        with open(infilename+'.py','w') as f:
          f.write(py)
      return compile( py, infilename, 'exec')

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
        dbg(DBG_BASE, "Using cached template for %r" % infilename)
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
      self.env.update( build_env( *kv_dicts, **kv_vars))
      def include_template( infilename, **arg_kv_vars):
        return self.expandFile(infilename, **arg_kv_vars).rstrip()
      self.env['include_template'] = include_template


      save_stdout = sys.stdout
      sys.stdout = StringIO()
      exec(code_object, self.env)
      s = sys.stdout.getvalue()
      sys.stdout = save_stdout
      return s


    def expandFile(self, infilename, *kv_dicts, **kv_vars):
      "Convenience function: combines compileFile and expand."
      dbg(DBG_BASE, "expandFile %r." % infilename)
      code_object = self.compileFile(infilename)
      return self.expand( code_object, *kv_dicts, **kv_vars)


    def expandString(self, 
        template_string,   infilename,
        *kv_dicts,         **kv_vars):
      '''
      Convenience function: combines compileString and expand.
        template_string
        infilename
        kv_dicts            dictionaries
        kv_vars             individual key/value pairs
      '''
      dbg(DBG_BASE, "expandString %r." % infilename)
      code_object = self.compileString(template_string, infilename)
      return self.expand( code_object, *kv_dicts, **kv_vars)


def usage(msg=''):
  '''
  Help for command line usage.
  '''
  if(msg):
    sys.stderr.write(msg+'\n')
  sys.stderr.write("Usage:  python pytem.py [options] infile, ...\n")
  sys.stderr.write("Options\n")
  sys.stderr.write("  (-h | --help          This help message.\n")
  sys.stderr.write("  (-d | --debug)        debug mask bits\n")
  sys.stderr.write("  (-s | --search_path)  path1,path2,...\n")
  sys.stderr.write("                        0x4000  Show python source\n")
  sys.stderr.write("                                for compiled templates.\n")
  sys.stderr.write("                        0x0100  Minor messages\n")
  sys.stderr.write("  -p                    If true, output the compiled template (i.e. pure python)\n")
  sys.stderr.write("                        named 'infile' to 'infile.py' for debugging.\n")
  sys.stderr.write("  (-o | --out)          Out file name. Defaults to '<stdout>' if\n")
  sys.stderr.write("                        not specified.\n")
  sys.stderr.write("Expands infiles in order. Keeping environment from one to the next\n")
  sys.stderr.write("If no infiles specified, use <stdin>.\n")
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
  infilenames = []
  outfilename = '<stdout>'
  pyfile = False

  if( len(args) == 0):
    usage()

  while len(args):
    arg = args.pop(0)
    if arg[0] == '-':       # flag argument
      if arg == '-h' or arg == '--help':
        usage()
      elif arg == '-d' or arg == '--debug':
          debug = int(args.pop(0),0)
      elif arg == '-s' or arg == '--search_path':
          search_path = re.split(r' *, *', args.pop())
      elif arg == '-p':
          pyfile = True
      elif arg == '-o' or arg == '--out':
          outfilename = args.pop(0)
      else:
          usage("Unrecognized command line argument, %r" % (arg,))
    else:                    # non-flag argument (input file name)
      infilenames.append( arg)
      break

  while len(args):
    infilenames.append( args.pop(0))

  outfile = ( sys.stdout
              if outfilename == '<stdout>'
              else open(outfilename, 'w'))

  pt = PyTem( pyfile=pyfile, search_path=search_path, debug=debug )
  if len(infilenames) == 0:
    outfile.write(pt.expandFile( '<stdin>'))
  else:
    while len(infilenames):
      arg = infilenames.pop(0)
      outfile.write(pt.expandFile( arg ))
  outfile.close()

if __name__ == '__main__':
    run();
    sys.exit(0)
