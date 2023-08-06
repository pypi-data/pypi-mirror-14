A native Python reader of the SWORD Project Bible Modules

This project is **not** an official `CrossWire <http://crosswire.org/>`_
project. It merely provides an alternative way to read the bible modules
created by CrossWires `SWORD <http://crosswire.org/sword/index.jsp>`_ project.

Features
--------

-  Read SWORD bibles (not commentaries etc.)
-  Detection of locally installed bible modules.
-  Supports all known SWORD module formats (ztext, ztext4, rawtext,
   rawtext4)
-  Read from zipped modules, like those available from
   http://www.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles
-  Clean text of OSIS, GBF or ThML tags.
-  Supports both python 2 and 3 (tested with 2.7 and 3.5)

License
-------

Since parts of the code is derived and/or copied from the SWORD project
(see canons.py) which is GPL2, this code is also under the GPL2 license.

Installation
------------

PySwords source code can be downloaded from PySwords `release list <https://gitlab.com/tgc-dk/pysword/tags>`_,
but it is also available from `PyPI <https://pypi.python.org/pypi/pysword/>`_
for install using ``pip`` or ``easy_install``.
It also available for `ArchLinux (AUR) <https://aur.archlinux.org/packages/?K=pysword>`_,
and will soon be available as a package in Debian and Fedora.

Example code
------------

Use modules from default datapath
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pysword.modules import SwordModules
    # Find available modules/bibles in standard data path.
    # For non-standard data path, pass it as an argument to the SwordModules constructor.
    modules = SwordModules()
    # In this case we'll assume the modules found is something like:
    # {'KJV': {'description': 'KingJamesVersion(1769)withStrongsNumbersandMorphology', 'encoding': 'UTF-8', ...}}
    found_modules = modules.parse_modules()
    bible = modules.get_bible_from_module('KJV')
    # Get John chapter 3 verse 16
    output = bible.get(books=['john'], chapters=[3], verses=[16])

Load module from zip-file
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pysword.modules import SwordModules
    # Load module in zip
    # NB: the zip content is only available as long as the SwordModules object exists
    modules = SwordModules('KJV.zip')
    # In this case the module found is:
    # {'KJV': {'description': 'KingJamesVersion(1769)withStrongsNumbersandMorphology', 'encoding': 'UTF-8', ...}}
    found_modules = modules.parse_modules()
    bible = modules.get_bible_from_module('KJV')
    # Get John chapter 3 verse 16
    output = bible.get(books=['john'], chapters=[3], verses=[16])

Manually create bible
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pysword.bible import SwordBible
    # Create the bible. The arguments are:
    # SwordBible(<module path>, <module type>, <versification>, <encoding>, <text formatting>)
    # Only the first is required, the rest have default values which should work in most cases.
    bible = SwordBible('/home/me/.sword/modules/texts/ztext/kjv/', 'ztext', 'default', 'utf8', 'OSIS')
    # Get John chapter 3 verse 16
    output = bible.get(books=['john'], chapters=[3], verses=[16])

Run tests
---------

To run the testsuite, first run the script that download the files used
for testing, and then use nosetests to run the testsuite:

.. code:: sh

    $ python tests/resources/download_bibles.py
    $ nosetests -v tests/

The tests should run and pass using both python 2 and 3.

Module formats
--------------

I'll use Python's struct module's format strings to describe byte
formatting. See https://docs.python.org/3/library/struct.html

There are current 4 formats for bible modules in SWORD.

ztext format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Take the Old Testament (OT) for example. Three files:

-  ot.bzv: Maps verses to character ranges in compressed buffers. 10
   bytes ('<IIH') for each verse in the Bible:

   -  buffer\_num (I): which compressed buffer the verse is located in
   -  verse\_start (I): the location in the uncompressed buffer where
      the verse begins
   -  verse\_len (H): length of the verse, in uncompressed characters

These 10-byte records are densely packed, indexed by VerseKey 'Indicies'
(docs later). So the record for the verse with index x starts at byte
10\*x.

-  ot.bzs: Tells where the compressed buffers start and end. 12 bytes
   ('<III') for each compressed buffer:

   -  offset (I): where the compressed buffer starts in the file
   -  size (I): the length of the compressed data, in bytes
   -  uc\_size (I): the length of the uncompressed data, in bytes
      (unused)

These 12-byte records are densely packed, indexed by buffer\_num (see
previous). So the record for compressed buffer buffer\_num starts at
byte 12\*buffer\_num.

-  ot.bzz: Contains the compressed text. Read 'size' bytes starting at
   'offset'.

ztext4 format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

ztext4 is the same as ztext, except that in the bzv-file the verse\_len
is now represented by 4-byte integer (I), making the record 12 bytes in
all.

rawtext format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Again OT example. Two files:

-  ot.vss: Maps verses to character ranges in text file. 6 bytes ('<IH')
   for each verse in the Bible:

   -  verse\_start (I): the location in the textfile where the verse
      begins
   -  verse\_len (H): length of the verse, in characters

-  ot: Contains the text. Read 'verse\_len' characters starting at
   'verse\_start'.

rawtext4 format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rawtext4 is the same as rawtext, except that in the vss-file the
verse\_len is now represented by 4-byte integer (I), making the record 8
bytes in all.
