..
   This file is part of IDUtils
   Copyright (C) 2015 CERN.

   IDUtils is free software; you can redistribute it and/or modify
   it under the terms of the Revised BSD License; see LICENSE file for
   more details.

   In applying this license, CERN does not waive the privileges and immunities
   granted to it by virtue of its status as an Intergovernmental Organization
   or submit itself to any jurisdiction.


=======
IDUtils
=======

.. image:: https://img.shields.io/travis/inveniosoftware/idutils.svg
        :target: https://travis-ci.org/inveniosoftware/idutils

.. image:: https://img.shields.io/coveralls/inveniosoftware/idutils.svg
        :target: https://coveralls.io/r/inveniosoftware/idutils

.. image:: https://img.shields.io/github/tag/inveniosoftware/idutils.svg
        :target: https://github.com/inveniosoftware/idutils/releases

.. image:: https://img.shields.io/pypi/dm/idutils.svg
        :target: https://pypi.python.org/pypi/idutils

.. image:: https://img.shields.io/github/license/inveniosoftware/idutils.svg
        :target: https://github.com/inveniosoftware/idutils/blob/master/LICENSE


Small library for validating and normalising persistent identifiers used in
scholarly communication.

* Free software: Revised BSD license
* Documentation: https://idutils.readthedocs.org.

Features
========

- Validation and normalization of persistent identifiers.
- Detection of persistent identifier scheme.
- Generation of resolving links for persistent identifiers.
- Supported schemes: ISBN10, ISBN13, ISSN, ISTC, DOI, Handle, EAN8, EAN13, ISNI
  ORCID, ARK, PURL, LSID, URN, Bibcode, arXiv, PubMed ID, PubMed Central ID,
  GND.

Installation
============

The IDUtils package is on PyPI so all you need is:

.. code-block:: console

    $ pip install idutils


..
   This file is part of IDUtils
   Copyright (C) 2015 CERN.

   IDUtils is free software; you can redistribute it and/or modify
   it under the terms of the Revised BSD License; see LICENSE file for
   more details.

   In applying this license, CERN does not waive the privileges and immunities
   granted to it by virtue of its status as an Intergovernmental Organization
   or submit itself to any jurisdiction.


Changes
=======

Version 0.2.0 (2016-04-07)

- Changes URL resolution for DOIs to use https://doi.org instead of
  http://dx.doi.org according to
  https://www.doi.org/doi_handbook/3_Resolution.html#3.8

Version 0.1.1 (2015-07-22)

- Fixes GND validation and normalization.
- Replaces invalid package name in `run-tests.sh` and makes `run-tests.sh` file
  executable. One can now use `docker-compose run --rm web /code/run-tests.sh`
  to run all the CI tests (pep257, sphinx, test suite).
- Initial release of Docker configuration suitable for local developments.
  `docker-compose build` rebuilds the image,
  `docker-compose run --rm web /code/run-tests.sh` runs the test suite.

Version 0.1.0 (2015-07-02)

- First public release.


