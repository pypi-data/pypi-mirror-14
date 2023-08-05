xmldirector.dita
================

DITA conversion support for XML Director

This module packages the 

- DITA Open Toolkit
- XMLMind DITA Converter

as Python module.

API
---

The module provides the following API::

    result = xmldirector.dita.converter.dita2html(ditamap, output_dir_or_file, converter)


- ``ditamap`` - path to DITA map file
- ``output_dir_or_file`` - output directory (DITA) or output filename (DITAC)
- ``converter`` - name of the converter to be used (``dita`` for DITA OT or ``ditac`` for 
   XMLMind Dita converter)

Commandline usage
-----------------

You can start a DITA conversion from the commandline::

  > bin/dita2html -d some.ditamap -o output_directory -c dita|ditac

- ``-d`` - path to DITA map file
- ``-o`` - name of output directory (for DITA-OT) or the HTML output file
  (XMLMind DITAC)
- ``-c`` - name of the converter to be used (``dita`` for DITA OT or ``ditac`` for 
   XMLMind Dita converter)

  


License
-------
This package is published under the GNU Public License V2 (GPL 2)

Source code
-----------
See https://bitbucket.com/ajung/xmldirector.dita

Bugtracker
----------
See https://bitbucket.com/ajung/xmldirector.dita/issues


Author
------
| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tuebingen, Germany
| info@zopyx.com
| www.zopyx.com

