..
    This file is part of jsonresolver
    Copyright (C) 2015 CERN.

    jsonresolver is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License; see LICENSE file for
    more details.

==============
 JSONResolver
==============

.. image:: https://img.shields.io/travis/inveniosoftware/jsonresolver.svg
        :target: https://travis-ci.org/inveniosoftware/jsonresolver

.. image:: https://img.shields.io/coveralls/inveniosoftware/jsonresolver.svg
        :target: https://coveralls.io/r/inveniosoftware/jsonresolver

.. image:: https://img.shields.io/github/tag/inveniosoftware/jsonresolver.svg
        :target: https://github.com/inveniosoftware/jsonresolver/releases

.. image:: https://img.shields.io/pypi/dm/jsonresolver.svg
        :target: https://pypi.python.org/pypi/jsonresolver

.. image:: https://img.shields.io/github/license/inveniosoftware/jsonresolver.svg
        :target: https://github.com/inveniosoftware/jsonresolver/blob/master/LICENSE


JSON data resolver with support for plugins.

*This is an experimental developer preview release.*

* Free software: BSD license
* Documentation: https://pythonhosted.org/jsonresolver/


..
    This file is part of jsonresolver
    Copyright (C) 2015, 2016 CERN.

    jsonresolver is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License; see LICENSE file for
    more details.

Changes
=======

Version 0.2.1 (released 2016-04-15)
-----------------------------------

Bug fixes
~~~~~~~~~

- Fixes issue with exceptions raised during e.g. resolver plugin
  loading being caught and not propagated.

Version 0.2.0 (released 2016-04-06)
-----------------------------------

Incompatible changes
~~~~~~~~~~~~~~~~~~~~

- Changes resolving to be based on hostname without 'http://' prefix.

Bug fixes
~~~~~~~~~

- Fixes issues with the hostname not being matched resulting in the
  same route on two hosts not to work.

Version 0.1.1 (released 2015-12-11)
-----------------------------------

Improved features
~~~~~~~~~~~~~~~~~

- Delays the url_map building until first resolve request.

Version 0.1.0 (released 2015-11-18)
-----------------------------------

- Initial public release.


