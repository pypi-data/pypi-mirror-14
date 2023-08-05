Setup Network
=============

A ``distributed`` network consists of one ``Scheduler`` node and several
``Worker`` nodes.  One can set these up in a variety of ways


``dcluster``
------------

The convenience script ``dcluster`` opens several ssh connections to your
target computers and initializes the network accordingly.  You can give it a
list of hostnames or IP addresses::

   $ dcluster 192.168.0.1 192.168.0.2 192.168.0.3 192.168.0.4

Or you can use normal UNIX grouping::

   $ dcluster 192.168.0.{1,2,3,4}

Or you can specify a hostfile that includes a list of hosts::

   $ cat hostfile.txt
   192.168.0.1
   192.168.0.2
   192.168.0.3
   192.168.0.4

   $ dcluster --hostfile hostfile.txt


``dscheduler`` and ``dworker``
---------------------------

Alternatively you can launch the ``dscheduler`` and ``dworker`` processes in
some other way either by manually SSHing into remote nodes or by using a
deployment system like SunGrid Engine.

Launch ``dscheduler`` on one node::

   $ dscheduler
   Start scheduler at 192.168.0.1:8786

Then launch ``dworker`` on the rest of the nodes, providing the address to the
node that hosts ``dscheduler``::

   $ dworker 192.168.0.1:8786
   Start worker at:            192.168.0.2:12345
   Registered with center at:  192.168.0.1:8786

   $ dworker 192.168.0.1:8786
   Start worker at:            192.168.0.3:12346
   Registered with center at:  192.168.0.1:8786

   $ dworker 192.168.0.1:8786
   Start worker at:            192.168.0.4:12347
   Registered with center at:  192.168.0.1:8786


``Scheduler`` and ``Worker`` objects
---------------------------------

Alternatively you can start up the ``distributed.scheduler.Scheduler`` and
``distributed.worker.Worker`` objects within a Python session manually.  Both
are ``torando.tcpserver.TCPServer`` objects.

Start the Scheduler, provide the listening port (defaults to 8786) and Tornado
IOLoop (defaults to ``IOLoop.current()``)

.. code-block:: python

   from distributed import Scheduler
   s = Scheduler(loop=loop)
   s.start(port)

On other nodes start worker processes that point to the IP address and port of
the scheduler.

.. code-block:: python

   from distributed import Worker
   w = Worker('192.168.0.1', 8786, loop=loop)
   w.start(0)  # choose randomly assigned port

Alternatively, replace ``Worker`` with ``Nanny`` if you want your workers to be
managed in a separate process by a local nanny process.

If you do not already have a Tornado event loop running you will need to create
and start one, possibly in a separate thread.

.. code-block:: python

   from tornado.ioloop import IOLoop
   loop = IOLoop()

   from threading import Thread
   t = Thread(target=loop.start)
   t.start()


Cleanup
-------

It is common and safe to terminate the cluster by just killing the processes.
The workers and scheduler have no persistent state.

Programmatically you can use the client interface (``rpc``) to call the
``terminate`` methods on the workers and schedulers.
