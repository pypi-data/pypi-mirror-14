.. include:: definitions.txt

.. _`faq`:

FAQ
===

What is the difference with Simulink/Labview?
-----------------------------------------------

These are the main design differences with respect  

* |procgraph| is Python based and free.
* |procgraph| has a text-based rather than graphical-based representation of models. Trust me, it's better.
* |procgraph| is designed for discrete, timestamped data from various realtime/recorded sources, rather than for continuous-time data.
* |procgraph| does not support feedback loops  (see: :ref:`whyNotFeedback`).


.. _whyNotFeedback:

Why no feedback loops?
-----------------------

The main reason is that, for arbitrary blocks, it is hard to reason
about a consistent semantics.

For example, consider the simple arrangement with one block with a closed loop: ::
  
               ________
      u ----> |        |
              | block  | -----> y
       -----> |________|  |
      |___________________,


At time 0, the signal ``u`` is defined, but ``y`` is not. That means that the code in
``block`` must have a special case for this situation. It's unclear at the moment 
how to design an API that takes into account this special case.

I felt that any choice would add a great deal of complexity, and would make |procgraph| into a full-fledged framework rather than a quick and non-obtrusive tool for rapid prototyping.

Suggestions are welcome...

