xmldirector.bookalope
=====================

Integration of 

- Plone (https://www.plone.org)
- XML Director (https://www.xml-director.info) 
- Bookalope (https://bookalope.net)

This Plone 4/5 add-on allows to generate Ebook formats (EPUB, EPUB3, Mobi) and
other formats (ICML, PDF, DOCX) from content stored in XML Director.

Requirements
------------

- Plone 4.3 (tested)
  
- Plone 5.0 (experimental, in progress)

- XML Director (xmldirector.plonecore)

Configuration
-------------

Install ``xmldirector.bookalope`` through the Plone add-on installer
and configure your Bookalope API key and choose if you are running against
Bookalope's production or beta environment.

API
---

There is only one public API method in order to interact with Bookalope
from XML Director code (see ``xmldirector/bookalope/browser/api.py``)::

  convert_bookalope(context, source, cover=None, formats=[], title=u'', author=u'', prefix=None, storage_path='result')

- ``context`` - a XML Director ``Connector`` instance
- ``source`` - source path of the DOCX file inside the directory configured for the given 
  Connector ``context`` e.g. ``src/index.docx``
- ``cover`` - source path of cover page image
- ``formats`` - a list of formats to be generated (supported: epub, epub3, docx, pdf, icml, mobi)
- ``title`` - title used for the ebook
- ``author`` - author name of the publication
- ``prefix`` - generated files will be stored under ``result/<prefix>.<format>``
- ``storage_path`` - subpath used to store the generated ebook files

License
-------
This package is published under the GNU Public License V2 (GPL 2)

Source code
-----------
See https://github.com/xml-director/xmldirector.bookalope

Bugtracker
----------
See https://github.com/xml-director/xmldirector.bookalope/issues


Author
------
| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tuebingen, Germany
| info@zopyx.com
| www.zopyx.com

