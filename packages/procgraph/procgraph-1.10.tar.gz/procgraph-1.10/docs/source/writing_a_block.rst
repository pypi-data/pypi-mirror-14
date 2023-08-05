
.. include:: definitions.txt

.. py:module:: procgraph

.. py:currentmodule:: procgraph

.. _`creating_new_blocks`:

Blocks
=======

|procgraph| **models** are created by interconnecting **blocks**. 
The abstractions that |procgraph| uses are common to many other environments, 
such as Simulink.

Each block has zero or more of the following:

* **configuration parameters**, 
  each with or without a default value, that must be specified when the model
  is instantiated.

* **input signals**

*  **output signals**


|procgraph| allows you to attach a documentation string to configuration 
parameters, inputs and outputs, that is reproduced neatly in the documentation, 
so use every occasion to document your ideas.


Creating blocks
---------------

There are three ways to create new blocks:

1. Every model created using |procgraph|'s model language can be reused as 
   a block from another model. Just define inputs, outputs, and configuration.

   The model syntax is explained in :ref:`creating_models`.

2. To create a *stateless* function from any Python function,
   you just need to use the decorator :py:func:`simple_block`.

   This is explained in :ref:`simple_blocks`.

3. To create a *stateful* block in Python, subclass the class ``Block``,
   and define the methods ``init()``, ``update()``, and so on.

   This is explained in :ref:`normal_blocks`.



Advanced topics
---------------
  
The previous three cases cover 95% of what you need to do in |procgraph|.
However, there are some special cases that require more discussion.

* **Generators*: A normal block updates its output only when it has new input.
  A block that produces output even without a new input is called a "Generator"
  and it is treated differently by |procgraph|.

  This is explained in :ref:`creating_generators`.
 
* Using timestamp from simple blocks.

  |towrite|



