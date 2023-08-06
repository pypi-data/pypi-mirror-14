Introduction
============

Any2csv is a helper module to ease producing CSV files from different sources.
It is mainly usefull to consume SQLAlchemy requests results or any other ORM
that produces objects.

Licence
=======

This package is covered by the permissive BSD licence.

Python versions
===============

Any2csv is tested with the help of tox on python 2.7 and python 3.4
It may work with older versions (some parts were developped using python 2.3)
but no tests or even garantee is made on this.

Example Usage
=============

::

	from any2csv import Any2CSV


	class SubObj(object):
		def __init__(self, v):
			self.field1 = v
			self.field2 = "%s%s" % ("field2", v)


	class MyObj(object):
		def __init__(self, v):
			self.field1 = v
			self.field2 = "%s%s" % ("field2", v)
			self.subobj = SubObj(v)

	vals = ['a', 'b', 'c']
	objlist = [MyObj(val) for val in vals]

	writer = Any2CSV(
		target_filename='testoutput1.csv',
		column_mappings=[
			{'attr': 'field1', 'colname': 'field 1'},
			{'attr': 'field2', 'colname': 'field 2'},
			{'attr': 'subobj.field1', 'colname': 'field 1 of subobj'},
			{'attr': 'subobj.field2', 'colname': 'field 2 of subobj'},
		]
	)

	writer.write(objlist)

In this example we use a simple in-memory list with dummy objects but the
Any2CSV adapter works with any iterator as long as it outputs objects and you
are able to describle the source attr and the desired colname.

If you want to apply rendering functions to your column you need to add a
renderer definition to the column_mappings, here is how to do it::

	import logging
	from any2csv import Any2CSV


	class SubObj(object):
		def __init__(self, v):
			self.field1 = v
			self.field2 = "%s_%s" % ("field2", v)


	class MyObj(object):
		def __init__(self, v):
			self.field1 = v
			self.field2 = "%s_%s" % ("field2", v)
			self.subobj = SubObj(v)


	def render_split(value=None):
		if value is None:
			v = u''
		else:
			v = value

		return v.split('_')[1]

	logging.basicConfig()
	vals = ['a', 'b', 'c']
	objlist = [MyObj(val) for val in vals]

	writer = Any2CSV(
		'testoutput2.csv',
		[
			{'attr': 'field1', 'colname': 'field 1'},
			{'attr': 'field2', 'colname': 'field 2', 'renderer': render_split},
			{'attr': 'subobj.field1', 'colname': 'field 1 of subobj'},
			{'attr': 'subobj.field2', 'colname': 'field 2 of subobj'},
		],
		show_first_line=True,
	)

	writer.write(objlist)

Changelog
=========

0.3.4 Nov. 5 2015
~~~~~~~~~~~~~~~~~

    - Fixed unicode support in Python2 (and reworked it in Python3)
    - Added possibility to pass iterables of dictionaries (as opposed to
      only instances) to the writer. For the moment the passed dict must
      have keys that match to target output columns, but we may add support
      for columns remapping in the future.

0.3.3 Jul. 29 2015
~~~~~~~~~~~~~~~~~~

	- Now based on `any2`_ for the base tools
	- Fully test covered
	- All raised exceptions now are based on Any2Error to help users catch them

.. _any2: https://bitbucket.org/faide/any2

Contributors
============

By order of contribution date:

	- `Florent Aide`_
	- Jérôme Collette

.. _Florent Aide: https://bitbucket.org/faide
