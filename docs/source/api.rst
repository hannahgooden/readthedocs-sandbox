API
===

An ezmsg system is created from a few basic components. Ezmsg provides a framework for you to define your own graphs using its building blocks. Inherit from its base components to define a pipeline that works for your needs.

.. TODO: add figure showing how components work together

Message
-------

To define unique data types, inherit from ``ez.Message``. Messages use `Python dataclasses <https://docs.python.org/3/library/dataclasses.html>`_ under the hood, so they can be treated in a similar way.

.. code-block:: python

   class YourMessage(ez.Message):
      attr1: int
      attr2: float

.. note:: 
   ``ez.Message`` uses type hints to define member variables, but does not enforce type checking.

Component
---------

``ezmsg`` allows you to build modular systems whose elements can be switched out easily. Consider the use case of building a processing pipeline where you will be experimenting with adding/subtracting steps until you find an optimal workflow. ``ezmsg`` allows you to easily separate each step into a discrete entity and piece together a workflow from those entities.

An ``ez.Component`` is a base class for a discrete step in the processing pipeline. 

Unit
^^^^

Collection
^^^^^^^^^^

System
^^^^^^

Stream
------