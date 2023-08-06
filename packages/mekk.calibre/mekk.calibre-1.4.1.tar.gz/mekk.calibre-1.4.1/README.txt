.. -*- mode: rst; compile-command: "rst2html README.txt README.html" -*-

===============================================================
mekk.calibre
===============================================================

This is a set of standalone scripts which I wrote to help
managing my Calibre_ ebook-library.

.. contents::
   :local:
   :depth: 2


Script list
===================================================

The following scripts are available:

``calibre_guess_and_add_isbn``

    Checks books without ISBN (set in metadata) for ISBN-like string
    present in leading pages. If found, add it to the metadata (what
    makes it possible to download full metadata, covers, etc).

``calibre_convert_docs_to_rtf``

    Convert any .doc to .rtf (unless already present) - using
    openoffice.

``calibre_add_if_missing``

    Checks given directory tree for books not yet present in calibre,
    add them if found. Uses binary file comparison to check whether
    the file is identical (file name and metadata are not used, on
    purpose).

``calibre_find_books_missing_in_database``

    Checks whether Calibre database directory contains some
    unregistered files and report them if found.

``calibre_report_duplicates``

    Report duplicates, adding information of which of them are surely
    safe to merge (because duplicated books are identical or because
    formats do not overlap), and which require careful examination
    (because different files in the same format exist).

Script details
===================================================

calibre_guess_and_add_isbn
--------------------------

Queries Calibre for all books without ISBN, then tries to locate ISBN
inside (via scanning a few leading pages) and updates Calibre book
metadata if ISBN is found.

Run it without parameters::

    calibre_guess_and_add_isbn

Any ISBN numbers found will be added to the book metadata (and the
script will report them). Books are scanned from the newest, so you
can abort (Ctrl-C) script once it handled new books.

Later on ISBN can be used to grab the book metatada and/or book cover
inside Calibre GUI. Just spawn Calibre and look for books with ISBN
set and missing metadata, for example using query like::

     isbn:~[0-9] not publisher:~[a-z]

(above means: isbn contains some digit, publisher does not contain any
letter). Depending on your workflow, you can then either 

- grab metadata automaticaly (mark all those books, right click,
  pick Edit Metadata Information/Download Metadata)

- review each book individually (mark those books, right click,
  pick Edit Metadata Information/Edit Metadata Individually, then
  click Fetch Metadata on every book successively and review whether
  it fits).

calibre_convert_docs_to_rtf
----------------------------------

Queries Calibre for all books which have only .doc format, then uses
OpenOffice to convert them to .rtf and add this format as an
alternative.

OpenOffice (and pyuno libraries provided by it) are used in the
process.

Run it without parameters::

    calibre_convert_docs_to_rtf

Note: from time to time the script happens to crash on the end of the
job (while finishing).  I haven't diagnosed the reasons (most likely
the problem is in the libraries I use), but the crash is harmless and
does not influence the actual conversion process.


calibre_find_books_missing_in_database
--------------------------------------

Reports the files present inside Calibre library directory but not
present in the database (and therefore not visible in the Calibre
interface).

The files are reported to standard output. To add them
all to calibre, pipe output. For example::

    calibre_find_books_missing_in_database | xargs -d "\n" calibredb add

(but, better, review everything beforehand)

.. note::

    The problematic scenario may happen for example if Calibre is used
    from two or more machines over synchronized or networked directory
    and, by mistake, two copies are run simultaneously. Or in case
    of some crashes.


calibre_add_if_missing
-----------------------------------

Scans given directory and/or specified files, adds to calibre all
books which are not yet present there.

Duplicate checking is done solely according to the file content.  The
file is skipped if identical file is already present in Calibre.
   
I initially wrote this script to handle *I want to ensure everything
is already imported and can be deleted* scenario, but over years I tend
to use it for most batch ebook imports.

Example::

    calibre_add_if_missing /home/jan/OldBooks

(import any books below ``OldBooks`` which are not yet present, don't
touch this directory - which probably can be removed afterwards).

Or maybe::

    calibre_add_if_missing --tag="programming,web-development" \
        --move=$HOME/ebooks-done  ./freshly-bought/*.epub

(add all ``.epub`` files from ``./freshly-bought``, tag them with
``programming`` and ``web-development``, move all succesfully imported
files to ``~/ebooks-done/``).

For all options, run::

    calibre_add_if_missing --help


calibre_report_duplicates
-------------------------

Analyzes calibre database looking for likely duplicates, and reports
them, adding info of which of those are surely identical, and which
require examination.

Do *not* perform any changes, just prints report (as text, or html, or
javascript-enabled html from which reviewed items can be removed by
clicking).

Example::

    calibre_report_duplicates -f txt

(text output to the console)::

    calibre_report_duplicates -f html -o /tmp/report.html

(HTML output redirected to file)::

    calibre_report_duplicates -f js -o /tmp/report.html

(also HTML, but with buttons to hide rows, handy for review).

See also::

    calibre_report_duplicates --help


Installation and configuration
===============================

Prerequisities
--------------

Calibre must be installed, properly configured and has some database
(otherwise it does not make sense to run those scripts).  The::

    calibredb

command must be in ``PATH`` (or ``calibredb`` variable inside ``.ini``
file must be properly set, see below).

Tools providing commands::

    pdftotext
    catdoc 
    djvutxt
    archmage

should be installed and present in ``PATH`` (or properly configured in
``.ini``, or disabled in ``.ini``, see below). On Ubuntu Linux or
Debian Linux those can be installed from standard repositories, just
install the following packages::

    poppler-utils 
    catdoc
    djvulibre-bin
    archmage

Python 2.6 or 2.7 is required (scripts are using some features
introduced in 2.6 - in particular tempfile extensions, subprocess and
namedtuple). Also, lxml library must be installed.  On Debian or
Ubuntu just install the following packages::

   python2.7
   python-lxml

For ``calibre_convert_docs_to_rtf`` to work, ootools_ library must be
installed. Simplest method to install it::

    easy_install ootools

(on Ubuntu `sudo easy_install ootools`).

I develop and use those scripts on Ubuntu Linux. They should work on
Windows or Mac if necessary tools are installed, but I've never tried
it.

Actual installation
--------------------

Simple::

    sudo pip install mekk.calibre

or::

    pip install --user mekk.calibre

should do (the latter requires adding ``~/.local/bin`` to
``PATH``). In case you don't want to mess with your system
or user directories, consider `using virtualenv`_.

.. _using virtualenv: http://blog.mekk.waw.pl/archives/6-Python-VirtualEnv.html

Configuration
--------------

The ``~/.calibre-utils`` file can be used to configure some program
settings.  The file is created, if missing, whenever any of the
scripts is run, and can be customized.

Here is the default content::

    [commands]
    catdoc = catdoc
    archmage = archmage
    djvutxt = djvutxt
    calibredb = calibredb
    pdftotext = pdftotext
    
    [isbn-search]
    guess_lead_lines = 10000
    guess_lead_pages = 10

The commands section defines location of the external tools being
used.  In case the commands are present in ``PATH``, bare names can be
used. Otherwise full path can be specified. Finally, if some tool is
missing, it can be defined as empty string.

The isbn-search section specifies how many leading pages (in
page-based document formats like PDF or DJVU) or lines (in the free
formats like TXT or CHM) are scanned looking for ISBN-like strings.

For example, the file can be changed so::

    [commands]
    catdoc = /usr/local/bin/catdoc
    archmage = 
    djvutxt = 
    calibredb = /opt/calibre/calibredb
    pdftotext = pdftotext
    
    [isbn-search]
    guess_lead_lines = 12000
    guess_lead_pages = 15

In such a case ``catdoc`` will be used from ``/usr/local/bin``,
calibredb will be expected in ``/opt/calibre``, ``pdftotext`` will be
sought in ``PATH``, and ``archmage`` and ``djvutxt`` will be treat as
missing (so the isbn guessing script won't be able to scan CHM and
DJVU files for ISBN and will ignore them).

History
====================

(only major changes described)

1.4.1
-----------

``calibre_add_if_missing``: added ``--force-language`` (to set book
language attribute).

``calibre_add_if_missing`` crashed in case it was to move the file out
(``--move`` option was used), but identically named file already
existed in the target directory. After the fix, file is moved to some
subdirectory of target instead.


1.4.0
-----------

``calibre_report_duplicates`` enhancements:

- output format is chosen by ``--format=txt`` or ``--format=html`` (instead
  of ``--html``)

- added javascript-enabled output (``--format=js``) which supports clicking-out
  report items

- using SimHash instead of difflib to look for similar titles. MUCH faster,
  provides a bit different but sensible results

- reporting similar authors

- new option ``--cache`` (use cached manifest to speed up reruns on large libraries)

- new option ``--output`` (name output file)


1.3.2
------------

Fixed errors:

- ``calibre_guess_and_add_isbn`` crashed with Unicode decode error
  while saving isbn to book with non-ascii character in title (wrong
  diagnostic print),

- as since calibre 1.0 ``calibredb catalog --sort-by=id`` crashes
  (and, therefore scripts internally using this command crash too), we
  use sort by timestamp instead.

1.3.1
------

``calibre_add_if_missing`` fixes:

- even runs executed without ``--cache`` preserve cached metadata for
  possible next run,

- runs with ``--cache`` ignore cached data if they are more than 24 hours old,

- in case file found in calibre catalog does not exist (what can happen if
  it was renamed or deleted while we run, or if cache is in use and some
  books were removed since it was created), ``calibre_add_if_missing`` just warns,
  but continues it's work (instead of exiting with an error).

1.3.0
---------------

Python3 compatibility work, scripts should be runnable under Python3
(note: daily I still use them under 2.7, so 3 is less tested).

``calibre_add_if_missing`` performs some comparison of epub internals
in case possible duplicate of similar size exists. In particular, 
it is able to ignore ``calibre_bookmarks`` (so duplicate epub is not
added due to this file being added or modified by viewer).

``calibre_add_if_missing`` has ``--cache`` option (reuse cached
catalog from previous run to speed up processing on large libraries).

``calibre_add_if_missing`` has ``--dry-run`` option.

1.2.4
-----------------

``calibre_add_if_missing`` has ``--move`` option (move succesfully
added files to another directory - likely something trash-like).

``calibre_add_if_missing`` has ``--title-from-name`` option (force
using filename as title instead of processing metadata).

``calibre_add_if_missing`` has ``--tag`` and ``--author`` options (force
given tags and/or author instead of processing metadata).

``calibre_add_if_missing`` copies filename as title for ``.doc``,
``.docx``, ``.rtf`` and ``.txt`` files. Those extremely rarely have
sensible metadata.

1.2.3
----------------

``calibre_find_books_missing_in_database`` no longer reports book
subdirectories and such (reasoning: I use book subfolders to store
things like source code added to the book or book sources, at the same
time it is not the place where calibre would put the book by itself).

Fixed two more "UnicodeEncodeError" bugs (reported for books without
files and with unicode character in names)

1.2.2
----------------

``calibre_guess_and_add_isbn`` catches various errors, reports them, and continues 
to work. For any errors information mentions problematic book name.

Ctrl-C aborts ISBN guessing and properly cleans up.

#5 - fix for ISBN's containing X letter. 

1.2.0
-----------------

``calibre_add_if_missing`` disables Calibre own duplicate checking
(which is title based, so too simplistic, and occasionally rejects
fine books) and prints detailed info about found actual duplicates (if
present).

Some ``calibre_report_duplicates`` improvements:

- pruning some redundant matches (if a is similar to b, a is similar
  to c, and b is similar to c, we don't report the latter),

- books which have same/similar author and title are not reported as
  duplicates if they have the same series and different series
  index (so different volumes of the same book are no longer
  reported as possible duplicates).

``calibre_guess_and_add_isbn`` fixes:

- #3 - avoiding crash on latin-1 encoded chm files (during ISBN detection)

- handling some Unicode charactes in ISBN text (hard space, long dash, …)

- verifying ISBN checksum before using it.

1.1.1
-----------------

Added ``calibre_report_duplicates``.

``calibre_add_if_missing`` can be given individual files (initially
only complete directories could be processed).


1.0.4
------------------

First serious release. Working
``calibre_find_books_missing_in_database``,
``calibre_guess_and_add_isbn``, ``calibre_convert_docs_to_rtf``,
``calibre_add_if_missing``.


Sources, bug reports
====================

The project is `hosted here`_.

.. _hosted here: http://bitbucket.org/Mekk/calibre_utils
.. _Calibre: http://calibre-ebook.com/
.. _ootools: http://pypi.python.org/pypi/ootools/0.1dev
