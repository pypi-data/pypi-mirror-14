from procgraph import Block

class Psychedelic(Block):
    Block.alias('psychedelic')
    Block.input('rgb', 'An RGB image.')
    Block.output('processed', 'The processed image.')
    
    def init(self):
        self.channel = 0
        
    def update(self):
        self.channel = (self.channel + 1) % 3

        rgb = self.input.rgb.copy()
        for i in [0, 1, 2]:
            if i != self.channel:
                rgb[:,:,i] = 0 
        
        self.output.processed = rgb
