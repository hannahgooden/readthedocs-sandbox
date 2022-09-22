API
===

An ``ezmsg`` system is created from a few basic components. ``ezmsg`` provides a framework for you to define your own graphs using its building blocks. Inherit from its base components to define a pipeline that works for your project.

.. TODO: add figure showing how components work together

Collection
----------

Connects ``Units`` together by defining a graph which connects ``OutputStreams`` to ``InputStreams``.

Lifecycle Hooks
^^^^^^^^^^^^^^^

.. py:method:: configure( self )

   Runs when the ``Collection`` is instantiated. This is the best place to call ``Unit.apply_settings()`` on each member ``Unit`` of the ``Collection``.

Overridable Methods
^^^^^^^^^^^^^^^^^^^^

.. py:method:: network( self ) -> NetworkDefinition

   In this method, define and return a ``NetworkDefinition`` which defines how ``InputStreams`` and ``OutputStreams`` from member ``Units`` will be connected.

.. py:method:: process_components( self ) -> Tuple[Unit|Collection, ...]

   In this method, define and return a tuple which contains ``Units`` and ``Collections`` which should run in their own processes.

Message
-------

To define unique data types, inherit from ``Message``. Messages use `Python dataclasses <https://docs.python.org/3/library/dataclasses.html>`_ under the hood, so they can be treated in a similar way.

.. code-block:: python

   class YourMessage(Message):
      attr1: int
      attr2: float

.. note:: 
   ``Message`` uses type hints to define member variables, but does not enforce type checking.

Network Definition
------------------

.. py:class:: NetworkDefinition()

   Wrapper on ``Iterator[Tuple[OutputStream, InputStream]]``.

.. _run-system:

run_system
----------

.. py:method:: run_system(system: System, num_buffers: int = 32, init_buf_size: int = 2**16, backend_process: BackendProcess=None)

   Begin execution of a ``System``.

Settings
--------

To pass parameters into a ``Unit``, ``Collection``, or ``System``, inherit from ``Settings``. ``Settings`` uses `Python dataclasses <https://docs.python.org/3/library/dataclasses.html>`_ under the hood, so it can be treated in a similar way.

.. code-block:: python

   class YourSettings(Settings): 
      setting1: int
      setting2: float

To use, add the ``Settings`` object to a ``Unit``.

.. code-block:: python

   class YourUnit(Unit):

      SETTINGS: YourSettings

Instantiate the ``Settings`` object in the ``Collection`` or ``System`` which will hold the ``Unit``.

.. code-block:: python

   class YourSystem(System):

      YOUR_UNIT = YourUnit()

      def configure():
         YOUR_UNIT.apply_settings(YourSettings(
            setting1: int,
            setting2: float
         ))

.. note:: 
   ``Settings`` uses type hints to define member variables, but does not enforce type checking.

State
-----

To track a mutable state for a ``Unit``, ``Collection``, or ``System``, inherit from ``State``. ``State`` uses `Python dataclasses <https://docs.python.org/3/library/dataclasses.html>`_ under the hood, so it can be treated in a similar way.

.. code-block:: python

   class YourState(State):
      state1: int
      state2: float

To use, add the ``State`` object to a ``Unit``. Member functions can then access and mutate the ``State`` as needed during function execution.

.. code-block:: python

   class YourUnit(Unit):

      STATE: YourState

.. note:: 
   ``State`` uses type hints to define member variables, but does not enforce type checking.

Stream
------

Facilitates a flow of ``Messages`` into or out of a ``Unit`` or ``Collection``. 

.. class:: InputStream(Message)

   Can be added to any ``Unit`` or ``Collection`` as a member variable. Methods may subscribe to it.


.. class:: OutputStream(Message)

   Can be added to any ``Unit`` or ``Collection`` as a member variable. Methods may publish to it.

System
------

A type of ``Collection`` which represents an entire ``ezmsg`` graph. ``Systems`` have no input or output streams and are runnable via :ref:`run-system`.

Lifecycle Hooks
^^^^^^^^^^^^^^^

.. py:method:: configure( self )

   Runs when the ``System`` is instantiated. This is the best place to call ``Unit.apply_settings()`` on each member ``Unit`` of the ``System``.

Overridable Methods
^^^^^^^^^^^^^^^^^^^^

.. py:method:: network( self ) -> NetworkDefinition

   In this method, define and return a ``NetworkDefinition`` which defines how ``InputStreams`` and ``OutputStreams`` from member ``Units`` will be connected.

.. py:method:: process_components( self ) -> Tuple[Unit|Collection, ...]

   In this method, define and return a tuple which contains ``Units`` and ``Collections`` which should run in their own processes.

Unit
----

Represents a single step in the graph. To create a ``Unit``, inherit from the ``Unit`` class.

Lifecycle Hooks
^^^^^^^^^^^^^^^

The following lifecycle hooks in the ``Unit`` class can be overridden:

.. py:method:: initialize( self ) 

   Runs when the ``Unit`` is instantiated. All required parameters for ``State`` variables must have be given values in this lifecycle hook if they do not have defaults already defined.

.. py:method:: shutdown( self )

   Runs when the ``System`` terminates.

Function Decorators
^^^^^^^^^^^^^^^^^^^

These function decorators can be added to member functions. A function can have any number and combination of decorators.

.. py:method:: @subscriber(InputStream)

   A function will run once per message received from the ``InputStream`` it subscribes to. Example:

   .. code-block:: python

      INPUT = ez.InputStream(Message)

      @subscriber(INPUT)
      async def print_message(self, message: Message) -> None:
         print(message)
   
   A function can have both ``@subscriber`` and ``@publisher`` decorators.

.. py:method:: @publisher(OutputStream)

   A function will yield messages on the designated ``OutputStream``.

   .. code-block:: python

      from typing import AsyncGenerator

      OUTPUT = OutputStream(ez.Message)

      @publisher(OUTPUT)
      async def send_message(self) -> AsyncGenerator:
         message = Message()
         yield(OUTPUT, message)

.. py:method:: @main

   Designates this function to run as the main thread for this ``Unit``. A ``Unit`` may only have one of these.

.. py:method:: @thread

   Designates this function to run as a background thread for this ``Unit``.

.. py:method:: @task 

   Designates this function to run as a task in the task/messaging thread.

.. py:method:: @process

   Designates this function to run in its own process.

.. py:method:: @timeit

   ``ezmsg`` will log the amount of time this function takes to execute.

Public Methods
^^^^^^^^^^^^^^

A class which inherits from ``Unit`` also inherits one public method:

.. function:: Unit.apply_settings( self, settings: Settings )

   Update a ``Unit`` 's ``Settings`` object.
