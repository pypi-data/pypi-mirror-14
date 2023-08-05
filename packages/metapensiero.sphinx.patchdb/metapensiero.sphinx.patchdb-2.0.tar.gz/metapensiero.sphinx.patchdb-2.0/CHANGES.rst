Changes
-------

2.0 (2016-03-01)
~~~~~~~~~~~~~~~~

* Shiny new tests suite

* New SQLiteSQL specific context

* Generalized and somewhat better `fake data domains` for MySQL and SQLite. **Warning**: the
  syntax in not backward compatible with previous implementation added in version 1.2.0.

* New placeholder scripts, to allow splitting schema in several different Sphinx environments

* Now two scripts cannot have the same title, even within the same document

* Fix onerror handling, broken long ago by a typo


1.7 (2016-02-20)
~~~~~~~~~~~~~~~~

* Fix packaging issues


1.6 (2016-02-10)
~~~~~~~~~~~~~~~~

* Data files and preload/postload scripts may be specified also as package relative resources

* Deprecate the ``--patch-storage`` option for ``patchdb``, replaced by a single positional
  argument: it's going to be removed in version 2.0, in the meanwhile it's still recognized


1.5 (2016-01-07)
~~~~~~~~~~~~~~~~

* Repackage dbloady as a standalone tool, metapensiero.sqlalchemy.dbloady


1.4.2 (2015-10-22)
~~~~~~~~~~~~~~~~~~

* Allow using keyed values (e.g. PostgreSQL HSTORE) to lookup instances in dbloady


1.4.1 (2015-09-23)
~~~~~~~~~~~~~~~~~~

* Augmented Sphinx autodoc DataDocumenter able to pretty print SA queries


1.4.0 (2015-08-19)
~~~~~~~~~~~~~~~~~~

* New experimental dbloady feature, mainly intendended for test fixtures: it is now able to
  take note about the instances it creates writing a YAML file with the same input format, and
  delete them from the database in a subsequent run


1.3.11 (2015-08-16)
~~~~~~~~~~~~~~~~~~~

* dbloady now flushes changes after each entity to honor referential integrity checks


1.3.10 (2015-08-15)
~~~~~~~~~~~~~~~~~~~

* Fix problem with the ``patchdb:script`` role, when the target gets splitted on two or more
  lines


1.3.9 (2015-08-08)
~~~~~~~~~~~~~~~~~~

* Fix problem with different MySQL drivers exceptions internals


1.3.8 (2015-08-08)
~~~~~~~~~~~~~~~~~~

* Allow longer patch ids, up to 100 characters


1.3.7 (2015-07-20)
~~~~~~~~~~~~~~~~~~

* Use PyMySQL by default, allow selection of a different driver with a command line option


1.3.6 (2015-07-06)
~~~~~~~~~~~~~~~~~~

* Do not decode patch id from UTF-8 but let the driver do that if needed


1.3.5 (2015-07-06)
~~~~~~~~~~~~~~~~~~

* Fix type of MySQL port number, must be an integer


1.3.4 (2015-07-06)
~~~~~~~~~~~~~~~~~~

* Accept also the port number to reach the MySQL server


1.3.3 (2015-06-24)
~~~~~~~~~~~~~~~~~~

* Some more tweaks to adapt dbloady to Python 3


1.3.2 (2015-06-23)
~~~~~~~~~~~~~~~~~~

* Flush the standard error stream to show the progress immediately

* Do not encode statements in UTF-8 but let the driver do that if needed


1.3.1 (2015-06-23)
~~~~~~~~~~~~~~~~~~

* Fix "brown paper bag" syntax error


1.3.0 (2015-06-21)
~~~~~~~~~~~~~~~~~~

* Use ``fdb`` instead of ``kinterbasdb`` for ``Firebird``

* Support the ``AXON`` format for the on disk patch storage


1.2.1 (2014-07-02)
~~~~~~~~~~~~~~~~~~

* Add script's "conditions" and "run-always" to the sphinx rendering

* dbloady's load_yaml() now returns a dictionary with loaded instances


1.2.0 (2014-06-19)
~~~~~~~~~~~~~~~~~~

* New "run-always" scripts

* Poor man "CREATE DOMAIN" for MySQL

* User defined assertions


1.1.2 (2014-06-05)
~~~~~~~~~~~~~~~~~~

* New --assume-already-applied option, useful when you start using ``patchdb``
  on an already existing database


1.1.1 (2014-06-03)
~~~~~~~~~~~~~~~~~~

* Fix packaging, adding a MANIFEST.in


1.1.0 (2014-06-03)
~~~~~~~~~~~~~~~~~~

* Use setuptools instead of distribute

* Use argparse instead of optparse

* New mimetype property on scripts, to select the right Pygments highlighter

* New MySQL specific context, using cymysql


1.0.7 (2013-08-23)
~~~~~~~~~~~~~~~~~~

* published on bitbucket


1.0.6 (2013-03-12)
~~~~~~~~~~~~~~~~~~

* dbloady: ability to load field values from external files


1.0.5 (2013-03-11)
~~~~~~~~~~~~~~~~~~

* dbloady: fix encoding error when printing messages coming from PostgreSQL

* dbloady: emit a progress bar on stderr


1.0.4 (2013-02-27)
~~~~~~~~~~~~~~~~~~

* dbloady, a new utility script, to load base data from a YAML stream.


1.0.3 (2012-11-07)
~~~~~~~~~~~~~~~~~~

* Fix ``:patchdb:script`` role


1.0.2 (2012-10-19)
~~~~~~~~~~~~~~~~~~

* Pickier way to split the multi-statements SQL scripts, now the
  ``;;`` separator must be on a line by its own

* More precise line number tracking when applying multi-statements SQL
  scripts

* Dump and load script dependencies and conditions as lists, to avoid
  pointless repeated splits and joins


1.0.1 (2012-10-13)
~~~~~~~~~~~~~~~~~~

* Fix error loading JSON storage, simplejson already yields unicode strings

* Possibly use the original title of the script as description, if not
  explicitly set

* More precise error on unknown script reference

* Minor corrections


1.0 (2012-10-10)
~~~~~~~~~~~~~~~~

* Added JSON support for the on disk `scripts storage`

* Adapted to work with SQLAlchemy 0.7.x

* Updated to work with docutils > 0.8

* Refactored as a `Sphinx domain <http://sphinx.pocoo.org/domains.html>`_

  .. attention:: This means that the directive names are now prefixed
                 with ``patchdb:`` (that is, the old ``script``
                 directive is now ``patchdb:script``). You can use the
                 `default-domain`__ directive if that annoys you.

  __ http://sphinx.pocoo.org/domains.html#directive-default-domain

* Renamed the status table from ``prst_applied_info`` to simply
  ``patchdb``

  .. attention:: This is the main incompatible change with previous
                 version: you should eventually rename the table
                 manually, sorry for the inconvenience.

* Renamed ``prst_patch_storage`` configuration setting to
  ``patchdb_storage``

* Each script ID is now lower case, to avoid ambiguities


0.3 (2010-11-14)
~~~~~~~~~~~~~~~~

* Updated to work with Sphinx 1.0

* New :script: role for cross-references

* New :file: option on script directive, to keep the actual text in an
  external file


0.2 (2010-03-03)
~~~~~~~~~~~~~~~~

* Compatibility with SQLAlchemy 0.6

* New patchdb command line tool


0.1 (2009-10-28)
~~~~~~~~~~~~~~~~

* Replace home brew solution with SQLAlchemy topological sort

* Use YAML for the persistent storage

* Mostly working Sphinx adaptor

* Rudimentary and mostly untested SQLAlchemy backend (basically only
  the direct PostgreSQL backend has been battle tested in production...)

* First standalone version


0.0
~~~

* still a PylGAM side-product

* simply a set of docutils directives

* started with Firebird in mind, but grown up with PostgreSQL
