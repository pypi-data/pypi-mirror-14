PyFileMaker
===========

Latest version of documentation and code is available at https://github.com/aeguana/PyFileMaker

PyFileMaker module is designed for both script and interactive use.
Any command used during interactive session is possible to type in a script.

Short introduction
------------------

For the full and up to date reference go to https://github.com/aeguana/PyFileMaker/tree/master/Examples

run python interactively (or better run ipython):

``$ ipython`` 


Setting of database and layout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the beginnig you have to set the server, database and layout::

  >> from PyFileMaker import FMServer

  >> fm = FMServer('http://login:password@filemaker.server.com')
  >> fm.
  [and press Tab to see available methods and variables]
  >> help fm.getDbNames
  [displays help for the method]

  >> fm.getDbNames()
  ['dbname','anoterdatabase']
  >> fm.setDb('dbname')

  >> fm.getLayoutNames()
  ['layoutname','anotherlayout']
  >> fm.setLayout('layoutname')

You can also type directly::

  >> fm = FMServer('http://login:password@filemaker.server.com','dbname','layoutname')


List fieldnames
~~~~~~~~~~~~~~~

Get the list of fields from the active layout::

  >> fm.doView()
  ['column1', 'column2']


Find records
~~~~~~~~~~~~

To search records::

  >> fm.doFind(column1='abc')
  <FMProResult instance with 2 records>
  [column1='abcdef'
  column2'='some data'
  RECORDID=1,
  column1='abc'
  column2='another data'
  RECORDID=2]

You've got list of 2 records, usually you need to work only with one record::

  >> a = fm.doFind(column1='abc')
  >> len(a)
  2
  >> r = a[0]
  >> r.
  [press Tab for available layout variables or for completition of variable name]

  >> r.column1
  'abcdef'
  >> r['column1']
  'abcdef'
  >> print r.column1
  abcdef
  >> r.column.related
  'content'

  >> fm.doFind( column1='abc', column__related='abc', LOP='OR', SKIP=1, MAX=1)

Get latest record if documentID field is autoincremented during insertion in FileMaker::

  >> fm.doFind( SORT=['documentID':'<'], MAX=1)

Or more low level access using dict - for operators, and non-ascii fields::

  >> fm.doFind( {'documentID.op':'lt', '-max':1})

Any combination of attributes is allowed...

BTW For query empty record::

  >> fm.doFind( column1='==')

Editing records
~~~~~~~~~~~~~~~

It's enought when you change some variables inside of previosly returned record::

  >> r = fm.doFindAny()[0]
  >> r.column = 'NEWVALUE'
  >> fm.doEdit(r)

This will update only changed column 'column' in table.
You can use changed old record in other functions too - doDup, doNew, doDelete.
doFind(r) will find record with the same RECORDID, but MODID is updated.

New records can be specified as arguments of doNew() like::

  fm.doNew(column1='newvalue', column2='old')
  fm.doNew({'column':'newvalue','column2':'old'})

Templates
~~~~~~~~~

The structure of returned data is suitable for use with Cheetah Templates.
It is really easy to write a template::

  import Cheetah.Template
  t = Cheetah.Template.Template('''
  Document Template
  ~~~~~~~~~~~~~~~~
  DocumentID: $documentID
  DocumentType: $DocumentType.documentType

  Item descriptions:
  #for $l in $DocumentLine
   - $l.description
  #end for      
  ''', searchList=[r[0]])


Debugging connection
~~~~~~~~~~~~~~~~~~~~

Best way howto debug what's wrong::

  >> fm._debug = True

then check printed url request by external tools (like curl, xmlstarlet):

``$ curl 'http://test:test@filemaker.server.com:80/fmi/xml/fmresultset.xml?-db=test&-layout=test&-findall' | xmlstarlet fo``

Error reporting
~~~~~~~~~~~~~~~

In case something is not running the way it should, please report an Issue on the the GitHub project https://github.com/aeguana/PyFileMaker.
New contributions to the code are welcomed.