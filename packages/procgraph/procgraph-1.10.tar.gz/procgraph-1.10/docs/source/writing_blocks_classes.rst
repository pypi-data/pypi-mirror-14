.. _normal_blocks:


More complicated blocks
------------------------

To create a stateful block, subclass the class ``Block`` and use the class methods
to define input, output and configuration.



Quick summary of Block API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a summary of how to create a new block type, and how to interact with
the API:

1. Subclass :py:class:`Block`.

2. Use the method :py:func:`Block.alias` to define the block type name.

3. Use the method :py:func:`Block.config` to define the block configuration (if any).

4. Use the method :py:func:`Block.input` and :py:func:`Block.output` to define input and output  
   signals (if any).

5. **do not use** the ``__init__()`` method; rather, do any initialization in the ``init()`` 
   method, which is called once, before any input is available.

6. Put the block logic in the ``update()`` function, which is called every time a new input is available.

In the ``init()`` function:

* You can access configuration parameters using the syntax: ::

      self.config.<parameter name>

* You can access state variables using: ::

      self.state.my_state = ...

* You cannot access input/output yet.


In the ``update()`` function:

* You can access configuration parameters and state variables.

* You can access input and output using the syntax: ::

      received = self.input['signal_name'] # by name
      received = self.input.signal_name    # by name (syntax sugar)
      received = self.input[0]             # by number

  and output as well: ::

      self.output.processed = ...
      self.output['processed'] = ...
      self.output[0] = ...



Example of a stateless block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is the minimal example of a stateless block. It defines
a gain block that could be invoked with this syntax: ::


     source --> |gain k=2| --> source_times_2


Note the use of :py:func:`Block.alias` to give an alias for the block type (if not given, the class name will be used); the use of :py:func:`Block.config` to specify a configuration parameter,
and :py:func:`Block.input`, :py:func:`Block.output` to specify (and document) input and output. ::

    from procgraph import Block
    
    class Gain(Block):
        ''' A simple example of a gain block. '''
    
        Block.alias('gain')
    
        Block.config('k', 'Multiplicative gain')
    
        Block.input('in', 'Input value')
        Block.output('out', 'Output multiplied by k.')
    
        def update(self):
            self.output[0] = self.input[0] * self.config.k
            # equivalent to:
            # self.output['out'] = self.input['in'] * self.config.k


The "meat" of the block goes in the ``update()`` function. It is called whenever 
one of the inputs change. In the ``update()`` function, you compute the
output from the input. To access the input, there are several 



Example of a stateful block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is a minimal example of a stateful block. It has one input and one output. 
The output is the sample average of the input. There are two state variables: the number
of samples processed and the current sample average.

Note how the block uses the ``init()`` function to initialize its structures,
and the ``self.state`` structure to hold them. ::

    class Expectation(Block):
        ''' Computes the sample expectation of a signal. '''
        Block.alias('expectation')
        
        Block.input('x', 'Any numpy array.')
        Block.output('Ex', 'Expectation of input.')
        
        def init(self): 
            self.state.num_samples = 0
        
        def update(self):
            N = self.state.num_samples
            
            if N == 0:
                self.state.Ex = self.input.x.copy()
            else:
                self.state.Ex = (self.state.Ex * N + self.input.x) / float(N + 1);
        
            self.state.num_samples += 1
            self.output.Ex = self.state.Ex 



(See :ref:`execution_model` for advanced topics dealing with timestamp)




The init() method
^^^^^^^^^^^^^^^^^

Do not use your class's constructor to initialize the block. There are
all sorts of issues with custom constructors that make writing things
such as module serialization hard.

Instead, |procgraph| provides the facilities you need for configuration,
initialization, etc.

The init() method is supposed to set up 
 method: basic usage.


The return value of init() is ignored, except in one special case described in the 
next section.

Advanced init() usage -- partial initialization

Note that there some special cases for which initialization cannot be
completed before until the block is in the model and signals are connected.
One typical example is when we want to write a block that can operate
on multiple signal, of which we do not know the number. Consider as an example
the case in which we want to write a block performing a "min" operation.::

	# three values
	|constant value=1| -> x 
	|constant value=2| -> y
	|constant value=3| -> z
	
	# take the min
	x,y,z -> |min| -> minimum

When the block min is initialized, it is outside the block


The update() method
^^^^^^^^^^^^^^^^^^^

* If the computation is not finished, return Block.UPDATE_NOT_FINISHED.
  This will tell |procgraph| to consider the computation still pending,
  and update() will be called again in the future with the same input signals.
  
  All other return values are just ignored by |procgraph|.



The finish() method
^^^^^^^^^^^^^^^^^^^

|towrite|




