API
===

``ezmsg`` allows you to build modular systems whose elements can be switched out easily. Consider the use case of building a processing pipeline where you will be experimenting with adding and removing steps until you find an optimal workflow. ``ezmsg`` allows you to easily separate each step into a discrete entity and piece together a workflow from those entities. Check out the `Examples <https://github.com/iscoe/ezmsg/tree/master/examples>`_ to see how this works!

An ``ezmsg`` system is created from a few basic components. ``ezmsg`` provides a framework for you to define your own graphs using its building blocks. Inherit from its base components to define a pipeline that works for your project.

.. TODO: add figure showing how components work together

Message
-------

To define unique data types, inherit from ``Message``. Messages use `Python dataclasses <https://docs.python.org/3/library/dataclasses.html>`_ under the hood, so they can be treated in a similar way.

.. code-block:: python

   class YourMessage(ez.Message):
      attr1: int
      attr2: float

.. note:: 
   ``Message`` uses type hints to define member variables, but does not enforce type checking.


Unit
----

A ``Unit`` represents a single step in the graph. To create a ``Unit``, inherit from the ``Unit`` class. Use lifecycle hooks, function decorators, and one public method to define a ``Unit`` 's behavior.

Lifecycle Hooks
^^^^^^^^^^^^^^^

The following lifecycle hooks in the ``Unit`` class can be overridden:

.. py:method:: initialize( self ) 

   Runs when the ``Unit`` is instantiated. All required parameters for ``State`` variables must have be given values in this lifecycle hook if they do not have defaults already defined.

.. py:method:: shutdown( self )

   Runs when the ``System`` terminates.

Function Decorators
^^^^^^^^^^^^^^^^^^^

These function decorators can be added to member functions:

.. py:method:: @subscriber(InputStream)

   A function will run once per message received from the ``InputStream`` it subscribes to. Include ``message: MessageType`` as a parameter when defining the function to access it within. Example:

   .. code-block:: python

      INPUT = ez.InputStream(ez.Message)

      @subscriber(INPUT)
      async def print_message(self, message: ez.Message) -> None:
         print(message)
   
   A function can have both ``@subscriber`` and ``@publisher`` decorators.

.. py:method:: @publisher(OutputStream)

   A function will yield messages on the designated ``OutputStream``.

   .. code-block:: python

      from typing import AsyncGenerator
      OUTPUT = ez.OutputStream(ez.Message)

      @publisher(OUTPUT)
      async def send_message(self) -> AsyncGenerator
         message = ez.Message
         yield(OUTPUT, message)

   

Methods
^^^^^^^

``Units`` have a single public method:

.. function:: Unit.apply_settings( self, settings: Settings )

   Update a ``Unit`` 's ``Settings`` object.


Collection
----------

A ``Collection`` can be created by connecting ``Units`` together.

System
------

A ``System`` is a subclass of ``Collection`` which is runnable. The top level of every ``ezmsg`` graph should be a ``System``. 

Stream
------

A ``Stream`` represents 