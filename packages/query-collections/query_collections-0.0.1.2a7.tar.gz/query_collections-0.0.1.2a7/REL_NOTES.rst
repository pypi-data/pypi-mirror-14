Query Collections Release Notes
===============================

This document will serve as purpose for documenting any changes with each release.

Releases are grouped by major, minor, version and listed by build:: MAJOR.MINOR.VERSION.BUILD

0.0.1 ALPHA
===========
2a(7)
-----
 - We can now query an item with the index operators! When accesing elements of a query_dict or query_list
    with the index operators (braces), you can prefix the index value (a string!) with '?' and it will
    perform a query instead of accessing that element.

2a(5)
-----
 - Fixed issue where wildcard returns list instead of a query_list, preventing further query chains.

2a(4)
-----
 - Addition of this release notes file!

2a(3)
-----
 - Fixed issue where a tuple was not properly queried with a wildcard

2a(2)
-----
 - Build version increment, addition of 2a(1)

2a(1)
-----
 - Welcome to 0.0.1.2a! There was a lot of internal refactoring removing circular dependencies, and overall cleaner.
 - Now you can query any dict or list object, it does not need to be a query_dict or query_list
        - use the 'query' method in the package