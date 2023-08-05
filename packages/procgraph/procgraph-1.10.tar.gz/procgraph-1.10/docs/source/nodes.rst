

Types of nodes:

	A - fixed number of inputs, fixed number of outputs
		Most of the blocks.
	
	B - variable number of inputs (>= K), fixed number of outputs
		For example: min, max, most numpy functions
			
	C - variable number of inputs (>= K), same number of outputs
		For example: sync


In the case of a Model: only type A is supported.

In the case of a Block, we allow all 3.

	class TypeA(Block):
		block_config()
		block_input('input1', 'desc')
		block_input('input2', 'desc')
		block_output('out', 'desc')
		...
		
	class TypeB(Block):
		block_input_is_variable('Signals to be summed (at least 2).', min=2)
		block_output('output2', 'Sum of the signals.')
		...

	class TypeC(Block):
		block_input_is_variable('Signals to be summed.', min=K)
		block_output_is_variable('Synchronized signals.')
		

In the case of a simple block




