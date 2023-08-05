
.. _tutorial_naming_signals:

Naming signals
---------------

We will see that |procgraph| models can become quite complex.
In particular, you are not limited to have only one series of blocks;
you can process the same signal in a parallel pathway.
So one necessary ability is being able to give *names* to signals
so that you can refer to them later.

You can see an example of this in :download:`tutorial01_signals.pg`:

.. literalinclude:: tutorial01_signals.pg
   :language: ruby

Here, we give the name ``rgb`` to the output of the first block.
Then, we can refer to this signal later, and use it as input to 
the second block. 

In general, if a block has multiple outputs, you would use the
syntax: ::

	|block| --> signal1, signal2, signal3
	
to give the various outputs names.

