ChangeLog
=========

Version 4.2.2 (2016-03-18)
--------------------------
- The get_relations() and get_tables() methods now also return system views
  and tables if you set the optional "system" parameter to True.
- Fixed a regression when using temporary tables with DB wrapper methods
  (thanks to Patrick TJ McPhee for reporting).

Version 4.2.1 (2016-02-18)
--------------------------
- Fixed a small bug when setting the notice receiver.
- Some more minor fixes and re-packaging with proper permissions.

Version 4.2 (2016-01-21)
------------------------
- The supported Python versions are 2.4 to 2.7.
- PostgreSQL is supported in all versions from 8.3 to 9.5.
- Set a better default for the user option "escaping-funcs".
- Force build to compile with no errors.
- New methods get_parameters() and set_parameters() in the classic interface
  which can be used to get or set run-time parameters.
- New method truncate() in the classic interface that can be used to quickly
  empty a table or a set of tables.
- Fix decimal point handling.
- Add option to return boolean values as bool objects.
- Add option to return money values as string.
- get_tables() does not list information schema tables any more.
- Fix notification handler (Thanks Patrick TJ McPhee).
- Fix a small issue with large objects.
- Minor improvements in the NotificationHandler.
- Converted documentation to Sphinx and added many missing parts.
- The tutorial files have become a chapter in the documentation.
- Greatly improved unit testing, tests run with Python 2.4 to 2.7 again.

Version 4.1.1 (2013-01-08)
--------------------------
- Add NotificationHandler class and method.  Replaces need for pgnotify.
- Sharpen test for inserting current_timestamp.
- Add more quote tests.  False and 0 should evaluate to NULL.
- More tests - Any number other than 0 is True.
- Do not use positional parameters internally.
  This restores backward compatibility with version 4.0.
- Add methods for changing the decimal point.

Version 4.1 (2013-01-01)
------------------------
- Dropped support for Python below 2.5 and PostgreSQL below 8.3.
- Added support for Python up to 2.7 and PostgreSQL up to 9.2.
- Particularly, support PQescapeLiteral() and PQescapeIdentifier().
- The query method of the classic API now supports positional parameters.
  This an effective way to pass arbitrary or unknown data without worrying
  about SQL injection or syntax errors (contribution by Patrick TJ McPhee).
- The classic API now supports a method namedresult() in addition to
  getresult() and dictresult(), which returns the rows of the result
  as named tuples if these are supported (Python 2.6 or higher).
- The classic API has got the new methods begin(), commit(), rollback(),
  savepoint() and release() for handling transactions.
- Both classic and DBAPI 2 connections can now be used as context
  managers for encapsulating transactions.
- The execute() and executemany() methods now return the cursor object,
  so you can now write statements like "for row in cursor.execute(...)"
  (as suggested by Adam Frederick).
- Binary objects are now automatically escaped and unescaped.
- Bug in money quoting fixed.  Amounts of $0.00 handled correctly.
- Proper handling of date and time objects as input.
- Proper handling of floats with 'nan' or 'inf' values as input.
- Fixed the set_decimal() function.
- All DatabaseError instances now have a sqlstate attribute.
- The getnotify() method can now also return payload strings (#15).
- Better support for notice processing with the new methods
  set_notice_receiver() and get_notice_receiver()
  (as suggested by Michael Filonenko, see #37).
- Open transactions are rolled back when pgdb connections are closed
  (as suggested by Peter Harris, see #46).
- Connections and cursors can now be used with the "with" statement
  (as suggested by Peter Harris, see #46).
- New method use_regtypes() that can be called to let getattnames()
  return regular type names instead of the simplified classic types (#44).

Version 4.0 (2009-01-01)
------------------------
- Dropped support for Python below 2.3 and PostgreSQL below 7.4.
- Improved performance of fetchall() for large result sets
  by speeding up the type casts (as suggested by Peter Schuller).
- Exposed exceptions as attributes of the connection object.
- Exposed connection as attribute of the cursor object.
- Cursors now support the iteration protocol.
- Added new method to get parameter settings.
- Added customizable row_factory as suggested by Simon Pamies.
- Separated between mandatory and additional type objects.
- Added keyword args to insert, update and delete methods.
- Added exception handling for direct copy.
- Start transactions only when necessary, not after every commit().
- Release the GIL while making a connection
  (as suggested by Peter Schuller).
- If available, use decimal.Decimal for numeric types.
- Allow DB wrapper to be used with DB-API 2 connections
  (as suggested by Chris Hilton).
- Made private attributes of DB wrapper accessible.
- Dropped dependence on mx.DateTime module.
- Support for PQescapeStringConn() and PQescapeByteaConn();
  these are now also used by the internal _quote() functions.
- Added 'int8' to INTEGER types. New SMALLINT type.
- Added a way to find the number of rows affected by a query()
  with the classic pg module by returning it as a string.
  For single inserts, query() still returns the oid as an integer.
  The pgdb module already provides the "rowcount" cursor attribute
  for the same purpose.
- Improved getnotify() by calling PQconsumeInput() instead of
  submitting an empty command.
- Removed compatibility code for old OID munging style.
- The insert() and update() methods now use the "returning" clause
  if possible to get all changed values, and they also check in advance
  whether a subsequent select is possible, so that ongoing transactions
  won't break if there is no select privilege.
- Added "protocol_version" and "server_version" attributes.
- Revived the "user" attribute.
- The pg module now works correctly with composite primary keys;
  these are represented as frozensets.
- Removed the undocumented and actually unnecessary "view" parameter
  from the get() method.
- get() raises a nicer ProgrammingError instead of a KeyError
  if no primary key was found.
- delete() now also works based on the primary key if no oid available
  and returns whether the row existed or not.

Version 3.8.1 (2006-06-05)
--------------------------
- Use string methods instead of deprecated string functions.
- Only use SQL-standard way of escaping quotes.
- Added the functions escape_string() and escape/unescape_bytea()
  (as suggested by Charlie Dyson and Kavous Bojnourdi a long time ago).
- Reverted code in clear() method that set date to current.
- Added code for backwards compatibility in OID munging code.
- Reorder attnames tests so that "interval" is checked for before "int."
- If caller supplies key dictionary, make sure that all has a namespace.

Version 3.8 (2006-02-17)
------------------------
- Installed new favicon.ico from Matthew Sporleder <mspo@mspo.com>
- Replaced snprintf by PyOS_snprintf.
- Removed NO_SNPRINTF switch which is not needed any longer
- Clean up some variable names and namespace
- Add get_relations() method to get any type of relation
- Rewrite get_tables() to use get_relations()
- Use new method in get_attnames method to get attributes of views as well
- Add Binary type
- Number of rows is now -1 after executing no-result statements
- Fix some number handling
- Non-simple types do not raise an error any more
- Improvements to documentation framework
- Take into account that nowadays not every table must have an oid column
- Simplification and improvement of the inserttable() function
- Fix up unit tests
- The usual assortment of minor fixes and enhancements

Version 3.7 (2005-09-07)
------------------------
Improvement of pgdb module:

- Use Python standard `datetime` if `mxDateTime` is not available

Major improvements and clean-up in classic pg module:

- All members of the underlying connection directly available in `DB`
- Fixes to quoting function
- Add checks for valid database connection to methods
- Improved namespace support, handle `search_path` correctly
- Removed old dust and unnessesary imports, added docstrings
- Internal sql statements as one-liners, smoothed out ugly code

Version 3.6.2 (2005-02-23)
--------------------------
- Further fixes to namespace handling

Version 3.6.1 (2005-01-11)
--------------------------
- Fixes to namespace handling

Version 3.6 (2004-12-17)
------------------------
- Better DB-API 2.0 compliance
- Exception hierarchy moved into C module and made available to both APIs
- Fix error in update method that caused false exceptions
- Moved to standard exception hierarchy in classic API
- Added new method to get transaction state
- Use proper Python constants where appropriate
- Use Python versions of strtol, etc. Allows Win32 build.
- Bug fixes and cleanups

Version 3.5 (2004-08-29)
------------------------
Fixes and enhancements:

- Add interval to list of data types
- fix up method wrapping especially close()
- retry pkeys once if table missing in case it was just added
- wrap query method separately to handle debug better
- use isinstance instead of type
- fix free/PQfreemem issue - finally
- miscellaneous cleanups and formatting

Version 3.4 (2004-06-02)
------------------------
Some cleanups and fixes.
This is the first version where PyGreSQL is moved back out of the
PostgreSQL tree. A lot of the changes mentioned below were actually
made while in the PostgreSQL tree since their last release.

- Allow for larger integer returns
- Return proper strings for true and false
- Cleanup convenience method creation
- Enhance debugging method
- Add reopen method
- Allow programs to preload field names for speedup
- Move OID handling so that it returns long instead of int
- Miscellaneous cleanups and formatting

Version 3.3 (2001-12-03)
------------------------
A few cleanups.  Mostly there was some confusion about the latest version
and so I am bumping the number to keep it straight.

- Added NUMERICOID to list of returned types. This fixes a bug when
  returning aggregates in the latest version of PostgreSQL.

Version 3.2 (2001-06-20)
------------------------
Note that there are very few changes to PyGreSQL between 3.1 and 3.2.
The main reason for the release is the move into the PostgreSQL
development tree.  Even the WIN32 changes are pretty minor.

- Add Win32 support (gerhard@bigfoot.de)
- Fix some DB-API quoting problems (niall.smart@ebeon.com)
- Moved development into PostgreSQL development tree.

Version 3.1 (2000-11-06)
------------------------
- Fix some quoting functions.  In particular handle NULLs better.
- Use a method to add primary key information rather than direct
  manipulation of the class structures
- Break decimal out in `_quote` (in pg.py) and treat it as float
- Treat timestamp like date for quoting purposes
- Remove a redundant SELECT from the `get` method speeding it,
  and `insert` (since it calls `get`) up a little.
- Add test for BOOL type in typecast method to `pgdbTypeCache` class
  (tv@beamnet.de)
- Fix pgdb.py to send port as integer to lower level function
  (dildog@l0pht.com)
- Change pg.py to speed up some operations
- Allow updates on tables with no primary keys

Version 3.0 (2000-05-30)
------------------------
- Remove strlen() call from pglarge_write() and get size from object
  (Richard@Bouska.cz)
- Add a little more error checking to the quote function in the wrapper
- Add extra checking in `_quote` function
- Wrap query in pg.py for debugging
- Add DB-API 2.0 support to pgmodule.c (andre@via.ecp.fr)
- Add DB-API 2.0 wrapper pgdb.py (andre@via.ecp.fr)
- Correct keyword clash (temp) in tutorial
- Clean up layout of tutorial
- Return NULL values as None (rlawrence@lastfoot.com)
  (WARNING: This will cause backwards compatibility issues)
- Change None to NULL in insert and update
- Change hash-bang lines to use /usr/bin/env
- Clearing date should be blank (NULL) not TODAY
- Quote backslashes in strings in `_quote` (brian@CSUA.Berkeley.EDU)
- Expanded and clarified build instructions (tbryan@starship.python.net)
- Make code thread safe (Jerome.Alet@unice.fr)
- Add README.distutils (mwa@gate.net & jeremy@cnri.reston.va.us)
- Many fixes and increased DB-API compliance by chifungfan@yahoo.com,
  tony@printra.net, jeremy@alum.mit.edu and others to get the final
  version ready to release.

Version 2.4 (1999-06-15)
------------------------
- Insert returns None if the user doesn't have select permissions
  on the table.  It can (and does) happen that one has insert but
  not select permissions on a table.
- Added ntuples() method to query object (brit@druid.net)
- Corrected a bug related to getresult() and the money type
- Corrected a bug related to negative money amounts
- Allow update based on primary key if munged oid not available and
  table has a primary key
- Add many __doc__ strings (andre@via.ecp.fr)
- Get method works with views if key specified

Version 2.3 (1999-04-17)
------------------------
- connect.host returns "localhost" when connected to Unix socket
  (torppa@tuhnu.cutery.fi)
- Use `PyArg_ParseTupleAndKeywords` in connect() (torppa@tuhnu.cutery.fi)
- fixes and cleanups (torppa@tuhnu.cutery.fi)
- Fixed memory leak in dictresult() (terekhov@emc.com)
- Deprecated pgext.py - functionality now in pg.py
- More cleanups to the tutorial
- Added fileno() method - terekhov@emc.com (Mikhail Terekhov)
- added money type to quoting function
- Compiles cleanly with more warnings turned on
- Returns PostgreSQL error message on error
- Init accepts keywords (Jarkko Torppa)
- Convenience functions can be overridden (Jarkko Torppa)
- added close() method

Version 2.2 (1998-12-21)
------------------------
- Added user and password support thanks to Ng Pheng Siong (ngps@post1.com)
- Insert queries return the inserted oid
- Add new `pg` wrapper (C module renamed to _pg)
- Wrapped database connection in a class
- Cleaned up some of the tutorial.  (More work needed.)
- Added `version` and `__version__`.
  Thanks to thilo@eevolute.com for the suggestion.

Version 2.1 (1998-03-07)
------------------------
- return fields as proper Python objects for field type
- Cleaned up pgext.py
- Added dictresult method

Version 2.0  (1997-12-23)
-------------------------
- Updated code for PostgreSQL 6.2.1 and Python 1.5
- Reformatted code and converted to use full ANSI style prototypes
- Changed name to PyGreSQL (from PyGres95)
- Changed order of arguments to connect function
- Created new type `pgqueryobject` and moved certain methods to it
- Added a print function for pgqueryobject
- Various code changes - mostly stylistic

Version 1.0b (1995-11-04)
-------------------------
- Keyword support for connect function moved from library file to C code
  and taken away from library
- Rewrote documentation
- Bug fix in connect function
- Enhancements in large objects interface methods

Version 1.0a (1995-10-30)
-------------------------
A limited release.

- Module adapted to standard Python syntax
- Keyword support for connect function in library file
- Rewrote default parameters interface (internal use of strings)
- Fixed minor bugs in module interface
- Redefinition of error messages

Version 0.9b (1995-10-10)
-------------------------
The first public release.

- Large objects implementation
- Many bug fixes, enhancements, ...

Version 0.1a (1995-10-07)
-------------------------
- Basic libpq functions (SQL access)
