Storage (HDFS/S3/...)
---------------------

Distributed includes convenience functions to interact with common data stores,
including the Hadoop File System (HDFS), Amazon's S3, or any normally mounted
network file system.  Convenience functions exist under the following
submodules

*  ``distributed.hdfs``
*  ``distributed.s3``

Low level bytes interface
-------------------------


Each submodule includes two functions ``read_bytes`` and ``write_bytes`` to
move raw bytes into and out of memory.  These functions ignore the data
encoding (CSV, Avro, raw arrays, etc..) and so are suitable for expert users or
to be used by other higher level functions.

``read_bytes``
~~~~~~~~~~~~~~

The ``read_bytes`` function takes in a path on the storage system and returns a
list of futures that refer to bytes in memory.

.. code-block::

   >>> futures = read_bytes('/data/2015/')
   >>> futures
   [<Future: status: finished, key: read_bytes-2576405bf5525818ef3b6c3f72378fa0>,
    <Future: status: finished, key: read_bytes-4dec252d7f1714175ff3e7d70663a1ba>,
    <Future: status: pending, key: read_bytes-01b6ceb9c31475589385f17b1dc86665>,
    <Future: status: pending, key: read_bytes-42dd7a97c73b7993ee1b37e0acb24e25>,
    ...

These bytes are typically then processed with normal in-memory Python
functions, like ``json.loads``, ``pd.read_csv``, or ``fastavro.reader``.  When
these functions don't accept bytestrings directly, but instead prefer a file
object, we use the ``BytesIO`` file interface.

Below we include the docstring for ``distributed.hdfs.read_bytes``, which
includes further performance considerations and keyword arguments.

.. autofunction:: distributed.hdfs.read_bytes

``write_bytes``
~~~~~~~~~~~~~~~


If the data is blocked, as in
HDFS, then each future corresponds to one block on the storage system.  If the
storage system is data-local, meaning that data lives directly on the compute
nodes, then care will be taken to load data on the right node in order to
ensure data locality and maximize I/O from disk.


As with all ``distributed`` operations, these futures begin execution
immediately.  To delay immediate execution supply the keyword argument
``lazy=True`` to receive lazy `dask value`_ objects that can be manipulated
and finally submited with the ``Executor.compute`` method.

.. _`dask value`: http://dask.readthedocs.org/en/latest/imperative.html

.. code-block::

   >>> lazy_values = read_bytes('/data/2015/')
   >>> lazy_values
   [Value('read_bytes-2576405bf5525818ef3b6c3f72378fa0'),
    Value('read_bytes-4dec252d7f1714175ff3e7d70663a1ba'),
    Value('read_bytes-01b6ceb9c31475589385f17b1dc86665'),
    Value('read_bytes-42dd7a97c73b7993ee1b37e0acb24e25'),
    ...



``read_bytes/write_bytes``




Distributed computes on data; it does not store data.  Distributed is not a
database.
