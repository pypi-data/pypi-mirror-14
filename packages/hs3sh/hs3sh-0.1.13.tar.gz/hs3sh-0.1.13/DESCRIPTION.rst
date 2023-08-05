HS3 Shell
=========

The HS3 Shell (**hs3sh**) is a command processor created to interact with Amazon
S3 and compatible storage services.

It's main intention is to test S3 compatible storage services against Amazon S3
without having to deal with the hard-to-remember parameters required by tools
like *awscli* or *s3curl.pl*.

Features

*   Connect to Amazon S3 as well as compatible storage services
*   Uses profiles for easy switching between S3 providers
*   Create, discover and delete buckets
*   Discover, write, read and copy objects
*   Multipart upload
*   Deal with metadata and versions
*   Work with ACLs (yet incomplete)
*   Generate pre-signed URLs

Dependencies
------------

You need to have at least Python 3.5 installed to run **hs3sh**.

It depends on the `boto3 <http://boto3.readthedocs.org/en/latest/>`_ for
communication with Amazon S3 and compatible stores.

Documentation
-------------

To be found at `readthedocs.org <http://hs3sh.readthedocs.org>`_

Installation
------------

Install **hs3sh** by running::

    $ pip install hs3sh


-or-

get the source from `gitlab.com <https://gitlab.com/simont3/hs3sh>`_,
unzip and run::

    $ python setup.py install


-or-

Fork at `gitlab.com <https://gitlab.com/simont3/hs3sh>`_

Contribute
----------

- Source Code: `<https://gitlab.com/simont3/hs3sh>`_
- Issue tracker: `<https://gitlab.com/simont3/hs3sh/issues>`_

Support
-------

If you've found any bugs, please let me know via the Issue Tracker;
if you have comments or suggestions, send an email to `<sw@snomis.de>`_

License
-------

The MIT License (MIT)

Copyright (c) 2016 Thorsten Simons (sw@snomis.de)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
