# PyTem Template Engine.

## Intro: What is PyTem?

PyTem is an implementation of a "Python-Server-Pages"-like template engine for Python 3+.
PyTem is, 

+ small -- a single python file.
+ simple  -- you can learn the syntax of templates and/or the PyTem API in just a few minutes.
+ hackable -- readable source code, so feel free to adapt it to your own python project.

PyTem's current status is "Alpha", but it is being used for real work on a daily basis.

PyTem can run as a standalone program from the command line, or can be imported into another Python 3 program and used via a small/simple API.

Copyright by Steve Beisner. Uses the MIT open source license.

## Installation

Install as python module:

```
pip install PyTem
```

Project source at [https://github.com/stevebeisner/PyTem]()

## Syntax of PyTem Templates

A PyTem template is a text file (.txt, .html, .markdown, etc.) containing, in addition the
"normal" text appropriate to the file type, python statements and python expressions.

## An Example of a PyTem Template

Here is a file named "pytem_demo4.tm", showing python statement lines and lines containing
pure text and python expressions.

```
This is a PyTem Template it will output these two initial
lines followed by a greeting followed by four numbered lines.
% count = 4
<%greeting%> to you, <% name.upper() %>. How are you?
%    for ix in range(count):
This is line #<% ix %>.
%    end
```

The third, fifth, and seventh lines of the above template are python statements,
as indicated by the '%' at the beginning of the line.
Indentation is not significant:  PyTem will correct the indentation of the python
statements during compilation of the template into pure python.
PyTem recognizes a change in required indentation by

1. a line whose last non-whitespace character is ':', indicating the
   start of a compound statement like "`% for`", "`% if`", "`% else`", etc.
3. a line like "`%  end`", indicating the close of a compound statement.

Anything written to Standard Output by a template's python lines will be
inserted into the template expansion.

The lines not beginning with "%" are text lines.  They will be output "as is", except
that python expressions, like "`<% ix %>`" will be replaced by the value of the
enclosed python expression. 

Here is a python program that will write the expanded template 
to standard output,

```
from pytem import PyTem
pt = PyTem()
s = pt.expandFile('pytem_demo4.tm', {'greeting': 'Hello',  'name': 'George'})
print(s)
```

## Including other templates

Inside a template file, another template file can be included, interpreted in the same
environment, using 

```
    <% include_template('another.tm') %>
```

**NOTE:** There is nothing special about this... it's just another python expression,
calling the function, "include_template".


## PyTem API -- General Comments

The API consists of three entry points: the constructor, `PyTem`, and two methods, `expandString`
and `expandFile`.  Usage means calling the constructor to obtain a PyTem instance, followed by
one or more calls to `expandString` or `expandFile`, each returning a string, and possibly modifying the evaluation environment for future calls to `expandString` or `expandFile` using
the same PyTem instance.

Evaluation of templates involves an _environment_ that provides variable bindings for the
evaluation of embedded python statements and expressions.  An initial environment may
optionally be specified when the PyTem constructor is called.  Subsequent calls to `expandString` and `expandFile` may update the environment, as may changes to variables make by python code 
inside the templates.

The environment is maintained inside the PyTem instance, so changes
made during an expansion will be visible to later expansions.  To start with a clean
environment, create another PyTem instance by calling the constructor again.

Compiled template files (but not template strings) are cached, so that they are compiled
once even if used multiple time with the same PyTem instance.

For debugging: if the pyfile option is true, then the compiled template (i.e. pure python)
named "infile" is saved in file, "infile.py", for debugging.

## PyTem API -- The Constructor

A instance of class, **PyTem**, is constructed and used for all subsequent operations.
A call to the constructor has the following signature:

```
  pytem = PyTem( search_path = ['.'],  debug = 0,  pyfile = False, env = {})
```

The constructor's optional keyword arguments are:

+ `search_path` defaults to ['.'], a list of directories in which to search for named templates.
  On the command line `search_path` is set with the option, "-s" or "--search_path".

+ `debug` defaults to 0x0000, provides an optional mask of bits to control debug output.
  On the command line `debug` is set with the option, "-d" or "--debug".

+ `pyfile` defaults to False. If True, a file with '.py' appended to the name of the input
  template file will be created, containing the python code for the "compiled" input template file.
  On the command line `pyfile` is set with the option, "-p".

+ `env`, the initial evaluation environment, defaults to the empty dictionary, `{}`.
  The `env` option can not be set on the command line.


## PyTem API -- Method `expandString`

The `expandString` method optionally updates the environment with a list of dictionaries and
key/value pairs, then expands the `template_string`.  The `infilename` serves as an identifier
of the string in error messages.

```
    expandString(self,  template_string,  infilename(string),  *kv_dicts,  **kv_vars )
```

The `expandString` method return the (string) expansion of the `template_string`.

## PyTem API -- Method `expandFile`

The `expandFile` method optionally updates the environment with a list of dictionaries and
key/value pairs, then expands the file named by `infilename`.  The file is searched for in
the directories specified in the `search_path` list parameter to the PyTem constructor. 

```
    expandFile(self,   infilename,  *kv_dicts,   **kv_vars)
```

The `expandFile` method return the (string) expansion of the file named by `infilename`.


## PyTem API -- Method `resetEnv`

```
    resetEnv(self, new_env)
```

The way PyTem manages its evaluation environment is unusual, but (we believe) useful and easy
to understand.

When the PyTem instance is created, a new, empty environment is created, and optionally
populated by the optional `env` argument to the constructor.

Each time the methods, `expandFile` or `expandString` is called the optional `kv_dicts` and
`kv_vars` arguments can update the environment. All these environment changes are cumulative:
they only update or add to the previous environment, but don't replace it, outright.  This
allows a set of expansions, and files included by `<%include_template ... %>`, to share an
environment and use it to pass information between templates.

At any point, the `resetEnv` method may be used to reset the environment back to a specific state.

## Standalone (CLI) Program

The installed module, `pytem.py`, can be run from the command line.  An example:

```
    python ?wherever-its-installed?/pytem.py  -o myfile.out  myfile.tm 
```

You might want to create a batch file (shell script) to do this, since `pytem.py` is
probably located deep in your site-packages directory.

```
Usage:  python pytem.py [options] infile, ...
Options
  (-h | --help          This help message.
  (-d | --debug)        debug mask bits
  (-s | --search_path)  path1,path2,...
                        0x4000  Show python source
                                for compiled templates.
                        0x0100  Minor messages
  -p                    Output the compiled template (i.e. pure python)
                        named with ".py" appended, for debugging. For infile,
                        "myfile.tm" the python file will be "myfile.tm.py".
  (-o | --out)          Out file name. Defaults to '<stdout>' if
                        not specified.
Expands infiles in order. Keeping environment from one to the next
If no infiles specified, use <stdin>.
```

