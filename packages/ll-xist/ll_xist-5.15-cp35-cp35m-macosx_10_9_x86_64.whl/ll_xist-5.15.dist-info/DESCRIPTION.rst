XIST provides an extensible HTML and XML generator. XIST is also a XML parser
with a very simple and pythonesque tree API. Every XML element type corresponds
to a Python class and these Python classes provide a conversion method to
transform the XML tree (e.g. into HTML). XIST can be considered
'object oriented XSLT'.

XIST also includes the following modules and packages:

* ``ll.ul4c`` is compiler for a cross-platform templating language with
  similar capabilities to `Django's templating language`__. ``UL4`` templates
  are compiled to an internal format, which makes it possible to implement
  template renderers in other languages and makes the template code "secure"
  (i.e. template code can't open or delete files).

  __ https://docs.djangoproject.com/en/1.5/topics/templates/

  There are implementations for Python, Java and Javascript.

* ``ll.ul4on`` provides functions for encoding and decoding a lightweight
  machine-readable text-based format for serializing the object types supported
  by UL4. It is extensible to allow encoding/decoding arbitrary instances
  (i.e. it is basically a reimplementation of ``pickle``, but with string
  input/output instead of bytes and with an eye towards cross-plattform
  support).

  There are implementations for Python, Java and Javascript.

* ``ll.orasql`` provides utilities for working with cx_Oracle_:

  - It allows calling functions and procedures with keyword arguments.

  - Query results will be put into Record objects, where database fields
    are accessible as object attributes.

  - The ``Connection`` class provides methods for iterating through the
    database metadata.

  - Importing the modules adds support for URLs with the scheme ``oracle`` to
    ``ll.url``.

  .. _cx_Oracle: http://cx-oracle.sourceforge.net/

* ``ll.make`` is an object oriented make replacement. Like make it allows
  you to specify dependencies between files and actions to be executed
  when files don't exist or are out of date with respect to one
  of their sources. But unlike make you can do this in a object oriented
  way and targets are not only limited to files.

* ``ll.color`` provides classes and functions for handling RGB color values.
  This includes the ability to convert between different color models
  (RGB, HSV, HLS) as well as to and from CSS format, and several functions
  for modifying and mixing colors.

* ``ll.sisyphus`` provides classes for running Python scripts as cron jobs.

* ``ll.url`` provides classes for parsing and constructing RFC 2396
  compliant URLs.

* ``ll.nightshade`` can be used to serve the output of PL/SQL
  functions/procedures with CherryPy__.

* ``ll.misc`` provides several small utility functions and classes.

* ``ll.astyle`` can be used for colored terminal output (via ANSI escape
  sequences).

* ``ll.daemon`` can be used on UNIX to fork a daemon process.

* ``ll.xml_codec`` contains a complete codec for encoding and decoding XML.

__ http://www.cherrypy.org/


Changes in 5.15 (released 03/18/2016)
-------------------------------------

* Calls to UL4 functions and templates now support specifying a ``*`` or
  ``**`` argument multiple times (similar to Python's PEP 448).

* Also ``*`` and ``**`` expressions are now allowed in list, set and dict
  "literals".

* The UL4 function ``sorted`` now supports a ``key`` and ``reverse`` argument.

* Strings in UL4 now support the ``splitlines`` method.

* An UL4 function ``ascii`` has been added.

* PySQL no longer supports the ``-- !!!`` command terminator. Use the
  ``raiseexceptions`` command instead to specify error handling.

* The PySQL command ``setvar`` now uses the ``name`` key as the variable name
  instead of the ``var`` key.

* A new PySQL command ``unsetvar`` has been added for deleting an existing
  variable.

* PySQL variables can now be used in expressions, e.g.::

    var('foo_10', 'str').upper()

* The PySQL function ``load`` has been replaced by two functions ``loadstr``
  for loading strings and ``loadbytes`` for loading bytes.

* ``orasql.Index`` now has a method ``itercolumns`` for iterating
  through the columns of the index.




