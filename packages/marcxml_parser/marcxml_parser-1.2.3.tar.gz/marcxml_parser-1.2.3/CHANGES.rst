Changelog
=========

1.2.3
-----
    - Fixed ability to query tags codes using indexing operator.

1.2.2
-----
    - Updated set of possible `i` characters.

1.2.1
-----
    - Fixed bug in the publication type parser.

1.2.0
-----
    - Implemented ``.get()`` method.

1.1.0 - 1.1.7
-------------
    - Fixed typos in documentation.
    - Added ``record_itrator()``.
    - Added support for file-like objects.
    - ISBN is now discriminated to valid and invalid. Added new method ``.get_invalid_ISBNs()``, ``.get_ISBNs()`` now returns just valid ISBNs.
    - Fixed bugs in ``.get_binding()``.
    - Added field ``URLu`` to output from ``.get_internal_urls()``.
    - Added one more test.
    - Fixed few typos in documentation.
    - Added support for ISSN querying.
    - Fixed bug in ``run_test.sh``.
    - Fixed parsing of the place to reflect changes in RDA.
    - Added more RDA fixes.
    - Fixed bug in parsing of the dates.

1.0.1
-----
    - Fixed small bugs in code and documentation.
    - Added more tests.

1.0.0
-----
    - First working version.
    - Fully documented and tested.

0.1.0
-----
    - Project created.
