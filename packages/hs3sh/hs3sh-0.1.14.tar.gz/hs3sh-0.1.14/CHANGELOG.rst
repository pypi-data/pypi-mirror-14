Release History
===============

**0.1.14 2016-04-01**

*   Changes:

    *   Command *acl* now implemented for buckets (object ACLs still not
        implemented)

**0.1.13 2016-03-25**

*   Fixed:

    *   A situation where *url* came up with a false URL when working on a
        compatible storage service

**0.1.12 2016-03-25**

*   Changes:

    *   Command *put* now supports multipart upload (``-m``)
    *   New command *url* generates a pre-signed URL for object access

**0.1.11 2016-03-23**

*   Changes:

    *   Now most commands output can be re-directed (\|, \>, \>\>)

**0.1.10 2016-03-19**

*   Changes:

    *   Now showing versioning status in *lsb*

**0.1.9 2016-03-16**

*   Changes:

    *   Replaced mkbucket/rmbucket with bucket
    *   Added the *acl* command

**0.1.8 2016-03-08**

*   Changes:

    *   Added command *lsp* to show the loaded profiles
    *   Fixed a bug that caused just one metapair being stored

**0.1.7 2016-03-08**

*   Fixed:

    *   A bug that caused *mkbucket* to crash
    *   Error message formatting

**0.1.6 2016-03-07**

*   Changed:

    *   Output of errors with length > 79 chars
    *   Added bucketacl and objectacl commands

**0.1.5 2016-03-06**

*   Changes:

    *   Introduces profiles and the .hs3sh.conf configuration file
    *   Added the *time* command to measure the processing time of commands

