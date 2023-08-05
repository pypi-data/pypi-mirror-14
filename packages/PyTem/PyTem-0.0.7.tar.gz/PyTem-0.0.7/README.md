# PyTem Template Engine.

### Intro: What is PyTem

PyTem is an implementation of a Python-Server-Pages-like template engine for Python 3+.
PyTem is, 

+ small -- a single python file.
+ simple  -- you can learn the syntax of templates and/or the PyTem API in just a few minutes.
+ hackable -- readable source code, so feel free to adapt it to your own python project.

PyTem's current status is "Alpha", missing mostly: good documentation.

PyTem can run as a standalone program from the command line, or can be imported into another Python 3 program and used via a small/simple API.

### Syntax of PyTem Templates

A PyTem template is a text file (.txt, .html, .markdown, etc.) containing, in addition the
"normal" text appropriate to the file type, python statements and python expressions.

## An Example of a PyTem Template

Here is the contents of a file named "pytem_demo4.tm",

```
This is a PyTem Template it will output these two initial
lines followed by a greeting followed by four numbered lines.
% count = 4
<%greeting%> to you, <% name.upper() %>. How are you?
%    for ix in range(count):
This is line #<% ix %>.
%    end
```

The first, third, and fifth lines of the above template are python statements,
as indicated by the '%' at the beginning of the line.
Indentation is not significant:  PyTem will correct the indentation of the python
statements during compilation of the template.   It recognizes a change in required
indentation by

1. a line whose last non-whitespace character is ':', indicating the
   start of a compound statement like 'for', 'if', 'else', etc.
3. a line like "%  end", indicating the close of a compound statement.


The lines not beginning with '%' are text lines.  They will be output "as is", except
that python expressions, like "<% ix %>" will be replaced by their values. 


Here is a python program that will write the expanded template 
to standard output,

```
from pytem import PyTem

pt = PyTem()
s = pt.expandFile('pytem_demo4.tm', {'greeting': 'Hello',  'name': 'George'})
print(s)
```


## Including other templates

To Be Specified


## Standalone (CLI) Program

To Be Specified


## The API

To Be Specified

