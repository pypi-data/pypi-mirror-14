Changes
-------

3.4 (2016-03-12)
~~~~~~~~~~~~~~~~

* Better recognition of boolean argument values, coming from say an HTTP channel as string
  literals

* Use tox to run the tests


3.3 (2016-02-23)
~~~~~~~~~~~~~~~~

* Handle the case when the column type cannot be determined


3.2 (2016-02-19)
~~~~~~~~~~~~~~~~

* Fix corner case with queries ordered by a subselect


3.1 (2016-02-07)
~~~~~~~~~~~~~~~~

* Fix metadata extraction of labelled columns on joined tables

* Adjust size of time fields and align them to the right


3.0 (2016-02-03)
~~~~~~~~~~~~~~~~

* Internal, backward incompatible code reorganization, splitting the main module into smaller
  pieces

* Handle corner cases with joined queries involving aliased tables


Previous changes are here__.

__ https://bitbucket.org/lele/metapensiero.sqlalchemy.proxy/src/master/OLDERCHANGES.rst
