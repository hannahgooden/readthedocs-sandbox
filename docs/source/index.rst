``ezmsg``
===================================

Messaging and Multiprocessing.

``ezmsg`` is a pure-python implementation of a directed acyclic graph (DAG) pub/sub messaging pattern based on LabGraph which is optimized and intended for use in constructing real-time neural signal processing implementations. ``ezmsg`` implements much of the LabGraph API (with a few notable differences), and owes a lot of its design to the LabGraph developers/project. Afterall, imitation is the sincerest form of flattery.

``ezmsg`` is extremely fast and uses Python's (currently) new multiprocessing.shared_memory module to facilitate efficient message passing without C++ or any compilation/build tooling.

Try experimenting with ``ezmsg`` immediately!
<insert google colab link here>

.. TODO: remove this, it's still here because the link is nice
Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.

Contents
--------

.. toctree::

   getting-started
   api
