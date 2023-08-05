ctext
=====

ctext is a simple Python wrapper and set of helper functions for the `CTP API <http://ctext.org/tools/api>`_, which fetches data from the `Chinese Text Project <http://ctext.org>`_ database, a digital library of pre-modern Chinese literature. Developed for Python 3.

Development status
------------------

This software is currently experimental. See http://ctext.org/tools/api for API details.

Installation
------------

::

    pip install ctext

Usage
-----

Textual items are identified by `CTP URNs <http://ctext.org/tools/api#urn>`_. Each URN identifies a text or part of a text. You can get these manually by visiting the http://ctext.org website (bottom-right of each page), or programmatically using the **searchtexts()** function. To use this library, first::

    from ctext import *

Some API functions (like getting the full structure of a text, or downloading a lot of data) may require an API key. If you have one, before calling any other functions, do this::

    setapikey("your-api-key-goes-here")

You can also set the interface language ("en" for English, "zh" for Chinese)::

    setlanguage("zh")

Similarly, automatic remapping to simplified Chinese can be done with::

    setremap("gb")



getstats
.........

::

    stats = getstats()

Simple wrapper around the `getstats API call <http://ctext.org/plugins/apilist/#getstats>`_.


getstatus
.........

::

    status = getstatus()

Simple wrapper around the `getstatus API call <http://ctext.org/plugins/apilist/#getstatus>`_.


gettexttitles
.............

::

    titles = gettexttitles()

Simple wrapper around the `gettexttitles API call <http://ctext.org/plugins/apilist/#gettexttitles>`_.


getcapabilities
...............

::

    capabilities = getcapabilities()

Simple wrapper around the `getcapabilities API call <http://ctext.org/plugins/apilist/#getcapabilities>`_.




readlink
........

::

    urn = readlink("http://ctext.org/mengzi")

Simple wrapper around the `readlink API call <http://ctext.org/plugins/apilist/#readlink>`_.


gettext
.......

::

    passages = gettext("ctp:analects/xue-er")

Simple wrapper around the `gettext API call <http://ctext.org/plugins/apilist/#gettext>`_. Note that the API gettext function needs to be called recursively to get the full text of an entire book; the Python helper functions **gettextasparagrapharray**, **gettextasstring**, and **gettextasobject** call gettext repeatedly to extract all corresponding textual data.

gettextasobject
...............

::

    data = gettextasobject("ctp:analects/xue-er")

Returns the full text of the requested URN as an object with a nested structure representing what each **gettext** API call returns.

gettextasparagrapharray
.......................

::

    passages = gettextasparagrapharray("ctp:analects/xue-er")

Returns the full text of the requested URN as a simple array of strings, each corresponding to one passage of text. Titles are omitted.

gettextasstring
...............

::

    string = gettextasstring("ctp:analects/xue-er")

Returns the full text of the requested URN as a single string. Each paragraph is separated with "\\n\\n".

gettextinfo
...........

::

    data = gettextinfo("ctp:analects")

Simple wrapper around the `gettextinfo API call <http://ctext.org/plugins/apilist/#gettextinfo>`_.

searchtexts
...........

::

    data = searchtexts("論語")

Simple wrapper around the `searchtexts API call <http://ctext.org/plugins/apilist/#searchtexts>`_.

setapikey
.........

::

    setapikey("your-api-key-goes-here")

This sets an API key which is then supplied to the CTP API with all subsequent API requests.


setlanguage
...........

::

    setlanguage("zh")

This sets the "if" (interface language) parameter, which is then supplied to the CTP API with all subsequent API requests.


setremap
........

::

    setlanguage("gb")

This sets the "remap" (character remapping) parameter, which is then supplied to the CTP API with all subsequent API requests.



License
-------


Copyright 2016 Donald Sturgeon. This code is licensed under the MIT License: http://opensource.org/licenses/mit-license.html
