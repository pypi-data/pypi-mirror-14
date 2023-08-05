An alternate jsonpickle handler for datetime
============================================

This ``jsonpickle`` handler serializes ``datetime.datetime``
objects as ISO-8601 formatted strings.  Such strings may be
treated as a ``DATETIME`` type in a RDBMS such as SQLite
allowing date-related query clauses to work with serialized
datetime objects directly.

Installation
------------

.. code:: bash

    pip install isodatetimehandler

Usage
-----

.. code:: python

    import isodatetimehandler

Then use ``jsonpickle`` as you normally would.
