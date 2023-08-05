.. _tutorial_basic_syntax:

Basic syntax
------------

The basic |procgraph| metaphors are *blocks* and *signals*. A *model* is an interconnection of blocks, and it is specified using |procgraph|'s *model language*. This language is very much inspired by ASCII art; the idea being that a graphical representation of blocks is useful to understand your models, yet, the fact that everything is plain text makes the source clear, and editing fast.

Enough words! The first model that we consider can be found in the file
:download:`tutorial00_basics.pg`:

.. literalinclude:: tutorial00_basics.pg
   :language: ruby

This model is composed by two blocks: :ref:`block:mplayer` and :ref:`block:mencoder`. An instantiation of a block is specified using the syntax  ``|block-type param=value|``, with multiple parameters allowed. A complete list of the blocks, with documentation on what parameters they accept, is available at :ref:`library`; this tutorial will explain also how to create your own blocks.

The two blocks are connected by the arrow ``-->``. This means that all signals from the first block flow into the second. In this case,  :ref:`block:mplayer` has only one output, and  :ref:`block:mencoder` has only one input, but we will see that blocks can be very flexible in how many signals they accept or produce.

It's time to run this model. As you might have guessed, the model transcodes one
video file to another format. Albeit |procgraph| is pretty much data-agnostic, most of the examples involve
reading and manipulating a video, as it is fun to have an immediate visual
feedback of what you are doing. All the scripts refer to the file :download:`coastguard.mp4`,
which should be in your current directory; you can, of course, use any video you want.

|procgraph| has both an API to run modules from inside your Python code (see :ref:`running`), and a command-line program that runs the models for you, called ``pg``. In this tutorial, we are going to use the latter. If |procgraph| is properly installed, you can run a model using
the syntax ``pg <model name>``. If you saved the above model to a file ``tutorial00_basics.pg``, then you can run it using: ::

	$ pg tutorial00_basics

The expected output is :download:`coastguard00.avi`.

