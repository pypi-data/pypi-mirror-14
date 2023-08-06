FLOTILS
#######

Some utility functions and classes I use in many projects.

.. image:: https://img.shields.io/pypi/v/flotils.svg   
    :target: https://pypi.python.org/pypi/flotils

.. image:: https://img.shields.io/pypi/l/flotils.svg   
    :target: https://pypi.python.org/pypi/flotils

.. image:: https://img.shields.io/pypi/dm/flotils.svg   
    :target: https://pypi.python.org/pypi/flotils

**Note:** This package does not follow the UNIX philosophy. (It does more than
one thing).
Though some modules might get moved to their own packages in the future,
this is currently not planned.

Documentation at
`GitHub <https://github.com/the01/python-flotils/tree/master/docs>`_

logable
=======
Module to ease logging efforts

**Supports**

* Using logging calls directly on instance
* Module logger
* Optional instance id
* Add method information to log
* Default logging config

In ``class Demo(Logable)`` you are able to use the logging calls directly
(eg. ``self.debug()``, ``self.warning()``, ``self.exception()``,..) to produce 
structured logging output like

::

 DEBUG:Demo:working on something
 INFO:Demo:Finished working
 DEBUG:root:Inbetween
 WARNING:Demo:Something might go wrong
 ERROR:Demo:Something went wrong
 WARNING:Demo:Told you!

The ``Logable`` class allows you to specify an id for an instance 
``Demo({'id': "demo2"})`` resulting in

::

 DEBUG:Demo.demo2:working on something
 INFO:Demo.demo2:Finished working
 DEBUG:root:Inbetween
 WARNING:Demo.demo2:Something might go wrong
 ERROR:Demo.demo2:Something went wrong
 WARNING:Demo.demo2:Told you!

Also supports method information:

::

 2015-12-27 20:30:48 DEBUG   [Demo.demo2.work_on_something] working on something
 2015-12-27 20:30:48 INFO    [Demo.demo2.work_on_something] Finished working
 2015-12-27 20:30:48 DEBUG   [root] Inbetween
 2015-12-27 20:30:48 WARNING [Demo.demo2.work_on_something_else] Something might go wrong
 2015-12-27 20:30:48 ERROR   [Demo.demo2.work_on_something_else] Something went wrong
 2015-12-27 20:30:48 WARNING [Demo.demo2.work_on_something_else] Told you!

For information on how to enable this, please have a look at
``logable.default_logging_config``


loadable
========
Module to ease json(file) efforts

**Supports**

* loading/writing json both as string and file
* ``date``, ``time`` and ``datetime`` types supported (saved and loaded as utc)
* class to load/save settings from/to file

``Loadable`` is a child class of ``Logable``, thus inheriting all logging
capabilities.

To tell ``class Demo(Loadable)`` to create an instance from a settings file,
just write ``Demo({'settings_file': "path/to/settings.json"})``.

Settings provided in ``__init__()`` overwrite the ones set in the file.


runable
=======
Module to ease starting/stoping of classes

**Supports**

* Startable (Class can be started ``start()``) 
* Stopable (Class can be stopped ``stop()``)
* StartStopable (``Startable()`` + ``Stopable()``)
* SignalStopWrapper (Listens for SIGTERM and SIGINT signals and stops the class)
