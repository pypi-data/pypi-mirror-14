# TODO: finish this?  This is really hard to write!
#
#
#from collections import namedtuple
#
#from procgraph import Block 
#
#Sample = namedtuple('Sample', 'timestamp value')
#
#if False:
#    class Sync2(Block):
#        ''' 
#        This block synchronizes a set of N sensor streams.
#        
#        The first signal is called the "master" signal.
#        The other (N-1) are slaves.
#         
#        '''
#        Block.alias('sync')
#    
#        Block.input_is_variable('Signals to synchronize. The first is the master.', min=2)
#        Block.output_is_variable('Synchronized signals.')
#    
#        def init(self):    
#            # output signals get the same name as the inputs
#            names = self.get_input_signals_names()
#            
#    #        self.state.ready = {}
#    #        for signal in names:
#    #            self.state.ready[signal] = None
#    
#            self.state.master = names[0]
#            self.state.slaves = names[1:]
#            
#            self.state.stage = {}
#            
#        def update(self):
#            def debug(s):
#                if True:
#                    print 'sync %s %s' % (self.name, s)
#                    
#            names = self.get_input_signals_names()
#            for i, name in enumerate(names):
#                current_timestamp = self.get_input_timestamp(i)
#                current_value = self.get_input (i)
#                if current_timestamp == 0: # XXX change this
#                    debug('Ignoring %s because timestamp still 0' % name)
#                    continue
#                sample = Sample(timestamp=current_timestamp, value=current_value)
#    
#                # - only add if there is a master
#                # - simply replace older samples
#                if  name == self.state.master or self.state.master in self.state.stage:
#                    
#                    if not name in self.state.stage or\
#                        current_timestamp != self.state.stage[name].timestamp:
#                    
#                        if name in self.state.stage:
#                            debug('Replacing signal "%s" with new  ts=%s' % \
#                              (name, current_timestamp))            
#                    
#                        debug('Inserting %s ts %s' % (name, sample.timestamp))
#                        self.state.stage[name] = sample
#                    
#                        
#                else:
#                    debug('Dropping %s because master "%s" not here' % \
#                          (name, self.state.master))
#            
#            debug('Num  %s' % (len(self.state.stage),))
#                    
#            # if all signals are present, add them
#            if len(self.state.stage) == 1 + len(self.state.slaves):
#    
#                for name, sample in self.state.stage.items():
#                    value, timestamp = sample
#                    self.set_output(name, value, timestamp)
#                    
#                self.state.stage = {} 
#                
#                debug('Sent one set')
#                
#            
#            
#    #    def next_data_status(self):
#    #        output = self.get_state('output')
#    #        if not output: # no output ready
#    #            return (False, None)
#    #        else:
#    #            timestamp = self.output[-1][0]
#    #            return (True, timestamp)
#        
#         
