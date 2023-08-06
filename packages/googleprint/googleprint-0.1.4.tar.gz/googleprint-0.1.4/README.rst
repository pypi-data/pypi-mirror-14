=============
googleprint
=============

A simple interface to Google Cloud Print.

Usage::

    >>> from googleprint import *
    >>> auth = OAuth2(access_token="qwertyuiopasdfghjkl", token_token="Bearer")
    >>> r = list_jobs(auth=auth)
    >>> r['jobs']
    [{"id": ...}, ...]
    >>> r = submit_job(printer="0e506d12-dbe0-54d3-7392-fd69d45ff2fc", content="test.pdf", auth=auth)
    >>> r['job']
    {"id": "abcdefgh", ...}
    >>> delete_job("abcdefgh", auth=auth)

Supports both Python 2 and 3:

- ≥ Python 2.6
- ≥ Python 3.2

Install
=======

Use pip to install the latest version from PyPI::

    pip install googleprint


Command line interface
======================

The module can be used from the command line via::

    python -m googleprint ...

See ``--help`` for details.


Tests
=====

The test suite requires three environment variables:

- ``CP_CLIENT_ID`` -- application "client id" (Google API)
- ``CP_CLIENT_SECRET`` -- application "client secret" (Google API)
- ``CP_REFRESH_TOKEN`` -- refresh token for an authorised Google Account
- ``CP_PRINTER_ID`` -- printer ID (optional, default: ``__google__docs``)

During the tests a PDF is printed. By default the Google Docs printer is used,
however it is more forgiving than typical printers, so I don't recommend using
it.

Example::

    CP_CLIENT_ID=1234567890.apps.googleusercontent.com \
    CP_CLIENT_SECRET=asdfghjklzxcvbnmqwertyuiop \
    CP_REFESH_TOKEN=mnbvcxzlkjhgfdspoiuytr \
    CP_PRINTER_ID=0e50ed12-dbe0-54d3-a4bd-fdf9d45ff2fc \
    tox
