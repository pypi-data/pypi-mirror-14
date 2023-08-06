kinto2xml
---------

Generate a blocklist.xml file from Kinto collections.

.. code-block::

    usage: kinto2xml [-h] [-s SERVER] [-a AUTH] [-b BUCKET] [-v] [-q] [-D]
                     [-o OUT]

    Build a blocklists.xml file.

    optional arguments:
      -h, --help            show this help message and exit
      -s SERVER, --server SERVER
                            The location of the remote server (with prefix)
      -a AUTH, --auth AUTH  BasicAuth token:my-secret
      -b BUCKET, --bucket BUCKET
                            Bucket name.
      -v, --verbose         Show all messages.
      -q, --quiet           Show only critical errors.
      -D, --debug           Show all messages, including debug messages.
      -o OUT, --out OUT     Output file.


CHANGELOG
#########

This document describes changes between each past release.

0.1.0 (2016-04-27)
==================

**Initial version**

- Create collection with the definition of the JSON schema.
- Fetch AMO blocklists information from the /blocked/blocklists.json AMO endpoint.
- Handle import configuration on the CLI.
  - Bucket / Collection names
  - Remote AMO endpoint configuration
  - Schema file path configuration
  - Schema or not schema
  - Verbosity level
  - Server selection
  - Auth credentials
  - Importation type selection
- Support for kinto-signer triggering
- Full SSL support for Python 2.7
- Full Python 2.7 and Python 3.4/3.5 support
- Handle the enabled flag to activate records
- Makefile rule to update the schema definition
- Export kinto blocklists in XML blocklist file version 2
- Export kinto blocklists in XML blocklist file version 3
- XML verifier that create a diff of two XML files


