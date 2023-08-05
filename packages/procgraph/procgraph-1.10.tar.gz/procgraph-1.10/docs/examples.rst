Overview
========


Why:
- usable from logs/realtime
- signals with different rates, semantics for sync


Sources
^^^^^^^
These could be, for example:
- log readers
- real interfaces
- random interfaces
Each source can produce more than one signal.
Each signal has independent timestamp.


The model can be run:
- from external, push-style

	model.push('input', rand(1))
	
- from 

Signals:
^^^^^^^
	name --
	shape -- might be None if not known
	
	Each sample has:
		timestamp, timestamp_host, value
		value of None means that processing did not get there


Methods:
	An empty constructor
	s.init(**params)
	s.get_signals()
	s.has_more()
	s.get()
	
	
	Example random generator:
	
		class RandomGenerator(Node):
		
			def init(variance):
				self.variance = variance
				self.define_input_signals(0)
				self.define_output_signals(1, dtype=float32)
				
			def update():
				self.set_output(0, rand(1) * self.variance)
	
	Example gain:
	
		class Gain(Node):
		
			def init(gain):
				self.gain = gain
				self.define_input_signals(1)
				self.define_output_signals(1)
			
			def update():
				self.set_output(0, self.get_input(0) * self.gain)

	Example with memory:
	
		class Delay(Node):
		
			def init():
				self.set_state(0, None)
				
			def update():
				self.set_output(0, self.get_state(0))
				self.set_state(0, self.get_input(0))
			
			
			

Processors:
^^^^^^^^^^

	s.reset()


Model connection
----------------

A model is defined by:

	a set of blocks
		attributes for the blocks
	a set of signals
		attributes for the signals
	which signal is the input/output to which block
	
	--- !model
	name: A simple model
	blocks:
		- block1:
		 anonymous
		 input 
		 output
	
	
	{
		'class': 'model',
	
	}
		
		{'class': 'block', 'name': 'block1', 
		  'parameters': {}, 'output': ['value'], 'input': []  }
	]

A common code representation



Syntax
======


The basic operation looks like this::

	u --> |operation| --> result
	
The form can be chained::

	u --> |filter| --> u1 --> |operation| --> result
	
Anonymous connections::

    u --> |operation| --> |operation2| --> result

Giving a name to the blocks::

	u --> |op1:operation| -->  result




Blocks have parameters. There are two ways to set them. 
Either in the block itself:


Or on a separate line

	op1.param1 = 1
	op1.param2 = 2

Setting a parameter online:

	u --> |op1 operation op:tan| --> result


model 1


y --> name(derivative) --> [y_dot, y_avg]

	y_dot --> |expectation:e1| --> y_dot_mean
	y_dot --> |expectation_mean:e2| --> y_dot_mean


log1(log_reader) --> *

log1: 
	directory: pwd
	
	
	
Feedback connections
--------------------

|input name=y| -> y -> |gain k=0.9| -> 
|feedback var=z| -> y_old -> |gain k=0.1| 


	y, y_old 
	
	
Syntax for multiple models in the same file
--------------------------------------------

Multiple models look like this::
    
        --- model <model name>
        
        model content
        
        --- model <model name>
        
        other
	
	
signals can be: 
	values = numpy array (size=())
	timestamp, values = tuple of two elements
	
* is an hash, must be in the form
	{signal_name: signal }
	
	
sources have symbols 

Other examples from http://bloodgate.com/perl/graph/manual/features.html


	[ Bonn ] { label: Berlin; } --> [ Berlin ]
[ Potsdam ], [ Mannheim ] 
  --> { end: back,0; }
[ Weimar ]
  --> { start: front,0; } [ Finsterwalde ], [ Aachen ]
       


model learning_example ------------------

	y --> |whitening| --> y_white      
	u --> |whitening| --> u_white

	[y_white, u_white] --> | Tlearner | --> T
                    

	y_gx --> |op|{a:2} --> y_gx_sign


model Tlearner -------------------

[ in0, in1 ] --------> |display|






Example: differentiation
-----------------------

This can be created 

	name: Discrete derivative, d/dt, deriv
	in: x
	out: x_dot
	
	# get the timestamp as a signal
	x  --> |timestamp| --> t
	
	# create a delayed version of x
	x ---> |delay| ---> x_old  --> |timestamp| --> t_old
	
	# compute differences
	[x, x_old] --> |-| --> x_inc  
	[t, t_old] --> |-| --> t_inc 
	
	[x_inc, t_inc] --> |/| --> x_dot
                


Using more ASCII art:
          +++++++++++
    x --> |timestamp| --> t ------------------------>|
    |     +++++++++++                                |
	|    +++++++             +++++++++++             |--->|/|-,
	|--> |delay| --> x_old --> |timestamp| --> t_old -->|        |
	|    +++++++      |       +++++++++++
	                |
	
	[x, x_old] --> |-| --> x_inc |
	                           |-> |/| --> x_dot
	[t, t_old] --> |-| --> t_inc |



Use cases
=========


Loading and using a model
-------------------------

	model = sg.load('model1.sgm')

	while True:
		model.push('y', rand(1))
		
		if not model.pipeline_full(): continue
		
		print model.get()




















