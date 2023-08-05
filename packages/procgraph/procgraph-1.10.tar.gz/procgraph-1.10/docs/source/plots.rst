
Usage patterns
==============

Wait until all signals are ready: ::

    def update(self):
        if not self.all_input_signals_ready():
            return


Filter an unknown number of signals. Just adapt the ``identity`` block. ::

    class Identity(Block):
        Block.alias('identity')
        Block.input_is_variable('Input signals.', min=1)
        Block.output_is_variable('Output signals, equal to input.')

        def update(self):
            # Just copy the input to the output
            for i in range(self.num_input_signals()):
                self.set_output(i, self.get_input(i),
                                   self.get_input_timestamp(i))





Plotting
========

Accumulate and plot history: ::

    commands -> |historyt interval=100| --> |plot width=$width height=200| -> commands_rgb
    