from procgraph import Generator, Block
import numpy as np
from procgraph_mpl.plot_generic import PlotGeneric
from procgraph_mpl.plot_anim import PlotAnim



class JitteryClock(Generator):
    Block.alias('jittery_clock')
    Block.config('interval', 'Delta between ticks.', default=0.1)
    Block.config('noise', 'Jitter.', default=0.02)
    Block.output('clock', 'Clock signal.')
    Block.config('length', 'Total interval', default=None)
    
    def init(self):
        self.state.clock = 0

    def update(self):
        self.set_output('clock', 'orig: %1.3f' % self.state.clock, timestamp=self.state.clock)
        
        dt = self.config.interval + np.random.rand() * self.config.noise
        self.state.clock += dt

    def next_data_status(self):
        if self.config.length is not None and self.state.clock > self.config.length:
            return (False, None)
        else:
            return (True, self.state.clock + self.config.interval)

class JitteryDisplay(Block):
    Block.alias('jittery_display')

    Block.input('clock')
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=320,
                                        height=240,
                                        transparent=False,
                                        tight=False,
                                        keep=True)
        self.first_timestamp = None
        self.plot_anim = PlotAnim()
        self.nframes = 0
        
    def update(self):
        if self.first_timestamp is None:
            self.first_timestamp = self.get_input_timestamp(0)
        self.time_since_start = self.get_input_timestamp(0) - self.first_timestamp
        self.nframes += 1
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
        
    def plot(self, pylab):
        self.plot_anim.set_pylab(pylab)
        self.plot_anim.text('clock', 0, 1, '%5.2f' % self.time_since_start)
        self.plot_anim.text('frames', 0, 0.5, '%d' % self.nframes)

        self.plot_anim.text('value', 0, 0.24, self.input.clock)
        pylab.axis((-0.2, 1.1, -0.1, 1.1))

