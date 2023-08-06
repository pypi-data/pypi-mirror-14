AtomicTempFile
====================

A context manager for atomic file writes.

::

  $ pip install atomictempfile

AtomicTempFile
--------------------

A temporary file object which will be atomically renamed to the specified
path on exit.

     with AtomicTempFile('whatever') as f:
      f.write('stuff')

This allows transactional behaviours with file writes.
